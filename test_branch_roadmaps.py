from app import create_app
from extensions import db
from models import User
from core.roadmap import generate_roadmap
from core.quiz_engine import get_quiz_questions
from core.interview_engine import get_interview_session_questions

def test_branches():
    app = create_app()
    with app.app_context():
        test_cases = [
            {"name": "ECE Student", "edu": "B.Tech (3rd Year)", "role": "Electronics Engineer"},
            {"name": "ECE Job Seeker", "edu": "Job Seeker", "role": "Electronics Engineer"},
            {"name": "Mech Job Seeker", "edu": "Job Seeker", "role": "Mechanical Engineer"},
            {"name": "AIML Professional", "edu": "Professional", "role": "AI Engineer"},
            {"name": "Civil Student", "edu": "B.Tech (3rd Year)", "role": "Civil Engineer"}
        ]

        for case in test_cases:
            print(f"\n--- Testing for: {case['name']} ---")
            mock_user = User(
                education_level=case['edu'],
                desired_role=case['role']
            )
            
            # Test Roadmap
            roadmap_data = generate_roadmap(mock_user)
            print(f"Roadmap Themes: {[m['title'] for m in roadmap_data['modules']]}")
            
            # Test Quiz Questions
            quiz_qs = get_quiz_questions(mock_user, week_number=1)
            print(f"Quiz Categories: {list(set([q.category for q in quiz_qs]))}")
            if quiz_qs:
                print(f"Sample Quiz Q: {quiz_qs[0].question_text[:50]}...")
            
            # Test Interview Questions
            interview_qs = get_interview_session_questions(mock_user)
            print(f"Interview Categories: {list(set([q.category for q in interview_qs]))}")
            if interview_qs:
                sample_tech = [q for q in interview_qs if q.category != "HR"]
                if sample_tech:
                    print(f"Sample Tech Interview Q: {sample_tech[0].question_text[:50]}...")

if __name__ == "__main__":
    test_branches()
