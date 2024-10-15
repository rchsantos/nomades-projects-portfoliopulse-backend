FROM python:3.12-alpine

# Set environment variables
# The PYTHONDONTWRITEBYTECODE need to load by the.env file
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Install dependencies
RUN apk update \
    && apk add --no-cache gcc musl-dev linux-headers mongodb-tools \
    && pip install --upgrade pip

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in poetry.lock
RUN pip install --upgrade pip \
    && pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Expose the port the app runs on
EXPOSE 5050
