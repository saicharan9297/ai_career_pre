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
    
    prep_weeks = user.prep_weeks or 1
    
    # Robust Role Detection
    tech_keywords = ['engineer', 'developer', 'coding', 'ai', 'data', 'software', 'tech', 'programmer', 'web', 'frontend', 'backend', 'fullstack', 'devops', 'stack', 'cloud', 'security', 'machine learning', 'data science']
    civil_service_keywords = ['ias', 'civil service', 'upsc', 'mro', 'revenue officer', 'tpsc', 'appsc', 'group 1', 'group 2', 'constable', 'sub-inspector', 'panchayat', 'administrative', 'ips', 'ifs', 'collector']
    finance_govt_keywords = ['income tax', 'tax', 'ssc', 'cgl', 'banking', 'bank', 'po', 'clerk', 'finance', 'audit', 'lic', 'rbi', 'ibps', 'accountant', 'budget', 'revenue']
    medical_keywords = ['medical', 'doctor', 'nurse', 'pharmacy', 'healthcare', 'dentist', 'physician', 'surgeon', 'clinic']
    science_keywords = ['science', 'research', 'physics', 'chemistry', 'biology', 'scientist', 'laboratory', 'biotech']
    
    is_tech = any(kw in role_lower for kw in tech_keywords)
    is_civil = any(kw in role_lower for kw in civil_service_keywords)
    is_finance_govt = any(kw in role_lower for kw in finance_govt_keywords)
    is_medical = any(kw in role_lower for kw in medical_keywords)
    is_science = any(kw in role_lower for kw in science_keywords)
    
    # Debug prints (will show in terminal)
    print(f"DEBUG: Generating roadmap for role: '{role_raw}'")
    print(f"DEBUG: Detection Flags - Tech: {is_tech}, Civil: {is_civil}, FinanceGovt: {is_finance_govt}, Medical: {is_medical}, Science: {is_science}")

    roadmap = []
    
    # Define potential themes based on role with specific subjects
    if is_tech:
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
                    {"name": "Indian Polity & Governance", "content": "Constitution, Preamble, Fundamental Rights, DPSP, Parliament, and Judiciary. Focus on Laxmikanth's core chapters."},
                    {"name": "State Administration", "content": "Role of Governor, CM, and State Legislature. Focus on local governance and PRIs."},
                    {"name": "Mandal/Revenue Administration", "content": "Specific duties of MRO, VRO, and land revenue systems in the state context."}
                ]
            },
            {
                "title": "History & Geography",
                "subjects": [
                    {"name": "Modern Indian History (1757-1947)", "content": "Establishment of British rule, Socio-religious reforms, and the stages of the Indian Freedom Struggle led by INC and others."},
                    {"name": "Ancient & Medieval History", "content": "Comprehensive study of Indus Valley, Vedic Age, Mauryas, Guptas, and Delhi Sultanate. Focus on Art and Culture."},
                    {"name": "Indian & World Geography", "content": "Physical, Social, and Economic Geography. Focus on Indian Monsoons, River systems, and Mapping."}
                ]
            },
            {
                "title": "Social Justice & Economy",
                "subjects": [
                    {"name": "Indian Economy Basics", "content": "Macro-economics, National Income, Banking, Inflation, and Budgeting. Focus on Economic Survey and Five-Year Plans."},
                    {"name": "Social Justice & International Relations", "content": "Welfare schemes, poverty, hunger, and India's bilateral/multilateral relations with neighbors and global powers."},
                    {"name": "State Schemes & Geography", "content": "Local welfare schemes, agriculture patterns, and state-specific economic challenges."}
                ]
            },
            {
                "title": "General Studies IV & Current Affairs",
                "subjects": [
                    {"name": "Ethics, Integrity & Aptitude", "content": "Emotional intelligence, values in administration, and solving foundational ethical case studies."},
                    {"name": "Science, Tech & Environment", "content": "Environment conservation, Biodiversity, Climate Change, and latest developments in Space, Defense, and IT."},
                    {"name": "Current Affairs & Preliminary Revision", "content": "Summarizing NCERTs, practicing previous year questions (PYQs), and mastering GS paper interconnections."}
                ]
            }
        ]
    elif is_finance_govt:
        all_themes = [
            {
                "title": "Quantitative Aptitude & Basics",
                "subjects": [
                    {"name": "Numerical Ability", "content": "Percentage, Profit & Loss, Simple/Compound Interest, and Data Interpretation."},
                    {"name": f"Core {role_raw} Concepts", "content": f"Foundational principles and basic regulations relevant to a {role_raw}."},
                    {"name": "Reasoning Ability", "content": "Logical reasoning, puzzles, and analytical thinking for competitive exams."}
                ]
            },
            {
                "title": "General Studies & Polity for Govt Roles",
                "subjects": [
                    {"name": "Indian Polity & Constitution", "content": "Basics of the Indian Constitution, Fundamental Rights, and the structure of Government."},
                    {"name": "History & Culture", "content": "Indian National Movement and significant historical milestones for competitive exams."},
                    {"name": "Geography & Economy", "content": "Physical geography of India and basic macroeconomic indicators (GDP, Inflation)."}
                ]
            },
            {
                "title": "Domain Knowledge & Law",
                "subjects": [
                    {"name": "Financial & Direct/Indirect Tax", "content": "Indian Tax laws, Budgeting, and GST frameworks (if applicable to Tax roles)."},
                    {"name": "Banking & Financial Awareness", "content": "Monetary policy, RBI roles, and banking history for finance aspirants."},
                    {"name": "English & Communication", "content": "Comprehension, grammar, and professional communication skills."}
                ]
            },
            {
                "title": "Final Preparation & Mocks",
                "subjects": [
                    {"name": "Mock Test Series", "content": "Practicing full-length previous year papers and mock tests for speed."},
                    {"name": "Interview & GD Prep", "content": "Mastering Group Discussions and personal interviews for final selection."},
                    {"name": "Current Affairs", "content": "Latest news, awards, and sports for a well-rounded competitive edge."}
                ]
            }
        ]
    elif is_medical:
        all_themes = [
            {
                "title": "Human Anatomy & Physiology",
                "subjects": [
                    {"name": "Skeletal & Muscular Systems", "content": "Comprehensive study of human bone structure and muscle groups."},
                    {"name": "Organ Systems", "content": "Detailed overview of Cardiovascular, Respiratory, and Digestive systems."},
                    {"name": "Physiological Processes", "content": "Metabolism, homeostasis, and neural communication basics."}
                ]
            },
            {
                "title": "Pharmacology & Patient Care",
                "subjects": [
                    {"name": "Drug Classifications", "content": "Understanding antibiotics, analgesics, and common specialist medications."},
                    {"name": "Clinical Procedures", "content": "Standard operating procedures for patient assessment and emergency care."},
                    {"name": "Medical Ethics", "content": "HIPAA compliance, patient confidentiality, and bioethical decision-making."}
                ]
            },
            {
                "title": "Specialized Medicine & Diagnostics",
                "subjects": [
                    {"name": "Diagnostic Tools", "content": "Interpreting X-rays, MRIs, and blood panel results accurately."},
                    {"name": "Pathology Basics", "content": "Study of disease mechanisms and common infection pathways."},
                    {"name": "Surgical/Clinical Support", "content": "Pre-operative and post-operative care protocols."}
                ]
            },
            {
                "title": "Health Administration & Public Health",
                "subjects": [
                    {"name": "Healthcare Policy", "content": "Insurance systems, public health initiatives, and global health trends."},
                    {"name": "Epidemiology", "content": "Tracking disease outbreaks and implementing community wellness programs."},
                    {"name": "Advanced Medical Research", "content": "Reviewing latest clinical trials and evidence-based practice updates."}
                ]
            }
        ]
    elif is_science:
        all_themes = [
            {
                "title": "Fundamentals of Physics & Chemistry",
                "subjects": [
                    {"name": "Classical Mechanics", "content": "Laws of motion, energy conservation, and fluid dynamics."},
                    {"name": "Molecular Bonding", "content": "Periodic table trends, ionic/covalent bonds, and stoichiometry."},
                    {"name": "Thermodynamics", "content": "Heat transfer, entropy, and laws of thermodynamics in research."}
                ]
            },
            {
                "title": "Biological Sciences & Genetics",
                "subjects": [
                    {"name": "Cellular Biology", "content": "Structure of eukaryotic/prokaryotic cells and metabolic pathways."},
                    {"name": "Genetics & Inheritance", "content": "Mendelian genetics, DNA replication, and CRISPR technology basics."},
                    {"name": "Microbiology", "content": "Familiarity with bacteria, viruses, and fungi in a research context."}
                ]
            },
            {
                "title": "Advanced Scientific Methodology",
                "subjects": [
                    {"name": "Data Analysis (R/Python)", "content": "Statistical modeling and visualizing research data sets."},
                    {"name": "Experimental Design", "content": "Formulating hypotheses and controlling variables in laboratory settings."},
                    {"name": "Peer Review & Publishing", "content": "Drafting scientific papers and understanding the impact factor system."}
                ]
            },
            {
                "title": "Interdisciplinary Science & Tech",
                "subjects": [
                    {"name": "Quantum Mechanics Basics", "content": "Introduction to wave-particle duality and uncertainty principles."},
                    {"name": "Environmental Science", "content": "Ecosystem dynamics, climate modeling, and sustainability research."},
                    {"name": "Bio-Technology Applications", "content": "Lab-on-a-chip, synthetic biology, and pharmaceutical R&D."}
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
            },
            {
                "title": f"Real-world {role_raw} Scenarios",
                "subjects": [
                    {"name": "Case Study Solvers", "content": f"Analyzing and solving historical problems faced by a {role_raw}."},
                    {"name": "Project Implementation", "content": f"Drafting professional proposals and execution plans as a {role_raw}."}
                ]
            },
            {
                "title": "Strategic Career Success",
                "subjects": [
                    {"name": "Targeted Networking", "content": f"Building a professional network and personal brand as a {role_raw}."},
                    {"name": "High-Stakes Interviews", "content": f"Practicing behavioral and technical interview questions for {role_raw} roles."}
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
        "prep_weeks": prep_weeks
    }
