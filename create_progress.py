from app import create_app
from models import User, UserProgress
from extensions import db

app = create_app()
with app.app_context():
    u = User.query.get(10)
    if u:
        p = UserProgress.query.filter_by(user_id=10, role='Software Engineer').first()
        if not p:
            p = UserProgress(user_id=10, role='Software Engineer', prep_weeks=u.prep_weeks)
            db.session.add(p)
            db.session.commit()
            print("UserProgress created for saicharan.")
        else:
            print("UserProgress already exists.")
    else:
        print("User 10 not found.")
