# llm-agent
## Intructions
## Must also have Python, and Docker installed.

This is a quick and simple way to use Langcahin with OpenAI.

Clone the repo to your local machine

```git clone https://github.com/bbonser/llm-agent```

Navigate to the folder where you pulled this down to and run the following command to build the Dockerfile and install the dependencies.

```docker
docker build -t llm-agent .
```
This will build the image from the Dockerfile.
Once completed run the following command to run the container.

```docker
docker run -p 8501:8501 llm-agent
```
Open a browser and navigate to http://localhost:8501

Add your OpenAI API key to get started.


## Docker Hub link
https://hub.docker.com/r/bbonser/llm-agent
