import sys
import os
sys.path.append(os.path.abspath(os.curdir))

from app import app
from models import User
from core.roadmap import generate_roadmap

def test_ias_roadmap():
    with app.app_context():
        user = User(desired_role="IAS", education_level="Graduate", available_time=4, prep_weeks=4)
        roadmap = generate_roadmap(user)
        print(f"Target Role: {roadmap['target_role']}")
        print(f"First Module Title: {roadmap['modules'][0]['title']}")
        for sub in roadmap['modules'][0]['subjects']:
            print(f"  - Subject: {sub['name']}")

if __name__ == "__main__":
    test_ias_roadmap()
