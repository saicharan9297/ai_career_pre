from models import Question, User
import random

def get_interview_session_questions(user):
    """
    Returns a list of 5 questions: 3 role-specific and 2 HR questions.
    """
    # Case-insensitive role and edu check
    role_raw = (user.desired_role or "").lower()
    edu = user.education_level or ""
    edu_lower = edu.lower()

    # Robust Role Detection (Synchronized with roadmap.py)
    tech_keywords = ['engineer', 'developer', 'coding', 'ai', 'data', 'software', 'tech', 'programmer', 'web', 'frontend', 'backend', 'fullstack', 'devops', 'stack', 'cloud', 'security', 'machine learning', 'data science', 'cse', 'it', 'ece', 'eee', 'iot', 'aiml', 'vlsi', 'embedded', 'robotics', 'mech', 'mechanical', 'civil', 'chemical', 'aerospace']
    civil_keywords = ['ias', 'civil service', 'upsc', 'mro', 'revenue officer', 'tpsc', 'appsc', 'group 1', 'group 2', 'constable', 'sub-inspector', 'panchayat', 'administrative', 'ips', 'ifs', 'collector', 'telangana', 'andhra']
    finance_keywords = ['income tax', 'tax', 'ssc', 'cgl', 'banking', 'bank', 'po', 'clerk', 'finance', 'audit', 'lic', 'rbi', 'ibps', 'accountant', 'budget', 'revenue']
    medical_keywords = ['medical', 'doctor', 'nurse', 'nursing', 'pharmacy', 'hospital', 'healthcare', 'dentist', 'physician', 'surgeon', 'clinic', 'radiology', 'psychiatry', 'dermatology', 'urology', 'nephrology', 'pulmonology', 'ophthalmology', 'ayurveda', 'homeopathy', 'public health']
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
    
    # B.Tech/M.Tech Branch Detection (Synchronized with roadmap.py)
    is_cse = any(kw in edu_lower or kw in role_raw for kw in ['cse', 'computer science', 'software', 'it', 'web', 'frontend', 'backend', 'fullstack', 'devops', 'cloud', 'security', 'cyber', 'network', 'system admin', 'data analyst', 'database', 'dba'])
    is_datascience = any(kw in edu_lower or kw in role_raw for kw in ['datascience', 'data science', 'scientist', 'analyst', 'statistics', 'tableau', 'power bi', 'sql', 'data engineer', 'big data', 'pandas', 'numpy', 'ml engineer'])
    is_ece = any(kw in edu_lower or kw in role_raw for kw in ['ece', 'electronics', 'communication', 'vlsi', 'embedded', 'microprocessor', 'microcontroller', 'signals', 'antenna', 'circuit', 'hardware', 'telecom', 'semiconductor', 'analog', 'digital systems', 'embedded engineer'])
    is_eee = any(kw in edu_lower or kw in role_raw for kw in ['eee', 'electrical', 'power system', 'power engineering', 'machines', 'control system', 'smart grid', 'renewable', 'high voltage', 'automation', 'instrumentation', 'electrical engineer'])
    is_mech = any(kw in edu_lower or kw in role_raw for kw in ['mech', 'mechanical', 'thermal', 'thermodynamics', 'manufacturing', 'solid mechanics', 'fluid mechanics', 'cad', 'cam', 'automobile', 'mechatronics', 'robotics', 'industrial', 'design engineer', 'mechanical engineer'])
    is_civil_eng = any(kw in edu_lower or kw in role_raw for kw in ['civil', 'construction', 'structural', 'surveying', 'geotech', 'geology', 'transportation', 'environmental eng', 'urban planning', 'hydrology', 'steel structures'])
    is_aiml = any(kw in edu_lower or kw in role_raw for kw in ['aiml', 'ai', 'machine learning', 'deep learning', 'neural network', 'nlp', 'computer vision', 'data science', 'analytics'])
    is_iot = any(kw in edu_lower or kw in role_raw for kw in ['iot', 'internet of things', 'mqtt', 'sensors', 'edge computing', 'wsn', 'connectivity'])
    is_chemical = any(kw in edu_lower or kw in role_raw for kw in ['chemical', 'petroleum', 'process engineering', 'polymer', 'biochemical', 'fertilizer', 'refinery'])
    is_aerospace = any(kw in edu_lower or kw in role_raw for kw in ['aerospace', 'aero', 'satellite', 'rocket', 'avionics', 'propulsion', 'flight', 'orbital'])
    is_cyber = any(kw in edu_lower or kw in role_raw for kw in ['cyber', 'security', 'penetration', 'ethical hacking', 'infosec', 'forensics', 'cryptography'])
    
    # Priority: Role keywords override education
    is_tech = is_role_tech or is_tech_edu
    if is_civil or is_finance or is_medical or is_science:
        is_tech = is_role_tech
    # 1. Fetch Technical/Role-Specific Pool
    if is_cyber:
        role_pool = Question.query.filter(Question.category == "Cyber Security").all()
    elif is_datascience:
        role_pool = Question.query.filter(Question.category == "Data Science").all()
    elif is_aiml:
        role_pool = Question.query.filter(Question.category == "AIML").all()
    elif is_ece:
        role_pool = Question.query.filter(Question.category == "ECE").all()
    elif is_eee:
        role_pool = Question.query.filter(Question.category == "EEE").all()
    elif is_mech:
        role_pool = Question.query.filter(Question.category == "MECH").all()
    elif is_civil_eng:
        role_pool = Question.query.filter(Question.category == "CIVIL").all()
    elif is_chemical:
        role_pool = Question.query.filter(Question.category == "CHEMICAL").all()
    elif is_iot:
        role_pool = Question.query.filter(Question.category == "IOT").all()
    elif is_aerospace:
        role_pool = Question.query.filter(Question.category == "AEROSPACE").all()
    elif is_medical:
        role_pool = Question.query.filter_by(category="Medical").all()
    elif is_science:
        role_pool = Question.query.filter_by(category="Science").all()
    elif is_tech:
        role_pool = Question.query.filter(Question.category.in_(["Coding", "Core CS", "CSE"])).all()
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
    else:
        # Check educational category if no role match
        edu = user.education_level or ""
        if 'School' in edu: category = "School"
        elif 'Intermediate' in edu: category = "Intermediate"
        elif any(kw in edu for kw in ['ITI', 'Diploma']): category = "Vocational"
        else: category = "Professional"
        role_pool = Question.query.filter_by(category=category).all()

    # --- Robust Fallback for Technical Branch questions ---
    # If a technical branch has fewer than 3 questions, supplement with general Coding questions
    if is_tech and len(role_pool) < 3:
        coding_pool = Question.query.filter(Question.category.in_(["Coding", "Core CS", "CSE"])).all()
        role_pool.extend(coding_pool)
    
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
