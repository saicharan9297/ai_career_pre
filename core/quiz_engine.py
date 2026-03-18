from models import QuizQuestion
import random

def get_quiz_questions(user, week_number=1, count=5):
    """
    Selects balanced MCQs based on user role and week number.
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
        
    # Fetch questions for the specific week
    week_questions = QuizQuestion.query.filter_by(category=category, week_number=week_number).all()
    
    # Always fetch some additional questions from the same category to ensure variety
    # even if the specific week has limited content.
    other_questions = QuizQuestion.query.filter_by(category=category).filter(QuizQuestion.week_number != week_number).all()
    
    # Final pool prioritization:
    # 1. Start with week-specific questions
    # 2. Add other questions from the same category
    # 3. Fallback to Professional/HR if still extremely low
    
    pool = list(week_questions)
    
    # If we have very few questions for this week, add more from the same category
    if len(pool) < count + 2:
        pool.extend([q for q in other_questions if q not in pool])
        
    # Final fallback for variety if pool is still small
    if len(pool) < count:
        fallback = QuizQuestion.query.filter(QuizQuestion.category.in_(["Professional", "HR"])).all()
        pool.extend([q for q in fallback if q not in pool])
    
    # Select random questions from the pool
    if len(pool) >= count:
        return random.sample(pool, count)
    
    # Shuffle if we return fewer than count
    random.shuffle(pool)
    return pool
