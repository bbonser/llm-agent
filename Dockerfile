# Use an official Python runtime as a parent image
FROM python:alpine

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
ADD . /app

# Install core dependencies.
RUN apt-get update && apt-get install -y libpq-dev build-essential

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8501 available to the world outside this container
EXPOSE 8501

# Run main.py when the container launches
CMD ["streamlit", "run", "app.py"]