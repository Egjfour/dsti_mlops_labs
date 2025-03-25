# Use latest Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory to /app and copy current dir
WORKDIR /app
COPY wine_app /app
COPY requirements.txt /app

RUN apt-get update
RUN apt-get install wget -y

# Install python dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN rm requirements.txt

# Run the registration script when the container launches
CMD ["python", "main.py"]

ENTRYPOINT ["gunicorn", "--bind=0.0.0.0:9696", "main:app"]
