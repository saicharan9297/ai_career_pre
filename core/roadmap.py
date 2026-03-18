def generate_roadmap(user):
    """
    Generates a personalized roadmap based on user profile and preparation duration.
    """
    role_raw = user.desired_role or "Career Search"
    role_lower = role_raw.lower()
    edu = user.education_level
    try:
        hours = int(user.available_time or 2)
    except (ValueError, TypeError):
        hours = 2
    
    prep_weeks = user.prep_weeks or 1
    
    # Robust Tech Keyword Detection
    tech_keywords = ['engineer', 'developer', 'coding', 'ai', 'data', 'software', 'tech', 'programmer', 'web', 'frontend', 'backend', 'fullstack', 'devops', 'stack', 'cloud', 'security', 'machine learning', 'data science']
    is_tech = any(kw in role_lower for kw in tech_keywords)
    
    roadmap = []
    
    # Define potential themes based on role with specific subjects
    if is_tech:
        all_themes = [
            {
                "title": "Foundations & Computer Science Logic",
                "subjects": [
                    {"name": "Data Structures", "content": "Mastering Arrays, Linked Lists, and Hash Tables. Focus on memory management and time complexity."},
                    {"name": "Algorithm Basics", "content": "Big O notation, Sorting (Merge, Quick), and Searching (Binary)."},
                    {"name": "Logic & Math", "content": "Boolean algebra, bitwise operations, and discrete math fundamentals."}
                ]
            },
            {
                "title": "Core Technology & Language Proficiency",
                "subjects": [
                    {"name": f"{role_raw} Core Languages", "content": "Deep dive into language syntax, control structures, and specific best practices for your role."},
                    {"name": "Git & Version Control", "content": "Branching strategies, merge conflict resolution, and collaborative workflows."},
                    {"name": "System APIs", "content": "Understanding I/O operations, network protocols (HTTP/HTTPS), and basic security."}
                ]
            },
            {
                "title": "Frameworks & Applied Development",
                "subjects": [
                    {"name": "Advanced Frameworks", "content": "Component lifecycle, state management (Redux/Context), and routing in modern web apps."},
                    {"name": "Database Integration", "content": "SQL vs NoSQL, schema design, and high-level ORM usage."},
                    {"name": "Testing Paradigms", "content": "Unit testing, TDD, and integration testing for robust codebases."}
                ]
            },
            {
                "title": "System Design & Production Readiness",
                "subjects": [
                    {"name": "Scalability & Performance", "content": "Horizontal vs Vertical scaling, load balancing, and caching strategies."},
                    {"name": "Architecture Patterns", "content": "Microservices vs Monoliths, event-driven design, and API Gateways."},
                    {"name": "CI/CD & Deployment", "content": "Docker, Kubernetes, and automated deployment pipelines."}
                ]
            }
        ]
    elif "ias" in role_lower or "civil service" in role_lower or "upsc" in role_lower:
        all_themes = [
            {
                "title": "Core Academic Syllabus I: History & Geography",
                "subjects": [
                    {"name": "Ancient & Medieval History", "content": "Comprehensive study of Indus Valley, Vedic Age, Mauryas, Guptas, and Delhi Sultanate. Focus on Art and Culture."},
                    {"name": "Modern Indian History (1757-1947)", "content": "Establishment of British rule, Socio-religious reforms, and the stages of the Indian Freedom Struggle led by INC and others."},
                    {"name": "Indian & World Geography", "content": "Physical, Social, and Economic Geography. Focus on Indian Monsoons, River systems, and Mapping."}
                ]
            },
            {
                "title": "Core Academic Syllabus II: Polity & Economy",
                "subjects": [
                    {"name": "Indian Polity & Governance", "content": "Constitution, Preamble, Fundamental Rights, DPSP, Parliament, and Judiciary. Focus on Laxmikanth's core chapters."},
                    {"name": "Indian Economy Basics", "content": "Macro-economics, National Income, Banking, Inflation, and Budgeting. Focus on Economic Survey and Five-Year Plans."},
                    {"name": "Social Justice & International Relations", "content": "Welfare schemes, poverty, hunger, and India's bilateral/multilateral relations with neighbors and global powers."}
                ]
            },
            {
                "title": "General Studies III & IV: Ethics & Technology",
                "subjects": [
                    {"name": "Ethics, Integrity & Aptitude", "content": "Emotional intelligence, values in administration, and solving foundational ethical case studies."},
                    {"name": "Science, Tech & Environment", "content": "Environment conservation, Biodiversity, Climate Change, and latest developments in Space, Defense, and IT."},
                    {"name": "Internal Security & Disaster Management", "content": "Challenges to internal security, terrorism, money laundering, and disaster management frameworks."}
                ]
            },
            {
                "title": "Current Affairs & Preliminary Revision",
                "subjects": [
                    {"name": "Daily News Analysis", "content": "Synthesizing news from The Hindu/Indian Express with the static syllabus. Focus on PIB summaries."},
                    {"name": "Academic Revision & Mock Prep", "content": "Summarizing NCERTs, practicing previous year questions (PYQs), and mastering GS paper 1/2 interconnections."},
                    {"name": "CSAT & Aptitude", "content": "Logical reasoning, reading comprehension, and basic numeracy for the Preliminary examination."}
                ]
            }
        ]
    else:
        all_themes = [
            {
                "title": "Industry Core Principles",
                "subjects": [
                    {"name": "Domain Foundations", "content": f"Key theories and industry standards for {role_raw}."},
                    {"name": "Professional Terminology", "content": "Commonly used jargon and communication patterns in the field."}
                ]
            },
            {
                "title": "Advanced Domain Expertise",
                "subjects": [
                    {"name": "Management Frameworks", "content": "SWOT, PESTEL, and other strategic analysis tools."},
                    {"name": "Technical Toolset", "content": "Key software and hardware used by industry professionals today."}
                ]
            },
            {
                "title": "Applied Case Studies",
                "subjects": [
                    {"name": "Scenario Analysis", "content": "Solving real-world business or administrative problems from history."},
                    {"name": "Implementation Planning", "content": "Drafting go-to-market strategies or policy proposals."}
                ]
            },
            {
                "title": "Strategic Career Preparation",
                "subjects": [
                    {"name": "Advanced Networking", "content": "Building a targeted professional network and LinkedIn brand."},
                    {"name": "High-Stakes Interviewing", "content": "Mastering behavioral questions and technical demonstrations."}
                ]
            }
        ]

    # Generate weekly modules
    for i in range(prep_weeks):
        # Cycle through themes if weeks > 4
        theme = all_themes[i % len(all_themes)]
        roadmap.append({
            "title": f"Week {i+1}: {theme['title']}",
            "subjects": theme['subjects']
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
    elif "ias" in role_lower or "civil service" in role_lower:
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
