from app import app
from core.quiz_engine import get_quiz_questions

class MockUser:
    def __init__(self, role, edu):
        self.desired_role = role
        self.education_level = edu

def test_quiz_generation():
    with app.app_context():
        test_cases = [
            {"role": "Doctor", "edu": "MBBS"},
            {"role": "Student", "edu": "School (6-10)"},
            {"role": "Student", "edu": "Intermediate (11-12)"},
            {"role": "Accountant", "edu": "B.Com"},
            {"role": "Nurse", "edu": "B.Sc Nursing"}
        ]
        
        for tc in test_cases:
            user = MockUser(tc['role'], tc['edu'])
            questions = get_quiz_questions(user, week_number=1)
            print(f"Role: {tc['role']} | Edu: {tc['edu']} | Questions: {len(questions)}")

if __name__ == "__main__":
    test_quiz_generation()
