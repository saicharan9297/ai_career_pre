import sys
import os
sys.path.append(os.path.abspath(os.curdir))

from app import app
from models import User
from core.quiz_engine import get_quiz_questions
from core.interview_engine import get_interview_session_questions

def verify_sync():
    with app.app_context():
        # Test 1: IAS User
        ias_user = User(desired_role="IAS", education_level="Graduate")
        quiz_qs = get_quiz_questions(ias_user, week_number=1, count=5)
        interview_qs = get_interview_session_questions(ias_user)
        
        print(f"--- IAS ROLE TEST ---")
        print(f"Quiz Questions (Week 1): {[q.sub_category for q in quiz_qs]}")
        print(f"Interview Questions: {[q.sub_category for q in interview_qs]}")
        
        # Test 2: Medical User
        med_user = User(desired_role="Medical Doctor", education_level="MBBS")
        quiz_qs_med = get_quiz_questions(med_user, week_number=1, count=5)
        interview_qs_med = get_interview_session_questions(med_user)
        
        print(f"\n--- MEDICAL ROLE TEST ---")
        print(f"Quiz Questions (Week 1): {[q.sub_category for q in quiz_qs_med]}")
        print(f"Interview Questions: {[q.sub_category for q in interview_qs_med]}")

if __name__ == "__main__":
    verify_sync()
