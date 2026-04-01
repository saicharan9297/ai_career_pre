import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if api_key:
    api_key = api_key.strip().strip("'").strip('"')
    genai.configure(api_key=api_key)
    
    models_to_test = [
        'gemini-1.5-flash',
        'gemini-1.5-pro',
        'gemini-pro',
        'models/gemini-1.5-flash',
        'models/gemini-pro'
    ]
    
    print(f"Testing Gemini API Key (Len: {len(api_key)})")
    
    for model_name in models_to_test:
        try:
            print(f"Testing {model_name}...", end=" ")
            model = genai.GenerativeModel(model_name)
            response = model.generate_content("Hi")
            print(f"SUCCESS: {response.text[:20]}...")
            # If we find a working one, we'll keep it as the primary choice for the app later
        except Exception as e:
            msg = str(e)
            if "403" in msg:
                print(f"FAIL: 403 Forbidden (Check Key/Billing)")
                break # If 403, key is bad, no point testing more models
            else:
                print(f"FAIL: {msg[:100]}")
else:
    print("No GEMINI_API_KEY found.")
