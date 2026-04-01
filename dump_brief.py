from app import create_app
from models import User, UserProgress
from extensions import db

app = create_app()
with app.app_context():
    users = User.query.all()
    print("COUNT: " + str(len(users)))
    for u in users:
        print(f"USER_ID: {u.id}")
        print(f"USERNAME: {u.username}")
        print(f"ROLE: {u.desired_role}")
        print(f"AGE: {u.age}")
        print(f"EDU: {u.education_level}")
        print(f"WEEKS: {u.prep_weeks}")
        print("-" * 20)
