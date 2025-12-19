"""
AI Image Analyzer - FastAPI + LangChain + Gemini
A powerful image analysis agent using LangChain and Google's Gemini AI
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from typing import Optional
import os
import base64
from dotenv import load_dotenv
from datetime import datetime
import logging

# LangChain imports
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor, create_structured_chat_agent
from langchain.tools import Tool
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema import HumanMessage
from langchain_core.messages import SystemMessage

# Import settings
from src.config import settings

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=settings.LOG_LEVEL)
logger = logging.getLogger(__name__)

# ============================================
# FASTAPI APP CONFIGURATION
# ============================================
app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================
# GEMINI AI CONFIGURATION
# ============================================
GEMINI_API_KEY = settings.GEMINI_API_KEY
DEMO_MODE = settings.DEMO_MODE

if not GEMINI_API_KEY or GEMINI_API_KEY == "your_gemini_api_key_here":
    logger.warning("⚠️  GEMINI_API_KEY not configured!")
    if DEMO_MODE:
        logger.info("🎭 DEMO_MODE enabled - Using mock responses")
    else:
        logger.warning("   Set DEMO_MODE=true in .env to test without API key")
else:
    logger.info("✅ GEMINI_API_KEY configured")

# Initialize Gemini model with vision capabilities (only if API key is valid)
llm = None
if GEMINI_API_KEY and GEMINI_API_KEY != "your_gemini_api_key_here":
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key=GEMINI_API_KEY,
        temperature=0.7,
    )

# ============================================
# PYDANTIC MODELS
# ============================================
class ImageAnalysisRequest(BaseModel):
    image: str  # Base64 encoded image
    mime_type: Optional[str] = "image/jpeg"

class AnalysisResponse(BaseModel):
    success: bool
    description: str
    timestamp: str
    agent_used: str = "LangChain + Gemini"

# ============================================
# DEMO MODE HELPER
# ============================================
def generate_mock_analysis() -> str:
    """Generate a realistic mock analysis for demo mode"""
    import random
    
    mock_responses = [
        """**Main Subject**: The image features a vibrant outdoor scene with natural elements.

**Visual Elements**: The composition showcases rich colors with excellent lighting. The color palette includes warm tones that create an inviting atmosphere. The image demonstrates good depth of field and professional framing.

**Context & Setting**: This appears to be captured in a natural outdoor environment, possibly during golden hour. The setting suggests a peaceful, serene location with ample natural light.

**Notable Details**: The image exhibits sharp focus on the primary subject with a pleasing bokeh effect in the background. The exposure is well-balanced, capturing details in both highlights and shadows.

**Mood & Atmosphere**: The overall mood is uplifting and positive. The image conveys a sense of tranquility and natural beauty, evoking feelings of peace and harmony with nature.

*Note: This is a DEMO response. Configure your GEMINI_API_KEY for real AI analysis.*""",
        
        """**Main Subject**: A captivating photograph showcasing interesting visual elements and composition.

**Visual Elements**: The image displays a harmonious blend of colors and textures. The lighting creates dynamic contrasts that draw the viewer's attention to key areas. The composition follows the rule of thirds, creating visual balance.

**Context & Setting**: The environment appears to be well-lit with natural or ambient lighting. The background complements the main subject without creating distractions.

**Notable Details**: Fine details are preserved throughout the image. The photographer has successfully captured the essence of the moment with technical precision. The color grading enhances the overall aesthetic appeal.

**Mood & Atmosphere**: The image emanates a professional quality with artistic sensibility. It creates an emotional connection through its visual storytelling, leaving a lasting impression on the viewer.

*Note: This is a DEMO response. Add your GEMINI_API_KEY to .env for actual AI-powered analysis.*""",
        
        """**Main Subject**: An engaging visual composition that captures attention through its subject matter and presentation.

**Visual Elements**: The photograph demonstrates excellent use of light and shadow. Colors are vibrant yet natural, creating visual interest. The composition is well-structured with clear focal points.

**Context & Setting**: The scene is set in an environment that provides context to the subject. The background elements support the narrative without overwhelming the main focus.

**Notable Details**: Attention to detail is evident in the sharpness and clarity of the image. The photographer has skillfully managed depth of field to emphasize the subject while maintaining contextual information.

**Mood & Atmosphere**: The overall feeling is one of authenticity and genuine moment capture. The image successfully communicates its intended message through visual language.

*Note: This is a DEMO MODE response. For real AI analysis powered by Google Gemini, please add your API key to the .env file.*"""
    ]
    
    return random.choice(mock_responses)

# ============================================
# IMAGE ANALYSIS AGENT
# ============================================
class ImageAnalyzerAgent:
    """LangChain Agent for analyzing images using Gemini AI"""
    
    def __init__(self, llm_instance=None):
        self.llm = llm_instance
        self.current_image = None
        self.current_mime_type = None
        self.demo_mode = DEMO_MODE and (llm_instance is None)
        
    def set_image(self, image_base64: str, mime_type: str):
        """Set the current image for analysis"""
        self.current_image = image_base64
        self.current_mime_type = mime_type
    
    def analyze_image_tool(self, query: str) -> str:
        """Tool for analyzing the current image"""
        if not self.current_image:
            return "No image has been uploaded for analysis."
        
        # Demo mode - return mock response
        if self.demo_mode:
            logger.info("🎭 Using DEMO MODE - Returning mock analysis")
            return generate_mock_analysis()
        
        try:
            # Create message with image
            message = HumanMessage(
                content=[
                    {
                        "type": "text",
                        "text": query
                    },
                    {
                        "type": "image_url",
                        "image_url": f"data:{self.current_mime_type};base64,{self.current_image}"
                    }
                ]
            )
            
            # Get response from Gemini
            response = self.llm.invoke([message])
            return response.content
            
        except Exception as e:
            logger.error(f"Error in image analysis: {str(e)}")
            return f"Error analyzing image: {str(e)}"
    
    def create_agent(self):
        """Create the LangChain agent with tools"""
        
        # In demo mode, skip agent creation
        if self.demo_mode:
            return None
        
        # Define tools
        tools = [
            Tool(
                name="analyze_image",
                func=self.analyze_image_tool,
                description="""Use this tool to analyze the uploaded image. 
                This tool can identify objects, describe scenes, read text, 
                analyze colors, composition, mood, and provide detailed descriptions.
                Input should be a specific question or request about the image."""
            )
        ]
        
        # Create agent prompt
        system_message = """You are an expert AI Image Analyzer powered by Google Gemini.
        Your role is to provide comprehensive, detailed analysis of images.
        
        When analyzing an image, you should:
        1. Identify the main subject and key elements
        2. Describe visual characteristics (colors, composition, lighting, style)
        3. Provide context about the setting or environment
        4. Note any interesting or unique details
        5. Describe the mood, atmosphere, or emotion conveyed
        
        Always use the 'analyze_image' tool to examine the uploaded image.
        Provide well-structured, engaging descriptions that are informative and easy to read.
        """
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_message),
            MessagesPlaceholder(variable_name="chat_history", optional=True),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        
        # Create agent
        agent = create_structured_chat_agent(
            llm=self.llm,
            tools=tools,
            prompt=prompt
        )
        
        # Create agent executor
        agent_executor = AgentExecutor(
            agent=agent,
            tools=tools,
            verbose=True,
            handle_parsing_errors=True,
            max_iterations=3
        )
        
        return agent_executor
    
    def analyze(self, custom_prompt: Optional[str] = None) -> str:
        """Run the agent to analyze the image"""
        
        if not self.current_image:
            raise ValueError("No image has been set for analysis")
        
        # Demo mode - return mock response directly
        if self.demo_mode:
            logger.info("🎭 DEMO MODE: Generating mock analysis")
            return generate_mock_analysis()
        
        # Default comprehensive analysis prompt
        default_prompt = """Analyze this image in detail and provide a comprehensive description. Include:

1. **Main Subject**: What is the primary focus of the image?
2. **Visual Elements**: Describe colors, composition, lighting, and style
3. **Context & Setting**: Where does this appear to be? What's the environment?
4. **Notable Details**: Any interesting or unique aspects worth mentioning
5. **Mood & Atmosphere**: What feeling or emotion does the image convey?

Please provide a well-structured, engaging description that captures all important aspects of the image."""
        
        prompt = custom_prompt or default_prompt
        
        # Create and run agent
        agent_executor = self.create_agent()
        result = agent_executor.invoke({"input": prompt})
        
        return result["output"]

# Initialize the agent
image_agent = ImageAnalyzerAgent(llm)

# ============================================
# API ENDPOINTS
# ============================================

@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serve the main HTML page"""
    try:
        # Try to read from src directory first, then root
        html_paths = [
            os.path.join(os.path.dirname(__file__), "index.html"),
            "index.html"
        ]
        
        for html_path in html_paths:
            if os.path.exists(html_path):
                with open(html_path, "r", encoding="utf-8") as f:
                    return HTMLResponse(content=f.read())
        
        # Fallback if no HTML found
        return HTMLResponse(content="<h1>AI Image Analyzer API</h1><p>Upload an image to /analyze endpoint</p>")
    except Exception as e:
        logger.error(f"Error serving HTML: {e}")
        return HTMLResponse(content="<h1>AI Image Analyzer API</h1><p>Upload an image to /analyze endpoint</p>")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "OK",
        "message": "AI Image Analyzer API is running",
        "framework": "FastAPI + LangChain",
        "ai_model": "Google Gemini 1.5 Flash",
        "api_key_configured": bool(GEMINI_API_KEY and GEMINI_API_KEY != "your_gemini_api_key_here"),
        "timestamp": datetime.now().isoformat()
    }

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_image(request: ImageAnalysisRequest):
    """
    Analyze an uploaded image using LangChain agent and Gemini AI
    
    Args:
        request: ImageAnalysisRequest containing base64 image and mime type
    
    Returns:
        AnalysisResponse with detailed image description
    """
    try:
        # Check if API key is configured (only warn in demo mode)
        if not GEMINI_API_KEY or GEMINI_API_KEY == "your_gemini_api_key_here":
            if not DEMO_MODE:
                raise HTTPException(
                    status_code=500,
                    detail="GEMINI_API_KEY not configured. Please add your API key to the .env file or set DEMO_MODE=true"
                )
            logger.info("🎭 Running in DEMO MODE")
        
        logger.info("📸 Starting image analysis with LangChain agent...")
        
        # Set the image in the agent
        image_agent.set_image(request.image, request.mime_type)
        
        # Run the agent analysis
        description = image_agent.analyze()
        
        logger.info("✅ Analysis complete")
        
        agent_name = "LangChain + Gemini 1.5 Flash"
        if DEMO_MODE and (not GEMINI_API_KEY or GEMINI_API_KEY == "your_gemini_api_key_here"):
            agent_name = "DEMO MODE (Add API key for real analysis)"
        
        return AnalysisResponse(
            success=True,
            description=description,
            timestamp=datetime.now().isoformat(),
            agent_used=agent_name
        )
        
    except Exception as e:
        logger.error(f"❌ Error analyzing image: {str(e)}")
        
        error_message = "Failed to analyze image"
        
        if "API key" in str(e):
            error_message = "Invalid API key. Please check your GEMINI_API_KEY in the .env file"
        elif "quota" in str(e).lower():
            error_message = "API quota exceeded. Please check your Gemini API usage limits"
        elif "SAFETY" in str(e):
            error_message = "Image content was flagged by safety filters"
        
        raise HTTPException(status_code=500, detail=error_message)

@app.post("/analyze-file")
async def analyze_uploaded_file(file: UploadFile = File(...)):
    """
    Analyze an uploaded image file directly
    
    Args:
        file: Uploaded image file
    
    Returns:
        AnalysisResponse with detailed image description
    """
    try:
        # Check if API key is configured (only warn in demo mode)
        if not GEMINI_API_KEY or GEMINI_API_KEY == "your_gemini_api_key_here":
            if not DEMO_MODE:
                raise HTTPException(
                    status_code=500,
                    detail="GEMINI_API_KEY not configured. Please add your API key to the .env file or set DEMO_MODE=true"
                )
            logger.info("🎭 Running in DEMO MODE")
        
        # Validate file type
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        logger.info(f"📸 Analyzing uploaded file: {file.filename}")
        
        # Read and encode image
        image_data = await file.read()
        image_base64 = base64.b64encode(image_data).decode("utf-8")
        
        # Set the image in the agent
        image_agent.set_image(image_base64, file.content_type)
        
        # Run the agent analysis
        description = image_agent.analyze()
        
        logger.info("✅ Analysis complete")
        
        agent_name = "LangChain + Gemini 1.5 Flash"
        if DEMO_MODE and (not GEMINI_API_KEY or GEMINI_API_KEY == "your_gemini_api_key_here"):
            agent_name = "DEMO MODE (Add API key for real analysis)"
        
        return AnalysisResponse(
            success=True,
            description=description,
            timestamp=datetime.now().isoformat(),
            agent_used=agent_name
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error analyzing file: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to analyze image: {str(e)}")

# ============================================
# STARTUP EVENT
# ============================================
@app.on_event("startup")
async def startup_event():
    """Log startup information"""
    logger.info("")
    logger.info("🚀 ============================================")
    logger.info("   AI Image Analyzer - FastAPI + LangChain")
    logger.info("   ============================================")
    logger.info(f"   📡 Server starting...")
    logger.info(f"   🤖 AI Model: Google Gemini 1.5 Flash")
    logger.info(f"   🔗 Framework: FastAPI + LangChain")
    logger.info(f"   🔑 API Key: {'✅ Configured' if GEMINI_API_KEY and GEMINI_API_KEY != 'your_gemini_api_key_here' else '❌ Not configured'}")
    logger.info("   ============================================")
    logger.info("")
    
    if not GEMINI_API_KEY or GEMINI_API_KEY == "your_gemini_api_key_here":
        logger.warning("⚠️  WARNING: GEMINI_API_KEY not configured!")
        logger.warning("   Please add your API key to the .env file")
        logger.warning("")

# ============================================
# MAIN ENTRY POINT
# ============================================
if __name__ == "__main__":
    import uvicorn
    
    logger.info(f"🚀 Starting server on {settings.HOST}:{settings.PORT}")
    logger.info(f"🐛 Debug mode: {settings.DEBUG}")
    
    uvicorn.run(
        "src.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
