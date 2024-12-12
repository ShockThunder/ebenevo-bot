# syntax=docker/dockerfile:1

# Use Python 3.10 as base image
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Command to run the Python script
RUN pip install telebot requests beautifulsoup4 python-dotenv tinydb
CMD ["python", "./main.py"]