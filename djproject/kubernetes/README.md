# Kubernetes Deployment Fixes

## Issues Found and Fixed

### 1. **Service Name Mismatch** ✅ FIXED
- **Problem**: Ingress was referencing service name `django-jobapp-service` but actual service was `django-job-app`
- **Fix**: Updated [ingress.yaml](ingress.yaml#L15) to use correct service name `django-job-app`

### 2. **Non-existent Health Check Endpoint** ✅ FIXED
- **Problem**: Probes were using `/health/` endpoint which Django doesn't provide by default
- **Fix**: Changed all probes (readiness, liveness, startup) from HTTP to TCP probes
- **Note**: If you want HTTP health checks, implement a `/health/` endpoint in your Django app

### 3. **Missing ConfigMap** ✅ FIXED
- **File Created**: [configmap.yaml](configmap.yaml)
- **Contains**: `ALLOWED_HOSTS` and `LOG_LEVEL` configuration
- **Deploy**: `kubectl apply -f kubernetes/configmap.yaml`

### 4. **Missing Secret** ✅ FIXED
- **File Created**: [secret.yaml](secret.yaml)
- **⚠️ ACTION REQUIRED**: Update these values in secret.yaml before deploying:
  - `database-url`: PostgreSQL connection string
  - `redis-url`: Redis connection URL
  - `secret-key`: Generate a random Django secret key

### 5. **Missing ServiceAccount & RBAC** ✅ FIXED
- **File Created**: [serviceaccount.yaml](serviceaccount.yaml)
- **Contains**: ServiceAccount, Role, and RoleBinding resources
- **Deploy**: `kubectl apply -f kubernetes/serviceaccount.yaml`

## Deployment Instructions

### Step 1: Update Secrets
Edit `kubernetes/secret.yaml` and set your actual database and Redis connection strings:

```bash
# Generate a random secret key (example)
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Step 2: Create Prerequisites
```bash
# Create ConfigMap, Secret, and ServiceAccount
kubectl apply -f kubernetes/configmap.yaml
kubectl apply -f kubernetes/secret.yaml
kubectl apply -f kubernetes/serviceaccount.yaml
```

### Step 3: Deploy Application
```bash
# Deploy the main application
kubectl apply -f kubernetes/deployment.yaml
kubectl apply -f kubernetes/service.yaml
kubectl apply -f kubernetes/ingress.yaml
```

### Step 4: Verify Deployment
```bash
# Check deployment status
kubectl get deployments -n default
kubectl get pods -n default
kubectl get services -n default

# Check for errors
kubectl describe deployment django-job-app
kubectl logs -n default -l app=django-job-app --tail=100
```

### Step 5: Access the Application
```bash
# For ClusterIP service (internal access)
kubectl port-forward svc/django-job-app 8000:80

# For NodePort service (on port 30007)
curl http://<node-ip>:30007

# For Ingress (depends on ingress controller setup)
curl http://<ingress-host>/
```

## Troubleshooting

### Pods stuck in Pending
- Check ConfigMap/Secret existence: `kubectl get configmap,secret -n default`
- Check ServiceAccount: `kubectl get serviceaccount -n default`

### ImagePullBackOff
- Verify Docker image exists: `sachinkumar26/djproject:latest`
- Check image repository credentials if private

### CrashLoopBackOff
- Check logs: `kubectl logs <pod-name> -n default`
- Verify DATABASE_URL and REDIS_URL in secret.yaml are correct
- Check if database/redis services are accessible

### Probes Failing (not using health checks)
- Current TCP probes check port 8000 connectivity
- If pods fail startup, increase `failureThreshold` values
- Monitor logs for startup issues

## File Checklist
- [x] deployment.yaml - Fixed health probes
- [x] service.yaml - No changes needed
- [x] ingress.yaml - Fixed service name reference
- [x] configmap.yaml - Created
- [x] secret.yaml - Created (requires configuration)
- [x] serviceaccount.yaml - Created

## Next Steps

1. **Configure Django for production**:
   - Set `DEBUG=False` in deployment (already set)
   - Configure proper ALLOWED_HOSTS in ConfigMap
   - Setup static file serving (using static volume)

2. **Add health endpoint** (optional but recommended):
   - Create a `/health/` view in Django
   - Update probes to use HTTP again for better diagnostics

3. **Setup persistent storage** (if needed):
   - Replace emptyDir volumes with PersistentVolumeClaim for production
   - Configure database backups
