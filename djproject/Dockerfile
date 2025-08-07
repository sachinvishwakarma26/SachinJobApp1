# Use a lightweight base image
FROM python:3.8-alpine

# Set work directory
WORKDIR /usr/src/app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apk update && apk add --no-cache \
    build-base \
    libffi-dev \
    musl-dev \
    postgresql-dev \
    gcc \
    python3-dev \
    linux-headers \
    jpeg-dev \
    zlib-dev

# Upgrade pip
RUN pip install --upgrade pip

# Install Python dependencies
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
# Add this line to install pytest
RUN pip install pytest

# Copy project files
COPY . /usr/src/app

# Expose the Django development server port
EXPOSE 8000

# Start the Django application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

