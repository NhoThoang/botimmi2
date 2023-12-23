# FROM ubuntu:18.04

# RUN apt-get update -y
# RUN apt-get install python3-pip -y
# RUN apt-get install gunicorn3 -y

# COPY requirements.txt requirements.txt
# COPY flaskapp /opt/

# RUN pip3 install -r requirements.txt
# WORKDIR /opt/

# CMD ["gunicorn3", "-b", "0.0.0.0:8000", "app:app", "--workers=5"]
# Use a smaller base image with Python 3 pre-installed



FROM python:3.9-slim

# Combine apt updates and installations for fewer layers
RUN apt-get update && apt-get install -y --no-install-recommends \
    gunicorn3 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements only for efficient dependency caching
COPY requirements.txt requirements.txt

# Install dependencies in a single layer
RUN pip3 install -r requirements.txt

# Copy application code
COPY flaskapp /opt/

# Set working directory
WORKDIR /opt/

# Expose port for the application
EXPOSE 8000

# Define the command to start the application
CMD ["gunicorn3", "-b", "0.0.0.0:8000", "app:app", "--workers=5"]
