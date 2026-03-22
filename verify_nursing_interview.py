from app import create_app
from extensions import db
from models import User
from core.interview_engine import get_interview_session_questions

def verify_nursing():
    app = create_app()
    with app.app_context():
        scenario = ("bsc nursing", "B.Sc Nursing")
        role, edu = scenario
        print(f"TESTING INTERVIEW: Role='{role}', Edu='{edu}'")
        user = User(desired_role=role, education_level=edu)
        questions = get_interview_session_questions(user)
        
        print(f"  Total Questions: {len(questions)}")
        for i, q in enumerate(questions, 1):
            is_hr = " (HR)" if q.category == "HR" else ""
            print(f"  {i}. [{q.category}]{is_hr} {q.question_text[:100]}...")
        print("-" * 40)

if __name__ == "__main__":
    verify_nursing()
