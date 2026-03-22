from app import create_app
from extensions import db
from models import Question

def check_medical_questions():
    app = create_app()
    with app.app_context():
        qs = Question.query.filter_by(category='Medical').all()
        for q in qs:
            print(f"ID: {q.id}, Question: {q.question_text}")

if __name__ == "__main__":
    check_medical_questions()
