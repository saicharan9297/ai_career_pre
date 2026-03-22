from app import app
from extensions import db
from models import Question

def seed_questions():
    questions = [
        # Full Stack / Web Development - Easy
        {
            "category": "Coding",
            "sub_category": "Web Development",
            "difficulty": "Easy",
            "question_text": "What does DOM stand for in Web Development?",
            "correct_answer": "Document Object Model",
            "hint": "It defines the logical structure of documents and the way they are accessed and manipulated."
        },
        # Full Stack / Web Development - Medium
        {
            "category": "Coding",
            "sub_category": "Full Stack",
            "difficulty": "Medium",
            "question_text": "Explain the concept of 'State' in a frontend framework like React or Vue.",
            "correct_answer": "An object that holds some information that may change over the lifetime of the component.",
            "hint": "It's what makes the component dynamic and responsive to user input."
        },
        # Full Stack / Web Development - Hard
        {
            "category": "Coding",
            "sub_category": "Full Stack Architecture",
            "difficulty": "Hard",
            "question_text": "What is the difference between Server-Side Rendering (SSR) and Client-Side Rendering (CSR)?",
            "correct_answer": "SSR renders the full page on the server; CSR renders the page in the browser using JavaScript.",
            "hint": "Think about initial load time, SEO, and the role of the client's CPU."
        },
        # Coding - Easy
        {
            "category": "Coding",
            "sub_category": "Arrays",
            "difficulty": "Easy",
            "question_text": "What is the time complexity of accessing an element in an array by its index?",
            "correct_answer": "O(1)",
            "hint": "Think about how memory addressing works for arrays."
        },
        # Coding - Medium
        {
            "category": "Coding",
            "sub_category": "Recursion",
            "difficulty": "Medium",
            "question_text": "Write a function (or describe logic) to find the nth Fibonacci number using recursion.",
            "correct_answer": "f(n) = f(n-1) + f(n-2)",
            "hint": "What are the base cases for f(0) and f(1)?"
        },
        # Coding - Hard
        {
            "category": "Coding",
            "sub_category": "Dynamic Programming",
            "difficulty": "Hard",
            "question_text": "Explain the difference between Memoization and Tabulation in Dynamic Programming.",
            "correct_answer": "Memoization is top-down; Tabulation is bottom-up.",
            "hint": "One uses a recursive approach with caching, the other uses an iterative table."
        },
        # IAS / Civil Services - Easy
        {
            "category": "IAS",
            "sub_category": "Polity",
            "difficulty": "Easy",
            "question_text": "Which Article of the Indian Constitution deals with the 'Right to Equality'?",
            "correct_answer": "Articles 14 to 18",
            "hint": "It is one of the Fundamental Rights."
        },
        {
            "category": "IAS",
            "sub_category": "History",
            "difficulty": "Easy",
            "question_text": "Who was the first Tirthankara of Jainism?",
            "correct_answer": "Rishabhanatha",
            "hint": "He is also known as Adinatha."
        },
        # IAS / Civil Services - Medium
        {
            "category": "IAS",
            "sub_category": "Geography",
            "difficulty": "Medium",
            "question_text": "Explain the phenomenon of 'Western Disturbances' and its impact on Indian agriculture.",
            "correct_answer": "Extratropical storms originating in the Mediterranean region that bring sudden winter rain to the northwestern parts of India.",
            "hint": "It is crucial for the growth of Rabi crops."
        },
        {
            "category": "IAS",
            "sub_category": "Polity",
            "difficulty": "Medium",
            "question_text": "What are the 'Directive Principles of State Policy' (DPSP) and are they legally enforceable?",
            "correct_answer": "Guidelines for the framing of laws by the government; they are non-justiciable (not enforceable by courts).",
            "hint": "Articles 36 to 51 of Part IV."
        },
        {
            "category": "IAS",
            "sub_category": "History",
            "difficulty": "Medium",
            "question_text": "Describe the administrative reforms introduced by Sher Shah Suri.",
            "correct_answer": "Reorganization of the land revenue system, introduction of Rupia, and construction of the Grand Trunk Road.",
            "hint": "He was the founder of the Suri Empire."
        },
        {
            "category": "IAS",
            "sub_category": "History",
            "difficulty": "Medium",
            "question_text": "What was the significance of the 1916 Lucknow Pact in the Indian National Movement?",
            "correct_answer": "An agreement between the Indian National Congress and the Muslim League to pressure the British for self-government.",
            "hint": "It marked the reunion of the moderate and extremist factions of the Congress."
        },
        # IAS / Civil Services - Hard
        {
            "category": "IAS",
            "sub_category": "Ethics",
            "difficulty": "Hard",
            "question_text": "Discus the ethical issues involved in 'Artificial Intelligence' and its impact on human privacy.",
            "correct_answer": "Data misuse, algorithmic bias, loss of human agency, and surveillance concerns.",
            "hint": "Think about the tradeoff between technological progress and fundamental rights."
        },
        {
            "category": "IAS",
            "sub_category": "Economy",
            "difficulty": "Hard",
            "question_text": "What is the 'Fiscal Responsibility and Budget Management (FRBM) Act' and why is it important for India?",
            "correct_answer": "An act to institutionalize financial discipline, reduce fiscal deficit, and improve public funds management.",
            "hint": "It aims for long-term macroeconomic stability."
        },
        # Business/Management - Medium
        {
            "category": "Professional",
            "sub_category": "Management",
            "difficulty": "Medium",
            "question_text": "What is the 'SWOT analysis' used for in organizational planning?",
            "correct_answer": "Identifying Strengths, Weaknesses, Opportunities, and Threats.",
            "hint": "It helps in strategic decision-making by evaluating internal and external factors."
        },
        {
            "category": "Professional",
            "sub_category": "Marketing",
            "difficulty": "Medium",
            "question_text": "Define 'Product Positioning' in a marketing context.",
            "correct_answer": "The process of establishing the image or identity of a product so that consumers perceive it in a certain way.",
            "hint": "It's about how the product sits in the customer's mind relative to competitors."
        },
        # Professional - Hard
        {
            "category": "Professional",
            "sub_category": "Leadership",
            "difficulty": "Hard",
            "question_text": "What is 'Transformational Leadership'?",
            "correct_answer": "A style of leadership where a leader works with teams to identify needed change and creates a vision to guide the change through inspiration.",
            "hint": "It focuses on motivation and positive development of followers."
        },
        # HR Questions
        {
            "category": "HR", "sub_category": "Introduction", "difficulty": "Easy",
            "question_text": "Tell me about yourself and your background.",
            "correct_answer": "Experience, Skills, Passion, Professional summary",
            "hint": "Focus on the 'Past, Present, Future' model."
        },
        {
            "category": "HR", "sub_category": "Behavioral", "difficulty": "Medium",
            "question_text": "What is your greatest professional achievement so far?",
            "correct_answer": "Context, Action, Result, Achievement, Impact",
            "hint": "Use the STAR method to structure your answer."
        },
        {
            "category": "HR", "sub_category": "Situational", "difficulty": "Hard",
            "question_text": "Describe a time you failed. How did you handle it?",
            "correct_answer": "Responsibility, Learning, Growth, Resilience, Solution",
            "hint": "Be honest and focus on the learning outcome."
        },
        {
            "category": "HR", "sub_category": "Behavioral", "difficulty": "Medium",
            "question_text": "Why do you want to work for this company?",
            "correct_answer": "Culture, Mission, Value alignment, Product interest",
            "hint": "Connect your personal values with the company's mission."
        },
        {
            "category": "HR", "sub_category": "Behavioral", "difficulty": "Easy",
            "question_text": "What are your greatest strengths and weaknesses?",
            "correct_answer": "Self-awareness, Improvement, Honesty, Professionalism",
            "hint": "Mention a weakness and how you are actively working to improve it."
        },
        {
            "category": "HR", "sub_category": "Situational", "difficulty": "Medium",
            "question_text": "How do you handle conflict in a team setting?",
            "correct_answer": "Communication, Empathy, Resolution, Professionalism, Collaboration",
            "hint": "Focus on open communication and finding a win-win solution."
        },
        # Additional Tech Questions
        {
            "category": "Coding", "sub_category": "Databases", "difficulty": "Medium",
            "question_text": "What is the difference between a JOIN and a UNION in SQL?",
            "correct_answer": "JOIN combines columns from multiple tables; UNION combines rows from multiple queries.",
            "hint": "Think about horizontal vs vertical combination of data."
        },
        {
            "category": "Coding", "sub_category": "Security", "difficulty": "Hard",
            "question_text": "Explain the concept of Cross-Site Scripting (XSS) and how to prevent it.",
            "correct_answer": "XSS is a vulnerability where malicious scripts are injected into web pages. Prevention includes input sanitization and Content Security Policy.",
            "hint": "It involves trust in the browser and improper handling of user input."
        },
        {
            "category": "Coding", "sub_category": "System Design", "difficulty": "Hard",
            "question_text": "What is Load Balancing and why is it important for high-traffic applications?",
            "correct_answer": "Distributing incoming network traffic across multiple servers. It ensures high availability and reliability. Distribution of traffic, scaling, availability.",
            "hint": "Think about avoiding a single point of failure."
        },
        # Additional Professional/IAS Questions
        {
            "category": "Professional", "sub_category": "Management", "difficulty": "Medium",
            "question_text": "What is the difference between a Manager and a Leader?",
            "correct_answer": "Managers focus on tasks and systems; Leaders focus on people and vision.",
            "hint": "Think about inspiration vs regulation."
        },
        {
            "category": "IAS", "sub_category": "Economy", "difficulty": "Medium",
            "question_text": "What is 'Fiscal Deficit' and why is it a concern for the economy?",
            "correct_answer": "The difference between total revenue and total expenditure of the government. High deficit can lead to inflation and debt.",
            "hint": "It's about the government's borrowing needs."
        },
        {
            "category": "IAS", "sub_category": "Ethics", "difficulty": "Hard",
            "question_text": "What do you understand by 'Crisis of Conscience'?",
            "correct_answer": "A situation where an individual is forced to act against their moral beliefs or values.",
            "hint": "It's a conflict between duty and morality."
        },
        # --- UPSC ---
        {
            "category": "UPSC", "sub_category": "Ethics", "difficulty": "Hard",
            "question_text": "How would you handle a situation where a superior gives you an illegal order?",
            "correct_answer": "Discuss constitutional morality, civil service conduct rules, and ethical courage.",
            "hint": "Think about the Hierarchy vs Rule of Law."
        },
        {
            "category": "UPSC", "sub_category": "International Relations", "difficulty": "Medium",
            "question_text": "Discuss the significance of 'Non-Alignment' in India's current foreign policy.",
            "correct_answer": "Strategic autonomy, multi-alignment, and national interest.",
            "hint": "Think about the Cold War origins vs current multi-polar world."
        },
        # --- Advanced Tech ---
        {
            "category": "Coding", "sub_category": "System Design", "difficulty": "Hard",
            "question_text": "How would you design a URL shortening service like Bitly?",
            "correct_answer": "Discuss hashing, database choice, scalability, and redirection logic.",
            "hint": "Think about how to handle millions of requests."
        },
        {
            "category": "Coding", "sub_category": "AI", "difficulty": "Medium",
            "question_text": "What is the difference between Overfitting and Underfitting in ML?",
            "correct_answer": "Bias vs Variance tradeoff, model complexity, and training error vs test error.",
            "hint": "Think about model generalization."
        }
    ]

    with app.app_context():
        # Clear existing questions to avoid duplicates on re-run
        db.session.query(Question).delete()
        for q in questions:
            new_q = Question(**q)
            db.session.add(new_q)
        db.session.commit()
        print("Database seeded with mock questions.")

def seed_quizzes():
    from models import QuizQuestion
    mcqs = [
        # --- TECH CATEGORY (Coding) ---
        # Week 1: Core CSE Foundations (OS, DBMS, Data Structures)
        {
            "category": "Coding", "sub_category": "OS", "week_number": 1, "difficulty": "Medium",
            "question_text": "What is the main purpose of an Operating System's kernel?",
            "option_a": "To provide a user interface", "option_b": "To manage system resources and communication between hardware and software", "option_c": "To compile source code", "option_d": "To browse the internet",
            "correct_option": "B"
        },
        {
            "category": "Coding", "sub_category": "Databases", "week_number": 1, "difficulty": "Medium",
            "question_text": "In a relational database, what does ACID stand for?",
            "option_a": "Atomicity, Consistency, Isolation, Durability", "option_b": "Access, Control, Identification, Data", "option_c": "Array, Code, Index, Database", "option_d": "Automatic, Centralized, Integrated, Distributed",
            "correct_option": "A"
        },
        {
            "category": "Coding", "sub_category": "Data Structures", "week_number": 1, "difficulty": "Easy",
            "question_text": "Which data structure follows the Last-In-First-Out (LIFO) principle?",
            "option_a": "Queue", "option_b": "Stack", "option_c": "Linked List", "option_d": "Hash Table",
            "correct_option": "B"
        },
        {
            "category": "Coding", "sub_category": "Algorithms", "week_number": 1, "difficulty": "Medium",
            "question_text": "What is the time complexity of a Binary Search on a sorted array?",
            "option_a": "O(n)", "option_b": "O(n log n)", "option_c": "O(log n)", "option_d": "O(1)",
            "correct_option": "C"
        },
        {
            "category": "Coding", "sub_category": "Databases", "week_number": 1, "difficulty": "Medium",
            "question_text": "What is the purpose of an 'Index' in a SQL database?",
            "option_a": "To encrypt data", "option_b": "To improve query performance", "option_c": "To define relationships", "option_d": "To back up data",
            "correct_option": "B"
        },

        # Week 2: Advanced Data Structures & Languages
        {
            "category": "Coding", "sub_category": "Data Structures", "week_number": 2, "difficulty": "Medium",
            "question_text": "What type of data structure is a Binary Search Tree (BST)?",
            "option_a": "Linear", "option_b": "Hierarchical", "option_c": "Matrix", "option_d": "Circular",
            "correct_option": "B"
        },
        {
            "category": "Coding", "sub_category": "Javascript", "week_number": 2, "difficulty": "Medium",
            "question_text": "What is 'Hoisting' in JavaScript?",
            "option_a": "Moving declarations to the top of their scope", "option_b": "Deleting unused variables", "option_c": "Compiling code to machine language", "option_d": "Loading scripts asynchronously",
            "correct_option": "A"
        },
        {
            "category": "Coding", "sub_category": "Git", "week_number": 2, "difficulty": "Easy",
            "question_text": "Which command is used to stage changes in Git?",
            "option_a": "git commit", "option_b": "git push", "option_c": "git add", "option_d": "git save",
            "correct_option": "C"
        },
        {
            "category": "Coding", "sub_category": "Networking", "week_number": 2, "difficulty": "Medium",
            "question_text": "What does HTTP stand for?",
            "option_a": "HyperText Transfer Protocol", "option_b": "High Tech Transfer Program", "option_c": "Home Tool Transfer Process", "option_d": "HyperLink Terminal Type",
            "correct_option": "A"
        },
        {
            "category": "Coding", "sub_category": "Algorithms", "week_number": 2, "difficulty": "High",
            "question_text": "Which sorting algorithm is generally considered the fastest in practice for large datasets?",
            "option_a": "Bubble Sort", "option_b": "Insertion Sort", "option_c": "Quick Sort", "option_d": "Selection Sort",
            "correct_option": "C"
        },

        # Week 3: Frameworks & Applied Development
        {
            "category": "Coding", "sub_category": "React", "week_number": 3, "difficulty": "Medium",
            "question_text": "In React, what are 'Hooks' used for?",
            "option_a": "Styling components", "option_b": "Connecting to external APIs only", "option_c": "Using state and other React features in functional components", "option_d": "Routing",
            "correct_option": "C"
        },
        {
            "category": "Coding", "sub_category": "Databases", "week_number": 3, "difficulty": "Medium",
            "question_text": "What is the purpose of an 'Index' in a SQL database?",
            "option_a": "To encrypt data", "option_b": "To improve query performance", "option_c": "To define relationships", "option_d": "To back up data",
            "correct_option": "B"
        },
        {
            "category": "Coding", "sub_category": "Testing", "week_number": 3, "difficulty": "Medium",
            "question_text": "What does TDD stand for in software development?",
            "option_a": "Total Data Design", "option_b": "Test Document Driven", "option_c": "Test Driven Development", "option_d": "Technical Design Document",
            "correct_option": "C"
        },
        {
            "category": "Coding", "sub_category": "React", "week_number": 3, "difficulty": "Hard",
            "question_text": "What is the use of the 'useEffect' dependency array?",
            "option_a": "To define global variables", "option_b": "To control when the effect function executes", "option_c": "To import local scripts", "option_d": "To manage child components",
            "correct_option": "B"
        },
        {
            "category": "Coding", "sub_category": "Databases", "week_number": 3, "difficulty": "Hard",
            "question_text": "What is the difference between SQL and NoSQL?",
            "option_a": "SQL is only for small data", "option_b": "NoSQL is always faster", "option_c": "SQL uses structured tables; NoSQL uses flexible schemas", "option_d": "SQL is web-only",
            "correct_option": "C"
        },

        # Week 4: System Design & Production
        {
            "category": "Coding", "sub_category": "Docker", "week_number": 4, "difficulty": "Medium",
            "question_text": "What is a major benefit of using Docker containers?",
            "option_a": "Increased hardware speed", "option_b": "Environment consistency across machines", "option_c": "Automatic code writing", "option_d": "Graphical UI design",
            "correct_option": "B"
        },
        {
            "category": "Coding", "sub_category": "Scalability", "week_number": 4, "difficulty": "Hard",
            "question_text": "What is 'Horizontal Scaling'?",
            "option_a": "Adding more RAM to a server", "option_b": "Adding more machines to the pool", "option_c": "Optimizing code loops", "option_d": "Changing the programming language",
            "correct_option": "B"
        },
        {
            "category": "Coding", "sub_category": "Cloud", "week_number": 4, "difficulty": "Easy",
            "question_text": "Which of these is a popular Cloud Computing provider?",
            "option_a": "HTTP", "option_b": "AWS", "option_c": "JSON", "option_d": "SQL",
            "correct_option": "B"
        },
        {
            "category": "Coding", "sub_category": "Deployment", "week_number": 4, "difficulty": "Medium",
            "question_text": "What does CI/CD stand for?",
            "option_a": "Calculated Input/Controlled Output", "option_b": "Continuous Integration/Continuous Deployment", "option_c": "Code Inspection/Code Design", "option_d": "Cloud Integration/Cloud Database",
            "correct_option": "B"
        },
        {
            "category": "Coding", "sub_category": "Architecture", "week_number": 4, "difficulty": "Hard",
            "question_text": "What is a 'Microservices' architecture?",
            "option_a": "One large application managing everything", "option_b": "A small collection of libraries", "option_c": "A system of small, independent services communicating over a network", "option_d": "Code written for microchips",
            "correct_option": "C"
        },

        # --- IAS CATEGORY ---
        # Week 2: History
        {
            "category": "IAS", "sub_category": "History", "week_number": 2, "difficulty": "Easy",
            "question_text": "The Indus Valley Civilization was primarily located in which modern-day region?",
            "option_a": "South India", "option_b": "Northwest India & Pakistan", "option_c": "Northeast India", "option_d": "Central India",
            "correct_option": "B"
        },
        {
            "category": "IAS", "sub_category": "History", "week_number": 2, "difficulty": "Medium",
            "question_text": "The 'Dandi March' was a part of which movement?",
            "option_a": "Non-Cooperation Movement", "option_b": "Quit India Movement", "option_c": "Civil Disobedience Movement", "option_d": "Swadeshi Movement",
            "correct_option": "C"
        },
        {
            "category": "IAS", "sub_category": "History", "week_number": 2, "difficulty": "Easy",
            "question_text": "Who was the founder of the Maurya Empire?",
            "option_a": "Ashoka", "option_b": "Bindusara", "option_c": "Chandragupta Maurya", "option_d": "Bimbisara",
            "correct_option": "C"
        },
        {
            "category": "IAS", "sub_category": "Geography", "week_number": 2, "difficulty": "Medium",
            "question_text": "In which state is the highest peak of South India, Anamudi, located?",
            "option_a": "Tamil Nadu", "option_b": "Karnataka", "option_c": "Kerala", "option_d": "Andhra Pradesh",
            "correct_option": "C"
        },
        {
            "category": "IAS", "sub_category": "History", "week_number": 2, "difficulty": "Medium",
            "question_text": "The First Battle of Panipat (1526) was fought between?",
            "option_a": "Babur and Ibrahim Lodi", "option_b": "Akbar and Hemu", "option_c": "Marathas and Ahmad Shah Abdali", "option_d": "Humayun and Sher Shah Suri",
            "correct_option": "A"
        },

        # Week 1: Polity
        {
            "category": "IAS", "sub_category": "Polity", "week_number": 1, "difficulty": "Easy",
            "question_text": "Who is the ex-officio Chairman of the Rajya Sabha?",
            "option_a": "President of India", "option_b": "Prime Minister", "option_c": "Vice President of India", "option_d": "Speaker of Lok Sabha",
            "correct_option": "C"
        },
        {
            "category": "IAS", "sub_category": "Polity", "week_number": 1, "difficulty": "Medium",
            "question_text": "Which Article of the Indian Constitution provides for the Election Commission?",
            "option_a": "Article 324", "option_b": "Article 315", "option_c": "Article 356", "option_d": "Article 280",
            "correct_option": "A"
        },
        {
            "category": "IAS", "sub_category": "Economy", "week_number": 1, "difficulty": "Medium",
            "question_text": "What is 'Inflation' in an economy?",
            "option_a": "Decrease in price of goods", "option_b": "Increase in purchasing power of money", "option_c": "General increase in prices and fall in purchasing value of money", "option_d": "A stock market crash",
            "correct_option": "C"
        },
        {
            "category": "IAS", "sub_category": "Polity", "week_number": 1, "difficulty": "Easy",
            "question_text": "Which part of the Indian Constitution deals with Fundamental Rights?",
            "option_a": "Part II", "option_b": "Part III", "option_c": "Part IV", "option_d": "Part V",
            "correct_option": "B"
        },
        {
            "category": "IAS", "sub_category": "Economy", "week_number": 1, "difficulty": "Medium",
            "question_text": "Who represents the 'Lender of Last Resort' in India?",
            "option_a": "SBI", "option_b": "Finance Ministry", "option_c": "RBI", "option_d": "NABARD",
            "correct_option": "C"
        },

        # Week 3: Ethics & Tech
        {
            "category": "IAS", "sub_category": "Ethics", "week_number": 3, "difficulty": "Medium",
            "question_text": "What is 'Emotional Intelligence' in administration?",
            "option_a": "Being extremely emotional", "option_b": "Ability to control others using emotions", "option_c": "Understanding and managing one's own and others' emotions effectively", "option_d": "Reading files quickly",
            "correct_option": "C"
        },
        {
            "category": "IAS", "sub_category": "Environment", "week_number": 3, "difficulty": "Easy",
            "question_text": "Where is the headquarters of the International Solar Alliance (ISA) located?",
            "option_a": "Paris", "option_b": "Delhi", "option_c": "Gurugram", "option_d": "Nairobi",
            "correct_option": "C"
        },
        {
            "category": "IAS", "sub_category": "Science", "week_number": 3, "difficulty": "Medium",
            "question_text": "What does a 'Light Year' measure?",
            "option_a": "Time", "option_b": "Speed", "option_c": "Distance", "option_d": "Intensity",
            "correct_option": "C"
        },
        {
            "category": "IAS", "sub_category": "Ethics", "week_number": 3, "difficulty": "Hard",
            "question_text": "What is the core principle of 'Utilitarianism'?",
            "option_a": "Duty for duty's sake", "option_b": "Greatest good for the greatest number", "option_c": "Individual self-interest", "option_d": "Religious law",
            "correct_option": "B"
        },
        {
            "category": "IAS", "sub_category": "Tech", "week_number": 3, "difficulty": "Medium",
            "question_text": "What is a 'Geostationary Orbit'?",
            "option_a": "Orbiting the moon", "option_b": "Staying fixed relative to a point on the rotating Earth", "option_c": "Passing over both poles", "option_d": "Entering the atmosphere",
            "correct_option": "B"
        },

        # Week 4: Current Affairs
        {
            "category": "IAS", "sub_category": "CSAT", "week_number": 4, "difficulty": "Medium",
            "question_text": "If a train 100m long passes a post in 10 seconds, what is its speed?",
            "option_a": "36 km/h", "option_b": "10 km/h", "option_c": "50 km/h", "option_d": "72 km/h",
            "correct_option": "A"
        },
        {
            "category": "IAS", "sub_category": "Current Affairs", "week_number": 4, "difficulty": "Easy",
            "question_text": "What is the primary role of the PIB (Press Information Bureau)?",
            "option_a": "Publishing newspapers", "option_b": "Providing news to international agencies only", "option_c": "Nodal agency of Govt. to disseminate information to media", "option_d": "Regulating social media",
            "correct_option": "C"
        },
        {
            "category": "IAS", "sub_category": "Polity", "week_number": 4, "difficulty": "Medium",
            "question_text": "Which constitutional amendment is known as the 'Mini Constitution'?",
            "option_a": "44th", "option_b": "24th", "option_c": "42nd", "option_d": "73rd",
            "correct_option": "C"
        },
        {
            "category": "IAS", "sub_category": "Revision", "week_number": 4, "difficulty": "Medium",
            "question_text": "What was the main purpose of the Non-Cooperation Movement?",
            "option_a": "To get violent revenge", "option_b": "To achieve Swaraj through non-violent means", "option_c": "To support the British war effort", "option_d": "To establish a monarchy",
            "correct_option": "B"
        },
        {
            "category": "IAS", "sub_category": "Geography", "week_number": 4, "difficulty": "Easy",
            "question_text": "Which latitude passes through the middle of India?",
            "option_a": "Equator", "option_b": "Tropic of Capricorn", "option_c": "Tropic of Cancer", "option_d": "Arctic Circle",
            "correct_option": "C"
        },

        # --- PROFESSIONAL CATEGORY ---
        # Week 1: Soft Skills
        {
            "category": "Professional", "sub_category": "Soft Skills", "week_number": 1, "difficulty": "Easy",
            "question_text": "What does the 'S' stand for in the SMART goals framework?",
            "option_a": "Sustainable", "option_b": "Strategic", "option_c": "Specific", "option_d": "Scalable",
            "correct_option": "C"
        },
        {
            "category": "Professional", "sub_category": "Communication", "week_number": 1, "difficulty": "Medium",
            "question_text": "What is 'Active Listening'?",
            "option_a": "Talking while others speak", "option_b": "Paying full attention and showing you've understood", "option_c": "Hearing background noise", "option_d": "Writing down every single word",
            "correct_option": "B"
        },
        {
            "category": "Professional", "sub_category": "Domain", "week_number": 1, "difficulty": "Easy",
            "question_text": "What is the primary goal of professional networking?",
            "option_a": "Getting free meals", "option_b": "Building mutually beneficial relationships", "option_c": "Collecting business cards only", "option_d": "Avoiding work",
            "correct_option": "B"
        },
        # Week 2: Leadership
        {
            "category": "Professional", "sub_category": "Leadership", "week_number": 2, "difficulty": "Medium",
            "question_text": "Which leadership style involves including team members in the decision-making process?",
            "option_a": "Autocratic", "option_b": "Laissez-faire", "option_c": "Democratic", "option_d": "Bureaucratic",
            "correct_option": "C"
        },
        {
            "category": "Professional", "sub_category": "Management", "week_number": 2, "difficulty": "Medium",
            "question_text": "What is a 'SWOT Analysis'?",
            "option_a": "Software Work Or Training", "option_b": "Strengths, Weaknesses, Opportunities, Threats", "option_c": "Strategic Work On Time", "option_d": "Systematic Weekly Online Test",
            "correct_option": "B"
        },
        # Week 3 & 4 (Expanding)
        {
            "category": "Professional", "sub_category": "Strategy", "week_number": 3, "difficulty": "Hard",
            "question_text": "What is 'Strategic Alignment' in an organization?",
            "option_a": "Putting chairs in a row", "option_b": "Ensuring all departments work towards common organizational goals", "option_c": "Following the competitor's strategy", "option_d": "Hiring only one type of person",
            "correct_option": "B"
        },
        {
            "category": "Professional", "sub_category": "Interviews", "week_number": 4, "difficulty": "Medium",
            "question_text": "What is the 'STAR' method used for in interviews?",
            "option_a": "Rating the interviewer", "option_b": "Situation, Task, Action, Result", "option_c": "Standard Technical Aptitude Review", "option_d": "Strategic Talk And Response",
            "correct_option": "B"
        },
        # --- FINANCE & GOVT ---
        {"category": "Finance/Govt", "sub_category": "Quantitative Aptitude", "week_number": 1, "difficulty": "Medium", "question_text": "A sum of money doubles itself in 8 years at simple interest. What is the rate of interest?", "option_a": "10%", "option_b": "12.5%", "option_c": "15%", "option_d": "8%", "correct_option": "B"},
        {"category": "Finance/Govt", "sub_category": "Quantitative Aptitude", "week_number": 1, "difficulty": "Easy", "question_text": "What is the average of first five prime numbers?", "option_a": "5.6", "option_b": "5.4", "option_c": "5.2", "option_d": "5.0", "correct_option": "A"},
        {"category": "Finance/Govt", "sub_category": "Reasoning", "week_number": 1, "difficulty": "Medium", "question_text": "If 'CLOSET' is coded as 'DMPTFU', how is 'OPEN' coded?", "option_a": "PQFO", "option_b": "PQFO", "option_c": "PQFO", "option_d": "PQFO", "correct_option": "A"},
        {"category": "Finance/Govt", "sub_category": "Core Concepts", "week_number": 1, "difficulty": "Easy", "question_text": "Identify the odd one out: RBI, SEBI, IRDAI, NASA", "option_a": "RBI", "option_b": "SEBI", "option_c": "IRDAI", "option_d": "NASA", "correct_option": "D"},
        {"category": "Finance/Govt", "sub_category": "Aptitude", "week_number": 1, "difficulty": "Medium", "question_text": "Find the next term in the series: 1, 4, 9, 16, ?", "option_a": "20", "option_b": "25", "option_c": "30", "option_d": "36", "correct_option": "B"},
        
        {"category": "Finance/Govt", "sub_category": "Banking", "week_number": 2, "difficulty": "Medium", "question_text": "What is the primary objective of the Monetary Policy Committee (MPC)?", "option_a": "Employment", "option_b": "Price Stability/Inflation Target", "option_c": "Stock regulation", "option_d": "Foreign aid", "correct_option": "B"},
        {"category": "Finance/Govt", "sub_category": "Taxation", "week_number": 2, "difficulty": "Medium", "question_text": "Which schedule of the Indian Constitution contains the three lists (Union, State, Concurrent)?", "option_a": "5th", "option_b": "7th", "option_c": "9th", "option_d": "12th", "correct_option": "B"},
        {"category": "Finance/Govt", "sub_category": "Finance", "week_number": 2, "difficulty": "Easy", "question_text": "What is 'Fiscal Deficit'?", "option_a": "Govt Revenue - Govt Expenditure", "option_b": "Govt Borrowing - Govt Revenue", "option_c": "Govt Expenditure - Govt Revenue (excluding borrowings)", "option_d": "Total Debt", "correct_option": "C"},
        {"category": "Finance/Govt", "sub_category": "Economics", "week_number": 2, "difficulty": "Medium", "question_text": "Which institution releases the 'Economic Survey' in India?", "option_a": "RBI", "option_b": "NITI Aayog", "option_c": "Ministry of Finance", "option_d": "World Bank", "correct_option": "C"},

        {"category": "Finance/Govt", "sub_category": "Financial Awareness", "week_number": 3, "difficulty": "Medium", "question_text": "What does 'Bull Market' signify in the stock exchange?", "option_a": "Falling prices", "option_b": "Stagnant prices", "option_c": "Rising prices", "option_d": "Market crash", "correct_option": "C"},
        {"category": "Finance/Govt", "sub_category": "Banking", "week_number": 3, "difficulty": "Medium", "question_text": "What is the full form of NEFT?", "option_a": "National Electronic Funds Transfer", "option_b": "Net Electronic Financial Terminal", "option_c": "Native Easy Fund Task", "option_d": "None of these", "correct_option": "A"},

        # --- CIVIL SERVICE ---
        {"category": "Civil Service", "sub_category": "Polity", "week_number": 1, "difficulty": "Hard", "question_text": "Which committee recommended the 3-tier Panchayati Raj system?", "option_a": "Ashok Mehta", "option_b": "Balwant Rai Mehta", "option_c": "GVK Rao", "option_d": "LM Singhvi", "correct_option": "B"},
        {"category": "Civil Service", "sub_category": "Polity", "week_number": 1, "difficulty": "Medium", "question_text": "The Tenth Schedule was added by which Amendment?", "option_a": "42nd", "option_b": "44th", "option_c": "52nd", "option_d": "61st", "correct_option": "C"},
        {"category": "Civil Service", "sub_category": "Polity", "week_number": 2, "difficulty": "Medium", "question_text": "Who appoints the Chief Election Commissioner of India?", "option_a": "Prime Minister", "option_b": "CJI", "option_c": "President", "option_d": "Speaker", "correct_option": "C"},
        {"category": "Civil Service", "sub_category": "History", "week_number": 2, "difficulty": "Hard", "question_text": "The battle of Plassey (1757) was fought between Siraj-ud-Daulah and?", "option_a": "Warren Hastings", "option_b": "Robert Clive", "option_c": "Lord Cornwallis", "option_d": "Lord Dalhousie", "correct_option": "B"},
        {"category": "Civil Service", "sub_category": "History", "week_number": 3, "difficulty": "Medium", "question_text": "Who is known as the 'Iron Man of India'?", "option_a": "Nehru", "option_b": "Sardar Patel", "option_c": "Ambedkar", "option_d": "Bose", "correct_option": "B"},
        {"category": "Civil Service", "sub_category": "Polity", "week_number": 3, "difficulty": "Hard", "question_text": "Article 360 deals with which type of emergency?", "option_a": "National", "option_b": "State", "option_c": "Financial", "option_d": "None", "correct_option": "C"},
        {"category": "Civil Service", "sub_category": "History", "week_number": 3, "difficulty": "Medium", "question_text": "Quit India Movement started in which year?", "option_a": "1920", "option_b": "1930", "option_c": "1942", "option_d": "1947", "correct_option": "C"},
        {"category": "Civil Service", "sub_category": "History", "week_number": 4, "difficulty": "Medium", "question_text": "Who was the Viceroy during the Partition of Bengal?", "option_a": "Curzon", "option_b": "Mountbatten", "option_c": "Ripon", "option_d": "Dalhousie", "correct_option": "A"},
        {"category": "Civil Service", "sub_category": "Economy", "week_number": 4, "difficulty": "Medium", "question_text": "Gini Coefficient measures:", "option_a": "Inflation", "option_b": "Inequality", "option_c": "GDP", "option_d": "Debt", "correct_option": "B"},
        {"category": "Civil Service", "sub_category": "Polity", "week_number": 4, "difficulty": "Medium", "question_text": "Fundamental Duties were added by:", "option_a": "42nd Amendment", "option_b": "44th", "option_c": "1st", "option_d": "None", "correct_option": "A"},
        {"category": "Civil Service", "sub_category": "Geography", "week_number": 4, "difficulty": "Easy", "question_text": "Largest delta in the world?", "option_a": "Nile", "option_b": "Sundarbans", "option_c": "Mississippi", "option_d": "Amazon", "correct_option": "B"},
        
        # --- PROFESSIONAL ---
        {"category": "Professional", "sub_category": "Management", "week_number": 1, "difficulty": "Easy", "question_text": "What is the 'Pareto Principle'?", "option_a": "50/50 rule", "option_b": "80/20 rule", "option_c": "100/0 rule", "option_d": "None", "correct_option": "B"},
        {"category": "Professional", "sub_category": "Soft Skills", "week_number": 1, "difficulty": "Medium", "question_text": "What is the primary purpose of a 'Stand-up' meeting?", "option_a": "Long deep discussions", "option_b": "Quick status update & blockers", "option_c": "Coffee break", "option_d": "Managerial review", "correct_option": "B"},
        {"category": "Professional", "sub_category": "Management", "week_number": 2, "difficulty": "Medium", "question_text": "In project management, what does 'CPM' stand for?", "option_a": "Core Path Method", "option_b": "Critical Path Method", "option_c": "Constant Project Mode", "option_d": "None", "correct_option": "B"},
        {"category": "Professional", "sub_category": "Soft Skills", "week_number": 2, "difficulty": "Easy", "question_text": "The ability to understand and share the feelings of another is:", "option_a": "Sympathy", "option_b": "Apathy", "option_c": "Empathy", "option_d": "Antipathy", "correct_option": "C"},
        {"category": "Professional", "sub_category": "Management", "week_number": 3, "difficulty": "Medium", "question_text": "What is 'Scope Creep'?", "option_a": "Expanding project beyond goals", "option_b": "Reducing costs", "option_c": "Hiring new staff", "option_d": "None", "correct_option": "A"},
        {"category": "Professional", "sub_category": "Management", "week_number": 3, "difficulty": "Easy", "question_text": "KPI stands for:", "option_a": "Key Performance Indicator", "option_b": "Knowledge Process Info", "option_c": "Key Plan Item", "option_d": "None", "correct_option": "A"},
        {"category": "Professional", "sub_category": "Management", "week_number": 4, "difficulty": "Hard", "question_text": "Theory X and Theory Y were developed by:", "option_a": "Maslow", "option_b": "McGregor", "option_c": "Herzberg", "option_d": "Drucker", "correct_option": "B"},
        {"category": "Professional", "sub_category": "Management", "week_number": 4, "difficulty": "Hard", "question_text": "What is 'Emotional Intelligence' expert Daniel Goleman's key pillar?", "option_a": "IQ", "option_b": "Self-awareness", "option_c": "Coding", "option_d": "Math", "correct_option": "B"},
        
        {"category": "Finance/Govt", "sub_category": "Financial Awareness", "week_number": 4, "difficulty": "Medium", "question_text": "FDI stands for:", "option_a": "Foreign Direct Investment", "option_b": "Fixed Deposit Info", "option_c": "Fast Data Integration", "option_d": "None", "correct_option": "A"},

        # --- UPSC ---
        {"category": "UPSC", "sub_category": "Polity", "week_number": 1, "difficulty": "Hard", "question_text": "Who is the custodian of the Indian Constitution?", "option_a": "President", "option_b": "Supreme Court", "option_c": "Parliament", "option_d": "Prime Minister", "correct_option": "B"},
        {"category": "UPSC", "sub_category": "History", "week_number": 1, "difficulty": "Hard", "question_text": "The Rowlatt Act was passed in which year?", "option_a": "1917", "option_b": "1918", "option_c": "1919", "option_d": "1920", "correct_option": "C"},
        {"category": "UPSC", "sub_category": "Geography", "week_number": 2, "difficulty": "Medium", "question_text": "Which Indian state has the longest coastline?", "option_a": "Maharashtra", "option_b": "Tamil Nadu", "option_c": "Gujarat", "option_d": "Andhra Pradesh", "correct_option": "C"},
        
        # --- SSC ---
        {"category": "SSC", "sub_category": "Quant", "week_number": 1, "difficulty": "Medium", "question_text": "Find the average of first 50 natural numbers.", "option_a": "25", "option_b": "25.5", "option_c": "26", "option_d": "24.5", "correct_option": "B"},
        {"category": "SSC", "sub_category": "English", "week_number": 1, "difficulty": "Easy", "question_text": "Synonym of 'Abundant'?", "option_a": "Scarce", "option_b": "Plentiful", "option_c": "Rare", "option_d": "Small", "correct_option": "B"},
        
        # --- APPSC / TSPSC ---
        {"category": "APPSC", "sub_category": "State History", "week_number": 1, "difficulty": "Medium", "question_text": "Who was the first Chief Minister of Andhra Pradesh?", "option_a": "T. Prakasam", "option_b": "N. Sanjiva Reddy", "option_c": "P.V. Narasimha Rao", "option_d": "None", "correct_option": "A"},
        {"category": "TSPSC", "sub_category": "State Formation", "week_number": 1, "difficulty": "Hard", "question_text": "In which year was the Telangana state formed?", "option_a": "2012", "option_b": "2013", "option_c": "2014", "option_d": "2015", "correct_option": "C"},
        
        # --- Advanced Tech (B.Tech/M.Tech) ---
        {"category": "Coding", "sub_category": "Cloud", "week_number": 5, "difficulty": "Medium", "question_text": "What is 'SaaS' in Cloud Computing?", "option_a": "Server as a Service", "option_b": "Software as a Service", "option_c": "Storage as a Service", "option_d": "System as a Service", "correct_option": "B"},
        {"category": "Coding", "sub_category": "DevOps", "week_number": 5, "difficulty": "Medium", "question_text": "What does CI/CD stand for?", "option_a": "Continuous Integration / Continuous Delivery", "option_b": "Core Integration / Core Delivery", "option_c": "Code Integration / Code Deployment", "option_d": "None", "correct_option": "A"},
        {"category": "Coding", "sub_category": "AI/ML", "week_number": 6, "difficulty": "Hard", "question_text": "What is the primary goal of Unsupervised Learning?", "option_a": "Predicting labels", "option_b": "Finding hidden patterns/clusters", "option_c": "Optimizing weights", "option_d": "None", "correct_option": "B"}
    ]

    with app.app_context():
        # Clear existing
        db.session.query(QuizQuestion).delete()
        for q_data in mcqs:
            try:
                new_q = QuizQuestion(
                    category=q_data.get('category'),
                    sub_category=q_data.get('sub_category'),
                    week_number=q_data.get('week_number', 1),
                    difficulty=q_data.get('difficulty', 'Medium'),
                    question_text=q_data.get('question_text'),
                    option_a=q_data.get('option_a', 'N/A'),
                    option_b=q_data.get('option_b', 'N/A'),
                    option_c=q_data.get('option_c', 'N/A'),
                    option_d=q_data.get('option_d', 'N/A'),
                    correct_option=q_data.get('correct_option', 'A')
                )
                db.session.add(new_q)
            except Exception as e:
                print(f"FAILED TO SEED: {q_data.get('question_text', 'UNKNOWN')}")
                # Log but continue or handle as needed
        db.session.commit()
        print(f"Seeded {len(mcqs)} quiz questions with multi-week mapping.")

if __name__ == "__main__":
    seed_questions()
    seed_quizzes()
    # Also seed all specialized categories
    try:
        from seed_medical_comprehensive import seed_medical_comprehensive
        seed_medical_comprehensive()
    except ImportError:
        print("Skipping seed_medical_comprehensive (not found)")

    try:
        from seed_educational import seed_educational_data
        seed_educational_data()
    except ImportError:
        print("Skipping seed_educational (not found)")

    try:
        from seed_extra import seed_extra_fields
        seed_extra_fields()
    except ImportError:
        print("Skipping seed_extra (not found)")
    
    try:
        from seed_advanced_content import seed_advanced_content
        seed_advanced_content()
    except ImportError:
        print("Skipping seed_advanced_content (not found)")

    try:
        from seed_btech_branches import seed_btech_branches
        seed_btech_branches()
    except ImportError:
        print("Skipping seed_btech_branches (not found)")
