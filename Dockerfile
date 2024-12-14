# syntax=docker/dockerfile:1

# Use Python 3.10 as base image
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY src/ /app/

# Install required packages
RUN pip install telebot requests beautifulsoup4 python-dotenv tinydb

# Command to run the Python script
CMD ["python", "./main.py"]