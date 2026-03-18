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
        # HR - Easy
        {
            "category": "HR",
            "sub_category": "Behavioral",
            "difficulty": "Easy",
            "question_text": "Tell me about yourself in 2 minutes.",
            "correct_answer": "Professional summary focusing on skills and goals.",
            "hint": "Focus on your background, achievements, and why you are here."
        },
        {
            "category": "HR",
            "sub_category": "Conflict Resolution",
            "difficulty": "Medium",
            "question_text": "How do you handle a disagreement with a direct supervisor?",
            "correct_answer": "Communicate professionally, provide evidence, and seek a collaborative solution.",
            "hint": "Focus on professionalism and the best outcome for the organization."
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
        # Tech - Data Structures
        {
            "category": "Coding",
            "sub_category": "Data Structures",
            "difficulty": "Easy",
            "question_text": "Which data structure follows the Last-In-First-Out (LIFO) principle?",
            "option_a": "Queue", "option_b": "Stack", "option_c": "Linked List", "option_d": "Hash Table",
            "correct_option": "B"
        },
        {
            "category": "Coding",
            "sub_category": "Algorithms",
            "difficulty": "Medium",
            "question_text": "What is the time complexity of a Binary Search on a sorted array?",
            "option_a": "O(n)", "option_b": "O(n log n)", "option_c": "O(log n)", "option_d": "O(1)",
            "correct_option": "C"
        },
        # Tech - Web
        {
            "category": "Coding",
            "sub_category": "Web Dev",
            "difficulty": "Easy",
            "question_text": "Which HTML tag is used to define an internal style sheet?",
            "option_a": "<css>", "option_b": "<script>", "option_c": "<style>", "option_d": "<link>",
            "correct_option": "C"
        },
        {
            "category": "Coding",
            "sub_category": "Javascript",
            "difficulty": "Medium",
            "question_text": "Inside which HTML element do we put the JavaScript?",
            "option_a": "<js>", "option_b": "<javascript>", "option_c": "<scripting>", "option_d": "<script>",
            "correct_option": "D"
        },
        # IAS - Polity
        {
            "category": "IAS",
            "sub_category": "Polity",
            "difficulty": "Easy",
            "question_text": "Who is the ex-officio Chairman of the Rajya Sabha?",
            "option_a": "President of India", "option_b": "Prime Minister", "option_c": "Vice President of India", "option_d": "Speaker of Lok Sabha",
            "correct_option": "C"
        },
        {
            "category": "IAS",
            "sub_category": "Polity",
            "difficulty": "Medium",
            "question_text": "Which Article of the Indian Constitution provides for the Election Commission?",
            "option_a": "Article 324", "option_b": "Article 315", "option_c": "Article 356", "option_d": "Article 280",
            "correct_option": "A"
        },
        # IAS - History
        {
            "category": "IAS",
            "sub_category": "History",
            "difficulty": "Easy",
            "question_text": "The Indus Valley Civilization was primarily located in which modern-day region?",
            "option_a": "South India", "option_b": "Northwest India & Pakistan", "option_c": "Northeast India", "option_d": "Central India",
            "correct_option": "B"
        },
        {
            "category": "IAS",
            "sub_category": "History",
            "difficulty": "Medium",
            "question_text": "The 'Dandi March' was a part of which movement?",
            "option_a": "Non-Cooperation Movement", "option_b": "Quit India Movement", "option_c": "Civil Disobedience Movement", "option_d": "Swadeshi Movement",
            "correct_option": "C"
        },
        # Professional
        {
            "category": "Professional",
            "sub_category": "Soft Skills",
            "difficulty": "Easy",
            "question_text": "What does the 'S' stand for in the SMART goals framework?",
            "option_a": "Sustainable", "option_b": "Strategic", "option_c": "Specific", "option_d": "Scalable",
            "correct_option": "C"
        },
        {
            "category": "Professional",
            "sub_category": "Leadership",
            "difficulty": "Medium",
            "question_text": "Which leadership style involves including team members in the decision-making process?",
            "option_a": "Autocratic", "option_b": "Laissez-faire", "option_c": "Democratic", "option_d": "Bureaucratic",
            "correct_option": "C"
        }
    ]

    with app.app_context():
        # Clear existing
        db.session.query(QuizQuestion).delete()
        for q_data in mcqs:
            q = QuizQuestion(**q_data)
            db.session.add(q)
        db.session.commit()
        print("Quiz questions seeded.")

if __name__ == "__main__":
    seed_questions()
    seed_quizzes()
