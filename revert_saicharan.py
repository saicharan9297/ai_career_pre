from app import create_app
from models import User
from extensions import db
import os

app = create_app()
with app.app_context():
    u = db.session.get(User, 10)
    if u:
        u.desired_role = 'Software Engineer'
        u.age = None
        u.education_level = None
        db.session.commit()
        print("REVERTED SUCCESS")
    else:
        print("USER 10 NOT FOUND")
