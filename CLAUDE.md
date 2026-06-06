# SachinJobApp1 - Django Job Portal

## Overview
A Django-based job listing portal aggregating job openings across 5 major Indian cities (Hyderabad, Bangalore, Chennai, Pune, Noida). Provides both HTML views for browsing and REST API endpoints for programmatic access.

## Tech Stack
- **Framework**: Django 4.2.7 + Django REST Framework 3.15.1
- **Database**: PostgreSQL (prod) / SQLite (dev)
- **Server**: Gunicorn (prod), Django dev server (dev)
- **Containerization**: Docker, Kubernetes
- **Reverse Proxy**: Nginx
- **CI/CD**: Jenkins + GitLab pipelines
- **Cache**: Redis 7 (optional)

## Project Structure

```
djproject/
├── djproject/               # Settings module
│   ├── settings.py         # Django config
│   ├── urls.py             # Main URL router
│   └── wsgi.py             # WSGI entry point
├── testapp/                # Primary app - job listings
│   ├── models.py           # 5 city job models (hydjobs, blorejobs, etc.)
│   ├── views.py            # Template views with pagination (25/page)
│   ├── admin.py            # Django admin config
│   ├── api/
│   │   ├── views.py        # DRF ViewSets for CRUD
│   │   ├── serializers.py  # Model serializers
│   │   └── urls.py         # API router
│   └── migrations/
├── myapi/                  # Secondary app (duplicate models, experimental)
├── templates/testapp/      # HTML templates (index1.html, hydjobs.html, etc.)
├── static/                 # CSS, images
├── manage.py               # Django CLI
├── requirements.txt        # Python dependencies
├── Dockerfile              # Multi-stage prod image
├── docker-compose.yml      # Local dev stack (PostgreSQL, Redis, Nginx)
├── docker-compose.prod.yml # Production environment
├── nginx.conf              # Nginx config
├── Jenkinsfile             # Jenkins CI/CD
├── .gitlab-ci.yml          # GitLab CI
└── deployment-config.yaml  # Kubernetes manifest
```

## Data Models
Each city has a corresponding model with fields:
- `date` - Job posting date
- `company` - Company name
- `title` - Job title
- `eligibility` - Eligibility criteria
- `address` - Job location
- `email` - Contact email
- `phonenumber` - Contact phone

**Models**: hydjobs, blorejobs, chennaijobs, punejobs, noidajobs

## Key Endpoints

### HTML Views (Template Rendering)
- `GET /` - Homepage
- `GET /hydjobs/` - Hyderabad jobs (paginated)
- `GET /blorejobs/` - Bangalore jobs
- `GET /punejobs/` - Pune jobs
- `GET /chennaijobs/` - Chennai jobs
- `GET /noidajobs/` - Noida jobs
- `GET /health/` - Kubernetes health check

### REST API Endpoints
- `GET/POST /api/hydjobsinfo/` - CRUD for Hyderabad jobs
- `GET/POST /api/blorejobsinfo/` - CRUD for Bangalore jobs
- `GET/POST /api/punejobsinfo/` - CRUD for Pune jobs
- `GET/POST /api/chennaijobsinfo/` - CRUD for Chennai jobs
- `GET/POST /api/noidajobsinfo/` - CRUD for Noida jobs

All API endpoints use DRF DefaultRouter for automatic URL generation and ViewSets for CRUD operations.

## Configuration

### Settings (settings.py)
- `DEBUG = True` (⚠️ Should be False in production)
- `ALLOWED_HOSTS = ['*']` (⚠️ Should be restricted in production)
- `DATABASES`: SQLite (dev) or PostgreSQL (prod via env vars)
- `STATIC_URL: /static/`
- `MIDDLEWARE`: Includes WhiteNoiseMiddleware for static file serving

### Environment Variables
- `DEBUG` - Enable debug mode
- `ALLOWED_HOSTS` - Allowed hostnames
- `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD` - Database config
- `REDIS_PASSWORD` - Redis authentication
- `DJANGO_SETTINGS_MODULE` - Settings module path

## Deployment

### Local Development
```bash
docker-compose up
```
Runs PostgreSQL, Django (hot-reload), Redis, and Nginx on port 80.

### Production
- **Docker Image**: Multi-stage build → Gunicorn with 4 workers
- **Kubernetes**: 2 replicas, rolling updates, image: `sachinkumar26/djproject:latest`
- **Health Checks**: Enabled for container health monitoring
- **Security**: Non-root user (django) in containers

### CI/CD
- **Jenkins**: Build Docker image → Push to Docker Hub → Deploy to Kubernetes
- **GitLab CI**: Alternative pipeline configuration

## Utilities
- `populate_jpbs.py` - Script to populate job data into database
- Django Admin interface at `/admin/`
- Virtual environment included (`venv/`)

## Security Notes
⚠️ **Current Issues**:
- `DEBUG = True` in settings (leaks sensitive info in production)
- `ALLOWED_HOSTS = ['*']` (accept any hostname)
- No HTTPS configuration visible in Django settings

## Architecture Patterns
- **Separation of Concerns**: testapp (primary), myapi (secondary/experimental)
- **REST API**: DRF ViewSets + DefaultRouter for automatic CRUD
- **Pagination**: Server-side pagination (25 items/page)
- **Static Files**: WhiteNoise for efficient serving
- **Containerization**: Multi-stage Docker builds for optimized images
