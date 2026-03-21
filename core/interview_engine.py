from models import Question, User
import random

def get_interview_session_questions(user):
    """
    Returns a list of 5 questions: 3 role-specific and 2 HR questions.
    """
    role_raw = (user.desired_role or "").lower()
    
    # Robust Role Detection (Synchronized with roadmap.py)
    tech_keywords = ['engineer', 'developer', 'coding', 'ai', 'data', 'software', 'tech', 'programmer', 'web', 'frontend', 'backend', 'fullstack', 'devops', 'stack', 'cloud', 'security', 'machine learning', 'data science']
    civil_keywords = ['ias', 'civil service', 'upsc', 'mro', 'revenue officer', 'tpsc', 'appsc', 'group 1', 'group 2', 'constable', 'sub-inspector', 'panchayat', 'administrative', 'ips', 'ifs', 'collector', 'telangana', 'andhra']
    finance_keywords = ['income tax', 'tax', 'ssc', 'cgl', 'banking', 'bank', 'po', 'clerk', 'finance', 'audit', 'lic', 'rbi', 'ibps', 'accountant', 'budget', 'revenue']
    medical_keywords = ['medical', 'doctor', 'nurse', 'pharmacy', 'healthcare', 'dentist', 'physician', 'surgeon', 'clinic', 'radiology', 'psychiatry', 'dermatology', 'urology', 'nephrology', 'pulmonology', 'ophthalmology', 'ayurveda', 'homeopathy', 'public health']
    science_keywords = ['science', 'research', 'physics', 'chemistry', 'biology', 'scientist', 'laboratory', 'biotech']
    
    is_role_tech = any(kw in role_raw for kw in tech_keywords)
    is_upsc = 'upsc' in role_raw or 'civil service' in role_raw or 'ias' in role_raw
    is_ssc = 'ssc' in role_raw or 'cgl' in role_raw
    is_appsc = 'appsc' in role_raw or 'ap' in role_raw and ('psc' in role_raw or 'group' in role_raw)
    is_tspsc = 'tspsc' in role_raw or 'tpsc' in role_raw or 'telangana' in role_raw and ('psc' in role_raw or 'group' in role_raw)
    
    is_civil = is_upsc or is_appsc or is_tspsc or any(kw in role_raw for kw in civil_keywords)
    is_finance = is_ssc or any(kw in role_raw for kw in finance_keywords)
    is_medical = any(kw in role_raw for kw in medical_keywords)
    is_science = any(kw in role_raw for kw in science_keywords)

    edu = user.education_level or ""
    is_tech_edu = any(kw in edu for kw in ['B.Tech', 'M.Tech', 'Diploma', 'ITI'])
    
    # Priority: Role keywords override education
    is_tech = is_role_tech or is_tech_edu
    if is_civil or is_finance or is_medical or is_science:
        is_tech = is_role_tech
    
    # 1. Fetch Technical/Role-Specific Pool
    if is_tech:
        role_pool = Question.query.filter(Question.category.in_(["Coding", "Core CS"])).all()
    elif is_upsc:
        role_pool = Question.query.filter(Question.category.in_(["Civil Service", "IAS", "UPSC"])).all()
    elif is_appsc or is_tspsc:
        cat = "APPSC" if is_appsc else "TSPSC"
        role_pool = Question.query.filter(Question.category.in_(["Civil Service", cat])).all()
    elif is_ssc:
        role_pool = Question.query.filter(Question.category.in_(["Finance/Govt", "SSC"])).all()
    elif is_civil:
        role_pool = Question.query.filter(Question.category.in_(["Civil Service", "IAS"])).all()
    elif is_finance:
        role_pool = Question.query.filter(Question.category.in_(["Finance/Govt"])).all()
    elif is_medical:
        role_pool = Question.query.filter_by(category="Medical").all()
    elif is_science:
        role_pool = Question.query.filter_by(category="Science").all()
    else:
        # Check educational category if no role match
        edu = user.education_level or ""
        if 'School' in edu: category = "School"
        elif 'Intermediate' in edu: category = "Intermediate"
        elif edu in ['ITI', 'Diploma']: category = "Vocational"
        else: category = "Professional"
        role_pool = Question.query.filter_by(category=category).all()
    
    # 2. Refine by role keywords if possible
    # We want to be more specific if the pool is large
    refined_role_pool = [q for q in role_pool if any(word in (q.sub_category or "").lower() or word in q.question_text.lower() for word in role_raw.split())]
    
    # If refinement is too narrow, use the category pool
    if len(refined_role_pool) < 3:
        refined_role_pool = role_pool
    
    # 3. IF THE POOL IS STILL EMPTY, FALLBACK GRACEFULLY
    if not refined_role_pool:
        # Fallback to "Professional" (Management/Leadership) which is safer than mixing all domains
        refined_role_pool = Question.query.filter(Question.category == "Professional").all()
        
    # Final catch-all to prevent crash, though Professional should have content
    if not refined_role_pool:
        refined_role_pool = Question.query.filter(Question.category != "HR").limit(10).all()
    
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
