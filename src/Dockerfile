# Use latest Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory to /app and copy current dir
WORKDIR /app
COPY src /app
COPY requirements.txt /app
# Could use docker compose instead but this is easier for our small use case
COPY .env /app

RUN apt-get update
RUN apt-get install wget -y
# Download and extract azcopy
RUN wget https://aka.ms/downloadazcopy-v10-linux && \
    tar -xvf downloadazcopy-v10-linux && \
    rm -f downloadazcopy-v10-linux

# Find the azcopy directory and change permissions
RUN find . -type f -name "azcopy" -exec chmod +x {} \;

# Move azcopy to a directory in your PATH
RUN find . -type f -name "azcopy" -exec mv {} /usr/local/bin/ \;

# Clean up any remaining directories
RUN find . -type d -name "azcopy*" -exec rm -rf {} +

# Install python dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN rm requirements.txt

# Run the registration script when the container launches
CMD ["python", "dsti_mlops_labs/registration/registration.py"]
