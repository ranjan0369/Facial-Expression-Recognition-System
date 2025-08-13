# Use official Python base image
FROM python:3.12-slim

# Set working directory inside container
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    cmake \
    pkg-config \
    libgtk-3-dev \
    libavcodec-dev \
    libavformat-dev \
    libswscale-dev \
    libtbb-dev \
    libjpeg-dev \
    libpng-dev \
    libtiff-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install pipenv
RUN pip install --no-cache-dir pipenv

# Copy Pipfile and Pipfile.lock first for caching
COPY Pipfile Pipfile.lock ./

# Install dependencies system-wide (inside container Python)
RUN pipenv install --system --deploy

# Copy source code and dataset
COPY src/ ./src
COPY haarcascade_frontalface_default.xml ./
# COPY facial-dataset/ ./facial-dataset

# Create result directory
# RUN mkdir -p result

# Set default command to run testing
CMD ["pipenv", "run", "python", "src/test.py"]