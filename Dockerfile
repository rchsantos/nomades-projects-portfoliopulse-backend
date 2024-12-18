FROM python:3.12-slim

# Set environment variables
# The PYTHONDONTWRITEBYTECODE need to load by the.env file
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Install dependencies
# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc g++ musl-dev \
    libhdf5-dev libc6-dev libssl-dev libblas-dev \
    liblapack-dev libcurl4-openssl-dev libffi-dev \
    libjpeg-dev zlib1g-dev libopenblas-dev git \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install Poetry
RUN pip install --no-cache-dir --upgrade pip \
    && pip install poetry


# Copy the current directory contents into the container at /app
COPY . /app

# Configure Poetry to install dependencies directly into the global environment
RUN poetry config virtualenvs.create false

# Install project dependencies
RUN poetry install --no-interaction --no-ansi


# Install any needed packages specified in poetry.lock
#RUN pip install --upgrade pip \
#    && pip install --no-cache-dir poetry \
#    && poetry config virtualenvs.create false \
#    && poetry install --no-interaction --no-ansi

# Expose the port the app runs on
EXPOSE 5050
