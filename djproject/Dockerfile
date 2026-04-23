# ============================================================================
# Development Dockerfile for Django Application (Easy Setup)
# ============================================================================

FROM python:3.8-slim

LABEL maintainer="Sachin Kumar <sachin@example.com>"
LABEL description="Django Job Application - Development"

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    DJANGO_SETTINGS_MODULE=djproject.settings \
    DEBUG=True

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    postgresql-client \
    curl \
    vim \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir gunicorn

# Copy application code
COPY . .

# Create directories for static and media files
RUN mkdir -p staticfiles media logs

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/health/ || exit 1

# Run development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]