# Use the official Python base image that includes Git support
FROM python:3.9-buster

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file first to leverage Docker cache
COPY requirements.txt .

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all files from your local directory to the working directory in the container
COPY . .

# Expose the port where Streamlit runs
EXPOSE 8501

# Command to run the Streamlit app
CMD ["streamlit", "run", "app.py"]
