# 🚀 Deployment Guide - AI Image Analyzer

Complete guide to deploy your FastAPI + LangChain + Gemini agent to various platforms.

---

## 📋 Pre-Deployment Checklist

✅ **Dynamic Port Configuration** - Uses `PORT` environment variable  
✅ **Demo Mode** - Works without API key for testing  
✅ **CORS Enabled** - Accepts requests from any origin  
✅ **Health Endpoint** - `/health` for monitoring  
✅ **Static Files** - Serves frontend from root  

---

## 🌐 Deployment Options

### **Option 1: Render.com** (Recommended - Free Tier Available)

#### **Steps:**

1. **Push to GitHub** (Already done ✅)
   ```bash
   git push origin main
   ```

2. **Create Render Account**
   - Go to: https://render.com
   - Sign up with GitHub

3. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository: `kasi845/agent_backend`
   - Configure:
     - **Name**: `ai-image-analyzer`
     - **Environment**: `Python 3`
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
     - **Instance Type**: Free

4. **Add Environment Variables**
   - Go to "Environment" tab
   - Add:
     ```
     GEMINI_API_KEY=your_actual_api_key_here
     DEMO_MODE=false
     ```
   - Or leave `DEMO_MODE=true` to test without API key

5. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment (3-5 minutes)
   - Your app will be live at: `https://ai-image-analyzer.onrender.com`

#### **Render Configuration File:**
Already created: `render.yaml`

---

### **Option 2: Railway.app** (Easy & Fast)

#### **Steps:**

1. **Create Railway Account**
   - Go to: https://railway.app
   - Sign up with GitHub

2. **New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose `kasi845/agent_backend`

3. **Configure**
   - Railway auto-detects Python
   - Add environment variables:
     ```
     GEMINI_API_KEY=your_api_key
     DEMO_MODE=false
     ```

4. **Deploy**
   - Railway automatically deploys
   - Get your URL from the dashboard

#### **Railway Configuration:**
Uses `Procfile` (already created)

---

### **Option 3: Heroku** (Classic Platform)

#### **Steps:**

1. **Install Heroku CLI**
   ```bash
   # Download from: https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Login**
   ```bash
   heroku login
   ```

3. **Create App**
   ```bash
   heroku create ai-image-analyzer
   ```

4. **Set Environment Variables**
   ```bash
   heroku config:set GEMINI_API_KEY=your_api_key
   heroku config:set DEMO_MODE=false
   ```

5. **Deploy**
   ```bash
   git push heroku main
   ```

6. **Open App**
   ```bash
   heroku open
   ```

#### **Heroku Configuration:**
Uses `Procfile` and `runtime.txt` (already created)

---

### **Option 4: Google Cloud Run** (Serverless)

#### **Steps:**

1. **Install gcloud CLI**
   ```bash
   # Download from: https://cloud.google.com/sdk/docs/install
   ```

2. **Create Dockerfile** (if not exists)
   ```dockerfile
   FROM python:3.11-slim
   
   WORKDIR /app
   
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt
   
   COPY . .
   
   CMD uvicorn main:app --host 0.0.0.0 --port $PORT
   ```

3. **Build and Deploy**
   ```bash
   gcloud run deploy ai-image-analyzer \
     --source . \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated
   ```

4. **Set Environment Variables**
   ```bash
   gcloud run services update ai-image-analyzer \
     --set-env-vars GEMINI_API_KEY=your_key,DEMO_MODE=false
   ```

---

### **Option 5: Vercel** (Frontend + API)

#### **Steps:**

1. **Install Vercel CLI**
   ```bash
   npm install -g vercel
   ```

2. **Create `vercel.json`**
   ```json
   {
     "builds": [
       {
         "src": "main.py",
         "use": "@vercel/python"
       }
     ],
     "routes": [
       {
         "src": "/(.*)",
         "dest": "main.py"
       }
     ]
   }
   ```

3. **Deploy**
   ```bash
   vercel
   ```

4. **Add Environment Variables**
   - Go to Vercel Dashboard
   - Settings → Environment Variables
   - Add `GEMINI_API_KEY` and `DEMO_MODE`

---

## 🔧 Environment Variables

All platforms need these environment variables:

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `PORT` | No | 8000 | Auto-assigned by platform |
| `GEMINI_API_KEY` | No* | - | Your Gemini API key |
| `DEMO_MODE` | No | true | Enable demo mode |

*Required for real AI analysis, optional if using demo mode

---

## 📊 Testing Your Deployment

### **1. Health Check**
```bash
curl https://your-app-url.com/health
```

Expected response:
```json
{
  "status": "OK",
  "message": "AI Image Analyzer API is running",
  "framework": "FastAPI + LangChain",
  "ai_model": "Google Gemini 1.5 Flash",
  "api_key_configured": true,
  "timestamp": "2025-12-19T..."
}
```

### **2. API Documentation**
Visit: `https://your-app-url.com/docs`

### **3. Test Image Analysis**
```bash
curl -X POST "https://your-app-url.com/analyze-file" \
  -F "file=@test_image.jpg"
```

---

## 🐛 Troubleshooting

### **Port Issues**
- ✅ Fixed: App now uses `PORT` environment variable
- Platform automatically assigns port

### **Module Not Found**
- Check `requirements.txt` is complete
- Rebuild: `pip install -r requirements.txt`

### **API Key Errors**
- Verify environment variable is set correctly
- Use demo mode for testing: `DEMO_MODE=true`

### **CORS Errors**
- Already configured to allow all origins
- Check frontend URL in requests

### **Slow Cold Starts**
- Normal for free tiers
- Upgrade to paid tier for faster response

---

## 💰 Cost Comparison

| Platform | Free Tier | Paid Starting | Best For |
|----------|-----------|---------------|----------|
| **Render** | 750 hrs/month | $7/month | Production |
| **Railway** | $5 credit/month | $5/month | Quick deploys |
| **Heroku** | No free tier | $7/month | Enterprise |
| **Cloud Run** | 2M requests/month | Pay-as-you-go | Serverless |
| **Vercel** | Unlimited | $20/month | Frontend+API |

---

## 🔒 Security Best Practices

1. **Never commit `.env` file** ✅ (Already in `.gitignore`)
2. **Use environment variables** ✅ (Configured)
3. **Enable HTTPS** ✅ (Auto on all platforms)
4. **Rotate API keys** regularly
5. **Monitor usage** via platform dashboards

---

## 📈 Monitoring & Logs

### **Render**
```bash
# View logs
render logs -s ai-image-analyzer
```

### **Railway**
- Dashboard → Deployments → View Logs

### **Heroku**
```bash
heroku logs --tail
```

### **Cloud Run**
- Cloud Console → Cloud Run → Logs

---

## 🚀 Quick Deploy Commands

### **Render (via CLI)**
```bash
render deploy
```

### **Railway**
```bash
railway up
```

### **Heroku**
```bash
git push heroku main
```

### **Vercel**
```bash
vercel --prod
```

---

## 📝 Post-Deployment

1. ✅ Test all endpoints
2. ✅ Check API documentation
3. ✅ Monitor logs for errors
4. ✅ Set up custom domain (optional)
5. ✅ Configure auto-scaling (if needed)

---

## 🎯 Recommended Platform

**For this project, we recommend Render.com:**

✅ Free tier available  
✅ Easy GitHub integration  
✅ Automatic deployments  
✅ Built-in SSL  
✅ Good performance  
✅ Simple environment variable management  

---

## 📞 Support

- **Render**: https://render.com/docs
- **Railway**: https://docs.railway.app
- **Heroku**: https://devcenter.heroku.com
- **Cloud Run**: https://cloud.google.com/run/docs

---

**Your app is ready to deploy! Choose your platform and go live! 🚀**
