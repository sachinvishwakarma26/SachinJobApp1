# Kubernetes Deployment - Job App

## Deployment Overview

This directory contains Kubernetes manifests for deploying the Job App application.

### Files

- **deployment.yaml** - Main application deployment (2 replicas)
- **service.yaml** - ClusterIP and NodePort services
- **ingress.yaml** - Nginx ingress configuration
- **configmap.yaml** - Application configuration
- **secret.yaml** - Sensitive data (database, Redis, secret key)
- **serviceaccount.yaml** - RBAC configuration

## Quick Deploy

### Step 1: Update Secrets
Edit `secret.yaml` and set your actual values:
```yaml
database-url: "postgresql://user:password@host:5432/dbname"
redis-url: "redis://redis-host:6379/0"
secret-key: "generate-random-key"
```

Generate a random secret key:
```bash
python -c "import secrets; print(secrets.token_urlsafe(50))"
```

### Step 2: Deploy
```bash
# Create all resources
kubectl apply -f kubernetes/

# Or deploy individually:
kubectl apply -f kubernetes/configmap.yaml
kubectl apply -f kubernetes/secret.yaml
kubectl apply -f kubernetes/serviceaccount.yaml
kubectl apply -f kubernetes/deployment.yaml
kubectl apply -f kubernetes/service.yaml
kubectl apply -f kubernetes/ingress.yaml
```

### Step 3: Verify
```bash
# Check deployments
kubectl get deployment -l app=jobapp

# Check pods
kubectl get pods -l app=jobapp

# Check services
kubectl get svc -l app=jobapp

# Check ingress
kubectl get ingress
```

### Step 4: Access the Application

**Port Forward (local access):**
```bash
kubectl port-forward svc/jobapp-service 8000:80
# Access: http://localhost:8000
```

**NodePort Service (any node):**
```bash
# Get a node IP
kubectl get nodes -o wide

# Access: http://<node-ip>:30007
```

**Ingress (requires nginx-ingress controller):**
```bash
# Access: http://localhost/ (depends on your ingress setup)
```

## Configuration

### Environment Variables
Modify `configmap.yaml` and `secret.yaml` before deployment:

**ConfigMap (non-sensitive):**
- `allowed-hosts`: Allowed hostnames for Django

**Secret (sensitive):**
- `database-url`: PostgreSQL connection string
- `redis-url`: Redis connection string
- `secret-key`: Django SECRET_KEY

## Troubleshooting

### Pods not starting
```bash
# Check pod events
kubectl describe pod <pod-name> -l app=jobapp

# Check logs
kubectl logs -l app=jobapp
```

### ImagePullBackOff
```bash
# Verify image exists
docker pull sachinkumar26/sapiensjobapp:2.0

# Check imagePullPolicy in deployment.yaml
```

### Service not reachable
```bash
# Test connectivity
kubectl exec -it <pod-name> -- wget -O- http://localhost:8000

# Check service endpoints
kubectl get endpoints
```

## Scaling

### Scale replicas
```bash
kubectl scale deployment djproject --replicas=4
```

### Update image
```bash
kubectl set image deployment/djproject jobapp=sachinkumar26/sapiensjobapp:2.1 --record
```

## Rollback

```bash
# View rollout history
kubectl rollout history deployment/djproject

# Rollback to previous version
kubectl rollout undo deployment/djproject
```

## Cleanup

```bash
# Delete all resources
kubectl delete -f kubernetes/

# Or delete specific resource
kubectl delete deployment djproject
```

## Application Info

- **App Label**: `app=jobapp`
- **Deployment Name**: `djproject`
- **Image**: `sachinkumar26/sapiensjobapp:2.0`
- **Port**: 8000
- **Replicas**: 2
- **ClusterIP Port**: 80 (maps to 8000)
- **NodePort**: 30007
