"""
Run script for AI Image Analyzer
Use this to start the server locally
"""

if __name__ == "__main__":
    import uvicorn
    from src.config import settings
    
    print("=" * 60)
    print("🚀 AI Image Analyzer - Starting Server")
    print("=" * 60)
    print(f"📡 Host: {settings.HOST}")
    print(f"🔌 Port: {settings.PORT}")
    print(f"🐛 Debug: {settings.DEBUG}")
    print(f"🎭 Demo Mode: {settings.DEMO_MODE}")
    print(f"🔑 API Key: {'✅ Configured' if settings.GEMINI_API_KEY and settings.GEMINI_API_KEY != 'your_gemini_api_key_here' else '❌ Not configured'}")
    print("=" * 60)
    print()
    
    uvicorn.run(
        "src.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
