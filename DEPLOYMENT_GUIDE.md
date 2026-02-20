# Render.com Deployment Guide

## Overview
This guide covers deploying your Django e-commerce application to Render.com. The necessary infrastructure files and configurations have been set up.

## Pre-Deployment Checklist

### 1. **Local Setup Verification**
- [ ] Verify Python 3.9+ installed
- [ ] Virtual environment created and activated
- [ ] All dependencies installed: `pip install -r requirements.txt`
- [ ] `.env` file created from `.env.example`
- [ ] Local tests passing: `python manage.py test`

### 2. **Environment Variables Setup**
Create a `.env` file in the project root with:
```
SECRET_KEY=your-generated-secret-key-here
DEBUG=False
ENVIRONMENT=production
DATABASE_URL=postgresql://user:password@host:port/dbname
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
CSRF_TRUSTED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

For generated secret key, use:
```python
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

### 3. **Database Migration**
For best compatibility with Render, use PostgreSQL:

**Option A: PostgreSQL (Recommended)**
- Render provides free PostgreSQL databases
- Update `DATABASE_URL` to PostgreSQL connection string
- Run migrations: `python manage.py migrate`

**Option B: MySQL (Local Development)**
- Keep MySQL for development
- Migrate to PostgreSQL for production
- Don't forget to set `DB_*` environment variables

### 4. **Static Files Collection**
```bash
python manage.py collectstatic --noinput
```
This collects all static assets for WhiteNoise to serve.

## Deployment Steps

### Option 1: Render Dashboard Deployment

1. **Connect Repository**
   - Log in to [render.com](https://render.com)
   - Click "New +" → "Web Service"
   - Connect your GitHub/GitLab repository
   - Select the repository

2. **Configure Service**
   - **Name**: `ethereal-jewelry` (or your preference)
   - **Environment**: `Python 3`
   - **Build Command**: (auto-detected from render.yaml)
   - **Start Command**: (auto-detected from render.yaml)
   - **Plan**: Free (or upgrade as needed)

3. **Add Environment Variables**
   In Render dashboard under "Environment":
   ```
   SECRET_KEY=your-secret-key
   DEBUG=False
   ENVIRONMENT=production
   DATABASE_URL=your-postgresql-url
   ALLOWED_HOSTS=your-domain.com,www.your-domain.com
   CSRF_TRUSTED_ORIGINS=https://your-domain.com,https://www.your-domain.com
   EMAIL_HOST_USER=your-email
   EMAIL_HOST_PASSWORD=your-password
   ```

4. **Database Setup**
   - Render will provision a PostgreSQL database
   - Copy the connection string to `DATABASE_URL`
   - Deployment will auto-run migrations via render.yaml

5. **Deploy**
   - Click "Create Web Service"
   - Monitor deployment logs
   - Once deployment succeeds, visit your service URL

### Option 2: Git Push Deployment

If you've linked Render to your repository:
```bash
git add .
git commit -m "Add Render deployment configuration"
git push origin main
```
Render will automatically trigger deployment based on `render.yaml`.

## Configuration Files Explained

### `render.yaml`
- Defines build and start commands
- Configures PostgreSQL database
- Sets environment variables for deployment
- Specifies Python version and build image

### `Procfile`
- Tells Render how to start the application
- Uses Gunicorn with 2 workers
- Binds to port from `$PORT` environment variable

### `requirements.txt` Updates
- **gunicorn**: Application server for production
- **whitenoise**: Serves static files (CSS, JS, images)
- **python-dotenv**: Loads environment variables from .env
- **dj-database-url**: Parses database connection strings
- **psycopg2-binary**: PostgreSQL database driver

### `Ecommerce/settings_production.py`
- Production-specific Django settings
- Loads configuration from environment variables
- Enables security features (HTTPS, HSTS, etc.)
- Configures WhiteNoise for static file serving

## Post-Deployment

### 1. **Verify Deployment**
- Visit your Render service URL
- Test homepage loads
- Check that CSS/JS/images display correctly
- Test database connections (login, admin panel)

### 2. **DNS Configuration** (for custom domain)
1. In Render dashboard, go to Settings → Custom Domains
2. Add your domain
3. Update your domain provider's DNS records:
   - Add CNAME pointing to Render's URL
   - Or use provided DNS records

### 3. **SSL Certificate**
- Automatically provisioned by Render
- Enforced via HTTPS redirects in settings

### 4. **Media Files**
- User-uploaded media stored in `/media` directory
- Served via WhiteNoise for static content
- For persistent storage, consider Render's Disks feature

### 5. **Monitoring & Logs**
- View logs in Render dashboard
- Monitor HTTP requests and errors
- Set up alerts for service restarts

## Troubleshooting

### Static Files Not Loading
- Ensure WhiteNoise middleware in settings.py
- Run `python manage.py collectstatic --noinput`
- Check `STATIC_ROOT` and `STATICFILES_STORAGE` settings

### Database Connection Failed
- Verify `DATABASE_URL` in environment variables
- Test database connection locally: `python manage.py dbshell`
- Ensure database migrations ran: `python manage.py migrate`

### 502 Bad Gateway
- Check application logs in Render dashboard
- Verify port binding: app should listen on `$PORT`
- Restart the service from Render dashboard

### Secret Key Not Set
- Add `SECRET_KEY` to environment variables
- Or set `DEBUG=False` to use fallback

### ALLOWED_HOSTS Error
- Update `ALLOWED_HOSTS` to include your domain
- Include both with and without `www`

## Performance Optimization

1. **Database Indexing**: Add indexes on frequently queried fields
2. **Caching**: Implement Redis for session/cache storage (if needed)
3. **CDN**: Consider Cloudflare for static content delivery
4. **Worker Processes**: Current config uses 2 workers; adjust based on traffic

## Security Recommendations

1. ✅ Use environment variables for sensitive data
2. ✅ Enable HTTPS redirects (configured in settings)
3. ✅ Set secure session cookies (configured)
4. ✅ Use strong SECRET_KEY
5. ✅ Enable CSRF protection (configured)
6. Consider: Rate limiting, WAF rules, monitoring

## Additional Resources

- [Render Docs - Deploy Python Django App](https://render.com/docs/deploy-django)
- [Django Deployment Guide](https://docs.djangoproject.com/en/6.0/howto/deployment/)
- [Gunicorn Application Server](https://gunicorn.org/)
- [WhiteNoise Documentation](http://whitenoise.evans.io/)

## Support

For Render-specific issues: https://support.render.com/
For Django-specific issues: https://www.djangoproject.com/
