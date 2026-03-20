from app import app
from core.quiz_engine import get_quiz_questions

class MockUser:
    def __init__(self, role, edu="MBBS"):
        self.desired_role = role
        self.education_level = edu

def verify_uniqueness():
    with app.app_context():
        user = MockUser("Doctor")
        for week in range(1, 5):
            print(f"\n--- Week {week} Topics ---")
            questions = get_quiz_questions(user, week_number=week, count=5)
            for i, q in enumerate(questions):
                print(f"{i+1}. [{q.sub_category}] {q.question_text}")

if __name__ == "__main__":
    verify_uniqueness()
