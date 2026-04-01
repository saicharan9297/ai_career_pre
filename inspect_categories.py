from app import create_app
from extensions import db
from models import Question, QuizQuestion

app = create_app()

with app.app_context():
    print("=== ALL INTERVIEW QUESTION CATEGORIES ===")
    results = db.session.query(Question.category, db.func.count(Question.id)).group_by(Question.category).all()
    for cat, count in results:
        print(f"  {cat}: {count}")

    print("\n=== ALL QUIZ QUESTION CATEGORIES ===")
    results = db.session.query(QuizQuestion.category, db.func.count(QuizQuestion.id)).group_by(QuizQuestion.category).all()
    for cat, count in results:
        print(f"  {cat}: {count}")
