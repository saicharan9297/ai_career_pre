import os
import sys
from app import create_app
from core.roadmap import generate_roadmap
from models import User

app = create_app()

with app.app_context():
    print("--- TESTING AI ROADMAP FOR: Physical Therapist ---")
    mock_user = User(
        username="testuser",
        desired_role="Physical Therapist",
        education_level="B.Tech 4th Year",
        prep_weeks=4,
        completed_modules=""
    )
    
    roadmap = generate_roadmap(mock_user)
    
    print(f"\nRAW ROADMAP TYPE: {type(roadmap)}")
    if roadmap and isinstance(roadmap, list) and len(roadmap) > 0:
        print(f"SAMPLE FIRST ELEMENT TYPE: {type(roadmap[0])}")
        print(f"SAMPLE FIRST ELEMENT: {roadmap[0]}")
    elif roadmap and isinstance(roadmap, dict):
        print(f"SAMPLE DICT KEYS: {roadmap.keys()}")
    
    print("\nFINAL ROADMAP OUTPUT:")
    if roadmap and isinstance(roadmap, dict):
        modules = roadmap.get('modules', [])
        print(f"GUIDANCE: {roadmap.get('guidance')}")
        for week in modules:
            print(f"\n{week.get('title')}")
            for subj in week.get('subjects', []):
                print(f"  - {subj.get('name')}: {subj.get('content')[:50]}...")
    else:
        print("FAIL: Roadmap was invalid or empty.")

print("\n--- TEST END ---")
