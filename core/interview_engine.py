from models import Question, User
import random

def get_interview_session_questions(user):
    """
    Returns a list of 5 questions: 3 role-specific and 2 HR questions.
    """
    role = (user.desired_role or "").lower()
    tech_keywords = ['engineer', 'developer', 'coding', 'ai', 'data', 'software', 'tech', 'programmer', 'web', 'frontend', 'backend', 'fullstack', 'devops', 'stack', 'cloud', 'security', 'machine learning', 'data science']
    # Robust Category Detection
    civil_keywords = ['ias', 'civil service', 'upsc', 'mro', 'revenue', 'ssc', 'govt', 'government']
    medical_keywords = ['medical', 'doctor', 'nurse', 'pharmacy', 'healthcare']
    science_keywords = ['science', 'research', 'physics', 'chemistry', 'biology', 'scientist']
    
    is_tech = any(kw in role for kw in tech_keywords)
    is_civil = any(kw in role for kw in civil_keywords)
    is_medical = any(kw in role for kw in medical_keywords)
    is_science = any(kw in role for kw in science_keywords)
    
    # 1. Fetch Technical/Role-Specific Pool
    if is_tech:
        role_pool = Question.query.filter(Question.category.in_(["Coding", "Core CS"])).all()
    elif is_civil:
        role_pool = Question.query.filter_by(category="Civil Service").all()
    elif is_medical:
        role_pool = Question.query.filter_by(category="Medical").all()
    elif is_science:
        role_pool = Question.query.filter_by(category="Science").all()
    else:
        role_pool = Question.query.filter(Question.category.notin_(["Coding", "Core CS", "HR"])).all()
    
    # Filter by role keywords if possible for additional refinement
    refined_role_pool = [q for q in role_pool if role in (q.sub_category or "").lower() or role in q.question_text.lower()]
    if len(refined_role_pool) < 3:
        refined_role_pool = role_pool # Fallback to the category pool
    
    if not refined_role_pool:
        # Extreme fallback to any non-HR if still empty
        refined_role_pool = Question.query.filter(Question.category != "HR").all()
    
    # 2. Fetch HR Pool
    hr_pool = Question.query.filter_by(category="HR").all()
    
    # Select questions
    selected_role = random.sample(refined_role_pool, min(3, len(refined_role_pool)))
    selected_hr = random.sample(hr_pool, min(2, len(hr_pool)))
    
    # Combine and shuffle
    total_questions = selected_role + selected_hr
    random.shuffle(total_questions)
    
    return total_questions

def evaluate_answer(question, user_answer):
    """
    Basic evaluation logic. In a real app, this would use LLM.
    """
    if not user_answer:
        return 0, "No answer provided."
    
    # Simple keyword matching
    correct_keywords = question.correct_answer.lower().split()
    user_words = user_answer.lower()
    matches = [word for word in correct_keywords if word in user_words]
    
    score = int((len(matches) / len(correct_keywords)) * 100) if correct_keywords else 50
    # Adjust score based on length and relevance
    if len(user_words.split()) > 10:
        score = min(score + 10, 100)
        
    feedback = f"You mentioned {len(matches)} key points correctly."
    if score >= 70:
        feedback += " Great job! Your explanation was thorough."
    elif score >= 40:
        feedback += " Good start, but try adding more technical details."
    else:
        feedback += " Consider reviewing the fundamental concepts for this topic."
        
    return score, feedback
