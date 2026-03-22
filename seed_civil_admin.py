from app import app
from extensions import db
from models import Question

def seed_civil_admin():
    with app.app_context():
        # High-level administrative and case study questions
        questions = [
            {"cat": "IAS", "sub": "Administration", "q": "As a Joint Collector, how would you handle a sudden outbreak of a communicable disease in a remote tribal area?", "ans": "I would immediately dispatch medical teams, ensure supply of clean water and medicines, coordinate with tribal leaders for awareness, and set up a temporary monitoring station."},
            {"cat": "IAS", "sub": "Governance", "q": "How would you ensure transparency and prevent corruption in the distribution of land titles under a new government scheme?", "ans": "By implementing a digital tracking system, conducting public social audits, involving local community committees, and setting up a clear grievance redressal mechanism."},
            {"cat": "IAS", "sub": "Ethics", "q": "You are pressured by a local politician to favor a specific contractor for a public works project. How do you respond?", "ans": "I would politely but firmly stick to the established legal procedures, document all communications, and ensure that the selection process is based entirely on merit and competitive bidding."},
            {"cat": "IAS", "sub": "Crisis Management", "q": "What is your approach to handling large-scale farmer protests regarding crop insurance delays in your district?", "ans": "I would call for an immediate meeting with farmer representatives, coordinate with insurance companies for quick claims processing, and ensure clear communication about the timeline for disbursement."},
            {"cat": "IAS", "sub": "Leadership", "q": "How do you motivate your subordinates in the revenue department to achieve 100% digitalization of land records within a tight deadline?", "ans": "By setting clear goals, providing necessary training and technical support, recognizing top performers publicly, and addressing any logistical bottlenecks they face."},
            {"cat": "IAS", "sub": "Case Study", "q": "A major bridge in your district has collapsed due to heavy rains. What are your first three actions as an administrator?", "ans": "1. Launch immediate search and rescue. 2. Divert traffic and secure the area. 3. Initiate a technical inquiry and coordinate with humanitarian agencies for relief."}
        ]
        
        seeded = 0
        for item in questions:
            exists = Question.query.filter_by(question_text=item['q']).first()
            if not exists:
                q = Question(
                    category=item['cat'],
                    sub_category=item['sub'],
                    difficulty="Hard",
                    question_text=item['q'],
                    correct_answer=item['ans'],
                    hint="Consider administrative protocols and ethical governance."
                )
                db.session.add(q)
                seeded += 1
        
        db.session.commit()
        print(f"Seeded {seeded} high-level administrative questions.")

if __name__ == "__main__":
    seed_civil_admin()
