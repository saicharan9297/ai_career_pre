from app import create_app
from extensions import db
from models import User
from core.roadmap import generate_roadmap

def verify_scenarios():
    app = create_app()
    with app.app_context():
        scenarios = [
            ("Cyber Security", "B.Tech (1st Year)"),
            ("Mechanical Engineer", "B.Tech (1st Year)"),
            ("Electronics Engineer", "B.Tech (1st Year)"),
            ("Cyber Security Specialist", "Job Seeker"),
            ("bank manager", "Degree")
        ]
        
        for role, edu in scenarios:
            print(f"TESTING: Role='{role}', Edu='{edu}'")
            user = User(desired_role=role, education_level=edu, prep_weeks=8)
            res = generate_roadmap(user)
            roadmap = res['modules']
            
            if roadmap:
                print(f"  Week 1 Title: {roadmap[0]['title']}")
                for sub in roadmap[0]['subjects']:
                    print(f"    - {sub['name']}: {sub['content'][:60]}...")
            else:
                print("  ERROR: NO ROADMAP GENERATED")
            print("-" * 40)

if __name__ == "__main__":
    verify_scenarios()
