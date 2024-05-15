# Use an official Python runtime as a base image
FROM python:3.12-slim

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# You might not want to use the .env file directly in production.
# For better security practices, consider passing environment variables
# through Docker run command or Docker Compose file. For now, we will
# copy the .env file into our image.
COPY .env /app

# Make port 8100 available to the world outside this container
EXPOSE 8100

# Define environment variable for the application (if any)
ENV FLASK_APP app.py
ENV FLASK_RUN_HOST 0.0.0.0

# Run the application
CMD ["flask", "run", "--port=8100"]
