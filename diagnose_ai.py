import os
import sys

# Add current directory to path
sys.path.append(os.getcwd())

print("--- AI DIAGNOSTIC START ---")

# 1. Check dependencies
try:
    import google.generativeai as genai
    import dotenv
    print("[SUCCESS] google-generativeai and python-dotenv are installed.")
except ImportError as e:
    print(f"[FAIL] Missing dependency: {str(e)}")
    print("Please run: pip install google-generativeai python-dotenv")
    sys.exit(1)

# 2. Check .env file
if os.path.exists(".env"):
    print("[SUCCESS] .env file found.")
    dotenv.load_dotenv()
else:
    print("[WARNING] .env file NOT found. Check if you renamed .env.example to .env")

# 3. Check API Key
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    if api_key == "your_gemini_api_key_here":
        print("[FAIL] GEMINI_API_KEY is still the placeholder value.")
    else:
        print(f"[SUCCESS] GEMINI_API_KEY found (starts with {api_key[:4]}...)")
else:
    print("[FAIL] GEMINI_API_KEY not found in environment.")

# 4. Test API Call
if api_key and api_key != "your_gemini_api_key_here":
    try:
        print("Testing Gemini API call...")
        from core.ai_service import call_llm
        response = call_llm("Hello, respond with the word 'READY' if you can hear me.")
        print(f"AI Response: {response}")
        if "READY" in response.upper():
            print("[SUCCESS] Gemini API is working correctly.")
        else:
            print("[WARNING] Received unexpected response from AI.")
    except Exception as e:
        print(f"[FAIL] Error during API call: {str(e)}")

print("--- AI DIAGNOSTIC END ---")
