from app import create_app
from models import User
from core.interview_engine import get_interview_session_questions

app = create_app()

def verify_role(role, edu):
    with app.app_context():
        user = User(username="test_user", desired_role=role, education_level=edu)
        questions = get_interview_session_questions(user)
        print(f"\n--- Verification for Role: {role} | Edu: {edu} ---")
        print(f"Total Questions: {len(questions)}")
        for i, q in enumerate(questions):
            print(f"  {i+1}. [{q.category}] {q.question_text[:100]}...")

if __name__ == "__main__":
    verify_role("IAS Officer", "Degree")
    verify_role("ECE Engineer", "B.Tech (4th Year)")
    verify_role("Software Developer", "Any")
    verify_role("Medical Doctor", "MBBS")
    verify_role("APPSC Group 1", "Degree")
