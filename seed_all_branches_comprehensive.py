from app import app, create_app
from extensions import db
from models import QuizQuestion, Question

def seed_all_branches():
    """
    Comprehensive seeding for 7 major B.Tech branches across multiple weeks.
    Branches: CSE, ECE, EEE, MECH, CHEMICAL, AIML, Data Science.
    """
    app = create_app()
    with app.app_context():
        # --- QUIZ QUESTIONS (Weeks 1-4) ---
        branch_quiz = [
            # DATA SCIENCE
            {"cat": "Data Science", "sub": "Statistics", "week": 1, "q": "Which measure of central tendency is most affected by outliers?", "a": "Mean", "b": "Median", "c": "Mode", "d": "Range", "ans": "A"},
            {"cat": "Data Science", "sub": "Probability", "week": 1, "q": "What is the probability of a certain event occurring?", "a": "0", "b": "0.5", "c": "1", "d": "Infinity", "ans": "C"},
            {"cat": "Data Science", "sub": "Python for DS", "week": 2, "q": "Which library is used primarily for data manipulation in Python?", "a": "Matplotlib", "b": "TensorFlow", "c": "Pandas", "d": "NLTK", "ans": "C"},
            {"cat": "Data Science", "sub": "SQL", "week": 2, "q": "Which SQL clause is used to filter records in a grouped set?", "a": "WHERE", "b": "HAVING", "c": "ORDER BY", "d": "GROUP BY", "ans": "B"},
            {"cat": "Data Science", "sub": "Machine Learning", "week": 3, "q": "Is Linear Regression a supervised or unsupervised learning algorithm?", "a": "Supervised", "b": "Unsupervised", "c": "Semi-supervised", "d": "Reinforcement", "ans": "A"},
            {"cat": "Data Science", "sub": "Visualization", "week": 3, "q": "Which chart type is best for showing trends over time?", "a": "Pie Chart", "b": "Line Chart", "c": "Scatter Plot", "d": "Histogram", "ans": "B"},
            {"cat": "Data Science", "sub": "Big Data", "week": 4, "q": "What does HDFS stand for in the context of Hadoop?", "a": "Hadoop Distributed File System", "b": "High Density Data Format System", "c": "Heavy Data Forwarding Service", "d": "None", "ans": "A"},

            # CHEMICAL
            {"cat": "CHEMICAL", "sub": "Reaction Engineering", "week": 2, "q": "For which order reaction is the half-life independent of initial concentration?", "a": "Zero order", "b": "First order", "c": "Second order", "d": "Third order", "ans": "B"},
            {"cat": "CHEMICAL", "sub": "Mass Transfer", "week": 3, "q": "The separation of a liquid mixture into its components by selective evaporation is called:", "a": "Absorption", "b": "Adsorption", "c": "Distillation", "d": "Leaching", "ans": "C"},
            
            # AIML
            {"cat": "AIML", "sub": "Deep Learning", "week": 2, "q": "Which function is commonly used as an activation function in the hidden layers of a CNN?", "a": "Sigmoid", "b": "Tanh", "c": "ReLU", "d": "Linear", "ans": "C"},
            {"cat": "AIML", "sub": "NLP", "week": 3, "q": "What does TF-IDF stand for in text processing?", "a": "Term Frequency - Inverse Document Frequency", "b": "Technical Focus - Internal Data Format", "c": "Total Frequency - Indexed Document File", "d": "None", "ans": "A"},

            # CSE (Refreshing/Deepening)
            {"cat": "CSE", "sub": "OS", "week": 2, "q": "Which scheduling algorithm is non-preemptive?", "a": "Round Robin", "b": "First-Come First-Served (FCFS)", "c": "Shortest Job First (Preemptive)", "d": "Priority (Preemptive)", "ans": "B"},
            {"cat": "CSE", "sub": "Networking", "week": 3, "q": "On which OSI layer does the IP protocol operate?", "a": "Data Link", "b": "Network", "c": "Transport", "d": "Application", "ans": "B"},
            {"cat": "CSE", "sub": "Database", "week": 4, "q": "What is the 3rd Normal Form (3NF) primarily designed to prevent?", "a": "Partial dependency", "b": "Transitive dependency", "c": "Multivalued dependency", "d": "Joins", "ans": "B"},

            # ECE (Refreshing/Deepening)
            {"cat": "ECE", "sub": "Microprocessors", "week": 2, "q": "What is the size of the data bus in the 8086 microprocessor?", "a": "8-bit", "b": "16-bit", "c": "20-bit", "d": "32-bit", "ans": "B"},
            {"cat": "ECE", "sub": "VLSI", "week": 3, "q": "In CMOS technology, what type of transistors are used?", "a": "BJTs only", "b": "PMOS and NMOS", "c": "NMOS only", "d": "JFETs", "ans": "B"},
            
            # MECH (Refreshing/Deepening)
            {"cat": "MECH", "sub": "Heat Transfer", "week": 2, "q": "The transfer of heat in solids is primarily by:", "a": "Conduction", "b": "Convection", "c": "Radiation", "d": "Refraction", "ans": "A"},
            {"cat": "MECH", "sub": "Production", "week": 3, "q": "Which process is used for making plastic bottles?", "a": "Forging", "b": "Blow Molding", "c": "Casting", "d": "Extrusion", "ans": "B"},
            
            # EEE (Refreshing/Deepening)
            {"cat": "EEE", "sub": "Power Electronics", "week": 2, "q": "A Triac is equivalent to two _______ connected in anti-parallel.", "a": "Diodes", "b": "BJTs", "c": "SCRs", "d": "MOSFETs", "ans": "C"},
            {"cat": "EEE", "sub": "Control Systems", "week": 3, "q": "The transfer function of a system is the ratio of Y(s) to X(s) under _______ initial conditions.", "a": "Unit", "b": "Variable", "c": "Zero", "d": "Infinity", "ans": "C"}
        ]

        # --- INTERVIEW QUESTIONS ---
        branch_interview = [
            {"cat": "Data Science", "sub": "ML", "diff": "Medium", "q": "Explain the Bias-Variance tradeoff.", "ans": "High bias can cause underfitting; high variance can cause overfitting. The goal is to find a balance where both errors are minimized."},
            {"cat": "Data Science", "sub": "Stats", "diff": "Hard", "q": "What is a p-value?", "ans": "The p-value is the probability of obtaining test results at least as extreme as the observed results, assuming the null hypothesis is correct."},
            {"cat": "CHEMICAL", "sub": "Safety", "diff": "Medium", "q": "What are the common safety protocols in a chemical plant?", "ans": "PPE usage, Pressure relief valves, HAZOP studies, Emergency shutdown systems, and proper ventilation."},
            {"cat": "AEROSPACE", "sub": "Navigation", "diff": "Medium", "q": "How does GPS work for aircraft navigation?", "ans": "Trilateration using signals from at least 4 satellites to determine latitude, longitude, altitude, and time."},
            {"cat": "CSE", "sub": "System Design", "diff": "Hard", "q": "How would you design a scalable notification system?", "ans": "Use a load balancer, message queues (Kafka/RabbitMQ), worker nodes for push/email/SMS, and a database for preference tracking."},
        ]

        # Add Quiz Questions
        seeded_quiz_count = 0
        for item in branch_quiz:
            q = QuizQuestion(
                category=item['cat'],
                sub_category=item['sub'],
                week_number=item['week'],
                difficulty="Medium",
                question_text=item['q'],
                option_a=item['a'], option_b=item['b'], option_c=item['c'], option_d=item['d'],
                correct_option=item['ans']
            )
            exists = QuizQuestion.query.filter_by(question_text=item['q']).first()
            if not exists:
                db.session.add(q)
                seeded_quiz_count += 1

        # Add Interview Questions
        seeded_interview_count = 0
        for item in branch_interview:
            qi = Question(
                category=item['cat'],
                sub_category=item['sub'],
                difficulty=item['diff'],
                question_text=item['q'],
                correct_answer=item['ans'],
                hint="Core technical concept of your field."
            )
            exists = Question.query.filter_by(question_text=item['q']).first()
            if not exists:
                db.session.add(qi)
                seeded_interview_count += 1

        db.session.commit()
        print(f"Seeded {seeded_quiz_count} comprehensive quiz questions.")
        print(f"Seeded {seeded_interview_count} comprehensive interview questions.")

if __name__ == "__main__":
    seed_all_branches()
