# 🐍 Python Setup Guide - AI Image Analyzer

## Quick Start with Python + FastAPI + LangChain

### ✅ What You Have

A complete **LangChain agent** implementation with:
- FastAPI backend server
- Intelligent image analysis agent
- Google Gemini AI integration
- Beautiful modern UI
- Comprehensive error handling

### 📋 Prerequisites

1. **Python 3.9+** - Check version:
   ```bash
   python --version
   ```

2. **pip** - Python package manager (comes with Python)

3. **Gemini API Key** - Get from: https://makersuite.google.com/app/apikey

---

## 🚀 Installation Steps

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `langchain` - Agent framework
- `langchain-google-genai` - Gemini integration
- `python-dotenv` - Environment variables
- `python-multipart` - File uploads
- And more...

### Step 2: Configure API Key

1. Open the `.env` file
2. Replace `your_gemini_api_key_here` with your actual API key:
   ```env
   GEMINI_API_KEY=AIzaSy...your_key_here
   ```
3. Save the file

### Step 3: Start the Server

```bash
python main.py
```

Or use uvicorn directly:
```bash
uvicorn main:app --reload --port 8000
```

### Step 4: Open the Application

Navigate to: **http://localhost:8000**

---

## 🤖 Understanding the LangChain Agent

### Agent Architecture

The `ImageAnalyzerAgent` class implements a LangChain agent with:

1. **Tools** - Functions the agent can use:
   - `analyze_image`: Sends image to Gemini for analysis

2. **Prompt Template** - Guides the agent's behavior:
   - System message defines the agent's role
   - Structured format for comprehensive analysis

3. **Agent Executor** - Orchestrates the workflow:
   - Receives user request
   - Decides which tools to use
   - Formats and returns results

### How It Works

```python
# 1. User uploads image
image_agent.set_image(base64_image, mime_type)

# 2. Agent analyzes with custom prompt
description = image_agent.analyze()

# 3. Agent uses the analyze_image tool
# 4. Tool sends image to Gemini
# 5. Gemini returns detailed description
# 6. Agent formats and returns result
```

### Key Components

**main.py** contains:
- `ImageAnalyzerAgent` class - The LangChain agent
- FastAPI routes - API endpoints
- Gemini integration - AI model setup
- Error handling - Comprehensive error management

---

## 📚 API Endpoints

### Interactive Documentation

FastAPI auto-generates API docs:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Available Endpoints

#### 1. Health Check
```bash
GET http://localhost:8000/health
```

#### 2. Analyze Image (Base64)
```bash
POST http://localhost:8000/analyze
Content-Type: application/json

{
  "image": "base64_encoded_data",
  "mime_type": "image/jpeg"
}
```

#### 3. Analyze Image (File Upload)
```bash
POST http://localhost:8000/analyze-file
Content-Type: multipart/form-data

file: <image_file>
```

---

## 🎯 Testing the Agent

### Test with Python Script

Create `test_agent.py`:

```python
import requests
import base64

# Read image
with open("test_image.jpg", "rb") as f:
    image_data = base64.b64encode(f.read()).decode()

# Send to agent
response = requests.post(
    "http://localhost:8000/analyze",
    json={
        "image": image_data,
        "mime_type": "image/jpeg"
    }
)

# Print result
result = response.json()
print(f"Agent: {result['agent_used']}")
print(f"Description:\n{result['description']}")
```

Run:
```bash
python test_agent.py
```

### Test with curl

```bash
curl -X POST "http://localhost:8000/analyze-file" \
  -F "file=@image.jpg"
```

---

## 🔧 Customization

### Modify Agent Behavior

Edit the system message in `main.py`:

```python
system_message = """You are an expert AI Image Analyzer.
Your custom instructions here...
"""
```

### Add More Tools

Extend the agent with additional tools:

```python
tools = [
    Tool(
        name="analyze_image",
        func=self.analyze_image_tool,
        description="Analyzes images"
    ),
    Tool(
        name="detect_objects",
        func=self.detect_objects_tool,
        description="Detects objects in images"
    ),
    # Add more tools...
]
```

### Change AI Model

Modify the model in `main.py`:

```python
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",  # Use Pro instead of Flash
    google_api_key=GEMINI_API_KEY,
    temperature=0.7,
)
```

---

## 🐛 Troubleshooting

### "ModuleNotFoundError"
```bash
pip install -r requirements.txt --force-reinstall
```

### "API key not configured"
- Check `.env` file exists
- Verify API key is correct
- No quotes around the key

### "Port already in use"
Change port in `main.py`:
```python
uvicorn.run("main:app", port=8001)  # Use different port
```

### Agent not responding
- Check logs in terminal
- Verify API key is valid
- Check internet connection

---

## 📊 Performance Tips

### Use Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Enable Caching

Add caching to reduce API calls:

```python
from functools import lru_cache

@lru_cache(maxsize=100)
def analyze_cached(image_hash):
    # Your analysis code
    pass
```

---

## 🚀 Production Deployment

### Environment Variables

Create production `.env`:
```env
GEMINI_API_KEY=your_production_key
PORT=8000
HOST=0.0.0.0
LOG_LEVEL=info
```

### Run with Gunicorn

```bash
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Docker Deployment

```bash
docker build -t image-analyzer .
docker run -p 8000:8000 --env-file .env image-analyzer
```

---

## 📝 Next Steps

1. ✅ Install dependencies
2. ✅ Add your Gemini API key
3. ✅ Start the server
4. ✅ Test with an image
5. ✅ Explore the API docs
6. ✅ Customize the agent
7. ✅ Deploy to production

---

## 🎓 Learning Resources

- **FastAPI**: https://fastapi.tiangolo.com/
- **LangChain**: https://python.langchain.com/
- **Gemini API**: https://ai.google.dev/docs
- **Python Async**: https://docs.python.org/3/library/asyncio.html

---

**Happy Coding! 🎉**
