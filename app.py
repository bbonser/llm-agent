from langchain.agents import ConversationalChatAgent, AgentExecutor
from langchain.callbacks import StreamlitCallbackHandler
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.memory.chat_message_histories import StreamlitChatMessageHistory
from langchain.tools import DuckDuckGoSearchRun
import streamlit as st
from streamlit_lottie import st_lottie
import requests
import json

# Load Lottie URL
lottie_url = 'https://lottie.host/058cd963-e4d5-49f4-b9e0-57f9c62c158b/pA6ZQJwSTP.json'  # Replace with your Lottie URL
lottie_json = requests.get(lottie_url).json()

st.set_page_config(page_title="LangChain: OpenAI ChatBot")
col1, col4 = st.columns([4, 1])
with col1:
    st.title("LangChain: OpenAI ChatBot")
with col4:
    st_lottie(lottie_json, width=100, height=100)

openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")

msgs = StreamlitChatMessageHistory()
memory = ConversationBufferMemory(
    chat_memory=msgs, return_messages=True, memory_key="chat_history", output_key="output"
)
if len(msgs.messages) == 0 or st.sidebar.button("Reset chat history"):
    msgs.clear()
    msgs.add_ai_message("How can I help you?")
    st.session_state.steps = {}

avatars = {"human": "user", "ai": "assistant"}
for idx, msg in enumerate(msgs.messages):
    with st.chat_message(avatars[msg.type]):
        # Render intermediate steps if any were saved
        for step in st.session_state.steps.get(str(idx), []):
            if step[0].tool == "_Exception":
                continue
            with st.expander(f"✅ **{step[0].tool}**: {step[0].tool_input}"):
                st.write(step[0].log)
                st.write(f"**{step[1]}**")
        st.write(msg.content)

if prompt := st.chat_input(placeholder="What is the tallest mountain in the world?"):
    st.chat_message("user").write(prompt)

    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    llm = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=openai_api_key, streaming=True)
    tools = [DuckDuckGoSearchRun(name="Search")]
    chat_agent = ConversationalChatAgent.from_llm_and_tools(llm=llm, tools=tools)
    executor = AgentExecutor.from_agent_and_tools(
        agent=chat_agent,
        tools=tools,
        memory=memory,
        return_intermediate_steps=True,
        handle_parsing_errors=True,
    )
    with st.chat_message("assistant"):
        st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
        response = executor(prompt, callbacks=[st_cb])
        st.write(response["output"])
        st.session_state.steps[str(len(msgs.messages) - 1)] = response["intermediate_steps"]

# Load another Lottie JSON from a URL
lottie_url = 'https://lottie.host/8a4240fd-d610-4b17-8e9c-ccf796b157b0/XUsYEgQXpe.json' 
another_lottie_json = requests.get(lottie_url).json()

# Add the Lottie animation to the bottom of the sidebar
with st.sidebar:
    st_lottie(another_lottie_json, width=300, height=300)