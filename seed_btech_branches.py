from app import app
from extensions import db
from models import QuizQuestion, Question

def seed_btech_branches():
    """
    Seeds the database with branch-specific technical content for B.Tech students.
    """
    with app.app_context():
        # --- QUIZ QUESTIONS ---
        branch_quiz = [
            # ECE (Electronics & Communication)
            {"cat": "ECE", "sub": "Digital Electronics", "q": "Which logic gate is known as the 'Universal Gate'?", "a": "AND", "b": "OR", "c": "NAND", "d": "XOR", "ans": "C"},
            {"cat": "ECE", "sub": "Signals & Systems", "q": "What is the Fourier Transform of a unit impulse function?", "a": "0", "b": "1", "c": "Infinity", "d": "Pi", "ans": "B"},
            {"cat": "ECE", "sub": "Communication", "q": "What does PCM stand for in digital communication?", "a": "Pulse Code Modulation", "b": "Phase Control Mode", "c": "Power Circuit Management", "d": "None", "ans": "A"},
            
            # EEE (Electrical & Electronics)
            {"cat": "EEE", "sub": "Electrical Machines", "q": "Which part of a DC machine is used to convert AC to DC?", "a": "Armature", "b": "Stator", "c": "Commutator", "d": "Brushes", "ans": "C"},
            {"cat": "EEE", "sub": "Power Systems", "q": "What is the standard frequency of AC power supply in India?", "a": "60 Hz", "b": "50 Hz", "c": "100 Hz", "d": "120 Hz", "ans": "B"},
            {"cat": "EEE", "sub": "Control Systems", "q": "A system is stable if its poles lie on the _______ of the s-plane.", "a": "Right side", "b": "Left side", "c": "Origin", "d": "Imaginary axis", "ans": "B"},

            # MECH (Mechanical)
            {"cat": "MECH", "sub": "Thermodynamics", "q": "Which law of thermodynamics defines the concept of Entropy?", "a": "Zeroth Law", "b": "First Law", "c": "Second Law", "d": "Third Law", "ans": "C"},
            {"cat": "MECH", "sub": "Fluid Mechanics", "q": "Bernoulli's equation is based on which principle?", "a": "Conservation of Mass", "b": "Conservation of Momentum", "c": "Conservation of Energy", "d": "None", "ans": "C"},
            {"cat": "MECH", "sub": "Machine Design", "q": "The ratio of ultimate stress to working stress is called:", "a": "Poisson's Ratio", "b": "Factor of Safety", "c": "Modulus of Elasticity", "d": "Bulk Modulus", "ans": "B"},

            # CIVIL (Civil)
            {"cat": "CIVIL", "sub": "Building Materials", "q": "What is the main constituent of Portland Cement?", "a": "Silica", "b": "Alumina", "c": "Lime", "d": "Iron Oxide", "ans": "C"},
            {"cat": "CIVIL", "sub": "Structural Analysis", "q": "A beam supported at both ends is called a:", "a": "Cantilever beam", "b": "Simply supported beam", "c": "Fixed beam", "d": "Continuous beam", "ans": "B"},
            {"cat": "CIVIL", "sub": "Surveying", "q": "What is the fundamental principle of surveying?", "a": "Working from part to whole", "b": "Working from whole to part", "c": "Both", "d": "None", "ans": "B"},

            # CHEMICAL (Chemical)
            {"cat": "CHEMICAL", "sub": "Reaction Engineering", "q": "What does CSTR stand for?", "a": "Continuous Stirred Tank Reactor", "b": "Chemical Storage Tank Reservoir", "c": "Core System Thermal Reactor", "d": "None", "ans": "A"},
            {"cat": "CHEMICAL", "sub": "Thermodynamics", "q": "Gibbs free energy (G) is defined as:", "a": "H + TS", "b": "H - TS", "c": "U + PV", "d": "U - TS", "ans": "B"},

            # AIML (AI & ML)
            {"cat": "AIML", "sub": "Machine Learning", "q": "Which algorithm is commonly used for classification?", "a": "Linear Regression", "b": "K-Means", "c": "Support Vector Machine (SVM)", "d": "PCA", "ans": "C"},
            {"cat": "AIML", "sub": "Neural Networks", "q": "What is the purpose of an activation function in a neural network?", "a": "To initialize weights", "b": "To introduce non-linearity", "c": "To reduce data size", "d": "None", "ans": "B"},
            
            # IOT (Internet of Things)
            {"cat": "IOT", "sub": "Communication", "q": "Which protocol is most commonly used in IoT for lightweight messaging?", "a": "HTTP", "b": "FTP", "c": "MQTT", "d": "SMTP", "ans": "C"},
            {"cat": "IOT", "sub": "Hardware", "q": "What is ESP32 primarily used for in IoT projects?", "a": "Display", "b": "Power generation", "c": "Wi-Fi & Bluetooth connectivity", "d": "Storage", "ans": "C"},

            # AEROSPACE (Aerospace)
            {"cat": "AEROSPACE", "sub": "Aerodynamics", "q": "The force that opposes the motion of an aircraft through the air is:", "a": "Lift", "b": "Weight", "c": "Thrust", "d": "Drag", "ans": "D"},
            {"cat": "AEROSPACE", "sub": "Propulsion", "q": "Which cycle is used in gas turbine engines?", "a": "Otto cycle", "b": "Diesel cycle", "c": "Brayton cycle", "d": "Rankine cycle", "ans": "C"}
        ]

        # --- INTERVIEW QUESTIONS ---
        branch_interview = [
            # ECE
            {"cat": "ECE", "sub": "VLSI", "diff": "Medium", "q": "What is the difference between FPGA and ASIC?", "ans": "FPGA is programmable and reconfigurable; ASIC is custom-designed for a specific task and cannot be changed after manufacture."},
            {"cat": "ECE", "sub": "Embedded Systems", "diff": "Medium", "q": "Explain the concept of an Interrupt in microcontrollers.", "ans": "An interrupt is a signal to the processor emitted by hardware or software indicating an event that needs immediate attention."},
            
            # EEE
            {"cat": "EEE", "sub": "Power Electronics", "diff": "Hard", "q": "What is the role of a Snubber circuit?", "ans": "A snubber circuit is used to suppress voltage spikes and limit the rate of change of voltage or current across a switching device."},
            {"cat": "EEE", "sub": "Machines", "diff": "Medium", "q": "Why is a transformer rated in kVA instead of kW?", "ans": "Because losses in a transformer depend on voltage and current independently of the power factor."},

            # MECH
            {"cat": "MECH", "sub": "Manufacturing", "diff": "Medium", "q": "What is the difference between TIG and MIG welding?", "ans": "TIG uses a non-consumable tungsten electrode and a separate filler rod; MIG uses a consumable wire electrode fed from a spool."},
            {"cat": "MECH", "sub": "Thermodynamics", "diff": "Hard", "q": "Explain the significance of the Carnot cycle.", "ans": "It provides the maximum theoretical efficiency that any heat engine can achieve operating between two temperatures."},

            # CIVIL
            {"cat": "CIVIL", "sub": "Geotechnical", "diff": "Hard", "q": "What is Consolidation in soil mechanics?", "ans": "Consolidation is the process by which soil decreases in volume due to the expulsion of water from voids under a long-term load."},
            {"cat": "CIVIL", "sub": "Structures", "diff": "Medium", "q": "What is the purpose of providing reinforcement in concrete?", "ans": "Concrete is strong in compression but weak in tension; steel reinforcement handles the tensile loads."},

            # CHEMICAL
            {"cat": "CHEMICAL", "sub": "Mass Transfer", "diff": "Hard", "q": "Explain the concept of Reflux Ratio in distillation.", "ans": "It is the ratio of the liquid returned to the column to the liquid removed as distillate; higher reflux improves separation but increases cost."},

            # AIML
            {"cat": "AIML", "sub": "Deep Learning", "diff": "Hard", "q": "What is the Vanishing Gradient problem?", "ans": "It occurs when the gradients of the loss function approach zero, making it difficult for the network to learn weights in early layers during backpropagation."},

            # IOT
            {"cat": "IOT", "sub": "Architecture", "diff": "Medium", "q": "Explain the difference between Edge Computing and Cloud Computing in IoT.", "ans": "Edge computing processes data locally near the source; cloud computing sends data to centralized servers for processing and storage."},
            
            # AEROSPACE
            {"cat": "AEROSPACE", "sub": "Structures", "diff": "Hard", "q": "What is Aeroelasticity?", "ans": "The study of the interaction between aerodynamic forces, elastic forces of the structure, and inertial forces."}
        ]

        # Add Quiz Questions
        seeded_quiz_count = 0
        for item in branch_quiz:
            q = QuizQuestion(
                category=item['cat'],
                sub_category=item['sub'],
                week_number=1, # Default to week 1 for general branch knowledge
                difficulty="Medium",
                question_text=item['q'],
                option_a=item['a'], option_b=item['b'], option_c=item['c'], option_d=item['d'],
                correct_option=item['ans']
            )
            # Check if exists to avoid duplicates
            exists = QuizQuestion.query.filter_by(question_text=item['q']).first()
            if not exists:
                db.session.add(q)
                seeded_quiz_count += 1

        # Add Interview Questions
        seeded_interview_count = 0
        for item in branch_interview:
            qi = Question(
                category=item['cat'],
                sub_category=item['sub'],
                difficulty=item['diff'],
                question_text=item['q'],
                correct_answer=item['ans'],
                hint="Think about the core engineering principles of your branch."
            )
            exists = Question.query.filter_by(question_text=item['q']).first()
            if not exists:
                db.session.add(qi)
                seeded_interview_count += 1

        db.session.commit()
        print(f"Seeded {seeded_quiz_count} branch-specific quiz questions.")
        print(f"Seeded {seeded_interview_count} branch-specific interview questions.")

if __name__ == "__main__":
    seed_btech_branches()
