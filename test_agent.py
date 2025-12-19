"""
Test script for the AI Image Analyzer
Tests the LangChain agent with a sample image
"""

import requests
import base64
import sys
from pathlib import Path

def test_health():
    """Test the health endpoint"""
    print("🔍 Testing health endpoint...")
    try:
        response = requests.get("http://localhost:8000/health")
        if response.status_code == 200:
            data = response.json()
            print("✅ Server is healthy!")
            print(f"   Framework: {data.get('framework')}")
            print(f"   AI Model: {data.get('ai_model')}")
            print(f"   API Key: {'✅ Configured' if data.get('api_key_configured') else '❌ Not configured'}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        print("   Make sure the server is running: python main.py")
        return False

def test_analyze_file(image_path):
    """Test image analysis with file upload"""
    print(f"\n📸 Testing image analysis with: {image_path}")
    
    if not Path(image_path).exists():
        print(f"❌ Image file not found: {image_path}")
        return False
    
    try:
        with open(image_path, "rb") as f:
            files = {"file": f}
            response = requests.post(
                "http://localhost:8000/analyze-file",
                files=files
            )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Analysis successful!")
            print(f"\n🤖 Agent: {data.get('agent_used')}")
            print(f"\n📝 Description:\n{data.get('description')}\n")
            return True
        else:
            error = response.json()
            print(f"❌ Analysis failed: {error.get('detail')}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_analyze_base64(image_path):
    """Test image analysis with base64 encoding"""
    print(f"\n📸 Testing base64 analysis with: {image_path}")
    
    if not Path(image_path).exists():
        print(f"❌ Image file not found: {image_path}")
        return False
    
    try:
        # Read and encode image
        with open(image_path, "rb") as f:
            image_data = base64.b64encode(f.read()).decode()
        
        # Determine mime type
        ext = Path(image_path).suffix.lower()
        mime_types = {
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.gif': 'image/gif',
            '.webp': 'image/webp'
        }
        mime_type = mime_types.get(ext, 'image/jpeg')
        
        # Send request
        response = requests.post(
            "http://localhost:8000/analyze",
            json={
                "image": image_data,
                "mime_type": mime_type
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Analysis successful!")
            print(f"\n🤖 Agent: {data.get('agent_used')}")
            print(f"\n📝 Description:\n{data.get('description')}\n")
            return True
        else:
            error = response.json()
            print(f"❌ Analysis failed: {error.get('detail')}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Main test function"""
    print("=" * 60)
    print("🧪 AI Image Analyzer - Test Suite")
    print("=" * 60)
    
    # Test health
    if not test_health():
        print("\n❌ Server is not running. Start it with: python main.py")
        sys.exit(1)
    
    # Check for image argument
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
        
        # Test file upload
        test_analyze_file(image_path)
        
        # Test base64
        test_analyze_base64(image_path)
    else:
        print("\n💡 Usage: python test_agent.py <path_to_image>")
        print("   Example: python test_agent.py test_image.jpg")
    
    print("\n" + "=" * 60)
    print("✅ Tests complete!")
    print("=" * 60)

if __name__ == "__main__":
    main()
