"""
Sample CBSE question bank for seeding ChromaDB.
Contains representative questions from each subject and class level.
These cover key NCERT topics and follow CBSE 2024-25 exam patterns.
"""

CBSE_QUESTIONS = [
    # ── Class 10 Mathematics ──────────────────────────────────────────────────
    {
        "id": "c10_math_001",
        "text": "Q: Find the HCF and LCM of 96 and 404 using the prime factorisation method.\nA: 96 = 2^5 × 3; 404 = 2^2 × 101. HCF = 2^2 = 4. LCM = 2^5 × 3 × 101 = 9696.",
        "class_level": 10, "subject": "Mathematics", "topic": "Number Systems", "type": "short_answer", "marks": 3,
    },
    {
        "id": "c10_math_002",
        "text": "Q: Prove that √2 is irrational.\nA: Assume √2 = p/q in lowest terms. Then 2q²=p², so p² is even, p is even. p=2k, then 2q²=4k², q²=2k², q is even. Contradiction since p/q is in lowest terms. Hence √2 is irrational.",
        "class_level": 10, "subject": "Mathematics", "topic": "Number Systems", "type": "long_answer", "marks": 5,
    },
    {
        "id": "c10_math_003",
        "text": "Q: Find the zeros of the quadratic polynomial 6x² – 3 – 7x and verify the relationship between zeros and coefficients.\nA: 6x²–7x–3 = (3x+1)(2x–3). Zeros: x = -1/3, x = 3/2. Sum = -1/3+3/2 = 7/6 = -b/a. Product = -1/3×3/2 = -1/2 = c/a. ✓",
        "class_level": 10, "subject": "Mathematics", "topic": "Algebra", "type": "short_answer", "marks": 3,
    },
    {
        "id": "c10_math_004",
        "text": "Q: Solve by elimination: 3x + 4y = 10 and 2x – 2y = 2.\nA: Multiply eq2 by 2: 4x – 4y = 4. Add to eq1: 7x = 14, x = 2. Substitute: 6+4y=10, y=1. Solution: x=2, y=1.",
        "class_level": 10, "subject": "Mathematics", "topic": "Algebra", "type": "short_answer", "marks": 3,
    },
    {
        "id": "c10_math_005",
        "text": "Q: A quadratic equation 2x² – 7x + 3 = 0. Find the discriminant and nature of roots.\nA: D = b²–4ac = 49 – 24 = 25 > 0. Two distinct real roots. x = (7±5)/4; x=3 or x=1/2.",
        "class_level": 10, "subject": "Mathematics", "topic": "Algebra", "type": "short_answer", "marks": 3,
    },
    {
        "id": "c10_math_006",
        "text": "Q: The sum of the 4th and 8th terms of an AP is 24 and the sum of the 6th and 10th terms is 34. Find the first term and the common difference.\nA: a+3d + a+7d = 24 → 2a+10d=24 → a+5d=12. a+5d + a+9d = 34 → 2a+14d=34 → a+7d=17. Solving: 2d=5, d=2.5, a=12-12.5= -0.5.",
        "class_level": 10, "subject": "Mathematics", "topic": "Algebra", "type": "long_answer", "marks": 5,
    },
    {
        "id": "c10_math_007",
        "text": "Q: Find the distance between points A(–6, 7) and B(–1, –5).\nA: d = √[(−1−(−6))²+(−5−7)²] = √[25+144] = √169 = 13 units.",
        "class_level": 10, "subject": "Mathematics", "topic": "Coordinate Geometry", "type": "short_answer", "marks": 2,
    },
    {
        "id": "c10_math_008",
        "text": "Q: Prove that the tangent at any point of a circle is perpendicular to the radius through the point of contact.\nA: Let O be centre, P point of contact, PT tangent. For any point Q on tangent, OQ > OP (Q is outside circle). Hence OP is shortest distance from O to tangent, so OP ⊥ PT.",
        "class_level": 10, "subject": "Mathematics", "topic": "Geometry", "type": "long_answer", "marks": 5,
    },
    {
        "id": "c10_math_009",
        "text": "Q: If sin A = 3/4, calculate cos A and tan A (A is acute).\nA: sin²A + cos²A = 1. cos²A = 1 – 9/16 = 7/16. cos A = √7/4. tan A = sin A/cos A = 3/√7.",
        "class_level": 10, "subject": "Mathematics", "topic": "Trigonometry", "type": "short_answer", "marks": 3,
    },
    {
        "id": "c10_math_010",
        "text": "Q: The angle of elevation of the top of a tower from a point on the ground, 20 m away from the base, is 30°. Find the height of the tower.\nA: tan 30° = h/20. 1/√3 = h/20. h = 20/√3 = 20√3/3 ≈ 11.55 m.",
        "class_level": 10, "subject": "Mathematics", "topic": "Trigonometry", "type": "short_answer", "marks": 3,
    },
    {
        "id": "c10_math_011",
        "text": "Q: A horse is tied to a peg at corner of a square field of side 15 m with a rope 5 m long. Find area it can graze.\nA: Area = (90/360)×π×5² = (1/4)×π×25 = 25π/4 ≈ 19.625 m².",
        "class_level": 10, "subject": "Mathematics", "topic": "Mensuration", "type": "short_answer", "marks": 3,
    },
    {
        "id": "c10_math_012",
        "text": "Q: The mean of the following data is 25: Classes 0-10, 10-20, 20-30, 30-40, 40-50 with frequencies 5, 8, 15, 7, 5. Verify.\nA: Σfx = 5×5+8×15+15×25+7×35+5×45 = 25+120+375+245+225 = 990. Σf = 40. Mean = 990/40 = 24.75 ≈ 25. ✓",
        "class_level": 10, "subject": "Mathematics", "topic": "Statistics & Probability", "type": "short_answer", "marks": 3,
    },
    # ── Class 10 Science ──────────────────────────────────────────────────────
    {
        "id": "c10_sci_001",
        "text": "Q: What is a chemical equation? Balance the equation: Fe + H₂O → Fe₃O₄ + H₂.\nA: A chemical equation represents a chemical reaction using symbols and formulae. Balanced: 3Fe + 4H₂O → Fe₃O₄ + 4H₂.",
        "class_level": 10, "subject": "Science", "topic": "Chemical Substances", "type": "short_answer", "marks": 3,
    },
    {
        "id": "c10_sci_002",
        "text": "Q: Distinguish between displacement reaction and double displacement reaction with examples.\nA: Displacement: A more reactive element displaces less reactive. E.g., Zn + CuSO₄ → ZnSO₄ + Cu. Double displacement: Exchange of ions between two compounds. E.g., NaCl + AgNO₃ → AgCl↓ + NaNO₃.",
        "class_level": 10, "subject": "Science", "topic": "Chemical Substances", "type": "short_answer", "marks": 3,
    },
    {
        "id": "c10_sci_003",
        "text": "Q: What happens when dilute HCl is added to iron fillings? Write the chemical equation.\nA: Iron reacts with dilute HCl to produce iron(II) chloride and hydrogen gas. Fe + 2HCl → FeCl₂ + H₂↑. Hydrogen gas is released with effervescence.",
        "class_level": 10, "subject": "Science", "topic": "Chemical Substances", "type": "short_answer", "marks": 3,
    },
    {
        "id": "c10_sci_004",
        "text": "Q: Draw and explain the structure of the human heart. Describe the path of blood flow through it.\nA: The human heart has 4 chambers: right atrium, right ventricle, left atrium, left ventricle. Deoxygenated blood → right atrium → right ventricle → pulmonary artery → lungs → pulmonary vein → left atrium → left ventricle → aorta → body.",
        "class_level": 10, "subject": "Science", "topic": "World of Living", "type": "long_answer", "marks": 5,
    },
    {
        "id": "c10_sci_005",
        "text": "Q: What is refraction of light? State Snell's law.\nA: Refraction is bending of light when it passes from one transparent medium to another. Snell's Law: n₁ sin θ₁ = n₂ sin θ₂, where n₁, n₂ are refractive indices and θ₁, θ₂ are angles of incidence and refraction.",
        "class_level": 10, "subject": "Science", "topic": "Natural Phenomena", "type": "short_answer", "marks": 3,
    },
    {
        "id": "c10_sci_006",
        "text": "Q: State and explain Ohm's Law. What are its limitations?\nA: V = IR. At constant temperature, current through a conductor is directly proportional to the voltage across it. Limitations: Does not apply to non-linear devices (diodes, transistors), does not hold at very high currents (conductor heats up).",
        "class_level": 10, "subject": "Science", "topic": "Effects of Current", "type": "short_answer", "marks": 3,
    },
    # ── Class 10 Social Science ───────────────────────────────────────────────
    {
        "id": "c10_sst_001",
        "text": "Q: Explain the causes of the First World War.\nA: Main causes: (1) Militarism – arms race among European powers; (2) Alliance System – Triple Alliance vs Triple Entente; (3) Imperialism – competition for colonies; (4) Nationalism – pan-Slavism, pan-Germanism; (5) Assassination of Archduke Franz Ferdinand (immediate cause).",
        "class_level": 10, "subject": "Social Science", "topic": "History", "type": "long_answer", "marks": 5,
    },
    {
        "id": "c10_sst_002",
        "text": "Q: What is federalism? List its key features.\nA: Federalism is a system where power is divided between central government and state/regional governments. Features: (1) Two levels of government; (2) Each level has its own jurisdiction; (3) Constitution guarantees authority; (4) Revenue sharing; (5) Independent judiciary.",
        "class_level": 10, "subject": "Social Science", "topic": "Political Science", "type": "short_answer", "marks": 3,
    },
    {
        "id": "c10_sst_003",
        "text": "Q: What is the difference between formal and informal sectors of employment in India?\nA: Formal sector: regulated, protected by law, fixed terms, social security (PF, ESI). Informal sector: unregulated, casual employment, no social security, low wages. Most Indian workers (about 90%) are in informal sector.",
        "class_level": 10, "subject": "Social Science", "topic": "Economics", "type": "short_answer", "marks": 3,
    },
    # ── Class 12 Physics ──────────────────────────────────────────────────────
    {
        "id": "c12_phy_001",
        "text": "Q: Derive the expression for electric potential due to a point charge at distance r.\nA: Work done bringing unit positive charge from ∞ to r: V = W/q = (1/4πε₀) × Q/r. Thus V = kQ/r where k = 9×10⁹ Nm²C⁻². Potential is scalar, positive for positive charge, negative for negative charge.",
        "class_level": 12, "subject": "Physics", "topic": "Electrostatics", "type": "long_answer", "marks": 5,
    },
    {
        "id": "c12_phy_002",
        "text": "Q: State Kirchhoff's laws. Apply them to find the current in each branch of a Wheatstone bridge.\nA: KCL: Sum of currents at a node = 0. KVL: Sum of EMFs = Sum of potential drops in a loop. In balanced Wheatstone bridge (P/Q = R/S), no current through galvanometer. Derive using KVL loops.",
        "class_level": 12, "subject": "Physics", "topic": "Current Electricity", "type": "long_answer", "marks": 5,
    },
    {
        "id": "c12_phy_003",
        "text": "Q: What is electromagnetic induction? State Faraday's laws.\nA: Production of EMF due to change in magnetic flux through a circuit. Faraday's Law 1: EMF is induced whenever magnetic flux changes. Law 2: Magnitude of induced EMF = rate of change of flux. ε = –dΦ/dt (Lenz's law gives negative sign).",
        "class_level": 12, "subject": "Physics", "topic": "Electromagnetic Induction & AC", "type": "short_answer", "marks": 3,
    },
    {
        "id": "c12_phy_004",
        "text": "Q: Explain the working of a convex lens and derive the lens maker's formula.\nA: Convex lens converges parallel rays to focal point. Lens maker's formula: 1/f = (n-1)[1/R₁ – 1/R₂] where n = refractive index, R₁ and R₂ are radii of curvature. Derived using refraction at each surface and combining.",
        "class_level": 12, "subject": "Physics", "topic": "Optics", "type": "long_answer", "marks": 5,
    },
    {
        "id": "c12_phy_005",
        "text": "Q: What is de Broglie hypothesis? Derive the expression for de Broglie wavelength.\nA: Every moving particle has wave-like properties. λ = h/p = h/mv where h = Planck's constant. For electron accelerated through potential V: λ = h/√(2meV). Experimental confirmation: Davisson-Germer experiment.",
        "class_level": 12, "subject": "Physics", "topic": "Dual Nature of Matter", "type": "short_answer", "marks": 3,
    },
    # ── Class 12 Chemistry ────────────────────────────────────────────────────
    {
        "id": "c12_chem_001",
        "text": "Q: What is Henry's law? Give two applications.\nA: At constant temperature, the solubility of a gas in a liquid is directly proportional to the partial pressure of the gas. p = KH × x (KH = Henry's constant). Applications: (1) Carbonated beverages (CO₂ dissolved under pressure); (2) Scuba diving (oxygen tanks, avoiding nitrogen narcosis).",
        "class_level": 12, "subject": "Chemistry", "topic": "Solutions", "type": "short_answer", "marks": 3,
    },
    {
        "id": "c12_chem_002",
        "text": "Q: Explain the mechanism of SN1 and SN2 reactions with examples.\nA: SN1 (Unimolecular): Two steps – formation of carbocation then attack by nucleophile. Favoured by tertiary substrates, polar protic solvents. E.g., t-BuBr + OH⁻. SN2 (Bimolecular): One step – backside attack, inversion of configuration. Favoured by primary substrates. E.g., CH₃Br + OH⁻.",
        "class_level": 12, "subject": "Chemistry", "topic": "Haloalkanes & Haloarenes", "type": "long_answer", "marks": 5,
    },
    {
        "id": "c12_chem_003",
        "text": "Q: What is electrochemical series? How is it useful?\nA: Arrangement of elements in increasing order of standard electrode potential (SRP). Uses: (1) Predict feasibility of redox reactions (higher SRP acts as cathode); (2) Compare relative strength of oxidising/reducing agents; (3) Calculate EMF of cell (Ecell = Ecathode – Eanode).",
        "class_level": 12, "subject": "Chemistry", "topic": "Electrochemistry", "type": "short_answer", "marks": 3,
    },
    {
        "id": "c12_chem_004",
        "text": "Q: Give the IUPAC name and structure of: (a) Aldol, (b) Phosgene, (c) Acetophenone.\nA: (a) Aldol = 3-hydroxybutanal, CH₃CH(OH)CH₂CHO; (b) Phosgene = carbonyl dichloride, COCl₂; (c) Acetophenone = 1-phenylethan-1-one, C₆H₅COCH₃.",
        "class_level": 12, "subject": "Chemistry", "topic": "Aldehydes Ketones Carboxylic Acids", "type": "short_answer", "marks": 3,
    },
    # ── Class 12 Mathematics ──────────────────────────────────────────────────
    {
        "id": "c12_math_001",
        "text": "Q: Find dy/dx if y = (sin x)^(cos x).\nA: Take log: ln y = cos x × ln(sin x). Differentiate: (1/y)(dy/dx) = –sin x × ln(sin x) + cos x × (cos x/sin x). dy/dx = y[cos x cot x – sin x ln(sin x)] = (sin x)^(cos x)[cos x cot x – sin x ln(sin x)].",
        "class_level": 12, "subject": "Mathematics", "topic": "Calculus", "type": "long_answer", "marks": 5,
    },
    {
        "id": "c12_math_002",
        "text": "Q: Evaluate ∫₀^π/2 (sin x)/(sin x + cos x) dx.\nA: Use property: ∫₀^a f(x)dx = ∫₀^a f(a-x)dx. Let I = ∫₀^π/2 cos x/(cos x + sin x)dx. Adding both: 2I = ∫₀^π/2 1 dx = π/2. So I = π/4.",
        "class_level": 12, "subject": "Mathematics", "topic": "Calculus", "type": "long_answer", "marks": 5,
    },
    {
        "id": "c12_math_003",
        "text": "Q: Find the area bounded by y = x², y = x + 2, using integration.\nA: Intersection: x²=x+2 → x²-x-2=0 → (x-2)(x+1)=0 → x=-1, x=2. Area = ∫₋₁² (x+2–x²)dx = [x²/2+2x–x³/3]₋₁² = (2+4–8/3)–(1/2–2+1/3) = 9/2 square units.",
        "class_level": 12, "subject": "Mathematics", "topic": "Calculus", "type": "long_answer", "marks": 5,
    },
    {
        "id": "c12_math_004",
        "text": "Q: Show that the relation R on Z defined by (a,b) ∈ R iff (a-b) is divisible by 5 is an equivalence relation.\nA: Reflexive: (a-a)=0 divisible by 5. ✓ Symmetric: if 5|(a-b) then 5|(b-a). ✓ Transitive: 5|(a-b) and 5|(b-c) → 5|(a-c). ✓ Hence R is equivalence relation.",
        "class_level": 12, "subject": "Mathematics", "topic": "Relations and Functions", "type": "short_answer", "marks": 3,
    },
    # ── Class 12 Biology ──────────────────────────────────────────────────────
    {
        "id": "c12_bio_001",
        "text": "Q: Explain Mendel's Law of Independent Assortment with a suitable example.\nA: When two pairs of traits are combined in a hybrid, the segregation of one pair is independent of the other. Dihybrid cross RRYY × rryy → F1 RrYy → F2 ratio 9:3:3:1. The genes for seed colour and shape assort independently (on different chromosomes).",
        "class_level": 12, "subject": "Biology", "topic": "Genetics & Evolution", "type": "long_answer", "marks": 5,
    },
    {
        "id": "c12_bio_002",
        "text": "Q: What is the central dogma of molecular biology? Describe the process of transcription.\nA: Central dogma: DNA → RNA → Protein. Transcription: DNA used as template to synthesise mRNA. Steps: (1) Initiation at promoter sequence; (2) RNA polymerase unwinds DNA; (3) Elongation – free nucleotides join as mRNA; (4) Termination at terminator sequence; (5) mRNA leaves nucleus.",
        "class_level": 12, "subject": "Biology", "topic": "Genetics & Evolution", "type": "long_answer", "marks": 5,
    },
    {
        "id": "c12_bio_003",
        "text": "Q: What is ELISA? How is it used in HIV detection?\nA: ELISA (Enzyme-Linked Immunosorbent Assay) detects antigens or antibodies using enzyme-linked antibodies. In HIV: Patient's serum mixed with HIV antigens. If HIV antibodies present, they bind. Enzyme-labelled secondary antibody added. Substrate added produces colour change. Positive = HIV infection.",
        "class_level": 12, "subject": "Biology", "topic": "Biotechnology", "type": "short_answer", "marks": 3,
    },
    # ── Class 12 Economics ────────────────────────────────────────────────────
    {
        "id": "c12_eco_001",
        "text": "Q: Explain the law of demand with a diagram. What are the exceptions to this law?\nA: Law of demand: Ceteris paribus, as price increases, quantity demanded decreases (inverse relationship). Demand curve slopes downward. Exceptions: (1) Giffen goods (inferior goods); (2) Veblen goods (status symbols); (3) Speculation (expected price rise); (4) Necessities of life.",
        "class_level": 12, "subject": "Economics", "topic": "Microeconomics - Introduction", "type": "long_answer", "marks": 5,
    },
    {
        "id": "c12_eco_002",
        "text": "Q: What is GDP? Explain the expenditure method of calculating GDP.\nA: GDP = total value of all final goods and services produced within a country in one year. Expenditure method: GDP = C + I + G + (X–M) where C = private consumption, I = investment, G = government expenditure, X = exports, M = imports.",
        "class_level": 12, "subject": "Economics", "topic": "Macroeconomics - National Income", "type": "short_answer", "marks": 3,
    },
    # ── Class 12 Accountancy ──────────────────────────────────────────────────
    {
        "id": "c12_acc_001",
        "text": "Q: What is goodwill? Explain the Average Profit Method of valuing goodwill.\nA: Goodwill is an intangible asset representing reputation, brand value, customer loyalty of a business. Average Profit Method: (1) Calculate average profit of past years; (2) Goodwill = Average Profit × Number of Years' Purchase. E.g., Avg profit ₹60,000, 3 years purchase → Goodwill = ₹1,80,000.",
        "class_level": 12, "subject": "Accountancy", "topic": "Partnership Accounts", "type": "short_answer", "marks": 3,
    },
    {
        "id": "c12_acc_002",
        "text": "Q: Prepare a Cash Flow Statement (Operating Activities section) from the given data: Net profit ₹5,00,000; Depreciation ₹80,000; Increase in Debtors ₹40,000; Decrease in Creditors ₹30,000.\nA: Net Profit = 5,00,000; Add: Depreciation = 80,000; Less: Increase in Debtors = (40,000); Less: Decrease in Creditors = (30,000). Net Cash from Operating Activities = ₹5,10,000.",
        "class_level": 12, "subject": "Accountancy", "topic": "Cash Flow Statement", "type": "short_answer", "marks": 3,
    },
]


def get_all_documents():
    """Return (documents, metadatas, ids) for ChromaDB ingestion."""
    docs, metas, ids = [], [], []
    for q in CBSE_QUESTIONS:
        docs.append(q["text"])
        metas.append({
            "class_level": q["class_level"],
            "subject": q["subject"],
            "topic": q["topic"],
            "type": q["type"],
            "marks": q["marks"],
        })
        ids.append(q["id"])
    return docs, metas, ids
