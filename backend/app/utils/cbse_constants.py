"""
CBSE syllabus constants, subject-topic mappings, and diagnostic question templates.
All data reflects the 2024-25 CBSE curriculum.
"""

SUBJECTS_BY_CLASS = {
    10: ["Mathematics", "Science", "Social Science", "English", "Hindi"],
    12: [
        "Physics",
        "Chemistry",
        "Mathematics",
        "Biology",
        "English",
        "Economics",
        "Accountancy",
        "Business Studies",
    ],
}

# Topics per subject with approximate marks weightage
SYLLABUS = {
    10: {
        "Mathematics": {
            "Number Systems": 6,
            "Algebra": 20,
            "Coordinate Geometry": 6,
            "Geometry": 15,
            "Trigonometry": 12,
            "Mensuration": 10,
            "Statistics & Probability": 11,
        },
        "Science": {
            "Chemical Substances": 25,
            "World of Living": 23,
            "Natural Phenomena": 12,
            "Effects of Current": 13,
            "Natural Resources": 7,
        },
        "Social Science": {
            "History": 20,
            "Geography": 20,
            "Political Science": 20,
            "Economics": 20,
        },
        "English": {
            "Reading Comprehension": 20,
            "Writing Skills": 20,
            "Grammar": 20,
            "Literature": 40,
        },
        "Hindi": {
            "Apathit Gadyansh": 15,
            "Vyakaran": 16,
            "Sahityik Gadya Khand": 14,
            "Kavya Khand": 14,
            "Lekhan": 21,
        },
    },
    12: {
        "Physics": {
            "Electrostatics": 16,
            "Current Electricity": 16,
            "Magnetic Effects of Current": 17,
            "Electromagnetic Induction & AC": 17,
            "Electromagnetic Waves": 4,
            "Optics": 18,
            "Dual Nature of Matter": 10,
            "Atoms & Nuclei": 12,
            "Electronic Devices": 7,
            "Communication Systems": 3,
        },
        "Chemistry": {
            "Solid State": 4,
            "Solutions": 5,
            "Electrochemistry": 5,
            "Chemical Kinetics": 5,
            "Surface Chemistry": 4,
            "Isolation of Elements": 3,
            "p-Block Elements": 8,
            "d & f Block Elements": 5,
            "Coordination Compounds": 3,
            "Haloalkanes & Haloarenes": 4,
            "Alcohols Phenols Ethers": 4,
            "Aldehydes Ketones Carboxylic Acids": 6,
            "Nitrogen Compounds": 4,
            "Biomolecules": 4,
            "Polymers": 3,
            "Chemistry in Everyday Life": 3,
        },
        "Mathematics": {
            "Relations and Functions": 8,
            "Algebra": 10,
            "Calculus": 35,
            "Vectors and 3D Geometry": 14,
            "Linear Programming": 5,
            "Probability": 8,
        },
        "Biology": {
            "Reproduction": 16,
            "Genetics & Evolution": 18,
            "Biology in Human Welfare": 14,
            "Biotechnology": 12,
            "Ecology": 10,
        },
        "Economics": {
            "Microeconomics - Introduction": 13,
            "Consumer Behaviour": 13,
            "Production and Costs": 10,
            "Market Forms": 13,
            "Macroeconomics - National Income": 10,
            "Money and Banking": 6,
            "Determination of Income": 12,
            "Government Budget": 6,
            "Balance of Payments": 7,
        },
        "Accountancy": {
            "Accounting Not for Profit": 10,
            "Partnership Accounts": 30,
            "Company Accounts": 20,
            "Financial Statements Analysis": 12,
            "Cash Flow Statement": 8,
        },
        "Business Studies": {
            "Nature and Significance of Management": 16,
            "Principles of Management": 14,
            "Business Environment": 10,
            "Planning": 12,
            "Organising": 14,
            "Staffing": 14,
            "Directing": 20,
        },
        "English": {
            "Reading Comprehension": 22,
            "Creative Writing": 18,
            "Grammar": 10,
            "Literature": 30,
        },
    },
}

# Question paper structure per total marks
PAPER_STRUCTURE = {
    40: {
        "Section A": {"type": "mcq", "count": 10, "marks_each": 1, "description": "Multiple Choice Questions"},
        "Section B": {"type": "short_answer", "count": 5, "marks_each": 2, "description": "Short Answer Questions"},
        "Section C": {"type": "long_answer", "count": 4, "marks_each": 5, "description": "Long Answer Questions"},
    },
    80: {
        "Section A": {"type": "mcq", "count": 20, "marks_each": 1, "description": "Multiple Choice Questions"},
        "Section B": {"type": "short_answer", "count": 6, "marks_each": 3, "description": "Short Answer Questions (3 marks)"},
        "Section C": {"type": "long_answer", "count": 4, "marks_each": 5, "description": "Long Answer Questions (5 marks)"},
        "Section D": {"type": "case_based", "count": 2, "marks_each": 4, "description": "Case-Based Questions"},
    },
}

MARKS_TO_DURATION = {40: 90, 80: 180}

GRADE_THRESHOLDS = [
    (91, "A1"),
    (81, "A2"),
    (71, "B1"),
    (61, "B2"),
    (51, "C1"),
    (41, "C2"),
    (33, "D"),
    (0, "E"),
]


def get_grade(percentage: float) -> str:
    for threshold, grade in GRADE_THRESHOLDS:
        if percentage >= threshold:
            return grade
    return "E"


# Diagnostic question templates per subject type
DIAGNOSTIC_QUESTIONS = {
    "_common": [
        {
            "id": "conf_overall",
            "type": "confidence",
            "question": "How confident do you feel about this subject overall?",
            "options": ["1 - Very Low", "2 - Low", "3 - Average", "4 - Good", "5 - Excellent"],
            "topic": None,
        },
        {
            "id": "past_marks",
            "type": "past_performance",
            "question": "What was your approximate score in your last test/exam for this subject?",
            "options": ["Below 33%", "33–50%", "51–60%", "61–75%", "76–90%", "Above 90%"],
            "topic": None,
        },
        {
            "id": "study_hours",
            "type": "past_performance",
            "question": "How many hours per week do you currently study this subject?",
            "options": ["Less than 1 hour", "1–2 hours", "3–4 hours", "5–6 hours", "More than 6 hours"],
            "topic": None,
        },
    ],
    "Mathematics": [
        {"id": "math_algebra", "type": "topic_strength", "question": "Rate your comfort with Algebra (equations, polynomials)", "options": ["1", "2", "3", "4", "5"], "topic": "Algebra"},
        {"id": "math_geometry", "type": "topic_strength", "question": "Rate your comfort with Geometry (triangles, circles, constructions)", "options": ["1", "2", "3", "4", "5"], "topic": "Geometry"},
        {"id": "math_trig", "type": "topic_strength", "question": "Rate your comfort with Trigonometry", "options": ["1", "2", "3", "4", "5"], "topic": "Trigonometry"},
        {"id": "math_stats", "type": "topic_strength", "question": "Rate your comfort with Statistics and Probability", "options": ["1", "2", "3", "4", "5"], "topic": "Statistics & Probability"},
        {"id": "math_calc", "type": "topic_strength", "question": "Rate your comfort with Calculus (derivatives, integrals) — Class 12 only", "options": ["1", "2", "3", "4", "5"], "topic": "Calculus"},
    ],
    "Science": [
        {"id": "sci_chemistry", "type": "topic_strength", "question": "Rate your comfort with Chemistry topics (acids, bases, reactions)", "options": ["1", "2", "3", "4", "5"], "topic": "Chemical Substances"},
        {"id": "sci_biology", "type": "topic_strength", "question": "Rate your comfort with Biology topics (life processes, reproduction)", "options": ["1", "2", "3", "4", "5"], "topic": "World of Living"},
        {"id": "sci_physics", "type": "topic_strength", "question": "Rate your comfort with Physics topics (electricity, light, force)", "options": ["1", "2", "3", "4", "5"], "topic": "Natural Phenomena"},
        {"id": "sci_environment", "type": "topic_strength", "question": "Rate your comfort with Environmental topics", "options": ["1", "2", "3", "4", "5"], "topic": "Natural Resources"},
    ],
    "Physics": [
        {"id": "phy_electrostatics", "type": "topic_strength", "question": "Rate your comfort with Electrostatics (electric field, potential, capacitors)", "options": ["1", "2", "3", "4", "5"], "topic": "Electrostatics"},
        {"id": "phy_current", "type": "topic_strength", "question": "Rate your comfort with Current Electricity (Ohm's law, circuits)", "options": ["1", "2", "3", "4", "5"], "topic": "Current Electricity"},
        {"id": "phy_optics", "type": "topic_strength", "question": "Rate your comfort with Optics (lenses, mirrors, interference)", "options": ["1", "2", "3", "4", "5"], "topic": "Optics"},
        {"id": "phy_modern", "type": "topic_strength", "question": "Rate your comfort with Modern Physics (atoms, nuclei, semiconductors)", "options": ["1", "2", "3", "4", "5"], "topic": "Atoms & Nuclei"},
        {"id": "phy_em", "type": "topic_strength", "question": "Rate your comfort with Electromagnetic Induction & AC Circuits", "options": ["1", "2", "3", "4", "5"], "topic": "Electromagnetic Induction & AC"},
    ],
    "Chemistry": [
        {"id": "chem_organic", "type": "topic_strength", "question": "Rate your comfort with Organic Chemistry (reactions, mechanisms)", "options": ["1", "2", "3", "4", "5"], "topic": "Aldehydes Ketones Carboxylic Acids"},
        {"id": "chem_inorganic", "type": "topic_strength", "question": "Rate your comfort with Inorganic Chemistry (p-block, d-block elements)", "options": ["1", "2", "3", "4", "5"], "topic": "p-Block Elements"},
        {"id": "chem_physical", "type": "topic_strength", "question": "Rate your comfort with Physical Chemistry (electrochemistry, kinetics, solutions)", "options": ["1", "2", "3", "4", "5"], "topic": "Electrochemistry"},
        {"id": "chem_coordination", "type": "topic_strength", "question": "Rate your comfort with Coordination Compounds", "options": ["1", "2", "3", "4", "5"], "topic": "Coordination Compounds"},
    ],
    "Biology": [
        {"id": "bio_reproduction", "type": "topic_strength", "question": "Rate your comfort with Reproduction (sexual, asexual, plant/animal)", "options": ["1", "2", "3", "4", "5"], "topic": "Reproduction"},
        {"id": "bio_genetics", "type": "topic_strength", "question": "Rate your comfort with Genetics and Evolution", "options": ["1", "2", "3", "4", "5"], "topic": "Genetics & Evolution"},
        {"id": "bio_biotech", "type": "topic_strength", "question": "Rate your comfort with Biotechnology", "options": ["1", "2", "3", "4", "5"], "topic": "Biotechnology"},
        {"id": "bio_ecology", "type": "topic_strength", "question": "Rate your comfort with Ecology and Environment", "options": ["1", "2", "3", "4", "5"], "topic": "Ecology"},
    ],
    "Social Science": [
        {"id": "sst_history", "type": "topic_strength", "question": "Rate your comfort with History (nationalism, world wars, modern India)", "options": ["1", "2", "3", "4", "5"], "topic": "History"},
        {"id": "sst_geography", "type": "topic_strength", "question": "Rate your comfort with Geography (resources, agriculture, industries)", "options": ["1", "2", "3", "4", "5"], "topic": "Geography"},
        {"id": "sst_polsci", "type": "topic_strength", "question": "Rate your comfort with Political Science (democracy, federalism)", "options": ["1", "2", "3", "4", "5"], "topic": "Political Science"},
        {"id": "sst_economics", "type": "topic_strength", "question": "Rate your comfort with Economics (development, sectors, money)", "options": ["1", "2", "3", "4", "5"], "topic": "Economics"},
    ],
    "Economics": [
        {"id": "eco_micro", "type": "topic_strength", "question": "Rate your comfort with Microeconomics (demand, supply, market structures)", "options": ["1", "2", "3", "4", "5"], "topic": "Microeconomics - Introduction"},
        {"id": "eco_macro", "type": "topic_strength", "question": "Rate your comfort with Macroeconomics (national income, money, banking)", "options": ["1", "2", "3", "4", "5"], "topic": "Macroeconomics - National Income"},
        {"id": "eco_bop", "type": "topic_strength", "question": "Rate your comfort with Balance of Payments and Government Budget", "options": ["1", "2", "3", "4", "5"], "topic": "Balance of Payments"},
    ],
    "Accountancy": [
        {"id": "acc_partnership", "type": "topic_strength", "question": "Rate your comfort with Partnership Accounts", "options": ["1", "2", "3", "4", "5"], "topic": "Partnership Accounts"},
        {"id": "acc_company", "type": "topic_strength", "question": "Rate your comfort with Company Accounts (shares, debentures)", "options": ["1", "2", "3", "4", "5"], "topic": "Company Accounts"},
        {"id": "acc_ratios", "type": "topic_strength", "question": "Rate your comfort with Financial Statement Analysis and Ratios", "options": ["1", "2", "3", "4", "5"], "topic": "Financial Statements Analysis"},
        {"id": "acc_cashflow", "type": "topic_strength", "question": "Rate your comfort with Cash Flow Statement", "options": ["1", "2", "3", "4", "5"], "topic": "Cash Flow Statement"},
    ],
    "Business Studies": [
        {"id": "bs_management", "type": "topic_strength", "question": "Rate your comfort with Principles and Functions of Management", "options": ["1", "2", "3", "4", "5"], "topic": "Nature and Significance of Management"},
        {"id": "bs_organising", "type": "topic_strength", "question": "Rate your comfort with Organising and Staffing", "options": ["1", "2", "3", "4", "5"], "topic": "Organising"},
        {"id": "bs_directing", "type": "topic_strength", "question": "Rate your comfort with Directing (motivation, leadership, communication)", "options": ["1", "2", "3", "4", "5"], "topic": "Directing"},
    ],
    "English": [
        {"id": "eng_reading", "type": "topic_strength", "question": "Rate your ability to understand unseen passages", "options": ["1", "2", "3", "4", "5"], "topic": "Reading Comprehension"},
        {"id": "eng_writing", "type": "topic_strength", "question": "Rate your confidence in essay/letter/notice writing", "options": ["1", "2", "3", "4", "5"], "topic": "Writing Skills"},
        {"id": "eng_grammar", "type": "topic_strength", "question": "Rate your comfort with Grammar (tenses, voice, reported speech)", "options": ["1", "2", "3", "4", "5"], "topic": "Grammar"},
        {"id": "eng_literature", "type": "topic_strength", "question": "Rate your comfort with Literature questions (poems, prose)", "options": ["1", "2", "3", "4", "5"], "topic": "Literature"},
    ],
    "Hindi": [
        {"id": "hin_gadya", "type": "topic_strength", "question": "Rate your comfort with Sahityik Gadya Khand", "options": ["1", "2", "3", "4", "5"], "topic": "Sahityik Gadya Khand"},
        {"id": "hin_kavya", "type": "topic_strength", "question": "Rate your comfort with Kavya Khand (poetry)", "options": ["1", "2", "3", "4", "5"], "topic": "Kavya Khand"},
        {"id": "hin_vyakaran", "type": "topic_strength", "question": "Rate your comfort with Vyakaran (grammar)", "options": ["1", "2", "3", "4", "5"], "topic": "Vyakaran"},
        {"id": "hin_lekhan", "type": "topic_strength", "question": "Rate your confidence in Lekhan (writing — nibandh, patra)", "options": ["1", "2", "3", "4", "5"], "topic": "Lekhan"},
    ],
}


def get_diagnostic_questions(subject: str) -> list:
    """Return diagnostic questions for a subject (common + subject-specific)."""
    common = DIAGNOSTIC_QUESTIONS["_common"]
    specific = DIAGNOSTIC_QUESTIONS.get(subject, [])
    return common + specific


def get_topics_for_subject(class_level: int, subject: str) -> list:
    return list(SYLLABUS.get(class_level, {}).get(subject, {}).keys())
