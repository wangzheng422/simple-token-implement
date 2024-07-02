# Use an official Python runtime as a parent image
FROM docker.io/python:3.11-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY simple-token-implement.py ./

# Install any needed packages specified in README.md
RUN pip install -U flask jsonify Lock 

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV FLASK_APP=simple-token-implement.py
ENV TOTAL_TOKENS=1

# Run simple-token-implement.py when the container launches
CMD ["flask", "run", "--host=0.0.0.0"]