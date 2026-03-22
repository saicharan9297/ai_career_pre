from app import create_app
from extensions import db
from models import User
from core.roadmap import generate_roadmap

def verify_scenarios():
    app = create_app()
    with app.app_context():
        scenarios = [
            ("bank manager", "Degree"),
            ("Electronics Engineer", "B.Tech 3rd Year"),
            ("Mechanical Designer", "B.Tech 2nd Year"),
            ("Data Scientist", "Job Seeker")
        ]
        
        for role, edu in scenarios:
            print(f"TESTING: Role='{role}', Edu='{edu}'")
            user = User(desired_role=role, education_level=edu, prep_weeks=8)
            res = generate_roadmap(user)
            roadmap = res['modules']
            
            if roadmap:
                print(f"  Strategy: {res['strategy']}")
                for week in roadmap[:1]: # Show first week
                    print(f"  {week['title']}")
                    for sub in week['subjects']:
                        print(f"    - {sub['name']}")
            else:
                print("  ERROR: NO ROADMAP GENERATED")
            print("-" * 40)

if __name__ == "__main__":
    verify_scenarios()
