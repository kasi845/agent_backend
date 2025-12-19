# 🤖 AI Image Analyzer - FastAPI + LangChain + Gemini

A powerful, production-ready image analysis agent built with **FastAPI**, **LangChain**, and **Google's Gemini AI**. Features a beautiful modern UI and intelligent agent-based image analysis.

![Python](https://img.shields.io/badge/Python-3.9+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green)
![LangChain](https://img.shields.io/badge/LangChain-0.3+-purple)
![Gemini](https://img.shields.io/badge/Gemini-AI-orange)

## ✨ Features

### 🤖 **LangChain Agent Architecture**
- Intelligent agent-based image analysis
- Structured prompts for comprehensive descriptions
- Tool-based architecture for extensibility
- Error handling and retry logic

### 🎨 **Modern UI/UX**
- Beautiful glassmorphism design
- Smooth animations and transitions
- Drag & drop image upload
- Real-time preview
- Responsive design

### 🚀 **FastAPI Backend**
- High-performance async API
- Multiple upload methods (base64, file upload)
- Comprehensive error handling
- CORS enabled
- Auto-generated API docs

### 🧠 **AI-Powered Analysis**
- Google Gemini 1.5 Flash model
- Detailed image descriptions including:
  - Main subject identification
  - Visual elements (colors, composition, lighting)
  - Context and setting
  - Notable details
  - Mood and atmosphere

## 🏗️ Architecture

```
┌─────────────────┐
│   Frontend      │
│   (HTML/CSS/JS) │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   FastAPI       │
│   Server        │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   LangChain     │
│   Agent         │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Gemini AI     │
│   (Vision)      │
└─────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))

### Installation

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure your API key:**
   
   Open the `.env` file and add your Gemini API key:
   ```env
   GEMINI_API_KEY=your_actual_api_key_here
   ```

3. **Start the FastAPI server:**
   ```bash
   python main.py
   ```
   
   Or use uvicorn directly:
   ```bash
   uvicorn main:app --reload --port 8000
   ```

4. **Open your browser:**
   
   Navigate to `http://localhost:8000`

## 📚 API Documentation

FastAPI automatically generates interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Endpoints

#### `GET /health`
Health check endpoint

**Response:**
```json
{
  "status": "OK",
  "message": "AI Image Analyzer API is running",
  "framework": "FastAPI + LangChain",
  "ai_model": "Google Gemini 1.5 Flash",
  "api_key_configured": true,
  "timestamp": "2025-12-19T16:23:28.000Z"
}
```

#### `POST /analyze`
Analyze image from base64 encoded data

**Request:**
```json
{
  "image": "base64_encoded_image_data",
  "mime_type": "image/jpeg"
}
```

**Response:**
```json
{
  "success": true,
  "description": "Detailed AI-generated description...",
  "timestamp": "2025-12-19T16:23:28.000Z",
  "agent_used": "LangChain + Gemini 1.5 Flash"
}
```

#### `POST /analyze-file`
Analyze uploaded image file directly

**Request:** Multipart form data with image file

**Response:** Same as `/analyze`

## 🛠️ Technology Stack

### Backend
- **FastAPI** - Modern, fast web framework
- **LangChain** - Agent orchestration framework
- **Uvicorn** - ASGI server
- **Pydantic** - Data validation
- **python-dotenv** - Environment management

### AI/ML
- **Google Generative AI** - Gemini 1.5 Flash model
- **LangChain Google GenAI** - LangChain integration

### Frontend
- **HTML5** - Semantic markup
- **CSS3** - Modern styling with animations
- **Vanilla JavaScript** - No framework dependencies

## 📁 Project Structure

```
agent/
├── main.py                 # FastAPI app with LangChain agent
├── requirements.txt        # Python dependencies
├── .env                   # Environment variables (API key)
├── .env.example           # Template for .env
├── index.html             # Frontend UI
├── styles.css             # Premium styling
├── script.js              # Frontend logic
├── README.md              # This file
├── PYTHON_GUIDE.md        # Python-specific guide
└── .gitignore            # Git ignore rules
```

## 🎯 How the LangChain Agent Works

### Agent Architecture

1. **ImageAnalyzerAgent Class**
   - Manages image state
   - Creates LangChain tools
   - Orchestrates analysis workflow

2. **Tools**
   - `analyze_image`: Analyzes the uploaded image using Gemini Vision

3. **Agent Prompt**
   - System message defines agent role
   - Structured prompts ensure comprehensive analysis
   - Agent scratchpad for reasoning

4. **Execution Flow**
   ```
   User uploads image
        ↓
   Agent receives analysis request
        ↓
   Agent uses analyze_image tool
        ↓
   Tool sends image to Gemini
        ↓
   Gemini returns description
        ↓
   Agent formats and returns result
   ```

## 🎨 Design Features

- **Glassmorphism Effects** - Modern frosted glass aesthetic
- **Dynamic Gradients** - Animated background effects
- **Smooth Animations** - Enhanced user experience
- **Dark Theme** - Easy on the eyes
- **Custom Typography** - Inter & Space Grotesk fonts
- **Responsive Layout** - Mobile-first approach

## 🔒 Security

- API key stored in `.env` (not committed to git)
- CORS configured for security
- Input validation with Pydantic
- Error messages don't expose sensitive info
- File size limits on uploads

## 🧪 Testing

### Test the API with curl

```bash
# Health check
curl http://localhost:8000/health

# Analyze image (file upload)
curl -X POST -F "file=@path/to/image.jpg" http://localhost:8000/analyze-file
```

### Test with Python

```python
import requests
import base64

# Read and encode image
with open("image.jpg", "rb") as f:
    image_data = base64.b64encode(f.read()).decode()

# Send request
response = requests.post(
    "http://localhost:8000/analyze",
    json={
        "image": image_data,
        "mime_type": "image/jpeg"
    }
)

print(response.json())
```

## 🐛 Troubleshooting

### Server won't start
- Check Python version: `python --version` (need 3.9+)
- Install dependencies: `pip install -r requirements.txt`
- Check if port 8000 is available

### API Key errors
- Ensure `.env` file exists in project root
- Verify API key is valid
- Check for extra spaces or quotes

### Import errors
- Reinstall dependencies: `pip install -r requirements.txt --force-reinstall`
- Use virtual environment: `python -m venv venv`

## 🚀 Deployment

### Using Docker (Optional)

Create a `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:
```bash
docker build -t image-analyzer .
docker run -p 8000:8000 --env-file .env image-analyzer
```

## 📈 Performance

- **Response Time**: ~2-5 seconds per image
- **Concurrent Requests**: Supports async processing
- **Max Image Size**: 50MB (configurable)
- **Supported Formats**: JPG, PNG, GIF, WebP

## 🤝 Contributing

Contributions welcome! Please feel free to submit issues and pull requests.

## 📄 License

MIT License - feel free to use this project for any purpose.

## 🙏 Acknowledgments

- **Google Gemini AI** - Powerful vision capabilities
- **LangChain** - Agent orchestration framework
- **FastAPI** - Modern Python web framework
- **The open-source community**

---

**Built with ❤️ using FastAPI, LangChain, and Google Gemini AI**
