FROM python:3.8-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app/
COPY manage.py /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

# ✅ FIX: move into directory that contains manage.py
WORKDIR /app/djproject

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# # Use a lightweight base image
# FROM python:3.8-alpine

# # Set work directory
# WORKDIR /usr/src/app

# # Set environment variables
# ENV PYTHONDONTWRITEBYTECODE=1
# ENV PYTHONUNBUFFERED=1
# ENV DJANGO_SETTINGS_MODULE=djproject.settings

# #ENV DJANGO_SETTINGS_MODULE=core.settings

# # Install system dependencies
# RUN apk update && apk add --no-cache \
#     build-base \
#     libffi-dev \
#     musl-dev \
#     postgresql-dev \
#     gcc \
#     python3-dev \
#     linux-headers \
#     jpeg-dev \
#     zlib-dev

# # Upgrade pip
# RUN pip install --upgrade pip

# # Install Python dependencies
# COPY ./requirements.txt /usr/src/app/requirements.txt
# RUN pip install --no-cache-dir -r requirements.txt
# # Add this line to install pytest
# #RUN pip install pytest

# # Copy project files
# COPY . /usr/src/app

# # Expose the Django development server port
# EXPOSE 8000

# # Start the Django application
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# base image
# FROM python:3.8-slim

# # set working dir
# WORKDIR /usr/src/app

# # copy requirements file first
# COPY requirements.txt .

# # install dependencies
# RUN pip install --no-cache-dir -r requirements.txt

# # copy all source code
# COPY . .

# # set django settings env
# ENV DJANGO_SETTINGS_MODULE=djproject.settings

# # expose port (example)
# EXPOSE 8000

# # run server
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]