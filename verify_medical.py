from app import app
from core.roadmap import generate_roadmap
from core.quiz_engine import get_quiz_questions

class MockUser:
    def __init__(self, role, edu, time="2 hours/day", weeks=4):
        self.desired_role = role
        self.education_level = edu
        self.available_time = time
        self.prep_weeks = weeks
        self.completed_modules = ""

def verify_medical_sync():
    with app.app_context():
        test_cases = [
            {"role": "Doctor (MBBS)", "edu": "MBBS"},
            {"role": "Staff Nurse", "edu": "B.Sc Nursing"},
            {"role": "Pharmacist", "edu": "B.Pharm"},
            {"role": "Dentist", "edu": "BDS"}
        ]

        for tc in test_cases:
            print(f"\n--- Testing: {tc['role']} ---")
            user = MockUser(tc['role'], tc['edu'])
            
            # Test Roadmap
            roadmap = generate_roadmap(user)
            print(f"Roadmap First Week: {roadmap['modules'][0]['title']}")
            for sub in roadmap['modules'][0]['subjects']:
                print(f"  - Subject: {sub['name']}")
            
            # Test Quiz Sync (Week 1)
            questions = get_quiz_questions(user, week_number=1, count=3)
            print(f"Quiz synced (Week 1)? {'Yes' if len(questions) > 0 else 'No (DB might be empty)'}")
            for q in questions:
                print(f"  - Q: {q.question_text} (Sub: {q.sub_category})")

if __name__ == "__main__":
    verify_medical_sync()
