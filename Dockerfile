# Use an official Python runtime as a parent image
FROM python:latest

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
ADD . /app

# Update package listings and upgrade libpq-dev and libpq5
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-15/libpq-dev=15.6-0+deb12u1 \
    postgresql-15/libpq5=15.6-0+deb12u1 && \
    rm -rf /var/lib/apt/lists/*

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8501 available to the world outside this container
EXPOSE 8501

# Run main.py when the container launches
CMD ["streamlit", "run", "app.py"]