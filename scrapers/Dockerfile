# Use the official Selenium standalone image
# FROM infologistix/docker-selenium-python:alpine
FROM seleniarm/standalone-chromium:latest

USER root

# Set working directory
WORKDIR /app

# Copy application code
COPY . /app

# RUN apk update && apk add --no-cache bash curl
RUN apt update && apt install -y --no-install-recommends \
    python3 \
    python3-pip && \
    apt clean && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
# RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir --break-system-packages -r requirements.txt


# SHELL ["/bin/bash", "-c"]

# Command to run your script
# CMD ["sleep", "infinity"]
CMD ["python3", "scraper_vinted.py"]
