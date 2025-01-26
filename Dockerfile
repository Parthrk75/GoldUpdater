# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY app /app

# Install the required Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Command to run the scheduler
CMD ["python", "scheduler.py"]
