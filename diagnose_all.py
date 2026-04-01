from app import create_app
from extensions import db
from models import Question, QuizQuestion, User, UserProgress, QuizAttempt

app = create_app()

with app.app_context():
    print("=== INTERVIEW QUESTIONS (Question Model) ===")
    results = db.session.query(Question.category, db.func.count(Question.id)).group_by(Question.category).all()
    for cat, count in results:
        print(f"  {cat}: {count}")

    print("\n=== QUIZ QUESTIONS (QuizQuestion Model) ===")
    results = db.session.query(QuizQuestion.category, db.func.count(QuizQuestion.id)).group_by(QuizQuestion.category).all()
    for cat, count in results:
        print(f"  {cat}: {count}")

    print("\n=== USER DATA PREP WEEKS CHECK ===")
    users = User.query.limit(5).all()
    for u in users:
        print(f"User {u.username} (ID: {u.id}): Profile Prep Weeks = {u.prep_weeks}, Role = {u.desired_role}")
        progress = UserProgress.query.filter_by(user_id=u.id, role=u.desired_role).first()
        if progress:
            print(f"  - Progress Record for {u.desired_role}: Prep Weeks = {progress.prep_weeks}")
        else:
            print(f"  - No Progress Record found for {u.desired_role}")
