import json
from app import create_app
from models import UserProgress
from extensions import db

app = create_app()
with app.app_context():
    p = UserProgress.query.filter_by(user_id=10, role='Software Engineer').first()
    if p:
        simulated_data = {
            'is_ai': True,
            'prep_weeks': 52,
            'modules': [
                {
                    'title': 'Week 1: AI SIMULATED CACHE',
                    'subjects': [
                        {'name': 'Caching Mastery', 'content': 'This content is loaded from the database cache.'}
                    ]
                }
            ]
        }
        p.roadmap_json = json.dumps(simulated_data)
        db.session.commit()
        print("SIMULATED AI CACHE SAVED for saicharan.")
    else:
        print("UserProgress not found.")
