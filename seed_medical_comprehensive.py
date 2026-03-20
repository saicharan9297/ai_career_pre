from app import app
from extensions import db
from models import QuizQuestion, Question

def seed_medical_comprehensive():
    with app.app_context():
        # Clear existing medical data to prevent duplicates
        QuizQuestion.query.filter_by(category="Medical").delete()
        Question.query.filter_by(category="Medical").delete()

        quiz_data = [
            # --- MBBS / DOCTOR (Weeks 1-4) ---
            # Week 1: Foundations (Anatomy, Physiology, Biochemistry)
            {"cat": "Medical", "sub": "Anatomy", "week": 1, "q": "Largest gland in the human body?", "a": "Pancreas", "b": "Liver", "c": "Spleen", "d": "Adrenal", "ans": "B"},
            {"cat": "Medical", "sub": "Physiology", "week": 1, "q": "Main pacemaker of the heart?", "a": "AV node", "b": "SA node", "c": "Purkinje fibers", "d": "Bundle of His", "ans": "B"},
            {"cat": "Medical", "sub": "Biochemistry", "week": 1, "q": "Which mineral is key for hemoglobin?", "a": "Calcium", "b": "Iron", "c": "Iodine", "d": "Magnesium", "ans": "B"},
            {"cat": "Medical", "sub": "Physiology", "week": 1, "q": "What is the tidal volume in a healthy adult?", "a": "200ml", "b": "500ml", "c": "1000ml", "d": "1500ml", "ans": "B"},
            
            # Week 2: Para-clinical (Pathology, Microbiology, Pharmacology, Forensic, Cardiology)
            {"cat": "Medical", "sub": "Pharmacology", "week": 2, "q": "Antidote for Heparin overdose?", "a": "Vitamin K", "b": "Protamine Sulfate", "c": "Atropine", "d": "Naloxone", "ans": "B"},
            {"cat": "Medical", "sub": "Pathology", "week": 2, "q": "Programmed cell death is called:", "a": "Necrosis", "b": "Apoptosis", "c": "Autolysis", "d": "Atrophy", "ans": "B"},
            {"cat": "Medical", "sub": "Microbiology", "week": 2, "q": "Which virus causes Dengue?", "a": "Retrovirus", "b": "Flavivirus", "c": "Rhabdovirus", "d": "Adenovirus", "ans": "B"},
            {"cat": "Medical", "sub": "Pharmacology", "week": 2, "q": "Mechanism of Action of Aspirin?", "a": "COX inhibitor", "b": "ACE inhibitor", "c": "Calcium blocker", "d": "None", "ans": "A"},

            # Week 3: Clinical (General Medicine, General Surgery, Pediatrics)
            {"cat": "Medical", "sub": "General Medicine", "week": 3, "q": "Which sign is positive in Meningitis?", "a": "Murphy sign", "b": "Kernig sign", "c": "McBurney sign", "d": "Rovsing sign", "ans": "B"},
            {"cat": "Medical", "sub": "Pediatrics", "week": 3, "q": "Standard fontanelle to close first?", "a": "Anterior", "b": "Posterior", "c": "Sphenoid", "d": "Mastoid", "ans": "B"},
            {"cat": "Medical", "sub": "General Surgery", "week": 3, "q": "Most common cause of acute abdomen?", "a": "Gallstones", "b": "Appendicitis", "c": "Hernia", "d": "Ulcer", "ans": "B"},
            {"cat": "Medical", "sub": "General Medicine", "week": 3, "q": "Hyperthyroidism symptom?", "a": "Weight gain", "b": "Weight loss", "c": "Cold intolerance", "d": "Bradycardia", "ans": "B"},

            # Week 4: Specializations (Obstetrics, Gynecology, Community Medicine, Ethics)
            {"cat": "Medical", "sub": "Obstetrics", "week": 4, "q": "First fetal movement felt by mother?", "a": "Lightening", "b": "Quickening", "c": "Engagement", "d": "Ballottement", "ans": "B"},
            {"cat": "Medical", "sub": "Community Medicine", "week": 4, "q": "Who is the 'father of epidemiology'?", "a": "Louis Pasteur", "b": "John Snow", "c": "Edward Jenner", "d": "Robert Koch", "ans": "B"},
            {"cat": "Medical", "sub": "Medical Ethics", "week": 4, "q": "Confidentiality is part of which pillar?", "a": "Justice", "b": "Autonomy", "c": "Beneficence", "d": "Non-maleficence", "ans": "B"},
            {"cat": "Medical", "sub": "Gynecology", "week": 4, "q": "Most common site of ectopic pregnancy?", "a": "Ovary", "b": "Fallopian Tube", "c": "Cervix", "d": "Abdomen", "ans": "B"},
            {"cat": "Medical", "sub": "Physio", "week": 4, "q": "Which muscle is known as 'boxer muscle'?", "a": "Trapezius", "b": "Serratus Anterior", "c": "Deltoid", "d": "Pectoralis Major", "ans": "B"},
            {"cat": "Medical", "sub": "Nursing", "week": 4, "q": "Bed sores primarily caused by:", "a": "Nutrition", "b": "Pressure/Ischemia", "c": "Infection", "d": "Age", "ans": "B"},
            
            # Additional Vet
            {"cat": "Medical", "sub": "Veterinary", "week": 1, "q": "Which bird has the largest egg?", "a": "Emu", "b": "Ostrich", "c": "Kiwi", "d": "Eagle", "ans": "B"},
            {"cat": "Medical", "sub": "Veterinary", "week": 2, "q": "Rabies is also known as:", "a": "Hydrophobia", "b": "Aerophobia", "c": "Photophobia", "d": "None", "ans": "A"},

            # Week 4: Specializations (Obstetrics, Gynecology, Community Medicine, Ethics)
            {"cat": "Medical", "sub": "Community Medicine", "week": 4, "q": "Primary goal of public health?", "a": "Profit", "b": "Prevention", "c": "Surgery", "d": "Research", "ans": "B"},
            {"cat": "Medical", "sub": "Medical Ethics", "week": 4, "q": "'Doing no harm' is:", "a": "Autonomy", "b": "Beneficence", "c": "Non-maleficence", "d": "Justice", "ans": "C"},
            {"cat": "Medical", "sub": "Obstetrics", "week": 4, "q": "Normal human pregnancy duration (weeks):", "a": "36", "b": "38", "c": "40", "d": "42", "ans": "C"},
            {"cat": "Medical", "sub": "Gynecology", "week": 4, "q": "Common cause of cervical cancer?", "a": "HPV", "b": "HIV", "c": "HBV", "d": "HSV", "ans": "A"},
            {"cat": "Medical", "sub": "Community Medicine", "week": 4, "q": "Vector for Malaria?", "a": "Housefly", "b": "Anopheles", "c": "Tick", "d": "Rat Flea", "ans": "B"},
            {"cat": "Medical", "sub": "Medical Ethics", "week": 4, "q": "Informed consent must be:", "a": "Coerced", "b": "Voluntary", "c": "Oral only", "d": "Implicit", "ans": "B"},
            {"cat": "Medical", "sub": "Obstetrics", "week": 4, "q": "ECTOPIC pregnancy occurs outside the:", "a": "Uterus", "b": "Ovary", "c": "Vagina", "d": "Fallopian Tube", "ans": "A"},

            # --- NURSING ---
            {"cat": "Medical", "sub": "Nursing Foundations", "week": 1, "q": "1st step in nursing process?", "a": "Planning", "b": "Assessment", "c": "Diagnosis", "d": "Evaluation", "ans": "B"},
            {"cat": "Medical", "sub": "Anatomy & Physiology for Nurses", "week": 1, "q": "Smallest unit of life?", "a": "Tissue", "b": "Cell", "c": "Organ", "d": "System", "ans": "B"},
            {"cat": "Medical", "sub": "Medical-Surgical Nursing", "week": 2, "q": "Polyuria is a symptom of:", "a": "Hypotension", "b": "Diabetes", "c": "Anemia", "d": "Fever", "ans": "B"},
            {"cat": "Medical", "sub": "Nutrition", "week": 2, "q": "Vitamin essential for blood clotting?", "a": "A", "b": "C", "c": "K", "d": "D", "ans": "C"},
            {"cat": "Medical", "sub": "Child Health Nursing", "week": 3, "q": "ORT treats:", "a": "Fever", "b": "Dehydration", "c": "Infection", "d": "Pain", "ans": "B"},
            {"cat": "Medical", "sub": "Community Health Nursing", "week": 4, "q": "Immunization level of prevention?", "a": "Primary", "b": "Secondary", "c": "Tertiary", "d": "None", "ans": "A"},

            # --- PHARMACY ---
            {"cat": "Medical", "sub": "Pharmaceutical Chemistry", "week": 1, "q": "pH of neutral solution?", "a": "5", "b": "7", "c": "9", "d": "14", "ans": "B"},
            {"cat": "Medical", "sub": "Pharmaceutics", "week": 2, "q": "Sublingual tablets are placed:", "a": "In ear", "b": "Under tongue", "c": "On skin", "d": "In mouth", "ans": "B"},
            {"cat": "Medical", "sub": "Pharmacology", "week": 3, "q": "First-pass effect occurs in:", "a": "Kidney", "b": "Liver", "c": "Heart", "d": "Lungs", "ans": "B"},
            {"cat": "Medical", "sub": "Hospital Pharmacy", "week": 4, "q": "Drug inventory manager?", "a": "Nurse", "b": "Pharmacist", "c": "Doctor", "d": "None", "ans": "B"},

            # --- DENTAL ---
            {"cat": "Medical", "sub": "Oral Anatomy", "week": 1, "q": "Number of deciduous teeth?", "a": "20", "b": "32", "c": "28", "d": "10", "ans": "A"},
            {"cat": "Medical", "sub": "Dental Materials", "week": 1, "q": "Material for fillings?", "a": "Titanium", "b": "Amalgam", "c": "Steel", "d": "Gold", "ans": "B"},
            {"cat": "Medical", "sub": "Oral Surgery", "week": 3, "q": "Tooth extraction is:", "a": "Scaling", "b": "Exodontia", "c": "Filling", "d": "None", "ans": "B"},

            # --- PHYSIO ---
            {"cat": "Medical", "sub": "Anatomy & Kinesiology", "week": 1, "q": "Knee joint type?", "a": "Hinge", "b": "Ball and socket", "c": "Pivot", "d": "Gliding", "ans": "A"},
            {"cat": "Medical", "sub": "Biomechanics", "week": 1, "q": "Center of gravity in adult (standing)?", "a": "S2", "b": "L4", "c": "T12", "d": "None", "ans": "A"},
            {"cat": "Medical", "sub": "Neuro-Physiotherapy", "week": 2, "q": "Rehab for Stroke usually focuses on:", "a": "Gait", "b": "Hearing", "c": "Vision", "d": "Speech", "ans": "A"},

            # --- VET ---
            {"cat": "Medical", "sub": "Veterinary Anatomy", "week": 1, "q": "Number of stomach compartments in cow?", "a": "1", "b": "2", "c": "4", "d": "6", "ans": "C"},
            {"cat": "Medical", "sub": "Animal Nutrition", "week": 1, "q": "Essential nutrient for wool production?", "a": "Sulfur", "b": "Iron", "c": "Calcium", "d": "Potassium", "ans": "A"},
            {"cat": "Medical", "sub": "Veterinary Medicine", "week": 2, "q": "Main zoonotic disease?", "a": "Rabies", "b": "Parvo", "c": "Distemper", "d": "Flu", "ans": "A"},
        ]

        interview_data = [
            {"cat": "Medical", "sub": "MBBS", "diff": "Medium", "q": "How would you handle a patient who refuses potentially life-saving treatment due to religious beliefs?", "ans": "Discuss autonomy and ethical deliberation."},
            {"cat": "Medical", "sub": "Cardiology", "diff": "Hard", "q": "Explain the management of a patient presenting with NSTEMI.", "ans": "Keywords: Antiplatelets Anticoagulants Beta-blockers ACE inhibitors Risk stratification Revascularization"},
            {"cat": "Medical", "sub": "Pediatrics", "diff": "Medium", "q": "How do you approach a case of 'failure to thrive' in an infant?", "ans": "Keywords: Nutritional assessment Developmental milestones Family history Systemic diseases Caloric intake"},
            {"cat": "Medical", "sub": "Nursing", "diff": "Medium", "q": "Describe your process for prioritizing patient care during a high-volume emergency shift.", "ans": "Triage and critical care prioritization."},
            {"cat": "Medical", "sub": "Pharmacy", "diff": "Medium", "q": "What steps do you take to prevent medication errors in a busy hospital setting?", "ans": "Double-check protocols and communication."},
            {"cat": "Medical", "sub": "Physiotherapy", "diff": "Medium", "q": "Describe the rehabilitation plan for a post-op ACL reconstruction.", "ans": "Keywords: Range of motion Quadriceps activation Swelling control Weight-bearing Progression Agility"},
            {"cat": "Medical", "sub": "Veterinary", "diff": "Medium", "q": "What are the key clinical signs of Milk Fever in dairy cows?", "ans": "Keywords: Hypocalcemia Recumbency Cold extremities Reduced appetite S-curve neck"},
            {"cat": "Medical", "sub": "Ayurveda", "diff": "Medium", "q": "Explain the concept of 'Prakriti' in Ayurvedic diagnosis.", "ans": "Keywords: Genetic constitution Dosha balance Mental-Physical traits Personalized treatment Diet Life-style"},
            {"cat": "Medical", "sub": "Radiology", "diff": "Hard", "q": "Describe the safety protocols for working in an MRI environment.", "ans": "Keywords: Magnetic field Projectile effect Ferromagnetic materials Quenching Shielding Implants screening"},
            {"cat": "Medical", "sub": "Public Health", "diff": "Medium", "q": "What is the importance of 'herd immunity' in vaccination programs?", "ans": "Keywords: Threshold coverage Chain of transmission Protecting vulnerable Eradication Outbreak prevention"}
        ]

        # Add Quiz Questions
        for item in quiz_data:
            q = QuizQuestion(
                category=item['cat'],
                sub_category=item['sub'],
                week_number=item['week'],
                difficulty="Medium",
                question_text=item['q'],
                option_a=item['a'],
                option_b=item['b'],
                option_c=item['c'],
                option_d=item['d'],
                correct_option=item['ans']
            )
            db.session.add(q)
        
        # Add Interview Questions
        for item in interview_data:
            q = Question(
                category=item['cat'],
                sub_category=item['sub'],
                difficulty=item['diff'],
                question_text=item['q'],
                correct_answer=item['ans'],
                hint="Think about domain-specific standards and protocols."
            )
            db.session.add(q)

        db.session.commit()
        print(f"Successfully seeded {len(quiz_data)} medical quiz questions and {len(interview_data)} interview questions.")

if __name__ == "__main__":
    seed_medical_comprehensive()
