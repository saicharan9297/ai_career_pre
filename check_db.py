from app import app
from models import QuizQuestion

with app.app_context():
    categories = ["Medical", "MBBS", "Nursing", "Pharmacy", "Dental"]
    for cat in categories:
        qs = QuizQuestion.query.filter_by(category=cat).all()
        print(f"--- Category: {cat} (Total: {len(qs)}) ---")
        for q in qs:
            print(f"  - Week {q.week_number}: {q.sub_category} | {q.question_text[:60]}...")
