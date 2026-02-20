# Render Deployment Troubleshooting Guide

## "Not Found" (404) Errors - Common Causes & Solutions

### Issues Fixed ✅

1. **Static Files Not Found**
   - **Problem**: Static files (CSS, JS, images) returning 404
   - **Solution**: Changed `STATICFILES_STORAGE` to use `CompressedStaticFilesStorage` instead of `CompressedManifestStaticFilesStorage`
   - **Why**: Manifest-based storage can cause issues on Render's ephemeral filesystem

2. **ALLOWED_HOSTS Configuration**
   - **Problem**: Domain not recognized, causing 400 Bad Request or redirects to 404
   - **Solution**: Updated `render.yaml` to include:
     - `ethereal-jewelry.onrender.com` (specific domain)
     - `*.onrender.com` (wildcard for preview deployments)
     - `127.0.0.1,localhost` (fallback)
   - **Added to settings.py**: Automatic Render domain detection in production

3. **CSRF_TRUSTED_ORIGINS**
   - **Problem**: Form submissions failing with 403 Forbidden
   - **Solution**: Added `CSRF_TRUSTED_ORIGINS` to `render.yaml` with both HTTP and HTTPS origins

4. **Static Files URL Routing**
   - **Problem**: Static files not served in production
   - **Solution**: Updated `urls.py` to explicitly serve static files even in production (WhiteNoise handles compression)

---

## Debugging Steps

### 1. Check Render Logs
```bash
# View live logs in Render dashboard
# Look for errors like:
# - "Not Found: /admin/"
# - "ModuleNotFoundError"
# - "TemplateDoesNotExist"
```

### 2. Verify Static Files Were Collected
The build command should show:
```
Running: pip install -r requirements.txt && python manage.py collectstatic --noinput
...collected 25 static files
```

If static files aren't being found, the build might be failing silently.

### 3. Check Database Migration
Ensure migrations ran successfully:
```bash
# In Render logs, look for:
# Operations to perform:
#   Apply all migrations...
# Running migrations...
```

### 4. Verify Environment Variables
Check that all required variables are set in Render dashboard:
- `DEBUG=false`
- `ENVIRONMENT=production`
- `ALLOWED_HOSTS=ethereal-jewelry.onrender.com,*.onrender.com`
- `SECRET_KEY=<your-secret-key>`
- `DATABASE_URL=<postgres-url>`

---

## Common 404 Errors Explained

| Error | Cause | Solution |
|-------|-------|----------|
| `/static/css/...` 404 | Static files not collected | Re-deploy or check `collectstatic` output |
| `/admin/` 404 | Admin not loaded | Ensure `django.contrib.admin` in `INSTALLED_APPS` |
| `/dashboard/` 404 | URL not found | Check `backends/urls.py` has the route |
| `/media/...` 404 | Media files missing | Expected on Render (ephemeral storage) - use cloud storage |
| Root path `/` 404 | Home view not found | Check `Ecommerce/views.py` has `Home` function |

---

## Special Notes for Render

### Ephemeral Filesystem
Render's free tier uses ephemeral storage - files written during deployment are deleted when the app stops.

**Impact on Media Files:**
- User-uploaded files won't persist between restarts
- **Solution**: Use AWS S3 or Cloudinary for persistent media storage

**Implementation:**
```python
# Add to requirements.txt:
boto3==1.26.165
django-storages==1.13.2

# Add to settings.py (production):
if ENVIRONMENT == 'production':
    USE_S3 = os.getenv('USE_S3', 'False') == 'True'
    if USE_S3:
        AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
        AWS_S3_ACCESS_KEY_ID = os.getenv('AWS_S3_ACCESS_KEY_ID')
        AWS_S3_SECRET_ACCESS_KEY = os.getenv('AWS_S3_SECRET_ACCESS_KEY')
        AWS_S3_REGION_NAME = 'us-east-1'
        DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
        MEDIA_URL = f'https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/media/'
```

### Database
- Render provides PostgreSQL automatically via `DATABASE_URL`
- Migrations run automatically in `render.yaml`
- No manual database setup needed

### Static Files with WhiteNoise
WhiteNoise automatically:
- Collects static files
- Serves them with compression
- Handles cache headers
- No additional CDN needed for free tier

---

## Deployment Checklist

Before pushing to Render:

- [ ] All environment variables set in Render dashboard
- [ ] `DEBUG=false` in production environment
- [ ] `ENVIRONMENT=production` set
- [ ] `ALLOWED_HOSTS` includes `ethereal-jewelry.onrender.com`
- [ ] `SECRET_KEY` is strong and unique
- [ ] Database migrations run successfully
- [ ] Static files collected without errors
- [ ] Template files exist in `templates/` directory
- [ ] No hardcoded localhost URLs in code

---

## Quick Fix Steps

If you're seeing "Not Found" errors:

1. **Re-deploy** the application to force static file collection:
   - In Render dashboard → Pull & Deploy → Latest commit

2. **Check logs** for the actual error message
   - Dashboard → Logs tab

3. **Clear browser cache** (Ctrl+Shift+Del)
   - Static files might be cached with old URLs

4. **Verify ALLOWED_HOSTS**
   - Make sure current domain is in the list

5. **Test without Cloudflare/Proxy**
   - If using a domain proxy, try accessing Render URL directly

---

## Still Having Issues?

Check [Render's Django Guide](https://render.com/docs/deploy-django) for additional help.
