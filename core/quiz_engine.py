from models import QuizQuestion
import random

def get_quiz_questions(user, count=5):
    """
    Selects balanced MCQs based on user role.
    """
    role = (user.desired_role or "").lower()
    
    # Detect role type
    tech_keywords = ['engineer', 'developer', 'coding', 'ai', 'data', 'software', 'tech', 'programmer', 'web', 'frontend', 'backend', 'fullstack', 'devops', 'stack', 'cloud', 'security', 'machine learning', 'data science']
    is_tech = any(kw in role for kw in tech_keywords)
    is_ias = any(kw in role for kw in ['ias', 'civil service', 'upsc'])
    
    if is_tech:
        category = "Coding"
    elif is_ias:
        category = "IAS"
    else:
        category = "Professional"
        
    # Fetch questions for the category
    questions = QuizQuestion.query.filter_by(category=category).all()
    
    # If not enough specific questions, add some from Professional/HR
    if len(questions) < count:
        fallback = QuizQuestion.query.filter(QuizQuestion.category.in_(["Professional", "HR"])).all()
        questions.extend([q for q in fallback if q not in questions])
    
    # Select random questions
    if len(questions) >= count:
        return random.sample(questions, count)
    return questions
