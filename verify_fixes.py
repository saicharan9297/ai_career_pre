from app import create_app
from extensions import db
from models import User, UserProgress, Question
from core.interview_engine import get_interview_session_questions
from core.roadmap import generate_roadmap

app = create_app()

def test_prep_weeks_update():
    with app.app_context():
        # Simulate a user
        user = User.query.filter_by(username="saicharan").first()
        if not user:
            print("Test user not found, skipping prep_weeks test.")
            return

        print(f"\n--- Testing Prep Weeks Update for {user.username} ---")
        role = "Full Stack Developer"
        new_weeks = 12
        
        # Simulate the logic in app.py onboarding
        progress = UserProgress.query.filter_by(user_id=user.id, role=role).first()
        if progress:
            print(f"Existing progress found for {role} with {progress.prep_weeks} weeks.")
            user.prep_weeks = new_weeks # This is my fix
            db.session.commit()
            print(f"Updated user.prep_weeks to {user.prep_weeks} (Target: {new_weeks})")
        
        # Verify roadmap generation
        roadmap = generate_roadmap(user)
        print(f"Roadmap generated {len(roadmap['modules'])} weeks.")
        if len(roadmap['modules']) == new_weeks:
            print("SUCCESS: Roadmap duration matches updated weeks.")
        else:
            print(f"FAILURE: Roadmap duration is {len(roadmap['modules'])}, expected {new_weeks}.")

def test_interview_role_specificity():
    with app.app_context():
        # Test 1: Medical Role
        user_med = User(desired_role="Doctor", education_level="MBBS")
        questions_med = get_interview_session_questions(user_med)
        print("\n--- Testing Interview Role Specificity (Doctor) ---")
        for q in questions_med:
            print(f"  [{q.category}] {q.question_text[:50]}...")
        
        # Test 2: Tech Role
        user_tech = User(desired_role="Software Engineer", education_level="B.Tech")
        questions_tech = get_interview_session_questions(user_tech)
        print("\n--- Testing Interview Role Specificity (Software Engineer) ---")
        for q in questions_tech:
            print(f"  [{q.category}] {q.question_text[:50]}...")

        # Verify no mixing (e.g., Medical in Tech)
        med_in_tech = [q for q in questions_tech if q.category == "Medical"]
        if med_in_tech:
            print("FAILURE: Medical questions found in Tech interview!")
        else:
            print("SUCCESS: No mixed domains found in Tech interview.")

if __name__ == "__main__":
    test_prep_weeks_update()
    test_interview_role_specificity()
