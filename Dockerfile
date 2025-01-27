# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the app directory into the container
COPY app /app

# Copy the requirements file into the container
COPY requirements.txt /app

# Install the required Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Command to run the scheduler
CMD ["python", "scheduler.py"]
