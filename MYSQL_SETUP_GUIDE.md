# MySQL Database Setup for Render Deployment

## ✅ Code Fixed - Now Set Up Your Database

I've updated the database configuration to:
- ✅ Work with external MySQL services (PlanetScale, Railway, Aiven, etc.)
- ✅ Support SSL connections for cloud databases
- ✅ Prevent deployment without DATABASE_URL set
- ✅ Better error messages

---

## 🔥 NEXT STEPS: Choose Your MySQL Provider

### Option 1: PlanetScale (Recommended - Serverless MySQL)

**Free Tier:**
- 5 GB storage
- 1 billion row reads/month
- Automatic backups

**Setup Steps:**

1. **Create Account:** https://planetscale.com
2. **Create Database:**
   - Click "Create a new database"
   - Name: `luxeprestige`
   - Region: Choose closest to your Render region (US West, US East, etc.)
   - Click "Create"

3. **Get Connection String:**
   - Click "Connect" button
   - Select "Django" from framework dropdown
   - Create a password (copy it - shown only once!)
   - You'll see connection details like:
     ```
     Host: aws.connect.psdb.cloud
     Username: xxxxxxxxx
     Password: pscale_pw_xxxxxx
     Database: luxeprestige
     Port: 3306
     ```

4. **Format DATABASE_URL:**
   ```
   mysql://USERNAME:PASSWORD@HOST:3306/DATABASE?ssl_mode=REQUIRED
   ```
   
   **Example:**
   ```
   mysql://abcd1234:pscale_pw_xyz789@aws.connect.psdb.cloud:3306/luxeprestige?ssl_mode=REQUIRED
   ```

---

### Option 2: Railway (Easiest Setup)

**Free Tier:**
- $5 free credit monthly
- Simple one-click MySQL

**Setup Steps:**

1. **Create Account:** https://railway.app
2. **New Project:**
   - Click "Start a New Project"
   - Click "Provision MySQL"
3. **Get DATABASE_URL:**
   - Click on MySQL service
   - Go to "Variables" tab
   - Copy the **MYSQL_URL** value (it's auto-generated)
   - Format: `mysql://root:password@containers-us-west-123.railway.app:6543/railway`

---

### Option 3: Aiven (Free MySQL Cloud)

**Free Tier:**
- 1 node, 1 CPU, 1GB RAM
- 5GB storage

**Setup Steps:**

1. **Create Account:** https://aiven.io
2. **Create Service:**
   - Choose MySQL
   - Select Free plan
   - Choose cloud region
3. **Get Connection Info:**
   - Service URI is your DATABASE_URL
   - Format: `mysql://user:password@mysql-xxx.aivencloud.com:12345/defaultdb?ssl-mode=REQUIRED`

---

## 📋 Add DATABASE_URL to Render

### Step 1: Copy Your Connection String

From whichever service you chose above, copy the full `DATABASE_URL` in this format:
```
mysql://username:password@host:port/database?ssl_mode=REQUIRED
```

### Step 2: Add to Render Environment

1. Go to: **https://dashboard.render.com**
2. Click: **LuxePrestige** service
3. Click: **Environment** (left sidebar)
4. Click: **"Add Environment Variable"**
5. **Key:** `DATABASE_URL`
6. **Value:** Paste your MySQL connection string
7. Click: **Add**

### Step 3: Verify All Environment Variables

Make sure you have these set:

```
ALLOWED_HOSTS = luxeprestige.onrender.com,.onrender.com,127.0.0.1,localhost
CSRF_TRUSTED_ORIGINS = https://luxeprestige.onrender.com,https://*.onrender.com
DATABASE_URL = mysql://your-connection-string-here
DEBUG = false
ENVIRONMENT = production
SECRET_KEY = p4am%1#mrvv0c!=(6ac7ji#t-xa(idnu)lm*b8)mvbkyooh1nk
```

### Step 4: Save & Deploy

1. Click **"Save Changes"** (bottom of page)
2. Render will automatically redeploy
3. Wait 2-3 minutes

---

## ✅ After Deployment

### Check Deployment Logs

You should see:
```
==> Running 'python manage.py migrate && gunicorn...'
Operations to perform:
  Apply all migrations: admin, auth, backends, contenttypes, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  ...
[INFO] Starting gunicorn 23.0.0
[INFO] Listening at: http://0.0.0.0:10000
```

### Test Your Site

1. **Health Check:** `https://luxeprestige.onrender.com/health/`
   - Should show database connection info

2. **Homepage:** `https://luxeprestige.onrender.com/`
   - Your site should load!

3. **Admin:** `https://luxeprestige.onrender.com/admin/`
   - Create superuser after first deploy

---

## 🔧 Migrate Data from Local MySQL (Optional)

If you have existing data in your local MySQL database:

### Option 1: Export/Import via JSON

```bash
# On local machine - export data
python manage.py dumpdata --natural-foreign --natural-primary > data.json

# Add to git (if data is not sensitive)
git add data.json
git commit -m "Add initial data"
git push

# In Render Shell (after first deploy):
# Dashboard → Shell → Run:
python manage.py loaddata data.json
```

### Option 2: Direct Database Migration

Use a tool like `mysqldump` to export and import to your cloud MySQL.

---

## 🆘 Troubleshooting

### "DATABASE_URL environment variable is required"
- You forgot to add DATABASE_URL in Render Environment variables
- Go to Environment tab and add it

### "Access denied for user"
- Wrong username/password in DATABASE_URL
- Check your cloud MySQL dashboard for correct credentials

### SSL Connection Error
- Make sure `?ssl_mode=REQUIRED` is at the end of DATABASE_URL
- Or check if your provider requires different SSL format

### Migrations Fail
- Make sure database exists on your cloud provider
- Check database name matches in DATABASE_URL

---

## 📞 Need Help?

Check logs in Render Dashboard → Your Service → Logs tab for specific error messages.
