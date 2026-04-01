import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY", "").strip().strip("'").strip('"')

def test_api(version="v1beta", model="gemini-1.5-flash"):
    url = f"https://generativelanguage.googleapis.com/{version}/models/{model}:generateContent?key={api_key}"
    headers = {'Content-Type': 'application/json'}
    data = {
        "contents": [{"parts": [{"text": "Hi"}]}]
    }
    
    print(f"Testing {version} {model}...", end=" ")
    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            print("SUCCESS")
            # print(response.json())
        else:
            print(f"FAIL ({response.status_code}) - {response.text[:100]}")
    except Exception as e:
        print(f"ERROR: {str(e)}")

if api_key:
    test_api("v1beta", "gemini-1.5-flash")
    test_api("v1", "gemini-1.5-flash")
    test_api("v1", "gemini-pro")
    test_api("v1beta", "gemini-pro")
else:
    print("No key found.")
