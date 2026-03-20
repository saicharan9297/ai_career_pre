from app import create_app
from extensions import db
from models import QuizQuestion

def seed_educational_data():
    app = create_app()
    with app.app_context():
        educational_mcqs = [
            # --- SCHOOL (6-10) ---
            # Week 1: Math & Logic
            {"category": "School", "sub_category": "Mathematics", "week_number": 1, "difficulty": "Easy",
             "question_text": "What is the value of Pi (π) approximately?", "option_a": "2.14", "option_b": "3.14", "option_c": "4.14", "option_d": "1.14", "correct_option": "B"},
            {"category": "School", "sub_category": "Computer Basics", "week_number": 1, "difficulty": "Easy",
             "question_text": "Which part of the computer is known as its 'Brain'?", "option_a": "Monitor", "option_b": "Keyboard", "option_c": "CPU", "option_d": "Mouse", "correct_option": "C"},
            
            # Week 2: Science
            {"category": "School", "sub_category": "Physics", "week_number": 2, "difficulty": "Medium",
             "question_text": "What is the SI unit of Force?", "option_a": "Joule", "option_b": "Watt", "option_c": "Newton", "option_d": "Pascal", "correct_option": "C"},
            {"category": "School", "sub_category": "Biology", "week_number": 2, "difficulty": "Easy",
             "question_text": "Which gas do plants absorb during photosynthesis?", "option_a": "Oxygen", "option_b": "Nitrogen", "option_c": "Carbon Dioxide", "option_d": "Hydrogen", "correct_option": "C"},
            
            # --- INTERMEDIATE (11-12) ---
            # Week 1: Advanced Science
            {"category": "Intermediate", "sub_category": "Advanced Physics", "week_number": 1, "difficulty": "Hard",
             "question_text": "What is the escape velocity from the Earth's surface approximately?", "option_a": "5.2 km/s", "option_b": "9.8 km/s", "option_c": "11.2 km/s", "option_d": "25.2 km/s", "correct_option": "C"},
            {"category": "Intermediate", "sub_category": "Advanced Chemistry", "week_number": 1, "difficulty": "Medium",
             "question_text": "What is the pH of a neutral solution at 25°C?", "option_a": "0", "option_b": "7", "option_c": "14", "option_d": "1", "correct_option": "B"},
            
            # Week 2: Competitive Exams
            {"category": "Intermediate", "sub_category": "Pattern Recognition", "week_number": 2, "difficulty": "Hard",
             "question_text": "In a competitive exam context, what does 'Negative Marking' aim to discourage?", "option_a": "Fast solving", "option_b": "Blind guessing", "option_c": "Using calculators", "option_d": "Reading questions", "correct_option": "B"},
            
            # --- VOCATIONAL (ITI/Diploma) ---
            # Week 1: Trade Theory & Safety
            {"category": "Vocational", "sub_category": "Safety", "week_number": 1, "difficulty": "Medium",
             "question_text": "What does a 'Class A' fire extinguisher primarily deal with?", "option_a": "Electrical fires", "option_b": "Ordinary combustibles (wood, paper)", "option_c": "Flammable liquids", "option_d": "Metal fires", "correct_option": "B"},
            {"category": "Vocational", "sub_category": "Trade Theory", "week_number": 1, "difficulty": "Medium",
             "question_text": "Which tool is used to check the squareness of a surface?", "option_a": "Vernier Caliper", "option_b": "Try Square", "option_c": "Micrometer", "option_d": "Spirit Level", "correct_option": "B"},
            
            # Week 2: Applied Engineering
            {"category": "Vocational", "sub_category": "Electrical", "week_number": 2, "difficulty": "Medium",
             "question_text": "What is the unit of Electric Resistance?", "option_a": "Volt", "option_b": "Ampere", "option_c": "Ohm", "option_d": "Watt", "correct_option": "C"},
            
            # --- HIGHER TECH (B.Tech/M.Tech) ---
            # Week 1: Design & Innovation
            {"category": "Coding", "sub_category": "Design Thinking", "week_number": 1, "difficulty": "Medium",
             "question_text": "What is the first stage of the Design Thinking process?", "option_a": "Ideate", "option_b": "Empathize", "option_c": "Prototype", "option_d": "Test", "correct_option": "B"},
            
            # Week 4: Leadership
            {"category": "Coding", "sub_category": "Leadership", "week_number": 4, "difficulty": "Hard",
             "question_text": "In Agile methodology, who is responsible for prioritizing the product backlog?", "option_a": "Scrum Master", "option_b": "Product Owner", "option_c": "Development Team", "option_d": "Stakeholders", "correct_option": "B"}
        ]

        for q_data in educational_mcqs:
            exists = QuizQuestion.query.filter_by(question_text=q_data['question_text']).first()
            if not exists:
                db.session.add(QuizQuestion(**q_data))
        
        db.session.commit()
        print(f"Added {len(educational_mcqs)} educational quiz questions across all levels.")

if __name__ == "__main__":
    seed_educational_data()
