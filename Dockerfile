# Dockerfile
FROM python:3.9-slim

# System-level dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy files
WORKDIR /app
COPY . /app

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# By default, run the Dash app
EXPOSE 8050
CMD ["python", "app.py"]

