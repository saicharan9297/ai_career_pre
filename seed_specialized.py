import sys
import os
sys.path.append(os.path.abspath(os.curdir))

from app import app, db
from models import QuizQuestion, Question

def seed_specialized_data():
    # --- QUIZ QUESTIONS (MCQs) ---
    extra_mcqs = [
        # IAS - Week 1: Polity
        {"category": "IAS", "sub_category": "Polity", "week_number": 1, "difficulty": "Medium",
         "question_text": "Who is considered the Architect of the Indian Constitution?", "option_a": "Mahatma Gandhi", "option_b": "Jawaharlal Nehru", "option_c": "B.R. Ambedkar", "option_d": "Sardar Patel", "correct_option": "C"},
        {"category": "IAS", "sub_category": "Polity", "week_number": 1, "difficulty": "Easy",
         "question_text": "How many Fundamental Rights are currently recognized by the Indian Constitution?", "option_a": "5", "option_b": "6", "option_c": "7", "option_d": "8", "correct_option": "B"},
        
        # IAS - Week 2: History
        {"category": "IAS", "sub_category": "History", "week_number": 2, "difficulty": "Medium",
         "question_text": "In which year did the Quit India Movement start?", "option_a": "1920", "option_b": "1930", "option_c": "1942", "option_d": "1945", "correct_option": "C"},
        {"category": "IAS", "sub_category": "History", "week_number": 2, "difficulty": "Hard",
         "question_text": "Who was the Governor-General of India during the 1857 Revolt?", "option_a": "Lord Dalhousie", "option_b": "Lord Canning", "option_c": "Lord Curzon", "option_d": "Lord Bentinck", "correct_option": "B"},

        # MEDICAL - Week 1: Anatomy (More)
        {"category": "Medical", "sub_category": "Anatomy", "week_number": 1, "difficulty": "Medium",
         "question_text": "Which valve separates the left atrium from the left ventricle?", "option_a": "Tricuspid", "option_b": "Mitral", "option_c": "Aortic", "option_d": "Pulmonary", "correct_option": "B"},
        
        # SCIENCE - Week 1: Physics (More)
        {"category": "Science", "sub_category": "Physics", "week_number": 1, "difficulty": "Hard",
         "question_text": "What is the work-energy theorem?", "option_a": "Work = Force x Distance", "option_b": "Work = Change in Kinetic Energy", "option_c": "Energy is always conserved", "option_d": "Power = Work / Time", "correct_option": "B"}
    ]

    # --- INTERVIEW QUESTIONS (Theoretical) ---
    interview_qs = [
        # IAS / Govt
        {"category": "Civil Service", "sub_category": "Polity", "difficulty": "Medium",
         "question_text": "Explain the significance of the Preamble to the Indian Constitution.", "correct_answer": "Identity card of the constitution keywords: Sovereign Socialist Secular Democratic Republic Justice Liberty Equality Fraternity"},
        {"category": "Civil Service", "sub_category": "Ethics", "difficulty": "Hard",
         "question_text": "How would you handle a situation where your political superior asks you to favor a specific contractor?", "correct_answer": "Ethical dilemma keywords: Neutrality Integrity Rule of Law Professionalism Transparency"},
        
        # Medical
        {"category": "Medical", "sub_category": "Clinical", "difficulty": "Medium",
         "question_text": "What are the common symptoms of a localized infection?", "correct_answer": "Keywords: Redness Swelling Heat Pain Loss of function Fever"},
        
        # Science
        {"category": "Science", "sub_category": "Research", "difficulty": "Hard",
         "question_text": "Describe the difference between a null hypothesis and an alternative hypothesis.", "correct_answer": "Keywords: Statistical significance No effect Relationship P-value Rejection"}
    ]

    with app.app_context():
        # Seed MCQs
        for q_data in extra_mcqs:
            exists = QuizQuestion.query.filter_by(question_text=q_data['question_text']).first()
            if not exists:
                db.session.add(QuizQuestion(**q_data))
        
        # Seed Interview Questions (Question table)
        for i_data in interview_qs:
            exists = Question.query.filter_by(question_text=i_data['question_text']).first()
            if not exists:
                db.session.add(Question(**i_data))
                
        db.session.commit()
        print(f"Seeded {len(extra_mcqs)} MCQs and {len(interview_qs)} Interview Questions.")

if __name__ == "__main__":
    seed_specialized_data()
