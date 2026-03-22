from app import app
from extensions import db
from models import Question

def seed_interviews():
    with app.app_context():
        questions = [
            # Data Science
            {"cat": "Data Science", "sub": "Statistics", "q": "What is the Central Limit Theorem and why is it important?", "ans": "The CLT states that the sampling distribution of the mean approaches a normal distribution as sample size increases, regardless of the population distribution. It allows us to use normal probability theory for inference."},
            {"cat": "Data Science", "sub": "ML Concepts", "q": "Explain the Bias-Variance tradeoff.", "ans": "Bias refers to error from overly simplistic assumptions; Variance refers to error from over-sensitivity to noise (overfitting). We aim for a balance to minimize total error."},
            {"cat": "Data Science", "sub": "Python", "q": "What is the difference between a list and a tuple in Python?", "ans": "Lists are mutable (can be changed); tuples are immutable. Tuples are generally faster and can be used as dictionary keys."},
            {"cat": "Data Science", "sub": "SQL", "q": "What is a Window Function in SQL?", "ans": "A window function performs a calculation across a set of table rows that are somehow related to the current row, like RANK() or SUM() OVER()."},
            {"cat": "Data Science", "sub": "Modeling", "q": "How do you handle missing data in a dataset?", "ans": "Options include: removing rows/cols, imputation (mean, median, mode), or using algorithms that handle missing data natively."},
            
            # Cyber Security
            {"cat": "Cyber Security", "sub": "Networking", "q": "What is the difference between IDS and IPS?", "ans": "IDS (Intrusion Detection System) monitors and alerts; IPS (Intrusion Prevention System) monitors and actively blocks suspicious traffic."},
            {"cat": "Cyber Security", "sub": "Cryptography", "q": "Explain Public Key Infrastructure (PKI).", "ans": "PKI is a set of roles, policies, and procedures needed to create, manage, distribute, and revoke digital certificates and manage public-key encryption."},
            {"cat": "Cyber Security", "sub": "Web Security", "q": "What is Cross-Site Scripting (XSS)?", "ans": "XSS is a vulnerability where an attacker injects malicious scripts into content from otherwise trusted websites."},
            {"cat": "Cyber Security", "sub": "General", "q": "What are the three pillars of the CIA Triad?", "ans": "Confidentiality, Integrity, and Availability."},
            {"cat": "Cyber Security", "sub": "Protocols", "q": "How does HTTPS differ from HTTP?", "ans": "HTTPS uses SSL/TLS to encrypt the communication between the client and the server, providing security and data integrity."},
            
            # AIML 
            {"cat": "AIML", "sub": "Deep Learning", "q": "What is an activation function like ReLU used for?", "ans": "It introduces non-linearity into the network, allowing it to learn complex patterns. ReLU is popular because it reduces the vanishing gradient problem."},
            {"cat": "AIML", "sub": "Architecture", "q": "What is a Convolutional Neural Network (CNN)?", "ans": "A CNN is a type of deep neural network most commonly applied to analyzing visual imagery, using convolutional layers to extract spatial features."},
            {"cat": "AIML", "sub": "Optimization", "q": "What is Gradient Descent?", "ans": "It is an iterative optimization algorithm used to find the minimum of a cost function (the weights that minimize error)."},
            
            # ECE
            {"cat": "ECE", "sub": "Digital", "q": "What is the difference between a Latch and a Flip-Flop?", "ans": "A latch is level-triggered (transparent when active); a flip-flop is edge-triggered (changes state only on a clock transition)."},
            {"cat": "ECE", "sub": "Embedded", "q": "Explain the I2C communication protocol.", "ans": "I2C is a synchronous, multi-master, multi-slave, packet-switched, single-ended, serial communication bus using two lines: SDA and SCL."},
            
            # MECH
            {"cat": "MECH", "sub": "Manufacturing", "q": "What is the difference between Stress and Strain?", "ans": "Stress is the internal resisting force per unit area; Strain is the deformation per unit original length caused by stress."},
            {"cat": "MECH", "sub": "Mechanisms", "q": "What is a Four-bar Linkage?", "ans": "It is the simplest movable closed-chain linkage, consistig of four bodies (links) connected by four joints (pivots)."}
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
                    hint="Focus on core principles."
                )
                db.session.add(q)
                seeded += 1
        
        db.session.commit()
        print(f"Seeded {seeded} specialized interview questions.")

if __name__ == "__main__":
    seed_interviews()
