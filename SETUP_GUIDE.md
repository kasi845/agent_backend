# 🚀 Quick Start - AI Image Analyzer

## ⚡ Fast Setup (3 Steps)

### 1️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 2️⃣ Add Your API Key
Edit `.env` file:
```env
GEMINI_API_KEY=your_actual_gemini_api_key_here
```

Get your key: https://makersuite.google.com/app/apikey

### 3️⃣ Start the Server
```bash
python main.py
```

Then open: **http://localhost:8000**

---

## 📋 What You Get

✅ **FastAPI Backend** - High-performance async server  
✅ **LangChain Agent** - Intelligent image analysis  
✅ **Gemini AI** - Google's latest vision model  
✅ **Modern UI** - Beautiful, responsive interface  
✅ **API Docs** - Auto-generated at `/docs`  

---

## 🎯 Quick Test

### Test with Browser
1. Open http://localhost:8000
2. Upload an image
3. Click "Analyze Image"
4. View AI-generated description

### Test with Python
```python
import requests
import base64

# Read image
with open("image.jpg", "rb") as f:
    img = base64.b64encode(f.read()).decode()

# Analyze
response = requests.post(
    "http://localhost:8000/analyze",
    json={"image": img, "mime_type": "image/jpeg"}
)

print(response.json()["description"])
```

### Test with curl
```bash
curl -X POST "http://localhost:8000/analyze-file" \
  -F "file=@image.jpg"
```

---

## 🤖 The LangChain Agent

### What is it?
A **LangChain agent** that intelligently analyzes images using:
- **Tools**: Functions to interact with Gemini AI
- **Prompts**: Structured instructions for comprehensive analysis
- **Executor**: Orchestrates the analysis workflow

### How it works:
```
Upload Image → Agent Receives Request → Uses analyze_image Tool
    ↓
Gemini AI Analyzes → Returns Description → Agent Formats Result
```

### Code Location:
- **main.py** - `ImageAnalyzerAgent` class
- Lines 30-150 contain the agent implementation

---

## 📚 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Web interface |
| `/health` | GET | Health check |
| `/analyze` | POST | Analyze (base64) |
| `/analyze-file` | POST | Analyze (file upload) |
| `/docs` | GET | API documentation |

---

## 🎨 Features

### Backend
- ⚡ FastAPI async framework
- 🤖 LangChain agent architecture
- 🧠 Gemini 1.5 Flash AI
- 📝 Pydantic validation
- 🔒 CORS security
- 📊 Comprehensive logging

### Frontend
- 🎨 Glassmorphism design
- 🖱️ Drag & drop upload
- 📱 Responsive layout
- ✨ Smooth animations
- 📋 Copy to clipboard
- 🌙 Dark theme

---

## 🐛 Troubleshooting

### "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### "API key not configured"
Add your key to `.env` file (no quotes)

### "Port 8000 in use"
Change port in `main.py`:
```python
uvicorn.run("main:app", port=8001)
```

---

## 📖 Full Documentation

- **README.md** - Complete documentation
- **PYTHON_GUIDE.md** - Python-specific guide
- **API Docs** - http://localhost:8000/docs

---

## 🎓 Learn More

- **FastAPI**: https://fastapi.tiangolo.com
- **LangChain**: https://python.langchain.com
- **Gemini**: https://ai.google.dev

---

**Ready to analyze images with AI! 🎉**
