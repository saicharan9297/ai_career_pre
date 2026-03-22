from core.roadmap import generate_roadmap
from models import User

class MockUser:
    def __init__(self, role, edu, time=2, weeks=4):
        self.desired_role = role
        self.education_level = edu
        self.available_time = time
        self.prep_weeks = weeks
        self.completed_modules = ""
        self.readiness_score = 0
        self.id = 999

def test_scenarios():
    scenarios = [
        ("ECE", "B.Tech 1st Year"),
        ("Electronics Engineer", "B.Tech"),
        ("Embedded Systems", "M.Tech"),
        ("VLSI Engineer", "Job Seeker"),
        ("Power Systems", "M.Tech"),
        ("Thermal Engineer", "M.Tech"),
        ("Structural Engineer", "M.Tech"),
        ("Embedded Systems", "Job Seeker"),
        ("Software Engineer", "M.Tech")
    ]
    
    for role, edu in scenarios:
        u = MockUser(role, edu)
        print(f"TESTING: Role='{role}', Edu='{edu}'")
        roadmap = generate_roadmap(u)
        modules = roadmap.get('modules', [])
        if modules:
             print(f"  First Subject: {modules[0]['subjects'][0]['name']}")
             # Check for DBMS or OS in the subjects
             all_names = [s['name'].lower() for m in modules for s in m['subjects']]
             if any(x in all_names for x in ['dbms', 'operating systems', 'os', 'database']):
                 print("  !! FOUND CSE SUBJECTS IN ECE ROADMAP !!")
        else:
             print("  Roadmap empty!")
        print("-" * 20)

if __name__ == "__main__":
    test_scenarios()
