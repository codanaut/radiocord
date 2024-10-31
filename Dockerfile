# Use an official Python runtime as the base image
FROM python:3.13

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file to the container
#COPY requirements.txt .

# Install the Python dependencies
#RUN pip install --no-cache-dir -r requirements.txt

RUN python3 -m pip install -U py-cord[voice]

RUN pip install audioop-lts

RUN apt-get -y update && apt-get -y upgrade && apt-get install -y --no-install-recommends ffmpeg

# Copy the rest of the application's code to the container
COPY . .

ENV PYTHONUNBUFFERED=1

# Specify the command to run your Flask app within the container
CMD ["python", "radiocord.py"]
