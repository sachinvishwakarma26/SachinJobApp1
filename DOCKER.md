# Docker Setup Guide for Django Job Application

This guide covers building, running, and deploying the Django application using Docker.

## Project Structure

- **Dockerfile**: Multi-stage production-ready image with Gunicorn
- **djproject/Dockerfile**: Development-focused image with Django dev server
- **docker-compose.yml**: Local development setup with PostgreSQL, Redis, and Nginx
- **docker-compose.prod.yml**: Production-ready setup
- **.dockerignore**: Optimized build context
- **nginx.conf**: Nginx reverse proxy configuration
- **.env.example**: Environment variables template

## Prerequisites

- Docker (v20.10+)
- Docker Compose (v1.29+)
- Git

## Quick Start - Local Development

### 1. Clone Repository

```bash
git clone https://github.com/sachinvishwakarma26/SachinJobApp1.git
cd SachinJobApp1
```

### 2. Setup Environment Variables

```bash
cp .env.example .env
# Edit .env with your configuration
```

### 3. Start Services

```bash
# Start all services (PostgreSQL, Django, Redis, Nginx)
docker-compose up -d

# View logs
docker-compose logs -f web
```

### 4. Access Application

- **Django App**: http://localhost:8000
- **Nginx Proxy**: http://localhost
- **PostgreSQL**: localhost:5432
- **Redis**: localhost:6379

### 5. Create Superuser

```bash
docker-compose exec web python manage.py createsuperuser
```

### 6. Run Migrations

```bash
docker-compose exec web python manage.py migrate
```

## Building Docker Images

### Production Image

```bash
# Build production image
docker build -t sachinkumar26/djproject:1.0 .

# Run production image
docker run -d \
  -p 8000:8000 \
  -e DATABASE_URL=postgresql://user:password@db:5432/djproject_db \
  sachinkumar26/djproject:1.0
```

### Development Image

```bash
# Build development image
docker build -t djproject-dev:latest djproject/

# Run development image
docker run -it -p 8000:8000 \
  -v $(pwd):/app \
  djproject-dev:latest
```

## Docker Compose Commands

```bash
# Start all services
docker-compose up -d

# Stop all services
docker-compose down

# View logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f web

# Execute Django command
docker-compose exec web python manage.py <command>

# Access shell
docker-compose exec web python manage.py shell

# Run migrations
docker-compose exec web python manage.py migrate

# Collect static files
docker-compose exec web python manage.py collectstatic

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Rebuild services
docker-compose up --build

# Remove containers, volumes, networks
docker-compose down -v
```

## Production Deployment

### 1. Setup Environment

```bash
cp .env.example .env.prod
# Configure .env.prod with production values
```

### 2. Start Production Stack

```bash
docker-compose -f docker-compose.prod.yml up -d
```

### 3. Database Migration

```bash
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate
```

### 4. Collect Static Files

```bash
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput
```

## Docker Hub Push

### Login to Docker Hub

```bash
docker login
```

### Tag Image

```bash
docker tag djproject:latest sachinkumar26/djproject:1.0
docker tag djproject:latest sachinkumar26/djproject:latest
```

### Push Image

```bash
docker push sachinkumar26/djproject:1.0
docker push sachinkumar26/djproject:latest
```

## Kubernetes Deployment

### Build and Push Image

```bash
docker build -t sachinkumar26/djproject:1.0 .
docker push sachinkumar26/djproject:1.0
```

### Deploy to Kubernetes

```bash
kubectl apply -f kubernetes/deployment.yaml
kubectl apply -f kubernetes/service.yaml
kubectl apply -f kubernetes/ingress.yaml

# Check deployment status
kubectl get deployments
kubectl get pods
kubectl get svc

# View logs
kubectl logs <pod-name>
```

## Health Checks

The application includes health checks:

```bash
# Check container health
docker inspect <container-id> | grep -A 5 Health

# Health endpoint
curl http://localhost:8000/health/
```

## Troubleshooting

### Port Already in Use

```bash
# Find and kill process using port
lsof -i :8000
kill -9 <PID>

# Or use different port
docker run -p 8001:8000 sachinkumar26/djproject:1.0
```

### Database Connection Issues

```bash
# Check PostgreSQL service
docker-compose logs db

# Test connection
docker-compose exec db psql -U postgres -d djproject_db
```

### Permission Denied Errors

```bash
# Fix file permissions
sudo chown -R $USER:$USER .

# Or use sudo
sudo docker-compose up
```

### Rebuild Everything

```bash
docker-compose down -v
docker system prune -a
docker-compose up --build
```

## Performance Optimization

### Multi-Stage Build

The Dockerfile uses multi-stage builds to reduce final image size:
- Stage 1: Builder (installs dependencies as wheels)
- Stage 2: Runtime (only copies wheels, reduces bloat)

### Layer Caching

Order of operations optimizes Docker cache:
1. Base image
2. System dependencies
3. Python dependencies (changes less frequently)
4. Application code (changes frequently)

### Resource Limits

Set resource limits in docker-compose:

```yaml
services:
  web:
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 512M
        reservations:
          cpus: '0.5'
          memory: 256M
```

## Security Best Practices

- ✅ Non-root user (django) runs the application
- ✅ Environment variables for secrets (not hardcoded)
- ✅ Multi-stage build reduces attack surface
- ✅ Security headers in Nginx
- ✅ SSL/TLS support (configure in nginx.conf)
- ✅ PostgreSQL password protected
- ✅ Redis password protected (production)

## Useful Tools

### Docker CLI

```bash
# View running containers
docker ps

# View all containers
docker ps -a

# View images
docker images

# Remove unused resources
docker system prune -a

# Export/Import images
docker save image:tag > image.tar
docker load < image.tar
```

### Docker Compose CLI

```bash
# Validate compose file
docker-compose config

# View service dependencies
docker-compose config --services

# Pull latest images
docker-compose pull
```

## Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/)
- [Nginx Documentation](https://nginx.org/en/docs/)

## Support

For issues or questions, please create an issue in the repository.
