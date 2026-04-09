# Resume Analyzer - Deployment Guide

## 📋 Pre-Deployment Checklist

✅ Files created:
- `Procfile` - For Heroku/Railway
- `render.yaml` - For Render
- `runtime.txt` - Python version specification
- `requirements.txt` - Updated with gunicorn
- `setup.sh` - Initialization script

---

## 🚀 OPTION 1: Deploy to Render (RECOMMENDED)

### Why Render?
- ✅ Free tier with 750 hours/month
- ✅ Auto-deploys from GitHub
- ✅ Easy persistent storage
- ✅ No credit card required for free tier

### Step-by-Step Instructions:

#### 1. Push Your Code to GitHub (if not already done)
```bash
git add .
git commit -m "Prepare for deployment"
git push origin main
```

#### 2. Sign Up for Render
- Go to https://render.com
- Click "Get Started for Free"
- Sign up with your GitHub account

#### 3. Create New Web Service
- Click "New +" button → "Web Service"
- Connect your GitHub repository
- Select "resume-analyzer" repository
- Click "Connect"

#### 4. Configure Your Service
Fill in these settings:
- **Name**: resume-analyzer (or any name you prefer)
- **Environment**: Python 3
- **Region**: Choose closest to your location
- **Branch**: main
- **Build Command**: 
  ```
  pip install -r requirements.txt && python -m spacy download en_core_web_sm && python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet')"
  ```
- **Start Command**: 
  ```
  gunicorn app:app
  ```

#### 5. Add Environment Variables
Click "Advanced" → "Add Environment Variable":
- **SECRET_KEY**: (generate a random string, e.g., `openssl rand -hex 32`)

#### 6. Create the Service
- Select **Free** instance type
- Click "Create Web Service"

#### 7. Wait for Deployment
- Render will build and deploy your app (takes 5-10 minutes)
- Once complete, you'll get a URL like: `https://resume-analyzer-xxxx.onrender.com`

#### 8. Initialize Database (First Time Only)
After first deployment, go to Shell tab in Render dashboard and run:
```bash
python -c "from app import app, db; app.app_context().push(); db.create_all()"
```

#### ⚠️ Important Notes for Render:
- Free tier apps sleep after 15 minutes of inactivity
- First request after sleep takes ~30 seconds
- Uploaded files are stored temporarily (reset on redeploy)

---

## 🚀 OPTION 2: Deploy to Railway

### Why Railway?
- ✅ $5 free credit monthly
- ✅ Very fast deployment
- ✅ Great developer experience
- ✅ Persistent file storage

### Step-by-Step Instructions:

#### 1. Push to GitHub (if not already done)
```bash
git add .
git commit -m "Prepare for deployment"
git push origin main
```

#### 2. Sign Up for Railway
- Go to https://railway.app
- Click "Start a New Project"
- Sign in with GitHub

#### 3. Deploy from GitHub
- Click "Deploy from GitHub repo"
- Select your repository
- Railway auto-detects it's a Python app

#### 4. Add Environment Variables
- Click on your service → "Variables" tab
- Add:
  - `SECRET_KEY`: (generate random string)

#### 5. Configure Build
Railway should auto-detect, but you can verify:
- Build Command: Uses requirements.txt automatically
- Start Command: Uses Procfile automatically

#### 6. Generate Domain
- Go to "Settings" tab
- Click "Generate Domain"
- You'll get a URL like: `https://your-app.up.railway.app`

#### 7. Initialize Database
Go to Railway dashboard → your service → Shell:
```bash
python -c "from app import app, db; app.app_context().push(); db.create_all()"
```

---

## 🚀 OPTION 3: Deploy to PythonAnywhere

### Why PythonAnywhere?
- ✅ 100% Python-focused
- ✅ Beginner-friendly interface
- ✅ Free tier available
- ✅ File storage included

### Step-by-Step Instructions:

#### 1. Sign Up
- Go to https://www.pythonanywhere.com
- Create a free "Beginner" account

#### 2. Open Bash Console
- Dashboard → "Consoles" → "Bash"

#### 3. Clone Your Repository
```bash
git clone https://github.com/YOUR_USERNAME/resume-analyzer.git
cd resume-analyzer
```

#### 4. Create Virtual Environment
```bash
mkvirtualenv --python=/usr/bin/python3.10 resumeapp
pip install -r requirements.txt
python -m spacy download en_core_web_sm
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet')"
```

#### 5. Setup Web App
- Go to "Web" tab
- Click "Add a new web app"
- Choose "Manual configuration"
- Select Python 3.10

#### 6. Configure WSGI File
Click on WSGI configuration file link and replace content with:
```python
import sys
import os

# Add your project directory
project_home = '/home/YOUR_USERNAME/resume-analyzer'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

# Set environment variables
os.environ['SECRET_KEY'] = 'your-secret-key-here'

# Import Flask app
from app import app as application
```

#### 7. Set Virtual Environment
- In Web tab, scroll to "Virtualenv" section
- Enter: `/home/YOUR_USERNAME/.virtualenvs/resumeapp`

#### 8. Initialize Database
In Bash console:
```bash
cd resume-analyzer
python -c "from app import app, db; app.app_context().push(); db.create_all()"
```

#### 9. Reload Web App
- Click big green "Reload" button
- Visit: `http://YOUR_USERNAME.pythonanywhere.com`

---

## 🔧 Post-Deployment Tasks

### 1. Test Your Application
- Visit your deployment URL
- Test candidate dashboard
- Test company dashboard
- Upload a test resume
- Verify applications ranking works

### 2. Monitor Your App
- Check logs for any errors
- Monitor resource usage

### 3. Set Up Custom Domain (Optional)
- Most platforms support custom domains in free tier
- Follow platform-specific docs

---

## ⚠️ Common Issues & Solutions

### Issue: NLTK/spaCy data not found
**Solution**: Make sure build command includes data downloads:
```bash
python -m spacy download en_core_web_sm
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet')"
```

### Issue: Database not initialized
**Solution**: Run initialization command:
```bash
python -c "from app import app, db; app.app_context().push(); db.create_all()"
```

### Issue: Upload folder permissions
**Solution**: Ensure uploads folder exists and is writable (done in code)

### Issue: App crashes on start
**Solution**: Check logs for missing dependencies, add to requirements.txt

---

## 📊 Feature Comparison

| Feature | Render | Railway | PythonAnywhere |
|---------|--------|---------|----------------|
| Free Tier | ✅ 750hrs | ✅ $5 credit | ✅ Limited |
| Auto Deploy | ✅ Yes | ✅ Yes | ❌ Manual |
| Setup Difficulty | 🟢 Easy | 🟢 Easy | 🟡 Medium |
| File Storage | ⚠️ Temporary | ✅ Persistent | ✅ Persistent |
| Custom Domain | ✅ Free | ✅ Free | 💰 Paid |
| Sleep on Idle | ✅ Yes | ❌ No | ❌ No |

---

## 🎯 My Recommendation

**Start with Render** because:
1. Completely free, no credit card needed
2. Easiest GitHub integration
3. Best for learning deployment
4. Can upgrade later if needed

**Note**: For production use with many users, consider upgrading to paid tier or using Railway/DigitalOcean.

---

## 📞 Need Help?

If you face any issues during deployment:
1. Check the platform's logs
2. Verify all environment variables are set
3. Ensure build commands completed successfully
4. Check that database is initialized

Good luck with your deployment! 🚀
