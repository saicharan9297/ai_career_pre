try:
    from core.ai_service import generate_roadmap_ai
    from models import QuizQuestion
    import json
except ImportError:
    generate_roadmap_ai = None

def get_recommendations(user):
    """
    Returns a list of recommended roles based on user profile and community trends.
    """
    from models import User, db
    from sqlalchemy import func
    
    edu = (user.education_level or "").lower()
    current_role = (user.desired_role or "").strip()
    
    # 1. Fetch Community Trends (Roles others are preparing for)
    # Get top 5 most popular roles excluding current user's role
    trending_query = db.session.query(
        User.desired_role, 
        func.count(User.id).label('user_count')
    ).filter(
        User.desired_role != None,
        User.desired_role != "",
        User.desired_role != current_role
    ).group_by(User.desired_role).order_by(func.count(User.id).desc()).limit(5).all()
    
    community_recs = []
    for role_name, count in trending_query:
        community_recs.append({
            "role": role_name,
            "description": f"Trending: {count} people are following this roadmap.",
            "is_community": True,
            "user_count": count
        })

    # 2. Base recommendations by education (Original fallback/static)
    static_recs = []
    if "b.tech" in edu or "m.tech" in edu:
        static_recs = [
            {"role": "Full Stack Developer", "description": "Mastering both frontend and backend technologies."},
            {"role": "Data Scientist", "description": "Analyzing complex data to drive business decisions."},
            {"role": "DevOps Engineer", "description": "Bridging the gap between development and operations."}
        ]
    elif "intermediate" in edu or "school" in edu:
        static_recs = [
            {"role": "Engineering Foundation", "description": "Strengthening math and physics for technical careers."},
            {"role": "Coding Basics (Python)", "description": "Starting your journey into software development."},
            {"role": "NDA / Defense Services", "description": "Preparing for a career in the Indian Armed Forces."}
        ]
    else:
        static_recs = [
            {"role": "Civil Services (IAS/IPS)", "description": "The peak of administrative careers in India."},
            {"role": "Banking (IBPS/PO)", "description": "Stable and prestigious career in the financial sector."},
            {"role": "Digital Marketing", "description": "Fast-paced career in the modern digital economy."}
        ]
    
    # Combine and prioritize community if available
    all_recs = community_recs + [r for r in static_recs if r['role'].lower().strip() != current_role.lower().strip()]
    
    # Return unique roles
    seen_roles = set([current_role.lower().strip()])
    final_recs = []
    for r in all_recs:
        role_key = r['role'].lower().strip()
        if role_key not in seen_roles:
            final_recs.append(r)
            seen_roles.add(role_key)
            
    return final_recs[:4]
def generate_roadmap(user):
    """
    Generates a personalized roadmap based on user profile and preparation duration.
    """
    role_raw = (user.desired_role or "Career Search").strip()
    role_lower = role_raw.lower()
    edu = user.education_level
    try:
        hours = int(user.available_time or 2)
    except (ValueError, TypeError):
        hours = 2
    
    # Robust Role Detection Keywords
    tech_keywords = ['engineer', 'developer', 'coding', 'ai', 'data', 'software', 'tech', 'programmer', 'web', 'frontend', 'backend', 'fullstack', 'devops', 'stack', 'cloud', 'security', 'machine learning', 'data science', 'cse', 'it', 'ece', 'eee', 'iot', 'aiml', 'vlsi', 'embedded', 'robotics', 'mech', 'mechanical', 'civil', 'chemical', 'aerospace']
    civil_service_keywords = ['ias', 'civil service', 'upsc', 'mro', 'revenue officer', 'tpsc', 'appsc', 'group 1', 'group 2', 'constable', 'sub-inspector', 'panchayat', 'administrative', 'ips', 'ifs', 'collector']
    finance_govt_keywords = ['income tax', 'tax', 'ssc', 'cgl', 'banking', 'bank', 'po', 'clerk', 'finance', 'audit', 'lic', 'rbi', 'ibps', 'accountant', 'budget', 'revenue', 'economist', 'tally']
    medical_keywords = ['medical', 'doctor', 'nurse', 'nursing', 'pharmacy', 'hospital', 'healthcare', 'dentist', 'physician', 'surgeon', 'clinic', 'cardiology', 'neurology', 'orthopedic', 'physiotherapy', 'veterinary', 'radiology', 'psychiatry', 'dermatology', 'urology', 'nephrology', 'pulmonology', 'ophthalmology', 'ayurveda', 'homeopathy', 'public health', 'therapist']
    creative_keywords = ['designer', 'graphic', 'ui', 'ux', 'artist', 'video', 'content', 'writer', 'editor', 'creative', 'animation', 'multimedia']
    business_keywords = ['manager', 'marketing', 'sales', 'hr', 'human resources', 'business', 'analyst', 'finance', 'consultant', 'operation', 'supply chain', 'mba']
    science_keywords = ['science', 'research', 'physics', 'chemistry', 'biology', 'scientist', 'laboratory', 'biotech']

    # Detailed Medical Role Flags
    is_mbbs = any(kw in role_lower for kw in ['mbbs', 'doctor', 'physician', 'surgeon', 'medical officer', 'cardiologist', 'neurologist', 'orthopedic surgeon', 'pediatrician', 'gynecologist', 'dermatologist', 'psychiatrist', 'radiologist', 'urologist', 'nephrologist', 'pulmonologist'])
    is_nursing = any(kw in role_lower for kw in ['nurse', 'nursing', 'anm', 'gnm', 'midwifery'])
    is_pharmacy = any(kw in role_lower for kw in ['pharmacist', 'pharmacy', 'b.pharm', 'm.pharm', 'druggist'])
    is_dental = any(kw in role_lower for kw in ['dentist', 'dental', 'bds', 'mds', 'orthodontist', 'periodontist'])
    is_physio = any(kw in role_lower for kw in ['physiotherapy', 'physiotherapist', 'physical therapist', 'therapist', 'bpt', 'mpt', 'rehabilitation'])
    is_vet = any(kw in role_lower for kw in ['veterinary', 'vet', 'animal doctor', 'bvg', 'mvg'])
    is_ayush = any(kw in role_lower for kw in ['ayurveda', 'homeopathy', 'bams', 'bhms', 'unani', 'yoga'])
    is_allied_health = any(kw in role_lower for kw in ['radiographer', 'lab technician', 'optometry', 'dialysis', 'paramedic'])
    
    # Combined medical flag
    is_medical_role = is_mbbs or is_nursing or is_pharmacy or is_dental or is_physio or is_vet or is_ayush or is_allied_health or any(kw in role_lower for kw in medical_keywords)
    is_medical = is_medical_role
    is_science = any(kw in role_lower for kw in science_keywords)
    
    prep_weeks = user.prep_weeks or 1
    
    # Specific ROLE matching (Prioritize keywords in desired_role)
    is_role_tech = any(kw in role_lower for kw in tech_keywords)
    is_upsc = 'upsc' in role_lower or 'civil service' in role_lower or 'ias' in role_lower or 'ips' in role_lower
    is_ssc = 'ssc' in role_lower or 'cgl' in role_lower or 'chsl' in role_lower
    is_appsc = 'appsc' in role_lower or 'ap' in role_lower and ('psc' in role_lower or 'group' in role_lower)
    is_tspsc = 'tspsc' in role_lower or 'tpsc' in role_lower or 'telangana' in role_lower and ('psc' in role_lower or 'group' in role_lower)
    
    is_civil_service = is_upsc or is_appsc or is_tspsc or any(kw in role_lower for kw in civil_service_keywords)
    is_finance_govt = is_ssc or any(kw in role_lower for kw in finance_govt_keywords)
    
    # Education Level Specific Flags
    edu_safe = edu or ""
    is_school = 'School' in edu_safe
    is_intermediate = 'Intermediate' in edu_safe
    is_iti_diploma = 'Diploma' in edu_safe or 'ITI' in edu_safe
    is_btech = 'B.Tech' in edu_safe
    is_mtech = 'M.Tech' in edu_safe
    is_higher_tech = is_btech or is_mtech

    # Specific B.Tech/M.Tech Branch Detection (Expanded for robust matching)
    edu_lower = (edu or "").lower()
    is_cse = any(kw in edu_lower or kw in role_lower for kw in ['cse', 'computer science', 'software', 'it', 'web', 'frontend', 'backend', 'fullstack', 'devops', 'cloud', 'security', 'cyber', 'network', 'system admin', 'data analyst', 'database', 'dba'])
    is_datascience = any(kw in edu_lower or kw in role_lower for kw in ['datascience', 'data science', 'scientist', 'analyst', 'statistics', 'tableau', 'power bi', 'sql', 'data engineer', 'big data', 'pandas', 'numpy', 'ml engineer'])
    is_ece = any(kw in edu_lower or kw in role_lower for kw in ['ece', 'electronics', 'communication', 'vlsi', 'embedded', 'microprocessor', 'microcontroller', 'signals', 'antenna', 'circuit', 'hardware', 'telecom', 'semiconductor', 'analog', 'digital systems', 'embedded engineer'])
    is_eee = any(kw in edu_lower or kw in role_lower for kw in ['eee', 'electrical', 'power system', 'power engineering', 'machines', 'control system', 'smart grid', 'renewable', 'high voltage', 'automation', 'instrumentation', 'electrical engineer'])
    is_mech = any(kw in edu_lower or kw in role_lower for kw in ['mech', 'mechanical', 'thermal', 'thermodynamics', 'manufacturing', 'solid mechanics', 'fluid mechanics', 'cad', 'cam', 'automobile', 'mechatronics', 'robotics', 'industrial', 'design engineer', 'mechanical engineer'])
    is_civil_eng = any(kw in edu_lower or kw in role_lower for kw in ['civil', 'construction', 'structural', 'surveying', 'geotech', 'geology', 'transportation', 'environmental eng', 'urban planning', 'hydrology', 'steel structures'])
    is_aiml = any(kw in edu_lower or kw in role_lower for kw in ['aiml', 'ai', 'machine learning', 'deep learning', 'neural network', 'nlp', 'computer vision', 'data science', 'analytics'])
    is_iot = any(kw in edu_lower or kw in role_lower for kw in ['iot', 'internet of things', 'mqtt', 'sensors', 'edge computing', 'wsn', 'connectivity'])
    is_chemical = any(kw in edu_lower or kw in role_lower for kw in ['chemical', 'petroleum', 'process engineering', 'polymer', 'biochemical', 'fertilizer', 'refinery'])
    is_aerospace = any(kw in edu_lower or kw in role_lower for kw in ['aerospace', 'aero', 'satellite', 'rocket', 'avionics', 'propulsion', 'flight', 'orbital'])
    is_cyber = any(kw in edu_lower or kw in role_lower for kw in ['cyber', 'security', 'penetration', 'ethical hacking', 'infosec', 'forensics', 'cryptography'])
    
    # Career Guidance Information
    guidance = None
    if is_school:
        guidance = "Educational Path: Complete your 10th standard first. After 10th, you can choose Intermediate (MPC/BiPC/CEC) for a general path or a Diploma (Polytechnic) for an early technical career."
    elif is_intermediate or is_iti_diploma:
        stage = "Intermediate" if is_intermediate else "Diploma"
        guidance = f"Educational Path: Complete your {stage} successfully. After this, you should pursue B.Tech or a Bachelor's degree in your field of interest for better job opportunities."
    
    # Combine tech role with tech education background
    is_tech = is_role_tech or is_higher_tech
    
    # ITI/Diploma should only be considered "Generic Tech" if no specific role matches and no other category matches
    if not (is_civil_service or is_finance_govt or is_medical or is_science) and is_iti_diploma:
        if is_role_tech or role_lower in ["", "career search", "job", "fresher"]:
            is_tech = True
    
    # If a specific NON-TECH role is specified, it should override the tech education background
    if is_civil_service or is_finance_govt or is_medical or is_science:
        is_tech = is_role_tech # Only consider it tech if they explicitly asked for a tech role

    
    # Final Priority: Technical Role > Civil Service > Finance > Medical > Science > School/Inter/Voc/HigherTech

    roadmap = []
    
    is_creative = any(k in role_lower for k in creative_keywords)
    is_business = any(k in role_lower for k in business_keywords)
    
    # --- 0. Try Loading Cached Roadmap ---
    from models import UserProgress, db
    progress = UserProgress.query.filter_by(user_id=user.id, role=role_raw).first()
    
    if progress and progress.roadmap_json:
        try:
            cached_data = json.loads(progress.roadmap_json)
            # Ensure it matches current prep_weeks
            if cached_data.get('prep_weeks') == prep_weeks:
                print(f"DEBUG: Using cached roadmap for {role_raw}")
                # Ensure strategy text is updated for current hours/weeks
                if hours >= 4:
                    strategy = f"Intensive ({hours}h/day for {prep_weeks} weeks) - Mastery-Oriented"
                else:
                    strategy = f"Steady Progress ({hours}h/day for {prep_weeks} weeks) - Balanced"
                cached_data['strategy'] = f"AI Personalized ({strategy})" if cached_data.get('is_ai') else strategy
                return cached_data
        except Exception as e:
            print(f"DEBUG: Error loading cached roadmap: {str(e)}")

    # --- 1. Attempt AI Roadmap Generation (RAG) ---
    if generate_roadmap_ai:
        try:
            # RAG: Retrieve potential subjects from Database to guide the AI
            role_keyword = role_lower.split()[0] if role_lower else ""
            context_qs = QuizQuestion.query.filter(
                QuizQuestion.category.contains(role_keyword)
            ).limit(10).all()
            
            search_context = "\n".join([f"- {q.sub_category}: {q.question_text[:100]}" for q in context_qs]) if context_qs else "General career foundations."
            
            user_profile = {
                'desired_role': role_raw,
                'education_level': edu,
                'prep_weeks': prep_weeks
            }
            
            print(f"DEBUG: Calling AI for roadmap: {role_raw}")
            ai_roadmap_raw = generate_roadmap_ai(user_profile, search_context)
            
            if ai_roadmap_raw and "Error" not in ai_roadmap_raw:
                # Basic cleanup
                clean_json = ai_roadmap_raw.strip()
                if clean_json.startswith("```json"):
                    clean_json = clean_json.replace("```json", "").replace("```", "").strip()
                elif clean_json.startswith("```"):
                    clean_json = clean_json.replace("```", "").strip()
                
                ai_roadmap = json.loads(clean_json)
                
                # Robust parsing for list or dict-wrapped-list
                if isinstance(ai_roadmap, dict):
                    # Try common keys
                    for key in ['weeks', 'roadmap', 'plan', 'modules']:
                        if key in ai_roadmap and isinstance(ai_roadmap[key], list):
                            ai_roadmap = ai_roadmap[key]
                            break
                
                if isinstance(ai_roadmap, list) and len(ai_roadmap) > 0:
                    print(f"DEBUG: Successfully generated AI roadmap for {role_raw}")
                    # Return consistent dictionary format
                    result = {
                        "strategy": f"AI Personalized ({hours}h/day for {prep_weeks} weeks)",
                        "modules": ai_roadmap,
                        "target_role": role_raw,
                        "tips": ["Use the personalized roadmap for targeted study", "Keep consistent with daily practice"],
                        "prep_weeks": prep_weeks,
                        "guidance": "AI Generated Path: This roadmap was dynamically generated based on your profile.",
                        "is_ai": True
                    }
                    
                    # Cache the successful AI roadmap
                    if progress:
                        try:
                            progress.roadmap_json = json.dumps(result)
                            db.session.commit()
                            print(f"DEBUG: Cached AI roadmap for {role_raw}")
                        except Exception as cache_err:
                            print(f"DEBUG: Failed to cache roadmap: {str(cache_err)}")
                    
                    return result
                else:
                    print(f"DEBUG: AI Roadmap list empty or invalid: {ai_roadmap}")
            else:
                print(f"DEBUG: AI Roadmap raw response failed: {ai_roadmap_raw[:100] if ai_roadmap_raw else 'Empty'}")
        except Exception as e:
            print(f"DEBUG: AI Roadmap Generation Error: {str(e)}")

    # --- 2. Rule-Based Fallback (Current Logic) ---
    is_generic = False
    if is_tech:
        if is_btech and "1st Year" in edu:
            # Common subjects but with branch-specific intro
            branch_intro = "Engineering"
            branch_special = {"name": "Workshop Practice", "content": "Basic hand tools, fitting, and simple engineering assembly."}
            
            if is_ece:
                branch_intro = "Electronics"
                branch_special = {"name": "Introduction to Electronics", "content": "Basic components (Resistors, Caps, Diodes) and breadboard prototyping."}
            elif is_mech:
                branch_intro = "Mechanical"
                branch_special = {"name": "Basic Mechanical Engineering", "content": "Mechanism basics, engine cycles, and material properties."}
            elif is_cse:
                branch_intro = "Computing"
                branch_special = {"name": "Basics of IT & AI", "content": "Introduction to computer systems, AI ethics, and cloud basics."}
            elif is_datascience:
                branch_intro = "Data Science"
                branch_special = {"name": "Introduction to Data Science", "content": "Understanding data types, lifecycle, and visualization basics."}
            elif is_eee:
                branch_intro = "Electrical"
                branch_special = {"name": "Basic Electrical Engineering", "content": "DC/AC circuits, energy sources, and safety protocols."}

            all_themes = [
                {
                    "title": f"1st Year: {branch_intro} Foundations",
                    "subjects": [
                        {"name": "Engineering Mathematics - I", "content": "Calculus, Matrix theory, and equations for technical analysis."},
                        {"name": "Programming for Problem Solving", "content": "Foundations of C/Python, logic building, and algorithms."},
                        branch_special
                    ]
                },
                {
                    "title": "Science & Professional Design",
                    "subjects": [
                        {"name": "Engineering Physics/Chemistry", "content": "Core science principles applied to modern technical challenges."},
                        {"name": "Engineering Drawing/Graphics", "content": "Visualizing and sketching 2D/3D engineering components."},
                        {"name": "English & Communication Skills", "content": "Professional report writing and soft skills development."}
                    ]
                }
            ]
        elif is_btech and "2nd Year" in edu:
            if is_ece:
                all_themes = [
                    {
                        "title": "Electronic Circuits & Digital Logic",
                        "subjects": [
                            {"name": "Electronic Devices & Circuits", "content": "Semiconductors, Diodes, and Transistor biasing/analysis."},
                            {"name": "Digital System Design", "content": "Logic gates, K-maps, Flip-flops, and Sequential circuit design."},
                            {"name": "Signals & Systems", "content": "Continuous/Discrete time signals, Fourier series, and Z-transforms."}
                        ]
                    },
                    {
                        "title": "Electrical Networks & Fields",
                        "subjects": [
                            {"name": "Network Analysis", "content": "KVL/KCL, Mesh/Nodal analysis, and Network theorems (Thevenin/Norton)."},
                            {"name": "Electromagnetic Fields", "content": "Electrostatics, Magnetostatics, and Maxwell's equations."},
                            {"name": "Analog Communications Basics", "content": "Amplitude/Frequency modulation and basic receiver designs."}
                        ]
                    }
                ]
            elif is_eee:
                all_themes = [
                    {
                        "title": "Electrical Machines & Networks",
                        "subjects": [
                            {"name": "Electrical Machines - I", "content": "DC Generators, Motors, and single-phase transformers."},
                            {"name": "Network Theory", "content": "Steady state analysis, transient response, and two-port networks."},
                            {"name": "Electromagnetic Fields", "content": "Static electric and magnetic fields, and time-varying fields."}
                        ]
                    },
                    {
                        "title": "Analog Electronics & Measurements",
                        "subjects": [
                            {"name": "Analog Electronics", "content": "Op-amps, oscillators, and power amplifiers for EEE."},
                            {"name": "Electrical Measurements", "content": "Galvanometers, bridges, and energy meters."},
                            {"name": "Digital Electronics Basics", "content": "Logic families and combinational logic design."}
                        ]
                    }
                ]
            elif is_mech:
                all_themes = [
                    {
                        "title": "Thermal & Fluid Engineering",
                        "subjects": [
                            {"name": "Engineering Thermodynamics", "content": "Laws of thermodynamics, entropy, and pure substances."},
                            {"name": "Fluid Mechanics", "content": "Fluid statics, dynamics, and Bernoulli's equation."},
                            {"name": "Mechanics of Solids", "content": "Stress, strain, shear force, and bending moment diagrams."}
                        ]
                    },
                    {
                        "title": "Manufacturing & Materials",
                        "subjects": [
                            {"name": "Material Science", "content": "Crystal structures, phase diagrams, and heat treatment of steel."},
                            {"name": "Manufacturing Processes", "content": "Casting, forming, and welding processes."},
                            {"name": "Machine Drawing", "content": "Orthographic projections and assembly drawings."}
                        ]
                    }
                ]
            elif is_civil_eng:
                all_themes = [
                    {
                        "title": "Structural Mechanics & Materials",
                        "subjects": [
                            {"name": "Strength of Materials", "content": "Stresses, strains, and deflection of beams."},
                            {"name": "Building Materials", "content": "Properties of cement, concrete, bricks, and timber."},
                            {"name": "Surveying - I", "content": "Linear measurements, leveling, and compass surveying."}
                        ]
                    },
                    {
                        "title": "Fluid & Geo-Engineering Basics",
                        "subjects": [
                            {"name": "Fluid Mechanics", "content": "Properties of fluids and pipe flow basics."},
                            {"name": "Engineering Geology", "content": "Weathering, rock types, and geological structures."},
                            {"name": "Computer Aided Design (CAD)", "content": "Basics of AutoCAD for civil engineering drawings."}
                        ]
                    }
                ]
            elif is_datascience:
                all_themes = [
                    {
                        "title": "Data Foundations & Programming",
                        "subjects": [
                            {"name": "Probability & Statistics", "content": "Descriptive/Inferential statistics, distributions, and hypothesis testing."},
                            {"name": "Python for Data Science", "content": "NumPy, Pandas, and Matplotlib for data manipulation."},
                            {"name": "Database Management Systems", "content": "SQL, Normalization, and Relational database design."}
                        ]
                    },
                    {
                        "title": "Data Warehousing & Math",
                        "subjects": [
                            {"name": "Data Warehousing & Mining", "content": "ETL processes, associations, and clustering basics."},
                            {"name": "Discrete Mathematics", "content": "CS logic, set theory, and probability theory foundations."},
                            {"name": "Object Oriented Programming (Python/Java)", "content": "Classes and structures for data application design."}
                        ]
                    }
                ]
            elif is_cyber:
                all_themes = [
                    {
                        "title": "Cyber Security Foundations & Networking",
                        "subjects": [
                            {"name": "Network Security & Protocols", "content": "TCP/IP vulnerabilities, Firewalls, VPNs, and IDS/IPS systems."},
                            {"name": "Cryptography Foundations", "content": "Symmetric/Asymmetric encryption, Hashing, and Digital signatures."},
                            {"name": "Ethical Hacking Basics", "content": "Vulnerability assessment, port scanning, and security auditing."}
                        ]
                    },
                    {
                        "title": "Advanced Security & Defense",
                        "subjects": [
                            {"name": "Web Application Security", "content": "OWASP Top 10, SQL injection, XSS, and secure coding practices."},
                            {"name": "Incident Response & Forensics", "content": "Malware analysis, log investigation, and digital evidence recovery."},
                            {"name": "Identity & Access Management", "content": "OAuth, SAML, Multi-factor authentication, and Zero Trust models."}
                        ]
                    }
                ]
            else: # Default/Professional Readiness (Fallback for Generic Tech)
                is_generic = True
                all_themes = [
                    {
                        "title": "Core Technical Foundations",
                        "subjects": [
                            {"name": "Problem Solving & Logic", "content": "Analytical thinking and structured problem-solving techniques."},
                            {"name": "Fundamentals of Technology", "content": "Understanding modern tech stacks and industry standards."},
                            {"name": "Professional Communication", "content": "Professional ethics and technical communication skills."}
                        ]
                    },
                    {
                        "title": "Industry Orientation & Real-world Prep",
                        "subjects": [
                            {"name": "Project Lifecycle Basics", "content": "Understanding how software and systems are built and maintained."},
                            {"name": "Database & Info Management", "content": "Essential data handling and storage concepts for all tech roles."},
                            {"name": "Digital Productivity Tools", "content": "Mastering tools for collaboration and documentation."}
                        ]
                    }
                ]
        elif is_btech and ("3rd Year" in edu or "4th Year" in edu):
            if is_ece:
                all_themes = [
                    {
                        "title": "Advanced Communication & VLSI",
                        "subjects": [
                            {"name": "Digital Communication", "content": "Source coding, PCM, digital modulation schemes (ASK/FSK/PSK)."},
                            {"name": "VLSI Design", "content": "CMOS technology, layout design, and HDL programming (Verilog/VHDL)."},
                            {"name": "Antennas & Wave Propagation", "content": "Radiation patterns, dipole antennas, and wave propagation modes."}
                        ]
                    },
                    {
                        "title": "Embedded Systems & Control",
                        "subjects": [
                            {"name": "Microprocessors & Microcontrollers", "content": "8086 architectures, 8051 programming, and interfacing techniques."},
                            {"name": "Control Systems Engineering", "content": "Time/Frequency response, stability analysis, and feedback control."},
                            {"name": "Digital Signal Processing", "content": "DFT, FFT, FIR/IIR filters, and realized architectures."}
                        ]
                    },
                    {
                        "title": "Emerging ECE Technologies",
                        "subjects": [
                            {"name": "Microwave Engineering", "content": "Waveguides, S-parameters, and microwave components."},
                            {"name": "Optical Communications", "content": "Fiber optics, light sources, and detectors."},
                            {"name": "Wireless & Mobile Networks", "content": "Cellular concepts, 4G/5G technology, and IoT connectivity."}
                        ]
                    }
                ]
            elif is_eee:
                 all_themes = [
                    {
                        "title": "Power Systems & Machines",
                        "subjects": [
                            {"name": "Power Systems Analysis", "content": "Load flow studies, fault analysis, and power system stability."},
                            {"name": "Electrical Machines - II", "content": "Three-phase induction motors, synchronous machines."},
                            {"name": "Power Electronics", "content": "SCRs, Converters, Inverters, and Choppers."}
                        ]
                    },
                    {
                        "title": "Control & Automation",
                        "subjects": [
                            {"name": "Control Systems", "content": "State variable analysis, stability, and compensation techniques."},
                            {"name": "Microprocessors & Interfacing", "content": "Architecture and programming for electrical automation."},
                            {"name": "Renewable Energy Sources", "content": "Solar, wind, and hybrid power systems."}
                        ]
                    },
                    {
                        "title": "Industrial Power & Protection",
                        "subjects": [
                            {"name": "Power System Protection", "content": "Relays, circuit breakers, and protection schemes."},
                            {"name": "Utilization of Electrical Energy", "content": "Illumination, traction, and industrial drives."},
                            {"name": "HVDC & FACTs", "content": "High voltage DC transmission and flexible AC transmission systems."}
                        ]
                    }
                ]
            elif is_mech:
                all_themes = [
                    {
                        "title": "Design & Dynamics",
                        "subjects": [
                            {"name": "Design of Machine Elements", "content": "Design of shafts, gears, bearings, and fasteners."},
                            {"name": "Dynamics of Machinery", "content": "Balancing, gyroscopes, and vibration analysis."},
                            {"name": "Kinematics of Machinery", "content": "Links, mechanisms, and cams."}
                        ]
                    },
                    {
                        "title": "Thermal Applications & Fluids",
                        "subjects": [
                            {"name": "Internal Combustion Engines", "content": "SI/CI engines, fuel systems, and emissions."},
                            {"name": "Heat & Mass Transfer", "content": "Conduction, convection, and radiation heat transfer."},
                            {"name": "Fluid Machines & Turbo Machinery", "content": "Pumps, turbines, and compressible flow."}
                        ]
                    },
                    {
                        "title": "Production & Modern Manufacturing",
                        "subjects": [
                            {"name": "Production Planning & Control", "content": "Inventory management, scheduling, and forecasting."},
                            {"name": "CAD/CAM", "content": "Geometric modeling and computer-aided manufacturing."},
                            {"name": "Metrology & Instrumentation", "content": "Measurement techniques and quality control."}
                        ]
                    }
                ]
            elif is_civil_eng:
                 all_themes = [
                    {
                        "title": "Structural Engineering & Analysis",
                        "subjects": [
                            {"name": "Structural Analysis - II", "content": "Matrix methods and indeterminate structures."},
                            {"name": "Design of Concrete Structures", "content": "Limit state design of beams, slabs, and columns."},
                            {"name": "Design of Steel Structures", "content": "Connections, tension/compression members, and plate girders."}
                        ]
                    },
                    {
                        "title": "Water Resources & Geo-Tech",
                        "subjects": [
                            {"name": "Geotechnical Engineering", "content": "Index properties, soil classification, and bearing capacity."},
                            {"name": "Water Resources Engineering", "content": "Hydrology, irrigation systems, and dam design."},
                            {"name": "Environmental Engineering", "content": "Water supply, sewage treatment, and solid waste management."}
                        ]
                    },
                    {
                        "title": "Transportation & Management",
                        "subjects": [
                            {"name": "Transportation Engineering", "content": "Highway design, traffic engineering, and railway basics."},
                            {"name": "Construction Management", "content": "Project planning, PERT/CPM, and resource allocation."},
                            {"name": "Remote Sensing & GIS", "content": "Applications of GIS in civil engineering projects."}
                        ]
                    }
                ]
            elif is_datascience:
                all_themes = [
                    {
                        "title": "Machine Learning & Advanced Analytics",
                        "subjects": [
                            {"name": "Machine Learning", "content": "Supervised learning (Regression, Classification) and Model evaluation."},
                            {"name": "Advanced Statistical Inference", "content": "Bayesian stats, ANOVA, and time-series forecasting."},
                            {"name": "Data Visualization", "content": "Storytelling with data using Tableau or Power BI."}
                        ]
                    },
                    {
                        "title": "Big Data & Deep Learning",
                        "subjects": [
                            {"name": "Big Data Analytics", "content": "Spark, Hadoop, and processing distributed datasets."},
                            {"name": "Introduction to Neural Networks", "content": "Perceptrons, backpropagation, and basic deep learning."},
                            {"name": "NLP & Text Mining", "content": "Sentiment analysis, tokenization, and vector embeddings."}
                        ]
                    },
                    {
                        "title": "Data Engineering & Ethics",
                        "subjects": [
                            {"name": "Data Engineering Pipelines", "content": "Airflow, Kafka, and cloud data architecture."},
                            {"name": "MLOps & Deployment", "content": "Model containerization (Docker) and monitoring."},
                            {"name": "Data Ethics & Privacy", "content": "Privacy-preserving AI, bias, and data regulations (GDPR)."}
                        ]
                    }
                ]
            elif is_aiml:
                all_themes = [
                    {
                        "title": "AI & Advanced Math",
                        "subjects": [
                            {"name": "Artificial Intelligence Fundamentals", "content": "Search algorithms, knowledge representation, and logic."},
                            {"name": "Mathematical Foundations for AI", "content": "Linear algebra, probability, and optimization techniques."},
                            {"name": "Machine Learning", "content": "Supervised, unsupervised, and reinforcement learning."}
                        ]
                    },
                    {
                        "title": "Deep Learning & Neural Networks",
                        "subjects": [
                            {"name": "Neural Networks & Deep Learning", "content": "CNNs, RNNs, and backpropagation mechanics."},
                            {"name": "Computer Vision", "content": "Image processing, object detection, and facial recognition."},
                            {"name": "Natural Language Processing", "content": "Text analysis, sentiment detection, and transformers (GPT)."}
                        ]
                    },
                    {
                        "title": "Scalable AI & Ethics",
                        "subjects": [
                            {"name": "Big Data Analytics", "content": "Processing large datasets using Spark/Hadoop."},
                            {"name": "AI Ethics & Fairness", "content": "Bias detection, transparency, and ethical AI deployment."},
                            {"name": "Cloud Computing for AI", "content": "Deploying models on AWS/Google Cloud."}
                        ]
                    }
                ]
            elif is_iot:
                all_themes = [
                    {
                        "title": "IoT Architecture & Embedded",
                        "subjects": [
                            {"name": "Introduction to IoT", "content": "IoT architecture, protocols (MQTT/CoAP), and ecosystem."},
                            {"name": "Embedded Systems", "content": "Real-time systems, RTOS, and hardware-software co-design."},
                            {"name": "Microcontrollers for IoT", "content": "Arduino, Raspberry Pi, and ESP32 programming."}
                        ]
                    },
                    {
                        "title": "Sensors & Networking",
                        "subjects": [
                            {"name": "Sensor & Actuator Technology", "content": "Types of sensors, signal conditioning, and interfacing."},
                            {"name": "Wireless Sensor Networks", "content": "Zigbee, LoRaWAN, and network topology."},
                            {"name": "IoT Communication Protocols", "content": "HTTP, WebSocket, and low-power networking."}
                        ]
                    },
                    {
                        "title": "Security & Data Analytics",
                        "subjects": [
                            {"name": "IoT Security", "content": "Cryptography, device authentication, and secure boot."},
                            {"name": "IoT Data Analytics", "content": "Edge computing and stream data processing."},
                            {"name": "Cloud for IoT", "content": "Integrating devices with Azure IoT / AWS IoT Core."}
                        ]
                    }
                ]
            elif is_chemical:
                all_themes = [
                    {
                        "title": "Chemical Process Foundations",
                        "subjects": [
                            {"name": "Chemical Reaction Engineering", "content": "Kinetics, reactor design (batch, CSTR, PFR), and catalysis."},
                            {"name": "Chemical Engineering Thermodynamics", "content": "Phase equilibria, solution thermodynamics, and reaction equilibria."},
                            {"name": "Fluid Mechanics for Chemical", "content": "Fluid flow through porous media and non-Newtonian fluids."}
                        ]
                    },
                    {
                        "title": "Heat & Mass Transfer",
                        "subjects": [
                            {"name": "Heat Transfer Operations", "content": "Heat exchangers, evaporators, and radiation."},
                            {"name": "Mass Transfer Operations", "content": "Distillation, absorption, extraction, and drying."},
                            {"name": "Process Dynamics & Control", "content": "Feedback loops, PID controllers, and system stability."}
                        ]
                    },
                    {
                        "title": "Industrial Chemistry & Safety",
                        "subjects": [
                            {"name": "Chemical Process Technology", "content": "Manufacturing of fertilizers, polymers, and petrochemicals."},
                            {"name": "Plant Design & Economics", "content": "Equipment sizing, cost estimation, and profitability."},
                            {"name": "Chemical Process Safety", "content": "Hazards, risk assessment, and environmental regulations."}
                        ]
                    }
                ]
            elif is_aerospace:
                all_themes = [
                    {
                        "title": "Aerodynamics & Structures",
                        "subjects": [
                            {"name": "Aerodynamics - I", "content": "Incompressible flow, airfoils, and wings."},
                            {"name": "Aerospace Structures", "content": "Stress/strain in thin-walled structures and composite materials."},
                            {"name": "Aircraft Performance", "content": "Take-off, landing, and cruising flight analysis."}
                        ]
                    },
                    {
                        "title": "Propulsion & Control",
                        "subjects": [
                            {"name": "Aircraft Propulsion", "content": "Gas turbines, jet engines, and propellers."},
                            {"name": "Flight Mechanics", "content": "Static and dynamic stability of aircraft."},
                            {"name": "Avionics & Navigation", "content": "Radar systems, flight instruments, and GPS."}
                        ]
                    },
                    {
                        "title": "Space & Advanced Propulsion",
                        "subjects": [
                            {"name": "Rocket Propulsion", "content": "Solid/Liquid propellants and nozzle design."},
                            {"name": "Orbital Mechanics", "content": "Satellite orbits, interplanetary trajectories, and Kepler's laws."},
                            {"name": "Computational Fluid Dynamics", "content": "Numerical methods for aerodynamic simulation."}
                        ]
                    }
                ]
            else: # Fallback to Advanced Tech/Professional Readiness
                is_generic = True
                all_themes = [
                    {
                        "title": "Advanced Technical Readiness",
                        "subjects": [
                            {"name": "Modern Professional Scenarios", "content": "Case studies and real-world problem solving for senior roles."},
                            {"name": "System Architecture Principles", "content": "High-level overview of how complex systems are designed."},
                            {"name": "Advanced Workflow Management", "content": "Agile, SDLC, and modern project management techniques."}
                        ]
                    },
                    {
                        "title": "Specialization & Emerging Tech",
                        "subjects": [
                            {"name": "AI & Machine Learning", "content": "Neural networks, Supervised/Unsupervised learning, and Model evaluation."},
                            {"name": "Cloud Computing & DevOps", "content": "Virtualization, AWS/Azure, and CI/CD pipelines."},
                            {"name": "Cyber Security Foundations", "content": "Cryptography, Network security, and Secure coding practices."}
                        ]
                    },
                    {
                        "title": "Project Management & Industry Standards",
                        "subjects": [
                            {"name": "System Design", "content": "Designing scalable systems, microservices, and load balancing."},
                            {"name": "Product Management Basics", "content": "Requirements gathering, user stories, and roadmap planning."},
                            {"name": "Professional Ethics & Communication", "content": "Workplace etiquette, presentation skills, and ethical hacking basics."}
                        ]
                    }
                ]
        elif is_mtech:
            if is_ece:
                all_themes = [
                    {
                        "title": "Advanced VLSI & Embedded R&D",
                        "subjects": [
                            {"name": "Advanced CMOS Design", "content": "Nanoscale device modeling, leakage power, and variability-aware design."},
                            {"name": "RTOS & Embedded Software", "content": "Real-time scheduling, kernel optimization, and device drivers."},
                            {"name": "Mixed Signal Design", "content": "ADC/DAC architectures and high-speed analog-digital layout."}
                        ]
                    },
                    {
                        "title": "5G Communications & Optical Networks",
                        "subjects": [
                            {"name": "MIMO & 5G Systems", "content": "Beamforming, massive MIMO, and OFDM concepts for M.Tech."},
                            {"name": "Photonic Integrated Circuits", "content": "WDM, optical switches, and silicon photonics foundations."},
                            {"name": "Information Theory & Coding", "content": "Entropy, Channel capacity, and modern error correction codes (LDPC)."}
                        ]
                    }
                ]
            elif is_eee:
                all_themes = [
                    {
                        "title": "Advanced Power Systems & Smart Grids",
                        "subjects": [
                            {"name": "Power System Dynamics", "content": "Large scale stability, transient studies, and swing equations."},
                            {"name": "HVDC & FACTs Control", "content": "Controlling power flow using high-power semiconductor converters."},
                            {"name": "Smart Grid Technologies", "content": "PMU integration, microgrids, and demand-side management."}
                        ]
                    },
                    {
                        "title": "Industrial Automation & Electric Vehicles",
                        "subjects": [
                            {"name": "Advanced Control Theory", "content": "Non-linear control and state-space estimation techniques."},
                            {"name": "EV Powertrain & Battery", "content": "Motor drives, BMS design, and charging infrastructure."},
                            {"name": "Digtial Signal Processors for Power", "content": "FPGA/DSP control for industrial machinery."}
                        ]
                    }
                ]
            elif is_mech:
                all_themes = [
                    {
                        "title": "Precision Manufacturing & Robotics",
                        "subjects": [
                            {"name": "Advanced Robotics", "content": "Kinematics, trajectory planning, and robot vision systems."},
                            {"name": "Additive Manufacturing (3D Printing)", "content": "Metal/Polymer printing, slicing algorithms, and material properties."},
                            {"name": "Finite Element Analysis (FEA)", "content": "Formulation of stiffness matrices and structural simulation."}
                        ]
                    },
                    {
                        "title": "Sustainable Energy & Design",
                        "subjects": [
                            {"name": "Computational Fluid Dynamics", "content": "Navier-Stokes solutions, meshing, and turbulence modeling."},
                            {"name": "Renewable Energy Research", "content": "Hydrogen fuels, advanced solar-thermal, and wind farm design."},
                            {"name": "CIM & Industry 4.0", "content": "Integrating IoT with manufacturing systems (Digital Twins)."}
                        ]
                    }
                ]
            elif is_civil_eng:
                all_themes = [
                    {
                        "title": "Structural Health & Dynamic Analysis",
                        "subjects": [
                            {"name": "Earthquake Engineering", "content": "Seismic forces, response spectrum, and base isolation."},
                            {"name": "Finite Element Methods in Civil", "content": "Modeling complex foundations and bridge architectures."},
                            {"name": "Advanced Concrete Technology", "content": "High-performance concrete and specialized additives."}
                        ]
                    },
                    {
                        "title": "Smart Cities & Environmental R&D",
                        "subjects": [
                            {"name": "Smart Infrastructure Management", "content": "Using sensors and GIS for urban planning and maintenance."},
                            {"name": "Waste-to-Energy Systems", "content": "Technical and chemical aspects of urban waste management."},
                            {"name": "Water Resources Modeling", "content": "Groundwater simulation and hydrological forecasting."}
                        ]
                    }
                ]
            else: # Fallback for M.Tech CSE/IT
                all_themes = [
                    {
                        "title": "Research Methodology & Advanced Computing",
                        "subjects": [
                            {"name": "Advanced Data Structures & Algorithms", "content": "Advanced tree structures, graph algorithms, and approximation algorithms."},
                            {"name": "Distributed Systems", "content": "Consensus protocols, distributed databases, and fault tolerance."},
                            {"name": "Research Methodology", "content": "Literature survey, experimental design, and thesis writing."}
                        ]
                    },
                    {
                        "title": "Specialized Electives & Industrial R&D",
                        "subjects": [
                            {"name": "Deep Learning & NLP", "content": "Transformer models, computer vision, and advanced neural architectures."},
                            {"name": "Internet of Things (IoT)", "content": "Embedded systems, sensor networks, and IoT security."},
                            {"name": "Big Data Analytics", "content": "Hadoop, Spark, and processing large-scale datasets."}
                        ]
                    }
                ]
        else:
            # Standard Tech roles / Generic Tech (Non-year specific)
            if is_ece:
                all_themes = [
                    {
                        "title": "Core Electronics Foundations",
                        "subjects": [
                            {"name": "Electronic Devices & Digital Circuits", "content": "Semiconductors, Logic gates, and circuit analysis fundamentals."},
                            {"name": "Signals & Communication Basics", "content": "Signals, systems, and modulation principles for ECE."},
                            {"name": "Network Theory", "content": "KVL/KCL, theorems, and steady-state analysis."}
                        ]
                    },
                    {
                        "title": "Advanced Communication & Embedded",
                        "subjects": [
                            {"name": "Digital Communication", "content": "PCM, modulation schemes, and information theory."},
                            {"name": "Microprocessors & Control Systems", "content": "8086/8051 architectures and feedback control systems."},
                            {"name": "VLSI Design & DSP", "content": "CMOS technology and digital signal processing basics."}
                        ]
                    }
                ]
            elif is_eee:
                all_themes = [
                    {
                        "title": "Electrical Power & Machines",
                        "subjects": [
                            {"name": "Electrical Machines", "content": "Generators, motors, and transformers core concepts."},
                            {"name": "Power Systems Analysis", "content": "Transmission, distribution, and fault analysis."},
                            {"name": "Network Theory", "content": "Circuit analysis and electromagnetic field theory."}
                        ]
                    },
                    {
                        "title": "Control Systems & Power Electronics",
                        "subjects": [
                            {"name": "Control Engineering", "content": "Stability analysis and industrial control systems."},
                            {"name": "Power Electronics", "content": "Converters, inverters, and power semiconductor devices."},
                            {"name": "Renewable Energy Basics", "content": "Solar and Wind power integration."}
                        ]
                    }
                ]
            elif is_datascience:
                all_themes = [
                    {
                        "title": "Core Data Science Foundations",
                        "subjects": [
                            {"name": "Python & SQL Mastery", "content": "Advanced data structures in Python and complex SQL queries."},
                            {"name": "Statistics & Analytics", "content": "Applying statistical models to real-world business data."},
                            {"name": "Machine Learning Foundations", "content": "Core algorithms (Linear, Logistic, trees) and evaluation."}
                        ]
                    },
                    {
                        "title": "Advanced Visualization & Big Data",
                        "subjects": [
                            {"name": "Data Visualization", "content": "Building interactive dashboards for stakeholder insights."},
                            {"name": "Big Data Environment", "content": "Managing data at scale with Hadoop/Spark frameworks."},
                            {"name": "Applied AI Techniques", "content": "Introduction to NLP and Computer Vision for business."}
                        ]
                    }
                ]
            elif is_mech:
                all_themes = [
                    {
                        "title": "Thermal & Mechanical Design",
                        "subjects": [
                            {"name": "Thermodynamics & Heat Transfer", "content": "Laws of thermodynamics and heat exchange mechanisms."},
                            {"name": "Design of Machine Elements", "content": "Failure analysis and component design (gears, shafts)."},
                            {"name": "Mechanics of Solids", "content": "Stress-strain analysis and structural dynamics."}
                        ]
                    },
                    {
                        "title": "Fluids & Modern Manufacturing",
                        "subjects": [
                            {"name": "Fluid Mechanics & Machinery", "content": "Bernoulli's principle, pumps, and turbines."},
                            {"name": "CAD/CAM & Production", "content": "Computer-aided design and manufacturing processes."},
                            {"name": "IC Engines & Energy", "content": "Internal combustion engines and sustainable energy."}
                        ]
                    }
                ]
            elif is_civil_eng:
                all_themes = [
                    {
                        "title": "Structural & Civil Foundations",
                        "subjects": [
                            {"name": "Strength of Materials", "content": "Analysis of stresses and strains in civil structures."},
                            {"name": "Concrete & Steel Design", "content": "Designing durable infrastructure using modern standards."},
                            {"name": "Geotechnical Engineering", "content": "Soil mechanics and foundation engineering."}
                        ]
                    },
                    {
                        "title": "Environmental & Water Resources",
                        "subjects": [
                            {"name": "Fluid Mechanics (Civil)", "content": "Open channel flow and peak runoff analysis."},
                            {"name": "Environmental Engineering", "content": "Water treatment and waste management systems."},
                            {"name": "Transportation & Surveying", "content": "Highway design and advanced surveying techniques."}
                        ]
                    }
                ]
            elif is_aiml:
                all_themes = [
                    {
                        "title": "Machine Learning & AI Core",
                        "subjects": [
                            {"name": "Statistical ML & Algorithms", "content": "Supervised learning, Regression, and Trees."},
                            {"name": "Neural Networks & Deep Learning", "content": "Backpropagation, CNNs, and optimization techniques."},
                            {"name": "Math for AI", "content": "Linear Algebra, Probability, and optimization foundations."}
                        ]
                    },
                    {
                        "title": "Applied AI & Data Science",
                        "subjects": [
                            {"name": "Natural Language Processing", "content": "Text mining, sentiment analysis, and LLMs basics."},
                            {"name": "Computer Vision", "content": "Object detection and image recognition pipelines."},
                            {"name": "Reinforcement Learning & Ethics", "content": "Agent-based learning and responsible AI deployment."}
                        ]
                    }
                ]
            elif is_iot:
                all_themes = [
                    {
                        "title": "IoT Systems & Networking",
                        "subjects": [
                            {"name": "IoT Architecture & Protocols", "content": "MQTT, CoAP, and layered IoT structures."},
                            {"name": "Wireless Sensor Networks", "content": "Zigbee, LoRa, and connectivity standards."},
                            {"name": "IoT Security", "content": "Device authentication and network layer security."}
                        ]
                    },
                    {
                        "title": "Embedded & Edge Computing",
                        "subjects": [
                            {"name": "Microcontrollers (ESP32/Ardu)", "content": "Hardware-software interfacing for IoT nodes."},
                            {"name": "RTOS & Real-time Systems", "content": "Managing concurrency in embedded devices."},
                            {"name": "Cloud for IoT Data", "content": "Processing time-series data at scale."}
                        ]
                    }
                ]
            elif is_chemical:
                all_themes = [
                    {
                        "title": "Chemical Process Engineering",
                        "subjects": [
                            {"name": "Reaction Engineering", "content": "Kinetics and reactor design (Batch/Flow)."},
                            {"name": "Mass & Heat Transfer", "content": "Separation processes and heat exchangers."},
                            {"name": "Chemical Thermodynamics", "content": "Phase equilibria and chemical potential."}
                        ]
                    },
                    {
                        "title": "Industrial Operations & Safety",
                        "subjects": [
                            {"name": "Process Dynamics & Control", "content": "Instrumentation and feedback loop management."},
                            {"name": "Chemical Plant Design", "content": "Equipment sizing and safety regulations (HAZOP)."},
                            {"name": "Petrochemical Technology", "content": "Industrial processing of polymers and fuels."}
                        ]
                    }
                ]
            elif is_aerospace:
                all_themes = [
                    {
                        "title": "Aerodynamics & Propulsion",
                        "subjects": [
                            {"name": "Incompressible Aerodynamics", "content": "Airfoils, wings, and lift generation theories."},
                            {"name": "Aircraft & Rocket Propulsion", "content": "Jet engines and propellant-based launch systems."},
                            {"name": "Flight Mechanics", "content": "Static and dynamic stability of aerospace vehicles."}
                        ]
                    },
                    {
                        "title": "Aerospace Structures & Space",
                        "subjects": [
                            {"name": "Structural Analysis (Aero)", "content": "Composite materials and thin-walled structure stress."},
                            {"name": "Orbital Mechanics", "content": "Satellite trajectories and celestial mechanics."},
                            {"name": "Avionics & Control", "content": "Auto-pilot systems and sensor fusion for flight."}
                        ]
                    }
                ]
            elif is_cyber:
                all_themes = [
                    {
                        "title": "Cyber Security Foundations & Networking",
                        "subjects": [
                            {"name": "Network Security & Protocols", "content": "TCP/IP vulnerabilities, Firewalls, VPNs, and IDS/IPS systems."},
                            {"name": "Cryptography Foundations", "content": "Symmetric/Asymmetric encryption, Hashing, and Digital signatures."},
                            {"name": "Ethical Hacking Basics", "content": "Vulnerability assessment, port scanning, and security auditing."}
                        ]
                    },
                    {
                        "title": "Advanced Security & Defense",
                        "subjects": [
                            {"name": "Web Application Security", "content": "OWASP Top 10, SQL injection, XSS, and secure coding practices."},
                            {"name": "Incident Response & Forensics", "content": "Malware analysis, log investigation, and digital evidence recovery."},
                            {"name": "Identity & Access Management", "content": "OAuth, SAML, Multi-factor authentication, and Zero Trust models."}
                        ]
                    }
                ]
            else:
                # Standard CSE Fallback
                all_themes = [
                    {
                        "title": "Core CSE Foundations (OS, DBMS, Data Structures)",
                        "subjects": [
                            {"name": "Operating Systems (OS)", "content": "Memory management, process synchronization, threading, and file systems."},
                            {"name": "Database Management Systems (DBMS)", "content": "SQL vs NoSQL, Indexing, Transaction ACID properties, and Normalization."},
                            {"name": "Data Structures & Big-O", "content": "Arrays, Linked Lists, Stacks, Queues, and time/space complexity analysis."}
                        ]
                    },
                    {
                        "title": f"Advanced Data Structures & {role_raw} Core",
                        "subjects": [
                            {"name": "Advanced Data Structures", "content": "Trees (BST, AVL), Graphs (DFS, BFS), and Hashing strategies."},
                            {"name": f"{role_raw} Core Languages", "content": "Deep dive into language syntax, control structures, and specific best practices for your role."},
                            {"name": "Computer Networks", "content": "TCP/IP, HTTP/HTTPS, DNS, and basic security in modern networking."}
                        ]
                    },
                    {
                        "title": "Frameworks & Applied Development",
                        "subjects": [
                            {"name": "Modern Frameworks", "content": "Component lifecycle, state management (Redux/Context), and routing in modern web/mobile apps."},
                            {"name": "System APIs & Integration", "content": "RESTful services, GraphQL, and integrating third-party APIs."},
                            {"name": "Testing & Debugging", "content": "Unit testing, TDD, and debugging complex distributed systems."}
                        ]
                    },
                    {
                        "title": "System Design & Production Readiness",
                        "subjects": [
                            {"name": "System Design & Scalability", "content": "Designing high-availability systems, microservices, and load balancing."},
                            {"name": "Cloud Deployment & DevOps", "content": "CI/CD pipelines, Docker, and AWS/Azure deployment basics."},
                            {"name": "Security & Best Practices", "content": "OWASP Top 10, authentication patterns, and scalable architecture."}
                        ]
                    }
                ]
    elif is_upsc:
        all_themes = [
            {
                "title": "UPSC Prelims: GS Paper I",
                "subjects": [
                    {"name": "History of India", "content": "Ancient, Medieval, and Modern history with focus on National Movement."},
                    {"name": "Indian and World Geography", "content": "Physical, Social, and Economic geography of India and the world."},
                    {"name": "Indian Polity & Governance", "content": "Constitution, Political System, Panchayati Raj, and Public Policy."}
                ]
            },
            {
                "title": "UPSC Prelims: GS Paper II (CSAT)",
                "subjects": [
                    {"name": "Comprehension & Interpersonal Skills", "content": "Communication skills, logical reasoning, and analytical ability."},
                    {"name": "Decision Making & Problem Solving", "content": "General mental ability and basic numeracy (Class X level)."},
                    {"name": "Data Interpretation", "content": "Charts, graphs, tables, and data sufficiency."}
                ]
            },
            {
                "title": "UPSC Mains: GS I & II Focus",
                "subjects": [
                    {"name": "Indian Heritage & Culture", "content": "Art forms, Literature, and Architecture from ancient to modern times."},
                    {"name": "International Relations", "content": "Bilateral, regional, and global groupings involving India."},
                    {"name": "Social Justice", "content": "Government policies and interventions for development in various sectors."}
                ]
            },
            {
                "title": "UPSC Mains: GS III & IV Focus",
                "subjects": [
                    {"name": "Technology & Economy", "content": "Economic development, Bio-diversity, Environment, and Security."},
                    {"name": "Ethics, Integrity & Aptitude", "content": "Attitude, Emotional Intelligence, and case studies on ethical dilemmas."},
                    {"name": "Disaster Management", "content": "Role of administration in dealing with natural and man-made disasters."}
                ]
            }
        ]
    elif is_appsc or is_tspsc:
        region = "Andhra Pradesh" if is_appsc else "Telangana"
        state_code = "AP" if is_appsc else "TS"
        all_themes = [
            {
                "title": f"{state_code}PSC Group I/II: General Studies",
                "subjects": [
                    {"name": "General Science", "content": "Contemporary developments in Science and Technology and Information Technology."},
                    {"name": "Environmental Issues", "content": "Disaster Management, Prevention and Mitigation Strategies."},
                    {"name": f"Economic & Social Development of India & {region}", "content": "Focus on state-specific policies and socio-economic history."}
                ]
            },
            {
                "title": f"History & Culture of {region}",
                "subjects": [
                    {"name": f"{region} Movement & State Formation", "content": f"Chronological history of {region} and its unique cultural identity." if is_tspsc else "Modern history of AP and bifurcated state challenges."},
                    {"name": "Social & Cultural History of India", "content": "Focus on the influence of regional movements on national history."},
                    {"name": "Regional Geography", "content": f"Physical and economic geography of {region}."}
                ]
            },
            {
                "title": "Indian Constitution & Polity",
                "subjects": [
                    {"name": "Indian Political System", "content": "Focus on federalism and center-state relations."},
                    {"name": "Panchayati Raj & Local Self Govt", "content": "Specific focus on state-level implementation and 73rd/74th amendments."},
                    {"name": "Public Administration", "content": "Role of District Administration and State Secretariat."}
                ]
            }
        ]
    elif is_ssc:
        all_themes = [
            {
                "title": "SSC CGL/CHSL: Tier I Preparation",
                "subjects": [
                    {"name": "General Intelligence & Reasoning", "content": "Analogies, spatial orientation, and critical thinking puzzles."},
                    {"name": "General Awareness", "content": "Scientific research, sports, history, culture, and geography."},
                    {"name": "Quantitative Aptitude", "content": "Computation of whole numbers, decimals, fractions and relationships."}
                ]
            },
            {
                "title": "SSC CGL: Tier II Advanced Quant & English",
                "subjects": [
                    {"name": "Arithmetical Abilities", "content": "Number Systems, Percentage, Ratio & Proportion, Average, and Interest."},
                    {"name": "Algebra & Geometry", "content": "Basic algebraic identities, elementary surds, and geometric problems."},
                    {"name": "English Language & Comprehension", "content": "Grammar, error recognition, fill in the blanks, and synonyms/antonyms."}
                ]
            },
            {
                "title": "SSC CGL: Statistics & Finance (If applicable)",
                "subjects": [
                    {"name": "Statistics for AAO/JSO", "content": "Probability, Statistical Errors, and Sampling distributions."},
                    {"name": "General Studies (Finance & Economics)", "content": "Fundamental principles of Economics and Indian Economy (CAG focus)."},
                    {"name": "Computer Proficiency", "content": "Basics of MS Office, Internet, and operating system shortcuts."}
                ]
            }
        ]
    elif is_creative:
            all_themes = [
                {
                    "title": "Design Fundamentals & Tools",
                    "subjects": [
                        {"name": "Color Theory & Typography", "content": "Mastering color palettes, legibility, and font pairings."},
                        {"name": "Adobe Creative Suite Basics", "content": "Introduction to Photoshop, Illustrator, and InDesign."},
                        {"name": "Composition & Layout", "content": "Grid systems, hierarchy, and balance in visual design."}
                    ]
                },
                {
                    "title": "Digital Assets & Portfolio",
                    "subjects": [
                        {"name": "Vector Illustration", "content": "Creating scalable graphics and logo design principles."},
                        {"name": "Image Editing & Retouching", "content": "Advanced Photoshop techniques for photo manipulation."},
                        {"name": "Portfolio Building", "content": "Curating work and presenting it on platforms like Behance/Dribbble."}
                    ]
                }
            ]
    elif is_business:
            all_themes = [
                {
                    "title": "Business Communication & Marketing",
                    "subjects": [
                        {"name": "Professional Writing", "content": "Email etiquette, report writing, and business proposals."},
                        {"name": "Digital Marketing Foundations", "content": "SEO, SEM, and social media marketing strategies."},
                        {"name": "Sales & Negotiation", "content": "Persuasion techniques and customer relationship management."}
                    ]
                },
                {
                    "title": "Management & Analytics",
                    "subjects": [
                        {"name": "Project Management Basics", "content": "Agile, Scrum, and task management tools like Trello/Jira."},
                        {"name": "Data Analysis for Business", "content": "Excel macros, pivot tables, and basic data visualization."},
                        {"name": "Leadership & Ethics", "content": "Team management and professional workplace behavior."}
                    ]
                }
            ]
    elif is_civil_service:
        all_themes = [
            {
                "title": "Polity & Governance",
                "subjects": [
                    {"name": "Indian Constitution", "content": "Preamble, Fundamental Rights, and Directive Principles of State Policy."},
                    {"name": "Parliamentary System", "content": "Structure and functions of the Union and State Legislatures."},
                    {"name": "Governance & Ethics", "content": "Transparency, accountability, and role of civil services in a democracy."}
                ]
            },
            {
                "title": "History & Culture",
                "subjects": [
                    {"name": "Indian National Movement", "content": "Key phases from 1857 to 1947 and prominent freedom fighters."},
                    {"name": "Ancient & Medieval History", "content": "Social, economic, and cultural developments of major Indian dynasties."},
                    {"name": "Indian Art & Culture", "content": "Architecture, sculpture, and performing arts across different eras."}
                ]
            },
            {
                "title": f"Current Affairs & {role_raw} Ethics",
                "subjects": [
                    {"name": "International Relations", "content": "India's foreign policy and bilateral relations with major world powers."},
                    {"name": "Social Justice & Welfare", "content": "Government schemes for vulnerable sections and social empowerment."},
                    {"name": "Economic Development", "content": "Indian economy, planning, and sustainable development goals."}
                ]
            },
            {
                "title": "Aptitude & Answer Writing",
                "subjects": [
                    {"name": "CSAT Mastery", "content": "Logical reasoning, data interpretation, and comprehension skills."},
                    {"name": "Mains Answer Writing", "content": "Structuring answers, time management, and effective communication."},
                    {"name": "Essay Strategy", "content": "Drafting coherent and impactful essays on contemporary issues."}
                ]
            }
        ]
    elif is_finance_govt:
        all_themes = [
            {
                "title": "Quantitative Aptitude & Basics",
                "subjects": [
                    {"name": "Numerical Ability", "content": "Percentages, Profit & Loss, Ratios, and basic arithmetic for competitive exams."},
                    {"name": "Data Interpretation", "content": "Deciphering charts, graphs, and tables to extract meaningful insights."},
                    {"name": "Speed Math Foundations", "content": "Shortcuts for calculation and number series patterns."}
                ]
            },
            {
                "title": "Reasoning & Banking Awareness",
                "subjects": [
                    {"name": "Logical Reasoning", "content": "Syllogism, Blood Relations, Seating arrangement, and Puzzles."},
                    {"name": "General Awareness", "content": "Current events, Banking terms, and Financial news (RBI, Fiscal policy)."},
                    {"name": "Verbal Reasoning", "content": "Critical thinking and statement-assumption based problems."}
                ]
            },
            {
                "title": "English & Communication",
                "subjects": [
                    {"name": "Reading Comprehension", "content": "Contextual understanding and vocabulary building."},
                    {"name": "Grammar & Error Spotting", "content": "Subject-verb agreement, Tenses, and Prepositions."},
                    {"name": "Sentence Rearrangement", "content": "Coherent paragraph construction and cohesive writing."}
                ]
            },
            {
                "title": "Financial Systems & Management",
                "subjects": [
                    {"name": "Taxation & Budgeting", "content": f"Basics of direct/indirect taxes and national budget highlights for {role_raw}."},
                    {"name": "Digital Banking & Security", "content": "KYC, UPI, and cybersecurity in modern financial transactions."},
                    {"name": "Ethics in Finance", "content": "Maintaining integrity and professional standards in government roles."}
                ]
            }
        ]
    elif is_mbbs:
        all_themes = [
            {
                "title": "Pre-clinical Foundations",
                "subjects": [
                    {"name": "Human Anatomy & Embryology", "content": "Detailed structure of the human body, including head, neck, and neuroanatomy."},
                    {"name": "Human Physiology", "content": "Functional systems of the body: Cardiovascular, Respiratory, and Nervous systems."},
                    {"name": "Medical Biochemistry", "content": "Molecular basis of health and metabolic pathways."}
                ]
            },
            {
                "title": "Para-clinical Insights",
                "subjects": [
                    {"name": "Pathology & Microbiology", "content": "Disease mechanisms and infectious agents affecting human health."},
                    {"name": "Pharmacology & Therapeutics", "content": "Principles of drug action and responsible clinical prescribing."},
                    {"name": "Forensic Medicine & Toxicology", "content": "Medical jurisprudence and toxicological investigations."}
                ]
            },
            {
                "title": "Clinical Specialties - I",
                "subjects": [
                    {"name": "General Medicine", "content": "Systemic diseases diagnosis and non-surgical management."},
                    {"name": "General Surgery", "content": f"Foundations of surgical procedures and perioperative care for {role_raw}."},
                    {"name": "Pediatrics & Neonatology", "content": "Healthcare from infancy through adolescence."}
                ]
            },
            {
                "title": "Clinical Specialties - II & Public Health",
                "subjects": [
                    {"name": "Obstetrics & Gynecology", "content": "Maternal health and reproductive system care."},
                    {"name": "Community Medicine", "content": "Public health strategies and preventive healthcare systems."},
                    {"name": "Specialty Rotations (ENT/Ophthal)", "content": "Foundations of ENT and Ophthalmology care."}
                ]
            }
        ]
    elif is_nursing:
        all_themes = [
            {
                "title": "Nursing Foundations & Anatomy",
                "subjects": [
                    {"name": "Anatomy & Physiology for Nurses", "content": "Structural foundations for patient assessment and care."},
                    {"name": "Nursing Foundations", "content": "Basic principles of patient care, hygiene, and hospital safety."}
                ]
            },
            {
                "title": "Medical-Surgical Nursing",
                "subjects": [
                    {"name": "Adult Health Nursing", "content": "Care for patients with systemic medical and surgical conditions."},
                    {"name": "Nutrition & Dietetics", "content": "Role of diet in patient recovery and health maintenance."}
                ]
            },
            {
                "title": "Specialized Nursing Practice",
                "subjects": [
                    {"name": "Child Health (Pediatric) Nursing", "content": "Patient care strategies specific to infants and children."},
                    {"name": "Mental Health Nursing", "content": "Care and support for psychiatric and psychological disorders."}
                ]
            },
            {
                "title": "Community Health & Pharmacology",
                "subjects": [
                    {"name": "Community Health Nursing", "content": "Role of nurses in public health and primary care settings."},
                    {"name": "Clinical Pharmacology", "content": "Medication administration, side effects, and dosage calculations."}
                ]
            }
        ]
    elif is_pharmacy:
        all_themes = [
            {
                "title": "Pharmaceutical Sciences - I",
                "subjects": [
                    {"name": "Pharmaceutical Chemistry", "content": "Medicinal chemistry and chemical properties of drugs."},
                    {"name": "Anatomy & Physiology", "content": "Biomedical foundations for understanding drug action."}
                ]
            },
            {
                "title": "Dosage Forms & Natural Products",
                "subjects": [
                    {"name": "Pharmaceutics", "content": "Formulation, manufacturing, and dispensing of various dosage forms."},
                    {"name": "Pharmacognosy", "content": "Study of drugs derived from natural and herbal sources."}
                ]
            },
            {
                "title": "Pharmacology & Quality Control",
                "subjects": [
                    {"name": "Human Pharmacology", "content": "Detailed mechanism of drug action on various organ systems."},
                    {"name": "Pharmaceutical Analysis", "content": "Methods for ensuring drug purity, strength, and quality."}
                ]
            },
            {
                "title": "Pharmacy Practice & Research",
                "subjects": [
                    {"name": "Hospital & Clinical Pharmacy", "content": "Management of hospital pharmacy and patient counseling."},
                    {"name": "Clinical Research & Regulatory Affairs", "content": "Drug trials and compliance with safety regulations."}
                ]
            }
        ]
    elif is_physio:
        all_themes = [
            {
                "title": "Musculoskeletal & Biomechanics",
                "subjects": [
                    {"name": "Anatomy & Kinesiology", "content": "Detailed study of bones, joints, and muscle movement."},
                    {"name": "Biomechanics of Human Motion", "content": "Physics of posture, gait, and force distribution in the body."},
                    {"name": "Exercise Therapy Foundations", "content": "Principles of strengthening, stretching, and mobilization."}
                ]
            },
            {
                "title": "Neurological & Cardio-Respiratory PT",
                "subjects": [
                    {"name": "Neuro-Physiotherapy", "content": "Rehabilitation for Stroke, Parkinson's, and Spinal Cord Injuries."},
                    {"name": "Cardiovascular & Pulmonary PT", "content": "Airway clearance techniques and cardiac rehabilitation protocols."},
                    {"name": "Electrotherapy & Modalities", "content": "Use of TENS, IFT, Ultrasound, and Laser in pain management."}
                ]
            }
        ]
    elif is_vet:
        all_themes = [
            {
                "title": "Animal Anatomy & Physiology",
                "subjects": [
                    {"name": "Veterinary Anatomy", "content": "Comparative anatomy of livestock, poultry, and small animals."},
                    {"name": "Animal Physiology", "content": "Metabolic and hormonal systems specific to various species."},
                    {"name": "Animal Nutrition", "content": "Feed formulation and nutritional requirements for health and production."}
                ]
            },
            {
                "title": "Veterinary Medicine & Surgery",
                "subjects": [
                    {"name": "Veterinary Pathology", "content": "Study of animal diseases and diagnostic necropsy."},
                    {"name": "Veterinary Medicine & Pharmacology", "content": "Diagnosis and treatment of infectious and non-infectious diseases."},
                    {"name": "Veterinary Surgery & Radiology", "content": "Foundations of animal anesthesia, soft tissue, and orthopedic surgery."}
                ]
            }
        ]
    elif is_ayush:
        all_themes = [
            {
                "title": "Traditional Foundations & Ayurveda",
                "subjects": [
                    {"name": "Padartha Vijnana", "content": "Metaphysical foundations and philosophy of Ayurveda."},
                    {"name": "Rachana Sharira", "content": "Anatomy from a traditional perspective (Marmas, Srotas)."},
                    {"name": "Kriya Sharira", "content": "Physiology of Doshas, Dhatus, and Malas."}
                ]
            },
            {
                "title": "Herbology & Therapeutics",
                "subjects": [
                    {"name": "Dravyaguna Vijnana", "content": "Study of medicinal plants and their pharmacological actions."},
                    {"name": "Bhaishajya Kalpana", "content": "Traditional pharmaceutical preparations and processing."},
                    {"name": "Kayachikitsa & Panchakarma", "content": "Internal medicine and detox therapies (Vamana, Virechana)."}
                ]
            }
        ]
    elif is_allied_health:
        all_themes = [
            {
                "title": "Diagnostic Foundations",
                "subjects": [
                    {"name": "Medical Imaging Physics", "content": "Principles of X-ray, CT, MRI, and Ultrasound physics."},
                    {"name": "Laboratory Techniques", "content": "Hematology, Biochemistry, and Microbiology automation."},
                    {"name": "Hospital Safety & Sterilization", "content": "Universal precautions and infection control in lab environments."}
                ]
            }
        ]
    elif is_dental:
        all_themes = [
            {
                "title": "Oral Foundations & Materials",
                "subjects": [
                    {"name": "Oral Anatomy & Histology", "content": "Structure and development of teeth and oral tissues."},
                    {"name": "Dental Materials", "content": "Properties and applications of materials used in dentistry."}
                ]
            },
            {
                "title": "Oral Pathology & Microbiology",
                "subjects": [
                    {"name": "General & Oral Pathology", "content": "Disease processes with focus on the oral cavity."},
                    {"name": "Pharmacology & Therapeutics", "content": "Drug action principles relevant to dental practice."}
                ]
            },
            {
                "title": "Clinical Dentistry - I",
                "subjects": [
                    {"name": "Oral & Maxillofacial Surgery", "content": "Surgical procedures involving teeth, jaw, and face."},
                    {"name": "Conservative Dentistry & Endodontics", "content": "Root canal treatments and tooth restoration techniques."}
                ]
            },
            {
                "title": "Clinical Dentistry - II",
                "subjects": [
                    {"name": "Prosthodontics", "content": "Artificial restoration of oral function and aesthetics."},
                    {"name": "Periodontology & Orthodontics", "content": "Care for gums and correction of dental irregularities."}
                ]
            }
        ]
    elif is_medical:
        # Generic medical fallback
        all_themes = [
            {
                "title": "General Medical Foundations",
                "subjects": [
                    {"name": "Basic Anatomy", "content": "Overview of human body systems."},
                    {"name": "First Aid & Emergency", "content": "Basic life support and emergency response."}
                ]
            }
        ]
    elif is_science:
        all_themes = [
            {
                "title": "Advanced Scientific Foundations",
                "subjects": [
                    {"name": "Physics & Chemistry Core", "content": "Advanced principles of matter, energy, and chemical reactions."},
                    {"name": "Research Methodology", "content": "Scientific inquiry, hypothesis testing, and systematic data collection."},
                    {"name": "Mathematical Modeling", "content": "Using math to simulate and predict scientific phenomena."}
                ]
            },
            {
                "title": "Specialized Domain Deep Dive",
                "subjects": [
                    {"name": "Biological Sciences", "content": "Genetics, Cell biology, and Biotechnology foundations."},
                    {"name": "Laboratory Practices", "content": "Safety standards, equipment calibration, and experimental accuracy."},
                    {"name": "Scientific Communication", "content": "Drafting research papers and presenting data to the community."}
                ]
            }
        ]
    elif is_school:
        all_themes = [
            {
                "title": "Foundational Academic Excellence",
                "subjects": [
                    {"name": "Mathematics Concepts", "content": "Algebra, Geometry, and Arithmetic for mental agility."},
                    {"name": "Science Fundamentals", "content": "Basics of Physics, Chemistry, and Biology to build curiosity."},
                    {"name": "Language Skills", "content": "Reading, writing, and vocabulary for effective expression."}
                ]
            },
            {
                "title": "Logic & Mental Ability",
                "subjects": [
                    {"name": "Critical Thinking", "content": "Solving puzzles and developing analytical reasoning skills."},
                    {"name": "Aptitude Basics", "content": "Introduction to pattern recognition and basic problem solving."},
                    {"name": "General Knowledge", "content": "Staying aware of geography, history, and current world events."}
                ]
            }
        ]
    elif is_intermediate:
        all_themes = [
            {
                "title": "Advanced Stream-Specific Study",
                "subjects": [
                    {"name": "Advanced Physics", "content": "Mechanics, Thermodynamics, and Electromagnetism for 11th-12th grade."},
                    {"name": "Advanced Chemistry", "content": "Organic, Inorganic, and Physical Chemistry fundamentals."},
                    {"name": "Mathematics / Biology", "content": "Calculus/Algebra or Human Physiology/Botany depth study."}
                ]
            },
            {
                "title": "Competitive Exam Strategy (JEE/NEET)",
                "subjects": [
                    {"name": "Pattern Recognition", "content": "Mastering objective question solving and time-saving shortcuts."},
                    {"name": "Previous Year Analysis", "content": "Solving PYQs for high-weightage topics."},
                    {"name": "Mock Test Strategy", "content": "Managing exam pressure and negative marking."}
                ]
            }
        ]
    elif is_iti_diploma:
        all_themes = [
            {
                "title": f"Core Technical Trade ({edu})",
                "subjects": [
                    {"name": "Trade Theory", "content": f"Fundamental principles of your specific trade in {edu}."},
                    {"name": "Workshop Calculation", "content": "Applied mathematics and engineering drawing for workshop practice."},
                    {"name": "Safety & Tool Handling", "content": "Industrial safety standards and specialized tool maintenance."}
                ]
            },
            {
                "title": "Applied Engineering & Systems",
                "subjects": [
                    {"name": "Material Science", "content": "Properties and uses of industrial materials (Metals, Polymers)."},
                    {"name": "Electrical & Electronics Basics", "content": "Understanding circuits, wiring, and basic electronic components."},
                    {"name": "Manufacturing Processes", "content": "Machining, welding, and assembly line fundamentals."}
                ]
            }
        ]
    else:
        all_themes = [
            {
                "title": f"Core Principles of {role_raw}",
                "subjects": [
                    {"name": f"{role_raw} Foundations", "content": f"Key theories and industry standards essential for any {role_raw}."},
                    {"name": "Domain Terminology", "content": f"Mastering the specific vocabulary and jargon used by a {role_raw}."}
                ]
            },
            {
                "title": f"Advanced {role_raw} Expertise",
                "subjects": [
                    {"name": "Strategic Analysis", "content": f"Using SWOT and other frameworks specifically for {role_raw} objectives."},
                    {"name": "Technical Toolset", "content": f"Mastering the software and specialized equipment required for a {role_raw}."}
                ]
            }
        ]

    # Flatten all subjects from themes
    all_subjects = []
    for theme in all_themes:
        for sub in theme['subjects']:
            all_subjects.append({
                "theme_title": theme['title'],
                "name": sub['name'],
                "content": sub['content']
            })

    def clean_title(raw_title):
        if "Week " in raw_title and ": " in raw_title:
            return raw_title.split(": ", 1)[1]
        return raw_title

    # Distribute subjects across prep_weeks
    if prep_weeks <= len(all_subjects):
        num_subjects = len(all_subjects)
        base_subs = num_subjects // prep_weeks
        rem_subs = num_subjects % prep_weeks
        
        current_idx = 0
        for i in range(prep_weeks):
            # Give base_subs to each week, and 1 extra for rem_subs weeks
            take = base_subs + (1 if i < rem_subs else 0)
            
            start_idx = current_idx
            end_idx = current_idx + take
            current_idx = end_idx
            
            week_subjects = all_subjects[start_idx:end_idx]
            
            display_title = clean_title(week_subjects[0]['theme_title']) if week_subjects else "General Preparation"
                
            roadmap.append({
                "title": f"Week {i+1}: {display_title}",
                "subjects": [{"name": s['name'], "content": s['content']} for s in week_subjects]
            })
    else:
        # If more weeks than subjects, give 1 subject per week and add Practice/Revision for extras
        for i in range(len(all_subjects)):
            sub = all_subjects[i]
            roadmap.append({
                "title": f"Week {i+1}: {clean_title(sub['theme_title'])}",
                "subjects": [{"name": sub['name'], "content": sub['content']}]
            })
        
        # Add extra weeks
        extra_weeks = prep_weeks - len(all_subjects)
        extra_titles = [
            "Advanced Case Studies & Real-world Scenarios",
            "Comprehensive Revision & Weak Area Focus",
            "Full-length Mock Interviews & Performance Analysis",
            "Final Polish & Behavioral Strategy"
        ]
        for i in range(extra_weeks):
            title = extra_titles[i % len(extra_titles)]
            roadmap.append({
                "title": f"Week {len(all_subjects) + i + 1}: {title}",
                "subjects": [
                    {"name": "Practical Application", "content": "Apply all learned concepts to complex mock scenarios and project work."},
                    {"name": "Revision", "content": "Review core fundamentals and clarify any remaining doubts from previous weeks."},
                    {"name": "Interview Simulation", "content": "Practice high-stakes mock interviews with focus on both technical and behavioral aspects."}
                ]
            })

    # --- 8. Final Assembly & Instructions ---
    if not roadmap and all_themes:
        roadmap = all_themes
    
    # If still no roadmap, or if it's a generic fallback and user asked for something specific
    if not roadmap:
        is_generic = True
        roadmap = [
            {
                "title": "General Career Foundations",
                "subjects": [
                    {"name": "Professional Communication", "content": "Mastering workplace English and interpersonal skills."},
                    {"name": "Digital Literacy", "content": "Essential tools like Excel, Word, and online collaboration."},
                    {"name": "Career Planning", "content": "Setting milestones and understanding industry expectations."}
                ]
            }
        ]
    
    instructions = None
    role_is_placeholder = role_lower in ["", "career search", "job", "fresher", "none"]
    
    if is_generic and not role_is_placeholder:
        instructions = f"We couldn't find a specialized roadmap for '{role_raw}'. To get a better result, try entering a more specific role (e.g., 'Java Developer', 'Civil Engineer', 'IAS') in your profile."

    # Strategy text
    if hours >= 4:
        strategy = f"Intensive ({hours}h/day for {prep_weeks} weeks) - Mastery-Oriented"
    else:
        strategy = f"Steady Progress ({hours}h/day for {prep_weeks} weeks) - Balanced"

    # Role-Specific Tips
    tips = []
    if is_tech:
        tips = ["Maintain GitHub consistency", "Optimize for Big O", "Build production-ready code"]
    elif is_civil_service:
        tips = ["Synthesize current events", "Practice answer writing within word limits", "Conceptual clarity over rote learning"]
    else:
        tips = ["Follow industry trends", "STAR method for interviews", "Strategic networking"]

    return {
        "strategy": strategy,
        "modules": roadmap[:prep_weeks], # Limit to requested duration
        "target_role": role_raw,
        "tips": tips,
        "prep_weeks": prep_weeks,
        "guidance": guidance or f"Career Path for {role_raw}",
        "instructions": instructions,
        "is_ai": False
    }
