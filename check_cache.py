from app import create_app
from models import UserProgress
from extensions import db
import json

app = create_app()
with app.app_context():
    # User ID 10 is saicharan
    p = UserProgress.query.filter_by(user_id=10, role='Software Engineer').first()
    if p:
        print(f"User: saicharan (ID 10), Role: {p.role}")
        print(f"Cache Present: {p.roadmap_json is not None}")
        if p.roadmap_json:
            data = json.loads(p.roadmap_json)
            print(f"Cache Is AI: {data.get('is_ai', False)}")
    else:
        print("UserProgress not found for user ID 10 and role 'Software Engineer'.")
