from app import create_app
from models import QuizQuestion, Question, db

def seed_branch_content():
    app = create_app()
    with app.app_context():
        # Clear existing low-count branch questions to avoid duplicates/mess
        # Actually, let's just add new ones. 
        
        branch_quiz_data = [
            # --- ECE ---
            {"cat": "ECE", "week": 1, "sub": "Electronic Devices", "q": "What is the majority carrier in a p-type semiconductor?", "oa": "Electrons", "ob": "Holes", "oc": "Neutrons", "od": "Protons", "ans": "B"},
            {"cat": "ECE", "week": 1, "sub": "Digital Circuits", "q": "Which gate is known as a Universal Gate?", "oa": "AND", "ob": "OR", "oc": "NAND", "od": "XOR", "ans": "C"},
            {"cat": "ECE", "week": 1, "sub": "Network Theory", "q": "In a series RLC circuit at resonance, the impedance is:", "oa": "Maximum", "ob": "Minimum", "oc": "Zero", "od": "Infinite", "ans": "B"},
            {"cat": "ECE", "week": 1, "sub": "Electronic Devices", "q": "A Zener diode is always used in which bias?", "oa": "Forward", "ob": "Reverse", "oc": "Zero", "od": "Both", "ans": "B"},
            {"cat": "ECE", "week": 1, "sub": "Digital Circuits", "q": "How many select lines are needed for a 8:1 Multiplexer?", "oa": "2", "ob": "3", "oc": "4", "od": "8", "ans": "B"},

            {"cat": "ECE", "week": 2, "sub": "Analog Circuits", "q": "What is the ideal input impedance of an Op-Amp?", "oa": "Zero", "ob": "Low", "oc": "High", "od": "Infinite", "ans": "D"},
            {"cat": "ECE", "week": 2, "sub": "Signals & Systems", "q": "A system is causal if its output depends on:", "oa": "Future inputs", "ob": "Past/Present inputs", "oc": "Only future", "od": "None", "ans": "B"},
            {"cat": "ECE", "week": 2, "sub": "Electromagnetics", "q": "Which Maxwell equation represents Gauss Law for Magnetism?", "oa": "div D = rho", "ob": "div B = 0", "oc": "curl E = -dB/dt", "od": "curl H = J", "ans": "B"},
            {"cat": "ECE", "week": 2, "sub": "Analog Circuits", "q": "Barkhausen criterion is related to:", "oa": "Amplifiers", "ob": "Oscillators", "oc": "Rectifiers", "od": "Filters", "ans": "B"},
            {"cat": "ECE", "week": 2, "sub": "Signals & Systems", "q": "The Fourier Transform of a Dirac Delta function is:", "oa": "1", "ob": "0", "oc": "Delta", "od": "Infinity", "ans": "A"},

            {"cat": "ECE", "week": 3, "sub": "Microprocessors", "q": "Which is an 8-bit microprocessor?", "oa": "8086", "ob": "8085", "oc": "80286", "od": "80386", "ans": "B"},
            {"cat": "ECE", "week": 3, "sub": "Control Systems", "q": "A system is stable if the poles lie on the:", "oa": "Right half of s-plane", "ob": "Left half of s-plane", "oc": "Imaginary axis", "od": "Origin", "ans": "B"},
            {"cat": "ECE", "week": 3, "sub": "Digital Communication", "q": "Which modulation is more robust to noise?", "oa": "AM", "ob": "FM", "oc": "PM", "od": "PCM", "ans": "D"},
            {"cat": "ECE", "week": 3, "sub": "Microprocessors", "q": "How many pins are there in IC 8085?", "oa": "20", "ob": "40", "oc": "16", "od": "24", "ans": "B"},
            {"cat": "ECE", "week": 3, "sub": "Control Systems", "q": "Negative feedback in a control system reduces:", "oa": "Stability", "ob": "Bandwidth", "oc": "Gain", "od": "Error", "ans": "C"},

            {"cat": "ECE", "week": 4, "sub": "VLSI Design", "q": "What does CMOS stand for?", "oa": "Common Metal Oxide", "ob": "Complementary Metal Oxide Semiconductor", "oc": "Circuit Metal Oxide", "od": "None", "ans": "B"},
            {"cat": "ECE", "week": 4, "sub": "Embedded Systems", "q": "Which is a Real-Time Operating System?", "oa": "Windows", "ob": "Linux", "oc": "FreeRTOS", "od": "DOS", "ans": "C"},
            {"cat": "ECE", "week": 4, "sub": "DSP", "q": "FFT is used to compute:", "oa": "DFT", "ob": "Convolution", "oc": "Correlation", "od": "Z-Transform", "ans": "A"},
            {"cat": "ECE", "week": 4, "sub": "Microwave", "q": "Waveguides act as a:", "oa": "Low pass filter", "ob": "High pass filter", "oc": "Band pass filter", "od": "All pass", "ans": "B"},
            {"cat": "ECE", "week": 4, "sub": "Embedded Systems", "q": "The I2C protocol uses how many wires?", "oa": "1", "ob": "2", "oc": "3", "od": "4", "ans": "B"},

            # --- EEE ---
            {"cat": "EEE", "week": 1, "sub": "Electrical Machines", "q": "A transformer works on the principle of:", "oa": "Self Induction", "ob": "Mutual Induction", "oc": "Eddy current", "od": "Static electricity", "ans": "B"},
            {"cat": "EEE", "week": 1, "sub": "Network Theory", "q": "Superposition theorem is applicable to:", "oa": "Linear circuits", "ob": "Non-linear circuits", "oc": "Both", "od": "None", "ans": "A"},
            {"cat": "EEE", "week": 1, "sub": "Power Systems Basics", "q": "The standard frequency of AC supply in India is:", "oa": "60 Hz", "ob": "50 Hz", "oc": "100 Hz", "od": "120 Hz", "ans": "B"},
            {"cat": "EEE", "week": 1, "sub": "Electrical Machines", "q": "DC motors convert electrical energy into:", "oa": "Heat", "ob": "Mechanical energy", "oc": "Magnetic energy", "od": "Chemical energy", "ans": "B"},
            {"cat": "EEE", "week": 1, "sub": "Network Theory", "q": "The unit of Inductance is:", "oa": "Farad", "ob": "Henry", "oc": "Ohm", "od": "Siemens", "ans": "B"},

            {"cat": "EEE", "week": 2, "sub": "Control Systems", "q": "Transfer function is defined for:", "oa": "Non-linear systems", "ob": "Linear Time-Invariant systems", "oc": "Time varying systems", "od": "Discrete systems", "ans": "B"},
            {"cat": "EEE", "week": 2, "sub": "Power Electronics", "q": "A thyristor is a:", "oa": "2-layer device", "ob": "3-layer device", "oc": "4-layer device", "od": "1-layer device", "ans": "C"},
            {"cat": "EEE", "week": 2, "sub": "Measurement", "q": "Megger is used to measure:", "oa": "Low resistance", "ob": "High insulation resistance", "oc": "Voltage", "od": "Current", "ans": "B"},
            {"cat": "EEE", "week": 2, "sub": "Power Electronics", "q": "Inverters convert DC to:", "oa": "Higher DC", "ob": "AC", "oc": "Pulsating DC", "od": "None", "ans": "B"},
            {"cat": "EEE", "week": 2, "sub": "Control Systems", "q": "The root locus starts from:", "oa": "Zeros", "ob": "Poles", "oc": "Infinity", "od": "Origin", "ans": "B"},

            # --- MECH ---
            {"cat": "MECH", "week": 1, "sub": "Thermodynamics", "q": "The Second Law of Thermodynamics introduces the concept of:", "oa": "Enthalpy", "ob": "Entropy", "oc": "Internal Energy", "od": "Temperature", "ans": "B"},
            {"cat": "MECH", "week": 1, "sub": "Fluid Mechanics", "q": "Bernoulli equation is based on conservation of:", "oa": "Mass", "ob": "Energy", "oc": "Momentum", "od": "Pressure", "ans": "B"},
            {"cat": "MECH", "week": 1, "sub": "Engineering Mechanics", "q": "The point where the entire weight of a body acts is called:", "oa": "Centroid", "ob": "Center of Gravity", "oc": "Center of Mass", "od": "None", "ans": "B"},
            {"cat": "MECH", "week": 1, "sub": "Thermodynamics", "q": "An isothermal process occurs at constant:", "oa": "Pressure", "ob": "Volume", "oc": "Temperature", "od": "Heat", "ans": "C"},
            {"cat": "MECH", "week": 1, "sub": "Fluid Mechanics", "q": "Viscosity of a liquid ______ with increase in temperature.", "oa": "Increases", "ob": "Decreases", "oc": "Remains same", "od": "Fluctuates", "ans": "B"},
            
            # --- CIVIL ---
            {"cat": "CIVIL", "week": 1, "sub": "Strength of Materials", "q": "The ratio of stress to strain within elastic limit is:", "oa": "Poisson ratio", "ob": "Modulus of Elasticity", "oc": "Bulk Modulus", "od": "Rigidity Modulus", "ans": "B"},
            {"cat": "CIVIL", "week": 1, "sub": "Building Materials", "q": "Which cement is used for underwater construction?", "oa": "OPC", "ob": "Quick Setting Cement", "oc": "White Cement", "od": "Low Heat Cement", "ans": "B"},

            # --- AIML ---
            {"cat": "AIML", "week": 1, "sub": "Probability", "q": "Bayes Theroem is used for calculating:", "oa": "Prior probability", "ob": "Posterior probability", "oc": "Likelihood", "od": "Evidence", "ans": "B"},
            {"cat": "AIML", "week": 4, "sub": "NLP", "q": "What does BERT stand for?", "oa": "Binary Entity", "ob": "Bidirectional Encoder Representations from Transformers", "oc": "Basic Entity", "od": "None", "ans": "B"},

            # --- IOT ---
            {"cat": "IOT", "week": 1, "sub": "IoT Basics", "q": "Which protocol is commonly used for IoT messaging?", "oa": "HTTP", "ob": "MQTT", "oc": "FTP", "od": "SMTP", "ans": "B"},
        ]

        for d in branch_quiz_data:
            q = QuizQuestion(
                category=d["cat"],
                week_number=d["week"],
                sub_category=d["sub"],
                question_text=d["q"],
                option_a=d["oa"],
                option_b=d["ob"],
                option_c=d["oc"],
                option_d=d["od"],
                correct_option=d["ans"],
                difficulty="Medium"
            )
            db.session.add(q)

        # --- INTERVIEW QUESTIONS ---
        branch_int_data = [
            {"cat": "ECE", "sub": "VLSI", "q": "Explain the Moore's Law and its significance in VLSI today.", "ans": "Moore's Law states that the number of transistors on a microchip doubles every two years. Today, it faces challenges like thermal limits and quantum tunneling, leading to 'More than Moore' technologies."},
            {"cat": "ECE", "sub": "Embedded", "q": "Difference between a Microprocessor and a Microcontroller?", "ans": "A microprocessor has only the CPU inside (requires external RAM, ROM), while a microcontroller has CPU, RAM, ROM, and I/O ports integrated on a single chip."},
            {"cat": "ECE", "sub": "Communication", "q": "What is Multiplexing and its types?", "ans": "Multiplexing is the process of combining multiple signals into one for transmission. Types include TDM (Time Division), FDM (Frequency Division), and WDM (Wavelength Division)."},
            {"cat": "ECE", "sub": "Signals", "q": "What is the Nyquist Sampling Theorem?", "ans": "It states that a continuous signal can be perfectly reconstructed from its samples if the sampling frequency is at least twice the highest frequency component of the signal."},
            {"cat": "ECE", "sub": "Electronics", "q": "Explain the working of a P-N junction diode.", "ans": "A P-N junction allows current to flow in one direction. In forward bias, the depletion layer narrows, allowing carriers to cross. In reverse bias, the layer widens, blocking current."},

            {"cat": "EEE", "sub": "Power Systems", "q": "Why is power transmitted at high voltages?", "ans": "To reduce current, which in turn reduces I^2R power losses in transmission lines and allows for thinner conductors."},
            {"cat": "EEE", "sub": "Machines", "q": "What is back EMF in a DC motor?", "ans": "When the motor rotates, it acts as a generator, creating an EMF that opposes the supply voltage. It helps the motor regulate its speed and current."},

            {"cat": "MECH", "sub": "Thermodynamics", "q": "Explain the Otto Cycle.", "ans": "The Otto cycle is the ideal cycle for spark-ignition engines (petrol). It consists of two isentropic processes and two isochoric (constant volume) processes."},
            {"cat": "MECH", "sub": "Manufacturing", "q": "Difference between Hot Working and Cold Working?", "ans": "Hot working is done above the recrystallization temperature, making metal easier to deform. Cold working is done below it, which increases strength but reduces ductility."},

            {"cat": "CIVIL", "sub": "Structures", "q": "What is Slump Test in concrete?", "ans": "It is used to determine the workability and consistency of fresh concrete. A high slump indicates highly workable (more liquid) concrete."},
            {"cat": "CIVIL", "sub": "Soil", "q": "Explain Liquid Limit and Plastic Limit.", "ans": "Liquid limit is the water content at which soil starts behaving like a liquid. Plastic limit is the content at which it becomes plastic in nature."},

            {"cat": "AIML", "sub": "Machine Learning", "q": "What is Overfitting and how to prevent it?", "ans": "Overfitting happens when a model learns noise in training data. Prevention includes regularization (L1/L2), cross-validation, and reducing model complexity."},
            {"cat": "AIML", "sub": "Deep Learning", "q": "What is the Vanishing Gradient problem?", "ans": "In deep networks, gradients can become extremely small during backpropagation, making it hard for early layers to learn. Solved by ReLU, ResNets, or Batch Norm."},

            {"cat": "IOT", "sub": "Networking", "q": "Explain the difference between MQTT and HTTP for IoT.", "ans": "MQTT is lightweight, pub-sub based, and better for low-bandwidth/battery devices. HTTP is request-response and has more overhead."},
        ]

        for d in branch_int_data:
            q = Question(
                category=d["cat"],
                sub_category=d["sub"],
                question_text=d["q"],
                correct_answer=d["ans"],
                difficulty="Medium"
            )
            db.session.add(q)

        db.session.commit()
        print("Successfully seeded branch-specific quiz and interview content!")

if __name__ == "__main__":
    seed_branch_content()
