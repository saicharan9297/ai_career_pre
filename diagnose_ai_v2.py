import os
import sys
import google.generativeai as genai
from dotenv import load_dotenv

sys.path.append(os.getcwd())
load_dotenv()

print("--- AI DIAGNOSTIC V2 START ---")
api_key = os.getenv("GEMINI_API_KEY")

if api_key:
    api_key = api_key.strip().strip("'").strip('"')
    print(f"Key loaded and cleaned (Length: {len(api_key)})")
else:
    print("[FAIL] GEMINI_API_KEY not found.")

genai.configure(api_key=api_key)

try:
    print("Listing available models...")
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"- {m.name}")
    
    print("\nTesting model call...")
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content("Help!")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"ERROR: {str(e)}")

print("--- AI DIAGNOSTIC V2 END ---")
