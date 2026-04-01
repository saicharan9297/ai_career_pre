import sys
import os

# Add the project root to sys.path
sys.path.append(os.getcwd())

from core.roadmap import generate_roadmap

class MockUser:
    def __init__(self, desired_role, education_level, available_time=2, prep_weeks=4):
        self.desired_role = desired_role
        self.education_level = education_level
        self.available_time = available_time
        self.prep_weeks = prep_weeks
        self.completed_modules = ""

def test_unknown_role():
    print("Testing Unknown Role: 'Space Architect'")
    user = MockUser(desired_role="Space Architect", education_level="B.Tech 3rd Year")
    roadmap = generate_roadmap(user)
    
    print(f"Strategy: {roadmap['strategy']}")
    print(f"Modules: {len(roadmap['modules'])}")
    print(f"First Module Title: {roadmap['modules'][0]['title']}")
    print(f"Instructions: {roadmap.get('instructions')}")
    
    assert "Space Architect" in roadmap['instructions']
    assert "Advanced Technical Readiness" in roadmap['modules'][0]['title']
    print("SUCCESS: Unknown role handled correctly.\n")

def test_placeholder_role():
    print("Testing Placeholder Role: 'Career Search'")
    user = MockUser(desired_role="Career Search", education_level="B.Tech 2nd Year")
    roadmap = generate_roadmap(user)
    
    print(f"Strategy: {roadmap['strategy']}")
    print(f"First Module Title: {roadmap['modules'][0]['title']}")
    print(f"Instructions: {roadmap.get('instructions')}")
    
    assert roadmap.get('instructions') is None or "Our AI generator is currently busy" in roadmap.get('instructions', "")
    assert "Core Technical Foundations" in roadmap['modules'][0]['title']
    print("SUCCESS: Placeholder role handled correctly.\n")

if __name__ == "__main__":
    try:
        test_unknown_role()
        test_placeholder_role()
        print("ALL TESTS PASSED")
    except Exception as e:
        print(f"TEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
