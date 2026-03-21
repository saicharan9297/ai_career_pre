from app import create_app
from models import User, Question
from core.roadmap import generate_roadmap
from core.interview_engine import get_interview_session_questions

app = create_app()

def verify_category(role, edu="Graduate"):
    with app.app_context():
        user = User(desired_role=role, education_level=edu)
        roadmap = generate_roadmap(user)
        questions = get_interview_session_questions(user)
        
        print(f"\n--- Verification for Role: {role} (Edu: {edu}) ---")
        if roadmap['modules']:
            print(f"Roadmap: {roadmap['modules'][0]['title']}...")
        else:
            print("Roadmap: FAILED (No modules)")
            
        print(f"Interview Questions: {len(questions)} fetched.")
        for q in questions[:3]:
            print(f"  [{q.category}] {q.question_text[:50]}...")

if __name__ == "__main__":
    verify_category("UPSC Civil Services")
    verify_category("SSC CGL Officer")
    verify_category("APPSC Group 1")
    verify_category("TSPSC Group 2")
    verify_category("Software Engineer", "B.Tech 4th Year")
    verify_category("Research Scientist", "M.Tech")
