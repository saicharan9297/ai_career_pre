from app import app
from extensions import db
from models import QuizQuestion, Question

def seed_medical_data():
    with app.app_context():
        # Clear existing medical questions if any (Optional but good for clean seed)
        # QuizQuestion.query.filter_by(category="Medical").delete()
        # Question.query.filter_by(category="Medical").delete()

        medical_quiz_data = [
            # WEEK 1: Pre-clinical / Foundations
            {"cat": "Medical", "sub": "Anatomy", "week": 1, "q": "Which is the largest organ in the human body?", "a": "Heart", "b": "Brain", "c": "Skin", "d": "Liver", "ans": "C"},
            {"cat": "Medical", "sub": "Physiology", "week": 1, "q": "What is the primary function of red blood cells?", "a": "Clotting", "b": "Oxygen transport", "c": "Immune response", "d": "Waste removal", "ans": "B"},
            {"cat": "Medical", "sub": "Biochemistry", "week": 1, "q": "Which molecule is the main source of energy for cells?", "a": "ATP", "b": "DNA", "c": "RNA", "d": "Protein", "ans": "A"},
            {"cat": "Medical", "sub": "Anatomy", "week": 1, "q": "How many bones are in the adult human body?", "a": "200", "b": "206", "c": "210", "d": "196", "ans": "B"},
            {"cat": "Medical", "sub": "Nursing Foundations", "week": 1, "q": "What is the first step in the nursing process?", "a": "Diagnosis", "b": "Planning", "c": "Assessment", "d": "Implementation", "ans": "C"},
            {"cat": "Medical", "sub": "Dental Materials", "week": 1, "q": "Which material is commonly used for dental fillings?", "a": "Titanium", "b": "Amalgam", "c": "Steel", "d": "Copper", "ans": "B"},
            {"cat": "Medical", "sub": "Pharmaceutical Chemistry", "week": 1, "q": "What is the pH of a neutral solution?", "a": "5", "b": "7", "c": "9", "d": "14", "ans": "B"},

            # WEEK 2: Para-clinical / Specializations
            {"cat": "Medical", "sub": "Pharmacology", "week": 2, "q": "What type of drug is Penicillin?", "a": "Antiviral", "b": "Antibiotic", "c": "Antifungal", "d": "Analgesic", "ans": "B"},
            {"cat": "Medical", "sub": "Pathology", "week": 2, "q": "Inflammation of the liver is known as:", "a": "Nephritis", "b": "Gastritis", "c": "Hepatitis", "d": "Arthritis", "ans": "C"},
            {"cat": "Medical", "sub": "Microbiology", "week": 2, "q": "Which organism causes tuberculosis?", "a": "Virus", "b": "Fungus", "c": "Bacterium", "d": "Protozoa", "ans": "C"},
            {"cat": "Medical", "sub": "Medical-Surgical Nursing", "week": 2, "q": "A core symptom of Diabetes Mellitus is:", "a": "Hypertension", "b": "Polyuria", "c": "Hypotension", "d": "Bradycardia", "ans": "B"},
            {"cat": "Medical", "sub": "Pharmaceutics", "week": 2, "q": "Which dosage form is intended for sublingual administration?", "a": "Capsule", "b": "Tablet", "c": "Syrup", "d": "Ointment", "ans": "B"},
            
            # WEEK 3: Clinical Practice
            {"cat": "Medical", "sub": "General Medicine", "week": 3, "q": "What is the normal resting heart rate for an adult?", "a": "40-60 bpm", "b": "60-100 bpm", "c": "100-120 bpm", "d": "120-140 bpm", "ans": "B"},
            {"cat": "Medical", "sub": "Pediatrics", "week": 3, "q": "A neonate is a child aged:", "a": "0-28 days", "b": "1-12 months", "c": "1-3 years", "d": "3-5 years", "ans": "A"},
            {"cat": "Medical", "sub": "Oral Surgery", "week": 3, "q": "Extraction of a tooth is known as:", "a": "Scaling", "b": "Obturation", "c": "Exodontia", "d": "Implantation", "ans": "C"},
            {"cat": "Medical", "sub": "General Surgery", "week": 3, "q": "The removal of the appendix is called:", "a": "Colectomy", "b": "Appendectomy", "c": "Gastrectomy", "d": "Mastectomy", "ans": "B"},
            
            # WEEK 4: Ethics & Community
            {"cat": "Medical", "sub": "Community Medicine", "week": 4, "q": "What is the primary goal of public health?", "a": "Profit", "b": "Disease Prevention", "c": "Surgery", "d": "Hospital building", "ans": "B"},
            {"cat": "Medical", "sub": "Medical Ethics", "week": 4, "q": "The principle of 'doing no harm' is known as:", "a": "Autonomy", "b": "Beneficence", "c": "Non-maleficence", "d": "Justice", "ans": "C"},
            {"cat": "Medical", "sub": "Hospital Pharmacy", "week": 4, "q": "Who is responsible for managing drug inventory in a hospital?", "a": "Nurse", "b": "Doctor", "c": "Pharmacist", "d": "Accountant", "ans": "C"}
        ]

        # Interview Questions
        medical_interview_data = [
            {"cat": "Medical", "sub": "MBBS", "diff": "Medium", "q": "How would you handle a patient who refuses potentially life-saving treatment due to religious beliefs?", "ans": "Discuss autonomy and ethical deliberation."},
            {"cat": "Medical", "sub": "Nursing", "diff": "Medium", "q": "Describe your process for prioritizing patient care during a high-volume emergency shift.", "ans": "Triage and critical care prioritization."},
            {"cat": "Medical", "sub": "Pharmacy", "diff": "Medium", "q": "What steps do you take to prevent medication errors in a busy hospital setting?", "ans": "Double-check protocols and communication."},
            {"cat": "Medical", "sub": "Dental", "diff": "Medium", "q": "Explain the importance of patient history in diagnosing complex oral conditions.", "ans": "Systemic health links to oral health."},
            {"cat": "Medical", "sub": "General", "diff": "Easy", "q": "Why did you choose a career in healthcare?", "ans": "Passion for service and science."}
        ]

        for item in medical_quiz_data:
            q = QuizQuestion(
                category=item['cat'],
                sub_category=item['sub'],
                week_number=item['week'],
                difficulty="Medium",
                question_text=item['q'],
                option_a=item['a'],
                option_b=item['b'],
                option_c=item['c'],
                option_d=item['d'],
                correct_option=item['ans']
            )
            db.session.add(q)
        
        for item in medical_interview_data:
            q = Question(
                category=item['cat'],
                sub_category=item['sub'],
                difficulty=item['diff'],
                question_text=item['q'],
                correct_answer=item['ans'],
                hint="Think about professional standards."
            )
            db.session.add(q)

        db.session.commit()
        print("Medical data seeded successfully!")

if __name__ == "__main__":
    seed_medical_data()
