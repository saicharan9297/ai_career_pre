from app import create_app
from extensions import db
from models import QuizQuestion, Question

def count_data():
    app = create_app()
    with app.app_context():
        quiz_count = QuizQuestion.query.count()
        interview_count = Question.query.count()
        print(f"Total Quiz Questions: {quiz_count}")
        print(f"Total Interview Questions: {interview_count}")

if __name__ == "__main__":
    count_data()
