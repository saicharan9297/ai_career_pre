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
            ("Data Analyst", "Job Seeker") # Should map to Data Science
        ]
        
        print(f"{'Branch/Role':<20} | {'Edu Level':<20} | {'First Theme':<30}")
        print("-" * 80)
        
        for role, edu in scenarios:
            # Create a mock user object (not saved to DB)
            user = User(desired_role=role, education_level=edu, prep_weeks=8)
            res = generate_roadmap(user)
            roadmap = res['modules']
            
            first_theme = roadmap[0]['title'] if roadmap else "NONE"
            print(f"{role:<20} | {edu:<20} | {first_theme:<30}")

if __name__ == "__main__":
    verify_branches()
