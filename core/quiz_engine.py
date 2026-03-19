from models import QuizQuestion
import random

def get_quiz_questions(user, week_number=1, count=5):
    """
    Selects balanced MCQs based on user role and week number.
    """
    role_raw = (user.desired_role or "").lower()
    
    # Robust Role Detection (Synchronized with roadmap.py)
    tech_keywords = ['engineer', 'developer', 'coding', 'ai', 'data', 'software', 'tech', 'programmer', 'web', 'frontend', 'backend', 'fullstack', 'devops', 'stack', 'cloud', 'security', 'machine learning', 'data science']
    civil_service_keywords = ['ias', 'civil service', 'upsc', 'mro', 'revenue officer', 'tpsc', 'appsc', 'group 1', 'group 2', 'constable', 'sub-inspector', 'panchayat', 'administrative', 'ips', 'ifs', 'collector']
    finance_govt_keywords = ['income tax', 'tax', 'ssc', 'cgl', 'banking', 'bank', 'po', 'clerk', 'finance', 'audit', 'lic', 'rbi', 'ibps', 'accountant', 'budget', 'revenue']
    medical_keywords = ['medical', 'doctor', 'nurse', 'pharmacy', 'healthcare', 'dentist', 'physician', 'surgeon', 'clinic']
    science_keywords = ['science', 'research', 'physics', 'chemistry', 'biology', 'scientist', 'laboratory', 'biotech']

    is_tech = any(kw in role_raw for kw in tech_keywords)
    is_civil = any(kw in role_raw for kw in civil_service_keywords)
    is_finance_govt = any(kw in role_raw for kw in finance_govt_keywords)
    is_medical = any(kw in role_raw for kw in medical_keywords)
    is_science = any(kw in role_raw for kw in science_keywords)

    if is_tech:
        category = "Coding"
    elif is_medical:
        category = "Medical"
    elif is_science:
        category = "Science"
    elif is_civil or is_finance_govt:
        category = "IAS" # Shared GS/Aptitude pool but different weekly priorities
    else:
        category = "Professional"
        
    # Map roadmap week to DB week (assuming 4 weeks of content)
    try:
        mapped_week = (int(week_number) - 1) % 4 + 1
    except (ValueError, TypeError):
        mapped_week = 1
    
    # Sub-category filtering based on ROLE and WEEK (Alignment with roadmap.py themes)
    preferred_subcats = []
    
    if is_tech:
        if mapped_week == 1: preferred_subcats = ['OS', 'Databases', 'Data Structures']
        elif mapped_week == 2: preferred_subcats = ['Data Structures', 'Javascript', 'Networking', 'Git']
        elif mapped_week == 3: preferred_subcats = ['React', 'Web', 'Testing']
        elif mapped_week == 4: preferred_subcats = ['System Design', 'Docker', 'Scalability', 'Cloud', 'Architecture']
    
    elif is_civil:
        if mapped_week == 1: preferred_subcats = ['Polity', 'Governance']
        elif mapped_week == 2: preferred_subcats = ['History', 'Geography']
        elif mapped_week == 3: preferred_subcats = ['Economy', 'Social Justice']
        elif mapped_week == 4: preferred_subcats = ['Ethics', 'Current Affairs', 'Environment', 'Science']
        
    elif is_finance_govt:
        if mapped_week == 1: preferred_subcats = ['Quants', 'Reasoning', 'Numerical Ability']
        elif mapped_week == 2: preferred_subcats = ['Polity', 'History', 'Geography', 'Economy']
        elif mapped_week == 3: preferred_subcats = ['Taxation', 'Banking', 'Financial Awareness']
        elif mapped_week == 4: preferred_subcats = ['Current Affairs', 'Revision', 'Mixed']
        
    elif is_medical:
        preferred_subcats = ['Anatomy', 'Physiology', 'Pharmacology', 'Clinical', 'Medical Ethics']
    elif is_science:
        preferred_subcats = ['Physics', 'Chemistry', 'Biology', 'Research', 'Genetics']

    # Base query for the correct category and week
    from sqlalchemy import func
    query = QuizQuestion.query.filter_by(category=category, week_number=mapped_week)
    
    questions = []
    if preferred_subcats:
        # Try to get questions from preferred sub-categories first
        questions = query.filter(QuizQuestion.sub_category.in_(preferred_subcats)).order_by(func.random()).limit(count).all()
        
    # If not enough specific questions, fill the rest from the same category/week
    if len(questions) < count:
        remaining = count - len(questions)
        excluded_ids = [q.id for q in questions]
        more_questions = query.filter(~QuizQuestion.id.in_(excluded_ids)).order_by(func.random()).limit(remaining).all()
        questions.extend(more_questions)
        
    # Final fallback: if still not enough, take any from the category regardless of week
    if len(questions) < count:
        remaining = count - len(questions)
        excluded_ids = [q.id for q in questions]
        fallback = QuizQuestion.query.filter_by(category=category).filter(~QuizQuestion.id.in_(excluded_ids)).order_by(func.random()).limit(remaining).all()
        questions.extend(fallback)
        
    return questions
