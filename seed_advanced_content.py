from app import app
from extensions import db
from models import QuizQuestion, Question

def seed_advanced_content():
    with app.app_context():
        # --- UPSC ---
        upsc_quiz = [
            {"cat": "UPSC", "sub": "Polity", "week": 1, "q": "Who is the custodian of the Indian Constitution?", "a": "President", "b": "Supreme Court", "c": "Parliament", "d": "Prime Minister", "ans": "B"},
            {"cat": "UPSC", "sub": "History", "week": 1, "q": "The Rowlatt Act was passed in which year?", "a": "1917", "b": "1918", "c": "1919", "d": "1920", "ans": "C"},
            {"cat": "UPSC", "sub": "Geography", "week": 2, "q": "Which Indian state has the longest coastline?", "a": "Maharashtra", "b": "Tamil Nadu", "c": "Gujarat", "d": "Andhra Pradesh", "ans": "C"},
            {"cat": "UPSC", "sub": "Economics", "week": 2, "q": "Who is the father of Indian Economics?", "a": "Dadabhai Naoroji", "b": "Mahatma Gandhi", "c": "Jawaharlal Nehru", "d": "Amartya Sen", "ans": "A"},
        ]
        
        upsc_interview = [
            {"cat": "UPSC", "sub": "Ethics", "diff": "Hard", "q": "How would you handle a situation where a superior gives you an illegal order?", "ans": "Discuss constitutional morality, civil service conduct rules, and ethical courage."},
            {"cat": "UPSC", "sub": "International Relations", "diff": "Medium", "q": "Discuss the significance of 'Non-Alignment' in India's current foreign policy.", "ans": "Strategic autonomy, multi-alignment, and national interest."},
        ]

        # --- SSC ---
        ssc_quiz = [
            {"cat": "SSC", "sub": "Quant", "week": 1, "q": "Find the average of first 50 natural numbers.", "a": "25", "b": "25.5", "c": "26", "d": "24.5", "ans": "B"},
            {"cat": "SSC", "sub": "English", "week": 1, "q": "Synonym of 'Abundant'?", "a": "Scarce", "b": "Plentiful", "c": "Rare", "d": "Small", "ans": "B"},
        ]

        # --- APPSC / TSPSC ---
        state_quiz = [
            {"cat": "APPSC", "sub": "State History", "week": 1, "q": "Who was the first Chief Minister of Andhra Pradesh?", "a": "T. Prakasam", "b": "N. Sanjiva Reddy", "c": "P.V. Narasimha Rao", "d": "None", "ans": "A"},
            {"cat": "TSPSC", "sub": "State Formation", "week": 1, "q": "In which year was the Telangana state formed?", "a": "2012", "b": "2013", "c": "2014", "d": "2015", "ans": "C"},
        ]

        # --- Advanced Tech (B.Tech/M.Tech) ---
        tech_quiz = [
            {"cat": "Coding", "sub": "Cloud", "week": 5, "q": "What is 'SaaS' in Cloud Computing?", "a": "Server as a Service", "b": "Software as a Service", "c": "Storage as a Service", "d": "System as a Service", "ans": "B"},
            {"cat": "Coding", "sub": "DevOps", "week": 5, "q": "What does CI/CD stand for?", "a": "Continuous Integration / Continuous Delivery", "b": "Core Integration / Core Delivery", "c": "Code Integration / Code Deployment", "d": "None", "ans": "A"},
            {"cat": "Coding", "sub": "AI/ML", "week": 6, "q": "What is the primary goal of Unsupervised Learning?", "a": "Predicting labels", "b": "Finding hidden patterns/clusters", "c": "Optimizing weights", "d": "None", "ans": "B"},
        ]

        tech_interview = [
            {"cat": "Coding", "sub": "System Design", "diff": "Hard", "q": "How would you design a URL shortening service like Bitly?", "ans": "Discuss hashing, database choice, scalability, and redirection logic."},
            {"cat": "Coding", "sub": "AI", "diff": "Medium", "q": "What is the difference between Overfitting and Underfitting in ML?", "ans": "Bias vs Variance tradeoff, model complexity, and training error vs test error."},
        ]

        # Add all to DB
        for item in upsc_quiz + ssc_quiz + state_quiz + tech_quiz:
            q = QuizQuestion(
                category=item['cat'],
                sub_category=item['sub'],
                week_number=item['week'],
                difficulty="Medium",
                question_text=item['q'],
                option_a=item['a'], option_b=item['b'], option_c=item['c'], option_d=item['d'],
                correct_option=item['ans']
            )
            db.session.add(q)

        for item in upsc_interview + tech_interview:
            qi = Question(
                category=item['cat'],
                sub_category=item['sub'],
                difficulty=item['diff'],
                question_text=item['q'],
                correct_answer=item['ans'],
                hint="Think about the core concepts and industry standards."
            )
            db.session.add(qi)

        db.session.commit()
        print("Advanced content seeded successfully!")

if __name__ == "__main__":
    seed_advanced_content()
