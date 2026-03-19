import sys
import os

# Add the project directory to sys.path
sys.path.append(os.path.abspath(os.curdir))

from app import app
from extensions import db
from models import User
from core.roadmap import generate_roadmap
from core.quiz_engine import get_quiz_questions

def test_tech_roadmap_8_weeks():
    with app.app_context():
        # Create a mock user
        user = User(
            username="test_tech",
            email="test_tech@example.com",
            password="password",
            desired_role="Full Stack Developer",
            prep_weeks=8
        )
        
        # Test Roadmap
        roadmap_data = generate_roadmap(user)
        print(f"Target Role: {roadmap_data['target_role']}")
        print(f"Prep Weeks: {roadmap_data['prep_weeks']}")
        
        for i, module in enumerate(roadmap_data['modules']):
            print(f"Week {i+1}: {module['title']}")
            for sub in module['subjects']:
                print(f"  - {sub['name']}")
        
        # Basic assertions
        assert len(roadmap_data['modules']) == 8
        assert "Core CSE Foundations" in roadmap_data['modules'][0]['title']
        
        print("\nRoadmap Verification Successful (8 Weeks distributed)!")
        
        # Test Quiz Questions for Week 1
        week1_questions = get_quiz_questions(user, week_number=1, count=3)
        print(f"\nWeek 1 Quiz Questions:")
        for q in week1_questions:
            print(f"  - {q.question_text} (Sub: {q.sub_category})")
            
        # Test Quiz Questions for Week 5
        week5_questions = get_quiz_questions(user, week_number=5, count=3)
        print(f"\nWeek 5 Quiz Questions (Mapped to DB Week 1):")
        for q in week5_questions:
            print(f"  - {q.question_text} (Sub: {q.sub_category})")

if __name__ == "__main__":
    test_tech_roadmap_8_weeks()
