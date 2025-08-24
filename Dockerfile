# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /code

# Copy the requirements file into the container
COPY ./requirements.txt /code/requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the rest of the application code into the container
COPY . /code/

# Expose the port the app runs on
EXPOSE 7860

# Command to run the application using uvicorn
# We use port 7860 as it's the default for Hugging Face Spaces
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
