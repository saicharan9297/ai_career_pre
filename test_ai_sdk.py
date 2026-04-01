import sys
import os

# Add the project root to sys.path
sys.path.append(os.getcwd())

from core.ai_service import call_llm

def test_ai():
    print("Testing AI SDK Call...")
    response = call_llm("Respond with ONLY the word SUCCESS.")
    print(f"Response: {response}")
    if "SUCCESS" in response.upper():
        print("SDK TEST PASSED")
    else:
        print("SDK TEST FAILED")

if __name__ == "__main__":
    test_ai()
