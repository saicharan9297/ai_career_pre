from app import app
from extensions import db
from models import Question

def seed_nursing_interviews():
    with app.app_context():
        questions = [
            {"cat": "Medical", "sub": "Nursing", "q": "What are the 'Five Rights' of medication administration?", "ans": "Right patient, Right drug, Right dose, Right route, and Right time."},
            {"cat": "Medical", "sub": "Clinical", "q": "How would you assess a patient's pain level using a standardized scale?", "ans": "By using the Visual Analog Scale (VAS) or Numeric Rating Scale (0-10) and asking the patient to describe the intensity and nature of the pain."},
            {"cat": "Medical", "sub": "Nursing", "q": "Explain the steps of hand hygiene according to WHO guidelines.", "ans": "Wet hands, apply soap, rub palms, back of hands, between fingers, thumbs, fingernails, rinse, and dry. Should take 40-60 seconds."},
            {"cat": "Medical", "sub": "Critical Care", "q": "What are the early signs of hypovolemic shock?", "ans": "Tachycardia (fast heart rate), hypotension (low blood pressure), cold/clammy skin, and decreased urine output."},
            {"cat": "Medical", "sub": "Nursing", "q": "How would you prepare a patient for a major surgery?", "ans": "Verify informed consent, ensure NPO status, perform skin prep, check vitals, and administer any ordered pre-op medications."},
            {"cat": "Medical", "sub": "Emergency", "q": "What is the primary goal of the ABCDE assessment in an emergency?", "ans": "Airway, Breathing, Circulation, Disability, and Exposure - to identify and treat life-threatening conditions immediately."},
            {"cat": "Medical", "sub": "Ethics", "q": "How do you maintain patient confidentiality in a digital hospital system?", "ans": "By using secure login credentials, never sharing passwords, logging off after use, and only accessing records necessary for care."},
            {"cat": "Medical", "sub": "Nursing", "q": "What is the purpose of a 'Nursing Care Plan'?", "ans": "To provide a structured framework for individualized patient care, identifying nursing diagnoses, goals, and interventions."},
            {"cat": "Medical", "sub": "Clinical", "q": "How do you manage a patient with a high fever (Hyperpyrexia)?", "ans": "Monitor vitals, administration of antipyretics as ordered, cold sponging, and ensuring adequate hydration."},
            {"cat": "Medical", "sub": "Nursing", "q": "What is the difference between sterile and clean technique?", "ans": "Sterile technique involves maintaining a field free of all microorganisms; clean technique focuses on reducing the number of microbes."}
        ]
        
        seeded = 0
        for item in questions:
            exists = Question.query.filter_by(question_text=item['q']).first()
            if not exists:
                q = Question(
                    category=item['cat'],
                    sub_category=item['sub'],
                    difficulty="Medium",
                    question_text=item['q'],
                    correct_answer=item['ans'],
                    hint="Consider standard nursing protocols and patient safety."
                )
                db.session.add(q)
                seeded += 1
        
        db.session.commit()
        print(f"Seeded {seeded} nursing-specific interview questions.")

if __name__ == "__main__":
    seed_nursing_interviews()
