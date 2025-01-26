# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the entire project contents into the container
COPY . /app

# Install the required Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Command to run the scheduler (assuming scheduler.py is inside the app directory)
CMD ["python", "app/scheduler.py"]
