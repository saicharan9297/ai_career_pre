import sys
import os
sys.path.append(os.path.abspath(os.curdir))

from app import app, db
from models import QuizQuestion

def seed_extra_fields():
    extra_mcqs = [
        # --- MEDICAL CATEGORY ---
        {"category": "Medical", "sub_category": "Anatomy", "week_number": 1, "difficulty": "Easy",
         "question_text": "What is the largest organ in the human body?", "option_a": "Liver", "option_b": "Heart", "option_c": "Skin", "option_d": "Brain", "correct_option": "C"},
        {"category": "Medical", "sub_category": "Anatomy", "week_number": 1, "difficulty": "Medium",
         "question_text": "How many bones are in the adult human body?", "option_a": "206", "option_b": "300", "option_c": "150", "option_d": "210", "correct_option": "A"},
        {"category": "Medical", "sub_category": "Pharmacology", "week_number": 2, "difficulty": "Medium",
         "question_text": "Which class of drugs is primarily used to treat bacterial infections?", "option_a": "Antivirals", "option_b": "Antibiotics", "option_c": "Analgesics", "option_d": "Antipyretics", "correct_option": "B"},
        {"category": "Medical", "sub_category": "Clinical", "week_number": 3, "difficulty": "Hard",
         "question_text": "What does 'Triage' mean in a medical emergency context?", "option_a": "A type of surgery", "option_b": "Determining priority based on severity", "option_c": "Ambulance siren", "option_d": "Insurance claim", "correct_option": "B"},
        {"category": "Medical", "sub_category": "Medical Ethics", "week_number": 4, "difficulty": "Medium",
         "question_text": "What does HIPAA primarily protect?", "option_a": "Hospital funding", "option_b": "Patient health information privacy", "option_c": "Doctor's salary", "option_d": "Patents", "correct_option": "B"},

        # --- SCIENCE CATEGORY ---
        {"category": "Science", "sub_category": "Physics", "week_number": 1, "difficulty": "Easy",
         "question_text": "What is the SI unit of Force?", "option_a": "Joule", "option_b": "Watt", "option_c": "Newton", "option_d": "Pascal", "correct_option": "C"},
        {"category": "Science", "sub_category": "Chemistry", "week_number": 2, "difficulty": "Medium",
         "question_text": "What is the atomic number of Carbon?", "option_a": "12", "option_b": "6", "option_c": "14", "option_d": "8", "correct_option": "B"},
        {"category": "Science", "sub_category": "Biology", "week_number": 3, "difficulty": "Medium",
         "question_text": "What is known as the 'Powerhouse of the Cell'?", "option_a": "Nucleus", "option_b": "Ribosome", "option_c": "Mitochondria", "option_d": "Golgi", "correct_option": "C"},
        {"category": "Science", "sub_category": "Research", "week_number": 4, "difficulty": "Medium",
         "question_text": "What is a 'controlled variable' in an experiment?", "option_a": "Factortested", "option_b": "Factor kept constant", "option_c": "Result", "option_d": "Hypothesis", "correct_option": "B"}
    ]

    with app.app_context():
        # Add to existing (don't delete)
        for q_data in extra_mcqs:
            # Simple check to avoid duplicates if run twice
            exists = QuizQuestion.query.filter_by(
                question_text=q_data['question_text']
            ).first()
            if not exists:
                new_q = QuizQuestion(**q_data)
                db.session.add(new_q)
        db.session.commit()
        print(f"Added {len(extra_mcqs)} extra multi-field quiz questions.")

if __name__ == "__main__":
    seed_extra_fields()
