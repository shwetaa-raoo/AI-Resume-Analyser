# 🚀 Quick Deployment Guide

Your Resume Analyzer app is ready to deploy! All files have been committed to GitHub.

## ✅ What's Been Done:

1. ✅ Created deployment configuration files:
   - `Procfile` - for Heroku/Railway
   - `render.yaml` - for Render
   - `runtime.txt` - Python version
   - `setup.sh` - initialization script

2. ✅ Updated `requirements.txt` with gunicorn (production server)

3. ✅ Updated `app.py` to use environment variables for production

4. ✅ All changes pushed to GitHub

---

## 🎯 RECOMMENDED: Deploy to Render (100% Free)

### Quick Steps:

1. **Go to Render**: https://render.com
   - Sign up with your GitHub account (it's free!)

2. **Create Web Service**:
   - Click "New +" → "Web Service"
   - Connect your GitHub: `ALOKKRYDV/resume-analyzer`
   - Click "Connect"

3. **Configure** (Render auto-detects most settings):
   - **Name**: resume-analyzer
   - **Environment**: Python 3
   - **Build Command**: 
     ```
     pip install -r requirements.txt && python -m spacy download en_core_web_sm && python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet')"
     ```
   - **Start Command**: 
     ```
     gunicorn app:app
     ```

4. **Add Environment Variable**:
   - Click "Advanced" → "Add Environment Variable"
   - Key: `SECRET_KEY`
   - Value: `your-secret-random-string-here-123456`

5. **Deploy**:
   - Select **Free** instance type
   - Click "Create Web Service"
   - Wait 5-10 minutes ⏳

6. **Initialize Database** (IMPORTANT - First time only!):
   - After deployment completes, go to "Shell" tab in Render
   - Run this command:
     ```bash
     python -c "from app import app, db; app.app_context().push(); db.create_all()"
     ```

7. **Access Your App** 🎉:
   - You'll get a URL like: `https://resume-analyzer-xxxx.onrender.com`
   - Visit it and start using your app!

---

## 📝 Notes:

- ⚠️ Free tier apps on Render sleep after 15 minutes of inactivity
- 🕐 First request after sleep takes ~30 seconds to wake up
- 💾 Uploaded files are temporary on free tier (reset on redeploy)
- 🚀 For production with persistent storage, upgrade to paid tier ($7/month)

---

## 🔄 Updating Your Deployed App:

Whenever you make changes locally:
```bash
git add .
git commit -m "Your update message"
git push origin main
```

Render will automatically redeploy! 🎯

---

## 🆘 Need More Options?

Check [DEPLOYMENT.md](DEPLOYMENT.md) for:
- Railway deployment (faster, $5 free credit)
- PythonAnywhere deployment (persistent storage)
- Troubleshooting guide
- Feature comparison

---

## 🎊 You're Ready!

Your app is deployment-ready. Just follow the steps above and you'll have it live in ~10 minutes!

Good luck! 🚀
