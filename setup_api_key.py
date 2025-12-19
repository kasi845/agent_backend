"""
Quick setup script to configure your Gemini API key
"""

import os
from pathlib import Path

def setup_api_key():
    """Interactive setup for Gemini API key"""
    
    print("=" * 60)
    print("🔑 AI Image Analyzer - API Key Setup")
    print("=" * 60)
    print()
    
    # Check if .env exists
    env_file = Path(".env")
    
    if not env_file.exists():
        print("❌ .env file not found!")
        print("Creating .env file...")
        env_file.write_text("GEMINI_API_KEY=your_gemini_api_key_here\n")
        print("✅ Created .env file")
        print()
    
    # Read current content
    current_content = env_file.read_text()
    
    # Check if key is configured
    if "your_gemini_api_key_here" in current_content or "GEMINI_API_KEY=" not in current_content:
        print("⚠️  API key not configured yet!")
        print()
        print("📝 To get your Gemini API key:")
        print("   1. Visit: https://makersuite.google.com/app/apikey")
        print("   2. Sign in with your Google account")
        print("   3. Click 'Create API Key' or 'Get API Key'")
        print("   4. Copy the key (starts with 'AIzaSy...')")
        print()
        
        # Ask for API key
        api_key = input("🔑 Paste your Gemini API key here (or press Enter to skip): ").strip()
        
        if api_key:
            if api_key.startswith("AIzaSy"):
                # Update .env file
                new_content = f"GEMINI_API_KEY={api_key}\n"
                env_file.write_text(new_content)
                print()
                print("✅ API key saved successfully!")
                print()
                print("🚀 Next steps:")
                print("   1. Run: python main.py")
                print("   2. Open: http://localhost:8000")
                print("   3. Upload an image and analyze!")
                print()
                return True
            else:
                print()
                print("❌ Invalid API key format!")
                print("   Gemini API keys should start with 'AIzaSy'")
                print()
                print("💡 Manual setup:")
                print(f"   1. Open the .env file in your editor")
                print(f"   2. Replace 'your_gemini_api_key_here' with your actual key")
                print(f"   3. Save the file")
                print()
                return False
        else:
            print()
            print("⏭️  Skipped API key setup")
            print()
            print("💡 Manual setup:")
            print(f"   1. Open the .env file in your editor")
            print(f"   2. Replace 'your_gemini_api_key_here' with your actual key")
            print(f"   3. Save the file and restart the server")
            print()
            return False
    else:
        print("✅ API key is already configured!")
        print()
        print("🚀 You're ready to go!")
        print("   Run: python main.py")
        print()
        return True

if __name__ == "__main__":
    setup_api_key()
    print("=" * 60)
