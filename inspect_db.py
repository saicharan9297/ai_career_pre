from app import create_app
from models import User, QuizQuestion
from core.roadmap import generate_roadmap
from core.quiz_engine import get_quiz_questions

def inspect_users():
    app = create_app()
    with app.app_context():
        users = User.query.all()
        print(f"Total Users: {len(users)}")
        for u in users:
            print(f"User: {u.email}, Role: '{u.desired_role}', Edu: '{u.education_level}'")
            roadmap_data = generate_roadmap(u)
            modules = roadmap_data.get('modules', [])
            if modules:
                print(f"  First Week Theme: {modules[0]['title']}")
                if modules[0]['subjects']:
                    print(f"  First Subject: {modules[0]['subjects'][0]['name']}")
            
            # Test quiz for this user
            questions = get_quiz_questions(u, week_number=1, count=1)
            if questions:
                print(f"  Quiz Category: {questions[0].category}, Sub: {questions[0].sub_category}")
            else:
                print("  No Quiz Questions Found!")
            print("-" * 30)

if __name__ == "__main__":
    inspect_users()
