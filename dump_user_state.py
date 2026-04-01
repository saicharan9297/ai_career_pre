from app import create_app
from models import User, UserProgress, QuizAttempt
from extensions import db

app = create_app()
with app.app_context():
    users = User.query.all()
    print("--- USER PROFILES ---")
    for u in users:
        print(f"User ID: {u.id}, Username: {u.username}")
        print(f"  Desired Role: {u.desired_role}")
        print(f"  Education: {u.education_level}")
        print(f"  Prep Weeks: {u.prep_weeks}")
        print(f"  Readiness Score: {u.readiness_score}")
        print(f"  Completed Modules: {u.completed_modules}")
        
        progress = UserProgress.query.filter_by(user_id=u.id).all()
        print(f"  --- Saved Progress ({len(progress)}) ---")
        for p in progress:
            print(f"    Role: {p.role}, Weeks: {p.prep_weeks}, Score: {p.readiness_score}, Modules: {p.completed_modules}")
        
        attempts = QuizAttempt.query.filter_by(user_id=u.id).all()
        print(f"  --- Quiz Attempts ({len(attempts)}) ---")
        for a in attempts:
            print(f"    Week {a.week_number} ({a.category}): Score {a.score}/{a.total_questions}")
        print("-" * 30)
