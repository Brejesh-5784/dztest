# check_models.py
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("❌ Error: GOOGLE_API_KEY not found in environment.")
else:
    print(f"✅ API Key found: {api_key[:5]}...*****")
    genai.configure(api_key=api_key)

    print("\n🔍 Available Models for your key:")
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"   - {m.name.replace('models/', '')}")
    except Exception as e:
        print(f"❌ Error listing models: {e}")