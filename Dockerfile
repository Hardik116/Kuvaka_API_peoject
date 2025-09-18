# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8501 for Streamlit and 8000 for the HTTP server
EXPOSE 5000 5000

# Run both the HTTP server and Streamlit app in parallel
CMD ["python", "app.py", "--server.port=5000"]
