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
    tech_keywords = ['engineer', 'developer', 'coding', 'ai', 'data', 'software', 'tech', 'programmer', 'web', 'frontend', 'backend', 'fullstack', 'devops', 'stack', 'cloud', 'security', 'machine learning', 'data science']
    civil_service_keywords = ['ias', 'civil service', 'upsc', 'mro', 'revenue officer', 'tpsc', 'appsc', 'group 1', 'group 2', 'constable', 'sub-inspector', 'panchayat', 'administrative', 'ips', 'ifs', 'collector']
    finance_govt_keywords = ['income tax', 'tax', 'ssc', 'cgl', 'banking', 'bank', 'po', 'clerk', 'finance', 'audit', 'lic', 'rbi', 'ibps', 'accountant', 'budget', 'revenue']
    medical_keywords = ['medical', 'doctor', 'nurse', 'pharmacy', 'healthcare', 'dentist', 'physician', 'surgeon', 'clinic', 'cardiology', 'neurology', 'orthopedic', 'physiotherapy', 'veterinary', 'radiology', 'psychiatry', 'dermatology', 'urology', 'nephrology', 'pulmonology', 'ophthalmology', 'ayurveda', 'homeopathy', 'public health']
    science_keywords = ['science', 'research', 'physics', 'chemistry', 'biology', 'scientist', 'laboratory', 'biotech']

    # Detailed Medical Role Flags
    is_mbbs = any(kw in role_lower for kw in ['mbbs', 'doctor', 'physician', 'surgeon', 'medical officer', 'cardiologist', 'neurologist', 'orthopedic surgeon', 'pediatrician', 'gynecologist', 'dermatologist', 'psychiatrist', 'radiologist', 'urologist', 'nephrologist', 'pulmonologist'])
    is_nursing = any(kw in role_lower for kw in ['nurse', 'nursing', 'anm', 'gnm', 'midwifery'])
    is_pharmacy = any(kw in role_lower for kw in ['pharmacist', 'pharmacy', 'b.pharm', 'm.pharm', 'druggist'])
    is_dental = any(kw in role_lower for kw in ['dentist', 'dental', 'bds', 'mds', 'orthodontist', 'periodontist'])
    is_physio = any(kw in role_lower for kw in ['physiotherapy', 'physiotherapist', 'bpt', 'mpt', 'rehabilitation'])
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
    is_civil = any(kw in role_lower for kw in civil_service_keywords)
    is_finance_govt = any(kw in role_lower for kw in finance_govt_keywords)
    
    # Education Level Specific Flags
    is_school = 'School' in edu
    is_intermediate = 'Intermediate' in edu
    is_iti_diploma = 'Diploma' in edu or 'ITI' in edu
    is_btech = 'B.Tech' in edu
    is_mtech = 'M.Tech' in edu
    is_higher_tech = is_btech or is_mtech
    
    # Career Guidance Information
    guidance = None
    if is_school:
        guidance = "Educational Path: Complete your 10th standard first. After 10th, you can choose Intermediate (MPC/BiPC/CEC) for a general path or a Diploma (Polytechnic) for an early technical career."
    elif is_intermediate or is_iti_diploma:
        stage = "Intermediate" if is_intermediate else "Diploma"
        guidance = f"Educational Path: Complete your {stage} successfully. After this, you should pursue B.Tech or a Bachelor's degree in your field of interest for better job opportunities."
    
    print(f"DEBUG ROADMAP: edu={edu}, is_school={is_school}, is_int={is_intermediate}, guidance={guidance}")
    
    # Combine tech role with tech education background
    is_tech = is_role_tech or is_higher_tech
    
    # ITI/Diploma should only be considered "Generic Tech" if no specific role matches and no other category matches
    if not (is_civil or is_finance_govt or is_medical or is_science) and is_iti_diploma:
        if is_role_tech or role_lower in ["", "career search", "job", "fresher"]:
            is_tech = True
    
    # If a specific NON-TECH role is specified, it should override the tech education background
    if is_civil or is_finance_govt or is_medical or is_science:
        is_tech = is_role_tech # Only consider it tech if they explicitly asked for a tech role
    
    # Final Priority: Technical Role > Civil Service > Finance > Medical > Science > School/Inter/Voc/HigherTech

    roadmap = []
    
    # Define potential themes based on ROLE first, then EDUCATION LEVEL
    if is_tech:
        if is_btech and "1st Year" in edu:
            all_themes = [
                {
                    "title": "Engineering Foundations & Programming",
                    "subjects": [
                        {"name": "Engineering Mathematics", "content": "Calculus, Linear Algebra, and Differential Equations for engineering analysis."},
                        {"name": "Programming for Problem Solving", "content": "Basics of C/Python, control structures, and functional thinking."},
                        {"name": "Engineering Physics", "content": "Optics, Electromagnetism, and Quantum basics for technical depth."}
                    ]
                },
                {
                    "title": "Digital Logic & Computer Basics",
                    "subjects": [
                        {"name": "Digital Electronics", "content": "Number systems, Logic gates, and Combinational circuit design."},
                        {"name": "Basic Electrical Engineering", "content": "DC/AC circuits, Transformers, and Power systems foundations."},
                        {"name": "Technical Communication", "content": "Report writing and professional presentation skills."}
                    ]
                }
            ]
        elif is_btech and "2nd Year" in edu:
            all_themes = [
                {
                    "title": "Core Computer Science Foundations",
                    "subjects": [
                        {"name": "Data Structures & Algorithms", "content": "Arrays, Lists, Stacks, Queues, and basic algorithmic complexity."},
                        {"name": "Discrete Mathematics", "content": "Set theory, Graph theory, and Combinatorics for CS logic."},
                        {"name": "Object Oriented Programming (Java/C++)", "content": "Classes, Inheritance, and Polymorphism in real-world design."}
                    ]
                },
                {
                    "title": "Computer Organization & Database Basics",
                    "subjects": [
                        {"name": "Computer Organization & Architecture", "content": "CPU design, Memory hierarchy, and Instruction set architectures."},
                        {"name": "Database Management Systems (Relational)", "content": "SQL, Normalization, and Entity-Relationship modeling."},
                        {"name": "Python for Data Science Basics", "content": "Introduction to NumPy, Pandas, and basic data visualization."}
                    ]
                }
            ]
        elif is_btech and ("3rd Year" in edu or "4th Year" in edu):
             all_themes = [
                {
                    "title": "Advanced Engineering & Professional Readiness",
                    "subjects": [
                        {"name": "Operating Systems & Networking", "content": "Process scheduling, TCP/IP, and Distributed system foundations."},
                        {"name": "Design & Analysis of Algorithms", "content": "Dynamic programming, Greedy algorithms, and NP-completeness."},
                        {"name": "Software Engineering Principles", "content": "SDLC, Design patterns, and Agile methodologies."}
                    ]
                },
                {
                    "title": "Specialization & Emerging Tech",
                    "subjects": [
                        {"name": "AI & Machine Learning", "content": "Neural networks, Supervised/Unsupervised learning, and Model evaluation."},
                        {"name": "Cloud Computing & DevOps", "content": "Virtualization, AWS/Azure, and CI/CD pipelines."},
                        {"name": "Cyber Security Foundations", "content": "Cryptography, Network security, and Secure coding practices."}
                    ]
                }
            ]
        else:
            # Standard Tech roles / Generic Tech
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
                        {"name": "Scalability & Performance", "content": "Horizontal vs Vertical scaling, load balancing, and caching strategies (Redis)."},
                        {"name": "CI/CD & Deployment", "content": "Docker, Kubernetes, and automated deployment pipelines with GitHub Actions/Jenkins."},
                        {"name": "Architecture Patterns", "content": "Microservices vs Monoliths, event-driven design, and API Gateways."}
                    ]
                }
            ]
    elif is_civil:
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

    # Strategy text
    if hours >= 4:
        strategy = f"Intensive ({hours}h/day for {prep_weeks} weeks) - Mastery-Oriented"
    else:
        strategy = f"Steady Progress ({hours}h/day for {prep_weeks} weeks) - Balanced"

    # Role-Specific Tips
    tips = []
    if is_tech:
        tips = ["Maintain GitHub consistency", "Optimize for Big O", "Build production-ready code"]
    elif is_civil:
        tips = ["Synthesize current events", "Practice answer writing within word limits", "Conceptual clarity over rote learning"]
    else:
        tips = ["Follow industry trends", "STAR method for interviews", "Strategic networking"]

    return {
        "strategy": strategy,
        "modules": roadmap,
        "target_role": role_raw,
        "tips": tips,
        "prep_weeks": prep_weeks,
        "guidance": guidance
    }
