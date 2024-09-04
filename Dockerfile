# Base Python image
FROM python:3.10.12-slim-bullseye

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file used for dependencies
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Copy the rest of the application code into the container at /app
COPY . .

# Command to run the app using Gunicorn
CMD ["python","wsgi.py"]