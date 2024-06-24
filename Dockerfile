# Use the official Ubuntu base image
FROM ubuntu:20.04

# Set environment variables to avoid prompts during installation
ENV DEBIAN_FRONTEND=noninteractive

# Install Python, pip, and Git
RUN apt-get update && \
    apt-get install -y python3 python3-pip git && \
    apt-get clean

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file first to leverage Docker cache
COPY requirements.txt .

# Install any dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy all files from your local directory to the working directory in the container
COPY . .

# Expose the port where Streamlit runs
EXPOSE 8501

# Command to run the Streamlit app
CMD ["streamlit", "run", "app.py"]
