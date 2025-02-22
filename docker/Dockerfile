# Dockerfile for production / HPC environment

FROM ubuntu:20.04

# Avoid interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3 python3-pip \
    libgl1-mesa-glx \
    gfortran \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /tmp/
RUN pip3 install --upgrade pip && pip3 install -r /tmp/requirements.txt

# Create a non-root user (optional best practice)
RUN useradd -m metalx
USER metalx
WORKDIR /home/metalx

# Copy project files
COPY --chown=metalx . /home/metalx

# Expose ports if needed (e.g., for Flask/Dash)
EXPOSE 5000

# Default command
CMD ["python3", "services/app.py"]
