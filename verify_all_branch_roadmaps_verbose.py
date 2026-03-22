from app import create_app
from extensions import db
from models import User
from core.roadmap import generate_roadmap

def verify_branches():
    app = create_app()
    with app.app_context():
        # Scenarios to test all 7 requested branches
        scenarios = [
            ("ECE", "B.Tech 3rd Year"),
            ("MECH", "B.Tech 2nd Year"),
            ("EEE", "B.Tech 4th Year"),
            ("CHEMICAL", "B.Tech 3rd Year"),
            ("AIML", "B.Tech 4th Year"),
            ("Data Science", "B.Tech 2nd Year"),
            ("CSE", "B.Tech 3rd Year"),
            ("Data Analyst", "Job Seeker")
        ]
        
        for role, edu in scenarios:
            print(f"TESTING: Role='{role}', Edu='{edu}'")
            user = User(desired_role=role, education_level=edu, prep_weeks=8)
            res = generate_roadmap(user)
            roadmap = res['modules']
            
            if roadmap:
                for week in roadmap[:2]: # Show first 2 weeks
                    print(f"  {week['title']}")
                    for sub in week['subjects']:
                        print(f"    - {sub['name']}: {sub['content'][:50]}...")
            else:
                print("  ERROR: NO ROADMAP GENERATED")
            print("-" * 40)

if __name__ == "__main__":
    verify_branches()
