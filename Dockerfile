# ============================================================================
# Multi-Stage Dockerfile for Django Application (Production-Ready)
# ============================================================================

# Stage 1: Builder - Install dependencies
# ============================================================================
FROM python:3.10-slim AS builder

WORKDIR /build

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements (from project root)
COPY requirements.txt .

# Create wheels and install packages
RUN pip wheel --no-cache-dir --wheel-dir /build/wheels -r requirements.txt


# Stage 2: Runtime - Final image
# ============================================================================
FROM python:3.10-slim

# Metadata
LABEL maintainer="Sachin Kumar <sachin@example.com>"
LABEL description="Django Job Application"
LABEL version="1.0"

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONPATH=/app/djproject \
    DJANGO_SETTINGS_MODULE=djproject.settings

# Install runtime dependencies only
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user for security
RUN groupadd -r django && useradd -r -g django django

WORKDIR /app

# Copy wheels from builder stage
COPY --from=builder /build/wheels /wheels
COPY --from=builder /build/requirements.txt .

# Install Python dependencies from wheels
RUN pip install --no-cache-dir --no-index --find-links=/wheels -r requirements.txt && \
    rm -rf /wheels

# Copy application code with correct ownership
COPY --chown=django:django . /app/

# Create and own necessary directories
RUN mkdir -p /app/djproject/staticfiles /app/djproject/media && \
    chown -R django:django /app

# Collect static files (as root, before switching to django user)
RUN cd /app/djproject && python manage.py collectstatic --noinput --clear

# Set working directory to Django project root (where manage.py is)
WORKDIR /app/djproject

# Switch to non-root user
USER django

EXPOSE 8000

# Health check - just verify port is listening
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/ || exit 1

# Run Gunicorn for production
CMD ["gunicorn", \
     "--bind", "0.0.0.0:8000", \
     "--workers", "4", \
     "--worker-class", "sync", \
     "--worker-tmp-dir", "/dev/shm", \
     "--timeout", "60", \
     "--access-logfile", "-", \
     "--error-logfile", "-", \
     "djproject.wsgi:application"]
