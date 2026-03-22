from models import QuizQuestion
import random

def get_quiz_questions(user, week_number=1, count=5):
    """
    Selects balanced MCQs based on user role and week number.
    """
    role_raw = (user.desired_role or "").lower()
    edu = user.education_level or ""
    
    # Robust Role Detection (Synchronized with roadmap.py)
    tech_keywords = ['engineer', 'developer', 'coding', 'ai', 'data', 'software', 'tech', 'programmer', 'web', 'frontend', 'backend', 'fullstack', 'devops', 'stack', 'cloud', 'security', 'machine learning', 'data science', 'cse', 'it', 'ece', 'eee', 'iot', 'aiml', 'vlsi', 'embedded', 'robotics', 'mech', 'mechanical', 'civil', 'chemical', 'aerospace']
    civil_service_keywords = ['ias', 'civil service', 'upsc', 'mro', 'revenue officer', 'tpsc', 'appsc', 'group 1', 'group 2', 'constable', 'sub-inspector', 'panchayat', 'administrative', 'ips', 'ifs', 'collector']
    finance_govt_keywords = ['income tax', 'tax', 'ssc', 'cgl', 'banking', 'bank', 'po', 'clerk', 'finance', 'audit', 'lic', 'rbi', 'ibps', 'accountant', 'budget', 'revenue']
    medical_keywords = [
        'medical', 'doctor', 'nurse', 'pharmacy', 'healthcare', 'dentist', 'physician', 'surgeon', 'clinic',
        'cardiolog', 'radiolog', 'dermato', 'pediatr', 'ortho', 'ayush', 'homeo', 'physio', 'dent', 
        'mbbs', 'bds', 'bams', 'bhms', 'nurs', 'pharm', 'hospital', 'clinic', 'surgeon', 'officer'
    ]
    science_keywords = ['science', 'research', 'physics', 'chemistry', 'biology', 'scientist', 'laboratory', 'biotech', 'researcher']

    is_mbbs = any(kw in role_raw for kw in ['mbbs', 'doctor', 'physician', 'surgeon', 'medical officer', 'cardiolog', 'radiolog', 'dermato', 'pediatr', 'ortho'])
    is_nursing = any(kw in role_raw for kw in ['nurse', 'nursing', 'anm', 'gnm'])
    is_pharmacy = any(kw in role_raw for kw in ['pharmacist', 'pharmacy', 'b.pharm', 'm.pharm', 'druggist'])
    is_dental = any(kw in role_raw for kw in ['dentist', 'dental', 'bds', 'mds'])
    
    is_medical_role = is_mbbs or is_nursing or is_pharmacy or is_dental or any(kw in role_raw for kw in medical_keywords)
    
    is_role_tech = any(kw in role_raw for kw in tech_keywords)
    is_civil = any(kw in role_raw for kw in civil_service_keywords)
    is_finance_govt = any(kw in role_raw for kw in finance_govt_keywords)
    is_medical = is_medical_role
    is_science = any(kw in role_raw for kw in science_keywords)

    is_higher_tech = 'B.Tech' in edu or 'M.Tech' in edu
    is_iti_diploma = 'ITI' in edu or 'Diploma' in edu
    is_school = 'School' in edu
    is_intermediate = 'Intermediate' in edu

    # B.Tech/M.Tech Branch Detection (Synchronized with roadmap.py)
    edu_lower = edu.lower()
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
    
    # Priority: Specialized role flags determine Category
    if is_civil: category = "Civil Service"
    elif is_finance_govt: category = "Finance/Govt"
    elif is_medical: category = "Medical"
    elif is_science: category = "Science"
    elif is_ece: category = "ECE"
    elif is_eee: category = "EEE"
    elif is_mech: category = "MECH"
    elif is_civil_eng: category = "CIVIL"
    elif is_chemical: category = "CHEMICAL"
    elif is_aiml: category = "AIML"
    elif is_iot: category = "IOT"
    elif is_aerospace: category = "AEROSPACE"
    elif is_role_tech or (is_higher_tech or is_iti_diploma): category = "Coding"
    elif is_school: category = "School"
    elif is_intermediate: category = "Intermediate"
    elif is_iti_diploma: category = "Vocational"
    else: category = "Professional"
        
    # Map roadmap week to DB week (assuming 4 weeks of content)
    try:
        mapped_week = (int(week_number) - 1) % 4 + 1
    except (ValueError, TypeError):
        mapped_week = 1
    
    # Sub-category filtering (Wait! Re-use the booleans for sub-cat selection too)
    preferred_subcats = []
    
    if is_ece:
        if mapped_week == 1: preferred_subcats = ['Electronic Devices', 'Digital Circuits', 'Network Theory']
        elif mapped_week == 2: preferred_subcats = ['Analog Circuits', 'Signals & Systems', 'Electromagnetics']
        elif mapped_week == 3: preferred_subcats = ['Microprocessors', 'Control Systems', 'Digital Communication']
        elif mapped_week == 4: preferred_subcats = ['VLSI Design', 'Embedded Systems', 'DSP', 'Microwave']
        
    elif is_eee:
        if mapped_week == 1: preferred_subcats = ['Electrical Machines', 'Network Theory', 'Power Systems Basics']
        elif mapped_week == 2: preferred_subcats = ['Control Systems', 'Power Electronics', 'Measurement']
        elif mapped_week == 3: preferred_subcats = ['Power System Analysis', 'Machines-II', 'Switchgear']
        elif mapped_week == 4: preferred_subcats = ['Smart Grids', 'Renewable Energy', 'Automation']
        
    elif is_mech:
        if mapped_week == 1: preferred_subcats = ['Thermodynamics', 'Fluid Mechanics', 'Engineering Mechanics']
        elif mapped_week == 2: preferred_subcats = ['Material Science', 'Manufacturing', 'Solid Mechanics']
        elif mapped_week == 3: preferred_subcats = ['Machine Design', 'Heat Transfer', 'Kinematics']
        elif mapped_week == 4: preferred_subcats = ['IC Engines', 'Turbo Machinery', 'CAD/CAM', 'Mechatronics']
        
    elif is_civil_eng:
        if mapped_week == 1: preferred_subcats = ['Strength of Materials', 'Building Materials', 'Surveying']
        elif mapped_week == 2: preferred_subcats = ['Structural Analysis', 'Fluid Mechanics', 'Concrete Technology']
        elif mapped_week == 3: preferred_subcats = ['Soil Mechanics', 'Hydrology', 'Environmental Engineering']
        elif mapped_week == 4: preferred_subcats = ['Steel Structures', 'Transportation', 'CAD', 'Management']

    elif is_aiml:
        if mapped_week == 1: preferred_subcats = ['Probability', 'Linear Algebra', 'Python Foundations']
        elif mapped_week == 2: preferred_subcats = ['Supervised Learning', 'Optimization', 'Data Preprocessing']
        elif mapped_week == 3: preferred_subcats = ['Neural Networks', 'Deep Learning', 'Unsupervised Learning']
        elif mapped_week == 4: preferred_subcats = ['NLP', 'Computer Vision', 'Reinforcement Learning', 'MLOps']

    elif is_iot:
        if mapped_week == 1: preferred_subcats = ['IoT Basics', 'MQTT', 'Sensors']
        elif mapped_week == 2: preferred_subcats = ['Embedded C', 'Microcontrollers', 'Interfacing']
        elif mapped_week == 3: preferred_subcats = ['WSN', 'Connectivity', 'IoT Protocols']
        elif mapped_week == 4: preferred_subcats = ['IoT Security', 'Edge Computing', 'Cloud Platforms']

    elif is_chemical:
        if mapped_week == 1: preferred_subcats = ['Reaction Engineering', 'Thermodynamics', 'Fluid Flow']
        elif mapped_week == 2: preferred_subcats = ['Heat Transfer', 'Mass Transfer', 'Process Control']
        elif mapped_week == 3: preferred_subcats = ['Chemical Technology', 'Reactor Design', 'Separation']
        elif mapped_week == 4: preferred_subcats = ['Plant Design', 'Safety', 'Economics', 'Polymers']

    elif is_aerospace:
        if mapped_week == 1: preferred_subcats = ['Aerodynamics', 'Structures', 'Flight Mechanics']
        elif mapped_week == 2: preferred_subcats = ['Propulsion', 'Avionics', 'Materials']
        elif mapped_week == 3: preferred_subcats = ['Rocket Propulsion', 'Orbital Mechanics', 'Control']
        elif mapped_week == 4: preferred_subcats = ['Space Mission', 'CFD', 'Stability', 'Navigation']

    elif category == "Coding":
        if mapped_week == 1: preferred_subcats = ['OS', 'DBMS', 'Data Structures']
        elif mapped_week == 2: preferred_subcats = ['Advanced Data Structures', 'Core Languages', 'Networking']
        elif mapped_week == 3: preferred_subcats = ['Frameworks', 'APIs', 'Testing']
        elif mapped_week == 4: preferred_subcats = ['Scalability', 'CI/CD', 'Architecture']

    elif is_civil:
        if mapped_week == 1: preferred_subcats = ['Polity', 'Governance']
        elif mapped_week == 2: preferred_subcats = ['History', 'Geography']
        elif mapped_week == 3: preferred_subcats = ['Economy', 'Social Justice']
        elif mapped_week == 4: preferred_subcats = ['Ethics', 'Current Affairs', 'Environment', 'Science']
        
    elif is_finance_govt:
        if mapped_week == 1: preferred_subcats = ['Numerical Ability', 'Reasoning', 'Core Concepts']
        elif mapped_week == 2: preferred_subcats = ['Polity', 'History', 'Geography', 'Economy']
        elif mapped_week == 3: preferred_subcats = ['Taxation', 'Banking', 'Financial Awareness']
        elif mapped_week == 4: preferred_subcats = ['Mock Tests', 'Interviews', 'Current Affairs']

    elif is_mbbs:
        if mapped_week == 1: preferred_subcats = ['Anatomy', 'Physiology', 'Biochemistry']
        elif mapped_week == 2: preferred_subcats = ['Pathology', 'Microbiology', 'Pharmacology', 'Forensic']
        elif mapped_week == 3: preferred_subcats = ['General Medicine', 'General Surgery', 'Pediatrics']
        elif mapped_week == 4: preferred_subcats = ['Obstetrics', 'Gynecology', 'Community Medicine']

    elif is_nursing:
        if mapped_week == 1: preferred_subcats = ['Anatomy', 'Nursing Foundations']
        elif mapped_week == 2: preferred_subcats = ['Medical-Surgical Nursing', 'Nutrition']
        elif mapped_week == 3: preferred_subcats = ['Child Health Nursing', 'Mental Health Nursing']
        elif mapped_week == 4: preferred_subcats = ['Community Health Nursing', 'Pharmacology']
        
    elif is_pharmacy:
        if mapped_week == 1: preferred_subcats = ['Pharmaceutical Chemistry', 'Anatomy', 'Physiology']
        elif mapped_week == 2: preferred_subcats = ['Pharmaceutics', 'Pharmacognosy']
        elif mapped_week == 3: preferred_subcats = ['Pharmacology', 'Pharmaceutical Analysis']
        elif mapped_week == 4: preferred_subcats = ['Hospital Pharmacy', 'Clinical Research']

    elif is_dental:
        if mapped_week == 1: preferred_subcats = ['Oral Anatomy', 'Dental Materials']
        elif mapped_week == 2: preferred_subcats = ['General Pathology', 'Microbiology', 'Pharmacology']
        elif mapped_week == 3: preferred_subcats = ['Oral Surgery', 'Conservative Dentistry', 'Endodontics']
        elif mapped_week == 4: preferred_subcats = ['Prosthodontics', 'Periodontology', 'Orthodontics']

    elif is_school:
        if mapped_week == 1: preferred_subcats = ['Mathematics', 'Logical Reasoning', 'Computer Basics']
        elif mapped_week == 2: preferred_subcats = ['Physics', 'Chemistry', 'Biology', 'Scientific Method']
        elif mapped_week == 3: preferred_subcats = ['History', 'Geography', 'Civics', 'Economy']
        elif mapped_week == 4: preferred_subcats = ['English', 'Public Speaking', 'Time Management']

    elif is_intermediate:
        if mapped_week == 1: preferred_subcats = ['Advanced Physics', 'Advanced Chemistry', 'Math', 'Biology']
        elif mapped_week == 2: preferred_subcats = ['Competitive Exams', 'Pattern Recognition', 'JEE', 'NEET']
        elif mapped_week == 3: preferred_subcats = ['English Literature', 'Ethics', 'IT Basics']
        elif mapped_week == 4: preferred_subcats = ['Career Planning', 'Research Methodology', 'Personality Development']

    elif is_iti_diploma:
        if mapped_week == 1: preferred_subcats = ['Trade Theory', 'Workshop Calculation', 'Safety']
        elif mapped_week == 2: preferred_subcats = ['Material Science', 'Electrical', 'Manufacturing']
        elif mapped_week == 3: preferred_subcats = ['Digital Literacy', 'Quality Management', 'Entrepreneurship']
        elif mapped_week == 4: preferred_subcats = ['Project Work', 'Practical Training', 'Soft Skills']

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
        
    # Final fallback: if still not enough, take any from the SAME category regardless of week
    if len(questions) < count:
        remaining = count - len(questions)
        excluded_ids = [q.id for q in questions]
        fallback = QuizQuestion.query.filter_by(category=category).filter(~QuizQuestion.id.in_(excluded_ids)).order_by(func.random()).limit(remaining).all()
        questions.extend(fallback)
        
    # ABSOLUTE LAST RESORT: if category is empty, only then fallback to 'Professional'
    if len(questions) < count and category != "Professional":
        remaining = count - len(questions)
        excluded_ids = [q.id for q in questions]
        pro_fallback = QuizQuestion.query.filter_by(category="Professional").filter(~QuizQuestion.id.in_(excluded_ids)).order_by(func.random()).limit(remaining).all()
        questions.extend(pro_fallback)
        
    return questions
