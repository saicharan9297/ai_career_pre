from app import create_app
from extensions import db
from models import Question

def check_categories():
    app = create_app()
    with app.app_context():
        cats = db.session.query(Question.category, db.func.count(Question.id)).group_by(Question.category).all()
        for cat, count in cats:
            print(f"Category: {cat}, Count: {count}")

if __name__ == "__main__":
    check_categories()
