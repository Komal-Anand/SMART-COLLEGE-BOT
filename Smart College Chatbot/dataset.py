"""
SmartCollegeBot - Comprehensive College Intent Dataset
Covers general college queries across admissions, academics, fees, facilities, etc.
"""

INTENTS = [
    # ─── GREETINGS & FAREWELLS ────────────────────────────────────────────────
    {
        "tag": "greeting",
        "patterns": [
            "hello", "hi", "hey", "good morning", "good afternoon", "good evening",
            "howdy", "what's up", "greetings", "hi there", "hello there", "hey there",
            "sup", "hiya", "yo"
        ],
        "responses": [
            "Hello! Welcome to SmartCollegeBot 🎓 How can I help you today?",
            "Hi there! I'm your college assistant. What would you like to know?",
            "Hey! Great to see you. Ask me anything about college life, admissions, or academics!"
        ]
    },
    {
        "tag": "goodbye",
        "patterns": [
            "bye", "goodbye", "see you", "take care", "later", "farewell",
            "see ya", "quit", "exit", "thanks bye", "that's all", "nothing more", "i'm done"
        ],
        "responses": [
            "Goodbye! Best of luck with your studies! 🌟",
            "Take care! Feel free to come back whenever you have more questions.",
            "See you later! Good luck with everything! 🎓"
        ]
    },
    {
        "tag": "thanks",
        "patterns": [
            "thanks", "thank you", "thank you so much", "thanks a lot", "many thanks",
            "much appreciated", "that was helpful", "great help", "awesome thanks", "cheers"
        ],
        "responses": [
            "You're welcome! Happy to help anytime 😊",
            "Glad I could help! Let me know if you have more questions.",
            "Anytime! That's what I'm here for 🎓"
        ]
    },

    # ─── ADMISSIONS ───────────────────────────────────────────────────────────
    {
        "tag": "admission_process",
        "patterns": [
            "how to apply", "admission process", "how do I get admission", "steps for admission",
            "admission procedure", "how to take admission", "apply for college",
            "what is the admission process", "how can i join", "application process",
            "how to enroll", "enrollment process", "registration process"
        ],
        "responses": [
            "📋 General Admission Process:\n\n1. **Register Online** – Fill the application form on the college portal\n2. **Submit Documents** – Academic transcripts, ID proof, passport photos\n3. **Entrance Exam** – Appear for relevant entrance test (JEE/NEET/CUET etc.) if required\n4. **Merit List** – Check cutoff and merit list on the college website\n5. **Counseling** – Attend counseling/interview session\n6. **Fee Payment** – Pay the admission fee within the deadline\n7. **Document Verification** – Submit original documents for verification\n\nTip: Always check the college's official website for exact deadlines!",
        ]
    },
    {
        "tag": "admission_eligibility",
        "patterns": [
            "eligibility for admission", "who can apply", "minimum marks required",
            "eligibility criteria", "what are the requirements", "qualification needed",
            "marks required for admission", "percentage required", "criteria for admission",
            "am i eligible", "can i apply", "eligibility for btech", "eligibility for mba"
        ],
        "responses": [
            "📌 Common Eligibility Criteria:\n\n**For B.Tech/BE:**\n• 10+2 with PCM (Physics, Chemistry, Math) — minimum 50–60%\n• Valid JEE Main/Advanced score (for top institutes)\n\n**For BCA/BBA/B.Com:**\n• 10+2 in any stream — minimum 45–55%\n\n**For MBA:**\n• Graduation in any discipline — minimum 50%\n• CAT/MAT/XAT/CMAT score required\n\n**For M.Tech:**\n• B.Tech/BE with minimum 55–60%\n• GATE score preferred\n\n*Note: Criteria vary by college. Reserved category students may get 5% relaxation.*"
        ]
    },
    {
        "tag": "admission_documents",
        "patterns": [
            "documents required for admission", "what documents do I need",
            "documents needed", "papers required", "admission documents",
            "what to bring for admission", "required certificates", "documents for enrollment"
        ],
        "responses": [
            "📄 Documents Typically Required for Admission:\n\n✅ 10th Marksheet & Certificate\n✅ 12th Marksheet & Certificate (or Graduation for PG)\n✅ Transfer Certificate (TC) from previous school/college\n✅ Migration Certificate (if from another board/university)\n✅ Character Certificate\n✅ Caste/Category Certificate (if applicable — SC/ST/OBC)\n✅ Aadhar Card / Voter ID / Passport (any government ID)\n✅ Passport-size photographs (6–8 copies)\n✅ Entrance Exam Scorecard (JEE/NEET/CAT etc.)\n✅ Medical Fitness Certificate\n\n*Bring both originals and photocopies. Some colleges also need an affidavit from parents.*"
        ]
    },
    {
        "tag": "admission_dates",
        "patterns": [
            "when does admission start", "admission dates", "last date for admission",
            "admission schedule", "when to apply", "application deadline",
            "when is admission open", "admission open", "form submission last date"
        ],
        "responses": [
            "📅 Typical Admission Timeline (General Guide):\n\n| Program | Application Period | Exam Dates | Result/Counseling |\n|---------|-------------------|-----------|-------------------|\n| B.Tech  | Jan – May | Apr – May | June – July |\n| MBBS/BDS| Feb – May | May (NEET) | July – Aug |\n| MBA     | Oct – Mar | Nov – Mar | Apr – May |\n| B.Sc/BA/B.Com | Mar – June | — | June – July |\n| M.Tech  | Feb – June | Feb (GATE) | May – July |\n\n⚠️ These are general timelines. Always verify exact dates on the official college/university website or NTA/respective exam authority."
        ]
    },

    # ─── FEES & SCHOLARSHIPS ──────────────────────────────────────────────────
    {
        "tag": "fee_structure",
        "patterns": [
            "fee structure", "how much is the fee", "fees for btech", "course fees",
            "annual fee", "total fee", "fees details", "cost of course",
            "how much does it cost", "tuition fees", "semester fees", "fees information",
            "fee payment", "how much to pay"
        ],
        "responses": [
            "💰 General Fee Structure (Approximate Annual Fees — India):\n\n| Program | Government College | Private College |\n|---------|-------------------|------------------|\n| B.Tech/BE | ₹50,000 – ₹1.5L | ₹80,000 – ₹4L |\n| MBBS | ₹15,000 – ₹1L | ₹10L – ₹25L |\n| MBA | ₹30,000 – ₹80,000 | ₹3L – ₹20L |\n| BCA/BBA/B.Com | ₹20,000 – ₹50,000 | ₹50,000 – ₹1.5L |\n| M.Tech | ₹30,000 – ₹80,000 | ₹1L – ₹3L |\n| B.Sc | ₹10,000 – ₹30,000 | ₹30,000 – ₹1L |\n\n*Fees include tuition, development charges & exam fee. Hostel, mess & transport are additional.*"
        ]
    },
    {
        "tag": "scholarships",
        "patterns": [
            "scholarship", "scholarships available", "how to get scholarship",
            "financial aid", "merit scholarship", "scholarship eligibility",
            "free education", "fee waiver", "education loan", "scholarship for poor students",
            "scholarship for sc st", "national scholarship", "government scholarship"
        ],
        "responses": [
            "🎓 Major Scholarships for Students in India:\n\n**Government Scholarships:**\n• **NSP (National Scholarship Portal)** – nsp.gov.in — for SC/ST/OBC/minority/merit students\n• **PM Scholarship Scheme** – for children of ex-servicemen\n• **State Government Scholarships** – vary by state\n• **Inspire Scholarship** – for science students, ₹80,000/year\n• **AICTE Pragati & Saksham** – for girl students / PwD in technical education\n\n**College-level:**\n• Merit-based fee waivers (top rankers in entrance exams)\n• Sports quota scholarships\n• Need-based financial assistance\n\n**Education Loans:**\n• SBI Scholar Loan, HDFC Credila, Axis Bank — up to ₹40L\n• Moratorium during study period\n\n💡 Tip: Apply on NSP portal early — deadlines are usually October–November."
        ]
    },
    {
        "tag": "hostel_fees",
        "patterns": [
            "hostel fees", "hostel charges", "hostel rent", "accommodation fees",
            "how much is hostel", "hostel cost", "hostel fee structure", "hostel expenses"
        ],
        "responses": [
            "🏠 Hostel & Accommodation Fees (Approximate):\n\n| Type | Annual Cost |\n|------|-------------|\n| Double-sharing room | ₹40,000 – ₹80,000 |\n| Triple-sharing room | ₹25,000 – ₹55,000 |\n| Single room | ₹70,000 – ₹1.5L |\n| Mess charges (meals) | ₹25,000 – ₹50,000/year |\n\n**Included in most hostel fees:**\n✅ Furnished room (bed, table, chair, wardrobe)\n✅ 24/7 security\n✅ Wi-Fi connectivity\n✅ Common bathrooms / attached bathroom (single rooms)\n\n*Exact fees vary by college. Contact the hostel warden or admin office for official rates.*"
        ]
    },

    # ─── COURSES & PROGRAMS ───────────────────────────────────────────────────
    {
        "tag": "courses_offered",
        "patterns": [
            "courses offered", "programs available", "what courses are there",
            "list of courses", "available courses", "which programs", "what can I study",
            "course list", "what are the departments", "streams available",
            "UG courses", "PG courses", "undergraduate programs", "postgraduate programs"
        ],
        "responses": [
            "📚 Common Programs Offered by Colleges:\n\n**Undergraduate (UG — 3/4 years):**\n• B.Tech/BE (Engineering — CS, ECE, Mech, Civil, AI/ML, etc.)\n• MBBS / BDS (Medical & Dental)\n• B.Sc (Physics, Chemistry, Biology, Math, IT, Nursing)\n• B.Com / BBA / BCA\n• BA (Arts, Economics, Psychology, English, etc.)\n• BPharma / B.Arch / B.Ed\n\n**Postgraduate (PG — 2 years):**\n• M.Tech / ME | MBA / PGDM\n• M.Sc | M.Com | MA | MCA | LLM\n\n**Diploma & Certificate Courses:**\n• Polytechnic Diploma (3 years after 10th)\n• Short-term certifications (6 months – 1 year)\n\n**PhD / Doctoral Programs** also available at most universities."
        ]
    },
    {
        "tag": "course_duration",
        "patterns": [
            "duration of course", "how many years", "course length",
            "how long is btech", "how long is mbbs", "how long is mba",
            "years in college", "years to complete", "course duration"
        ],
        "responses": [
            "⏱️ Course Durations:\n\n| Program | Duration |\n|---------|----------|\n| B.Tech / BE | 4 years |\n| MBBS | 5.5 years (incl. 1-yr internship) |\n| BDS | 5 years (incl. 1-yr internship) |\n| BBA / BCA / B.Sc | 3 years |\n| BA / B.Com | 3 years |\n| B.Arch | 5 years |\n| MBA / PGDM | 2 years |\n| M.Tech / M.Sc / MA / M.Com | 2 years |\n| MCA | 2 years |\n| PhD | 3–5 years |\n| Polytechnic Diploma | 3 years |\n| Lateral Entry (B.Tech) | 3 years (2nd year onwards) |"
        ]
    },

    # ─── ACADEMIC CALENDAR & EXAMS ────────────────────────────────────────────
    {
        "tag": "exam_schedule",
        "patterns": [
            "exam schedule", "when are exams", "exam dates", "examination timetable",
            "when is the exam", "exam time table", "semester exam dates",
            "internal exams", "external exams", "mid term exam", "end term exam"
        ],
        "responses": [
            "📅 Typical Academic & Exam Calendar:\n\n**Semester 1 (July – November):**\n• Classes: July – October\n• Mid-Term Exams: September\n• End-Term Exams: November\n\n**Semester 2 (January – May):**\n• Classes: January – April\n• Mid-Term Exams: March\n• End-Term Exams: May\n\n**Result Declaration:** Usually 3–4 weeks after end-term exams\n\n📌 Internal Assessment (CIE): Continuous — includes assignments, quizzes, practicals\n📌 External Exam (SEE): Semester-end theory papers\n\n*Always check your college's academic calendar on the official website or student portal for exact dates.*"
        ]
    },
    {
        "tag": "result",
        "patterns": [
            "result", "how to check result", "when will result come", "result date",
            "marksheet", "scorecard", "grade card", "semester result",
            "how to see result", "results declared", "check my marks", "CGPA", "SGPA"
        ],
        "responses": [
            "📊 How to Check Your Result:\n\n1. Visit your college/university's official website\n2. Go to the **Student Portal / Examination Section**\n3. Login with your **Enrollment Number / Registration ID**\n4. Select **Semester & Year**\n5. Download your **Grade Card / Marksheet**\n\n**Understanding Grades:**\n| Grade | Points | Meaning |\n|-------|--------|---------|\n| O | 10 | Outstanding |\n| A+ | 9 | Excellent |\n| A | 8 | Very Good |\n| B+ | 7 | Good |\n| B | 6 | Above Average |\n| C | 5 | Average |\n| F | 0 | Fail |\n\n**SGPA** = Semester Grade Point Average\n**CGPA** = Cumulative GPA across all semesters\n\n💡 Worried about a result? You can apply for re-evaluation within 2 weeks of result declaration."
        ]
    },
    {
        "tag": "attendance",
        "patterns": [
            "attendance", "attendance requirement", "minimum attendance",
            "how much attendance required", "attendance policy", "shortage of attendance",
            "attendance rules", "attendance percentage", "proxy attendance",
            "attendance problem", "low attendance"
        ],
        "responses": [
            "📋 Attendance Policy:\n\n**Minimum Required Attendance:** 75% in most colleges (some require 85%)\n\n**Consequences of Low Attendance:**\n• Below 75% → Debarred from appearing in semester exams\n• 65–74% → Condonation possible with medical/valid reason (at college's discretion)\n• Below 65% → Typically detained (must repeat the semester)\n\n**Attendance Calculation:**\n```\nAttendance % = (Classes Attended / Total Classes Held) × 100\n```\n\n**Tips to Maintain Attendance:**\n✅ Check attendance regularly on the student portal\n✅ Apply for medical leave with a doctor's certificate immediately\n✅ Meet your class teacher/mentor if you're approaching the shortage threshold\n\n⚠️ Sports/cultural events, NCC/NSS activities may grant attendance as per college policy."
        ]
    },
    {
        "tag": "backlog",
        "patterns": [
            "backlog", "back paper", "failed in exam", "how to clear backlog",
            "supplementary exam", "ex student exam", "fail in semester",
            "reappear in exam", "how to pass failed subject", "arrear exam"
        ],
        "responses": [
            "📝 Clearing Backlogs / Arrears:\n\n**What is a Backlog?**\nA subject you failed in the semester examination.\n\n**How to Clear It:**\n1. **Supplementary/Back Exam** – Most colleges conduct back paper exams in June–July or November–December\n2. **Re-Appear** – Fill the back exam form (available on student portal)\n3. **Improvement Exam** – Some universities allow improvement for low grades too\n\n**Important Rules:**\n• Number of allowed attempts varies (usually unlimited, but time-bound)\n• Maximum backlog limit for graduation: typically all subjects must be cleared within N+2 years\n• CGPA gets updated after clearing backlog\n• Some companies have a 'no active backlog' criterion for campus placements\n\n💡 Consult your academic advisor or examination cell immediately after results."
        ]
    },

    # ─── LIBRARY ──────────────────────────────────────────────────────────────
    {
        "tag": "library",
        "patterns": [
            "library", "library timings", "library hours", "how to use library",
            "borrow books", "library membership", "library facilities",
            "e-library", "digital library", "online resources", "library rules",
            "issue books", "return books", "library fine"
        ],
        "responses": [
            "📚 Library Information:\n\n**Timings:** Generally 8:00 AM – 9:00 PM (Mon–Sat); 10 AM – 5 PM (Sun)\n\n**Services Available:**\n✅ Book lending (usually 2–4 books at a time for 7–14 days)\n✅ Reference section (in-library reading)\n✅ E-journals & Research databases (IEEE, Springer, Elsevier, JSTOR)\n✅ Newspaper & Magazine section\n✅ Digital library / e-learning terminals\n✅ Printing & photocopying\n\n**How to Borrow Books:**\n1. Get your Library Card (issued at the time of admission)\n2. Search for books in the online catalog (OPAC)\n3. Present your library card at the issue desk\n4. Return within the due date to avoid fines\n\n**Fines:** Typically ₹2–₹5 per day per book for late returns\n\n💡 Access e-resources like NPTEL, SWAYAM, and NDLI (National Digital Library) free with student registration."
        ]
    },

    # ─── HOSTEL & ACCOMMODATION ───────────────────────────────────────────────
    {
        "tag": "hostel_facilities",
        "patterns": [
            "hostel facilities", "hostel rules", "hostel amenities", "hostel life",
            "is hostel available", "hostel for boys", "hostel for girls",
            "hostel timings", "hostel in time", "stay in college", "on campus housing"
        ],
        "responses": [
            "🏠 Hostel Facilities & Rules:\n\n**Facilities Provided:**\n✅ Furnished rooms (Single/Double/Triple sharing)\n✅ 24/7 security & CCTV surveillance\n✅ Wi-Fi internet access\n✅ Mess facility (veg + non-veg options)\n✅ Common room with TV\n✅ Indoor games (TT, carom, chess)\n✅ Laundry facility\n✅ Medical room / first aid\n✅ Visitor room\n\n**Common Hostel Rules:**\n• Curfew: Boys – 10 PM, Girls – 9 PM (varies by college)\n• Visitors allowed only in visitor areas during specified hours\n• No alcohol, smoking, or ragging — strict action taken\n• Maintain cleanliness & noise discipline\n• Visitors of opposite gender not allowed in rooms\n\n**Admission to Hostel:**\nFill the hostel application form during college admission. Allotment is usually on a first-come, first-served or merit basis."
        ]
    },

    # ─── TRANSPORT ────────────────────────────────────────────────────────────
    {
        "tag": "transport",
        "patterns": [
            "transport facility", "bus facility", "college bus", "transportation",
            "bus routes", "bus timings", "how to commute", "travel to college",
            "college transport fee", "shuttle service"
        ],
        "responses": [
            "🚌 College Transport Facilities:\n\n**Services Typically Available:**\n• College buses covering major city routes and surrounding areas\n• Timings: Morning pick-up 7:00–8:30 AM | Evening drop 4:00–6:00 PM\n• AC & Non-AC buses available\n\n**Fee:** Usually ₹8,000 – ₹20,000/year depending on distance\n\n**How to Avail:**\n1. Fill the transport application form at the Transport Office\n2. Pay the transport fee for the semester/year\n3. Collect your bus pass\n4. Check the bus route chart for your area\n\n**For Outstation Students:**\n• Railway/bus station pickup available on joining day\n• Nearby railway stations are usually 2–10 km from most campuses\n\n💡 If college transport doesn't cover your route, check for local city buses, auto, or cab-pooling with classmates."
        ]
    },

    # ─── PLACEMENTS & CAREER ──────────────────────────────────────────────────
    {
        "tag": "placements",
        "patterns": [
            "placements", "campus placement", "job placement", "recruitment",
            "placement statistics", "highest package", "average package",
            "companies that hire", "which companies visit", "placement cell",
            "placement process", "off campus", "on campus placement"
        ],
        "responses": [
            "💼 Campus Placements — What to Expect:\n\n**Typical Placement Process:**\n1. **Pre-Placement Talk (PPT)** – Company presents itself to students\n2. **Aptitude Test** – Quantitative, Verbal, Logical Reasoning\n3. **Technical Round** – Domain-specific questions (DSA, DBMS, Networks etc.)\n4. **HR Interview** – Behavioral, situational, personality questions\n5. **Offer Letter** – Selected students receive offer letters\n\n**Average Packages by Sector (India):**\n| Sector | Fresher CTC |\n|--------|-------------|\n| IT/Software | ₹3.5L – ₹12L |\n| Core Engineering | ₹3L – ₹8L |\n| MBA (Finance/Marketing) | ₹5L – ₹15L |\n| Government PSU | ₹4L – ₹12L |\n| Analytics/Data Science | ₹5L – ₹14L |\n\n**Top Recruiters (General):** TCS, Infosys, Wipro, Cognizant, Accenture, HCL, Amazon, Deloitte, IBM, L&T\n\n💡 Prepare: LeetCode / GeeksforGeeks for coding, aptitude books (RS Aggarwal), mock interviews."
        ]
    },
    {
        "tag": "internship",
        "patterns": [
            "internship", "how to get internship", "summer internship", "industrial training",
            "IT training", "internship opportunities", "stipend for internship",
            "internship after semester", "where to find internship", "internship portal"
        ],
        "responses": [
            "💻 Internships & Industrial Training:\n\n**When to Do Internships:**\n• After 2nd year (Summer — May/June): Most common for tech students\n• After 3rd year: Pre-final year — often converts to full-time\n• B.Tech students must complete 4–6 weeks of mandatory IT Training\n\n**Where to Find Internships:**\n🔗 Internshala (internshala.com) — Most popular for Indian students\n🔗 LinkedIn — Apply via job postings\n🔗 LetsIntern / HelloIntern\n🔗 Company websites (apply directly)\n🔗 Campus Placement Cell notices\n\n**What Recruiters Look For:**\n✅ Strong fundamentals (DSA, DBMS, OS)\n✅ Projects on GitHub\n✅ Good communication skills\n✅ Certifications (Google, AWS, Coursera)\n\n**Stipend Range:** ₹5,000 – ₹50,000/month (varies widely)\n\n💡 Tip: Apply at least 2–3 months before the internship start date."
        ]
    },
    {
        "tag": "higher_education",
        "patterns": [
            "after graduation", "higher studies", "masters abroad", "MS after btech",
            "MBA after graduation", "study abroad", "GRE", "GMAT", "IELTS", "TOEFL",
            "foreign university", "US university", "UK university", "PhD abroad"
        ],
        "responses": [
            "🌍 Higher Education Options After Graduation:\n\n**In India:**\n• M.Tech/M.Sc — via GATE exam (IITs, NITs, IIITs)\n• MBA — via CAT/MAT/XAT (IIMs and top B-schools)\n• PhD — via UGC NET / CSIR / institute-specific entrance\n\n**Abroad (MS / MBA / PhD):**\n| Exam | Purpose |\n|------|---------|\n| GRE | MS/PhD in USA, Canada, Germany |\n| GMAT | MBA in USA, UK, Europe |\n| IELTS / TOEFL | English proficiency (required everywhere) |\n| SAT | UG admissions abroad |\n\n**Top Destinations:** USA 🇺🇸 | UK 🇬🇧 | Canada 🇨🇦 | Germany 🇩🇪 | Australia 🇦🇺 | Singapore 🇸🇬\n\n**Timeline for MS in USA:**\n• Start GRE/IELTS prep: ~1.5–2 years before intake\n• Applications: September–December for Fall intake\n• Visa (F-1): April–July\n\n💡 Popular portals: GradCafe, Yocket, Shiksha Study Abroad"
        ]
    },

    # ─── FACILITIES ───────────────────────────────────────────────────────────
    {
        "tag": "sports_facilities",
        "patterns": [
            "sports", "sports facilities", "gym", "ground", "sports activities",
            "cricket ground", "basketball court", "football ground", "swimming pool",
            "sports room", "indoor games", "outdoor sports", "fitness center"
        ],
        "responses": [
            "🏟️ Sports & Fitness Facilities:\n\n**Outdoor Sports:**\n⚽ Football / Cricket / Athletics Ground\n🏸 Badminton / Tennis Courts\n🏐 Volleyball / Basketball Courts\n\n**Indoor Sports:**\n🏓 Table Tennis | ♟️ Chess | 🥊 Boxing / Martial Arts\n🎳 Carrom | Billiards (in some colleges)\n\n**Fitness:**\n🏋️ Gymnasium with modern equipment\n🏊 Swimming pool (in many well-equipped colleges)\n\n**Participation:**\n• Intra-college sports tournaments (annual sports meet)\n• Inter-college/university level competitions\n• State & national level representation possible\n\n**Sports Quota:** Many colleges offer sports quota admission with relaxed cutoffs for state/national level players.\n\n💡 Regular sports participation can earn you additional attendance credit and certificates in many colleges!"
        ]
    },
    {
        "tag": "cafeteria",
        "patterns": [
            "cafeteria", "canteen", "food", "mess", "where to eat",
            "college food", "food facilities", "mess menu", "canteen timings",
            "veg food", "non veg food", "food quality", "tiffin service"
        ],
        "responses": [
            "🍽️ Cafeteria & Food Facilities:\n\n**Types of Food Facilities:**\n• **Mess** – For hostelites; monthly subscription; full meals\n• **Canteen / Food Court** – Open to all; à la carte; faster options\n• **Tuck Shop** – Snacks, beverages, stationery\n\n**Typical Meal Timings (Mess):**\n| Meal | Timing |\n|------|--------|\n| Breakfast | 7:00 AM – 9:00 AM |\n| Lunch | 12:00 PM – 2:00 PM |\n| Evening Snacks | 4:30 PM – 6:00 PM |\n| Dinner | 7:30 PM – 9:30 PM |\n\n**Food Options:**\n✅ Veg & Non-Veg both available in most colleges\n✅ South Indian, North Indian, Chinese cuisine options\n✅ Special menu on festivals\n\n**Canteen Timings:** Usually 7:30 AM – 9:00 PM\n\n💡 Mess committees (run by students) often manage quality — raise complaints through your student representative."
        ]
    },
    {
        "tag": "medical_facilities",
        "patterns": [
            "medical facility", "health center", "sick room", "doctor in college",
            "medical room", "hospital", "emergency medical", "first aid",
            "health insurance", "ambulance", "college doctor", "dispensary"
        ],
        "responses": [
            "🏥 Medical Facilities on Campus:\n\n**What's Available:**\n✅ On-campus Health Center / Dispensary\n✅ Qualified doctor & nursing staff\n✅ First aid room in hostels\n✅ Ambulance service (24/7 in most colleges)\n✅ Tie-up with nearby private/government hospitals\n\n**Services:**\n• OPD consultation (free or nominal charge for students)\n• Common medicines dispensed free\n• Blood pressure, sugar, basic health checkups\n• Mental health counseling (increasingly available)\n\n**Health Insurance:**\n• Many colleges provide group health insurance (₹1L – ₹5L coverage)\n• Check during admission whether this is included in your fee\n\n**Emergency:** Always save the college health center number and your warden's number on your phone.\n\n🚨 For emergencies, dial 112 (National Emergency) or 108 (Ambulance)"
        ]
    },
    {
        "tag": "wifi_internet",
        "patterns": [
            "wifi", "internet", "internet facility", "wifi on campus", "network",
            "broadband", "wi-fi password", "internet speed", "connectivity",
            "online resources", "internet access", "campus network"
        ],
        "responses": [
            "📶 Wi-Fi & Internet Facilities:\n\n**Campus Wi-Fi:**\n✅ High-speed Wi-Fi typically available across campus (classrooms, labs, library, hostels)\n✅ Speed: Usually 100 Mbps – 1 Gbps (shared)\n✅ Login with your student credentials (Registration No. + Password)\n\n**Hostel Internet:**\n• Wi-Fi included in hostel fees at most colleges\n• Some colleges provide LAN port in rooms\n• Fair-usage policy may apply (50–100 GB/month)\n\n**How to Connect:**\n1. Connect to campus Wi-Fi SSID\n2. Open browser → captive portal appears\n3. Login with your student ID\n\n**Blocked/Restricted:**\n• Some colleges restrict gaming, torrent, social media during peak hours\n• VPN usage may be blocked\n\n💡 For academics: Access NPTEL, SWAYAM, NDLI, IEEE Xplore, and Google Scholar free via campus network."
        ]
    },

    # ─── STUDENT LIFE & ACTIVITIES ────────────────────────────────────────────
    {
        "tag": "clubs_societies",
        "patterns": [
            "clubs", "societies", "student clubs", "cultural club", "technical club",
            "drama club", "music club", "coding club", "photography club", "robotics",
            "how to join clubs", "extracurricular activities", "student activities",
            "student organizations", "NSS", "NCC"
        ],
        "responses": [
            "🎭 Student Clubs & Societies:\n\n**Technical Clubs:**\n🤖 Robotics Club | 💻 Coding/Programming Club | 🔬 Science Society | 📡 IEEE/ACM Student Chapter\n\n**Cultural Clubs:**\n🎭 Drama & Theatre | 🎵 Music Club | 💃 Dance Club | 🎨 Fine Arts Club | 📷 Photography Club\n\n**Service Organizations:**\n🌱 NSS (National Service Scheme) — community service, earn credits\n🎖️ NCC (National Cadet Corps) — military training, leadership\n\n**Entrepreneurship & Business:**\n💡 E-Cell / Entrepreneurship Club | 📊 Business Club | 🗣️ Debate & MUN Club\n\n**How to Join:**\n• Watch for club recruitment drives at the start of the semester\n• Attend club orientation sessions (usually August–September)\n• Some clubs have tryouts; others are open to all\n\n💡 Active participation in clubs counts toward extra-curricular certificates, which add great value to your resume!"
        ]
    },
    {
        "tag": "events_fests",
        "patterns": [
            "college fest", "annual fest", "tech fest", "cultural fest", "events",
            "college events", "workshops", "seminars", "hackathon", "competitions",
            "sports meet", "annual day", "farewell", "fresher party"
        ],
        "responses": [
            "🎉 College Events & Fests:\n\n**Annual Fests (Typical Calendar):**\n🎭 **Cultural Fest** – Dance, music, drama, fashion show (usually Feb–March)\n🔬 **Technical Fest / Tech Symposium** – Coding contests, robotics, paper presentations (October–November)\n🏆 **Sports Meet** – Inter-department & inter-college sports (December–January)\n🎓 **Annual Day / Convocation** – Graduation ceremony with awards\n\n**Other Events:**\n• Freshers' Welcome Party (August–September)\n• Farewell Function for final-year students (April–May)\n• National/International level hackathons & workshops\n• Industry expert guest lectures\n• MUN (Model United Nations) conferences\n\n**Participation Benefits:**\n✅ Certificates for CV\n✅ Cash prizes in competitions\n✅ Networking with students from other colleges\n✅ Platform to showcase talents\n\n💡 Follow your college's social media pages (Instagram/LinkedIn) for event updates!"
        ]
    },

    # ─── ACADEMICS & SYLLABUS ─────────────────────────────────────────────────
    {
        "tag": "syllabus",
        "patterns": [
            "syllabus", "curriculum", "subjects", "what will I study",
            "course content", "topics covered", "study material",
            "semester subjects", "first year subjects", "core subjects",
            "elective subjects", "credit system"
        ],
        "responses": [
            "📖 Syllabus & Curriculum:\n\n**For B.Tech (CSE) — Sample:**\n\n*Year 1:* Mathematics, Physics, Chemistry, Programming Fundamentals (C/Python), Engineering Drawing, Communication Skills\n\n*Year 2:* Data Structures, OOP (Java/C++), DBMS, Computer Organization, Discrete Math, Statistics\n\n*Year 3:* Algorithms, Operating Systems, Computer Networks, Software Engineering, Web Development, Electives\n\n*Year 4:* AI/ML, Cloud Computing, Capstone Project, Electives\n\n**Credit System (CBCS):**\n• Each subject has credit weightage (2–4 credits)\n• Total: ~160–180 credits for B.Tech graduation\n• CGPA calculated on credit-weighted average\n\n**Electives:** You can choose your specialization in 3rd–4th year (AI/ML, Cybersecurity, IoT, Data Science, etc.)\n\n💡 Download the complete syllabus PDF from your university's official website under the 'Academics' section."
        ]
    },

    # ─── ANTI-RAGGING ─────────────────────────────────────────────────────────
    {
        "tag": "anti_ragging",
        "patterns": [
            "ragging", "anti ragging", "ragging complaint", "someone is ragging me",
            "ragging helpline", "what to do if ragged", "ragging rules",
            "eve teasing", "harassment in college", "bullying"
        ],
        "responses": [
            "🚫 Anti-Ragging Policy — Zero Tolerance:\n\nRagging is a **criminal offense** in India under UGC Regulations 2009.\n\n**What Counts as Ragging:**\n• Physical abuse, humiliation, or forced acts by seniors\n• Mental harassment, abusive language\n• Forcing consumption of alcohol\n• Any act that causes distress to a student\n\n**What to Do if You Face Ragging:**\n📞 **Anti-Ragging Helpline:** 1800-180-5522 (UGC — Free, 24/7)\n📧 **Online Complaint:** helpline.antiragging.in\n🏫 Contact your Hostel Warden, Dean of Students, or Principal immediately\n\n**Punishment for Offenders:**\n• Rustication / Expulsion from college\n• FIR and criminal charges\n• Cancellation of scholarship\n\n**Your Rights:**\n✅ Right to study in a safe environment\n✅ Complaint to be kept confidential\n✅ Protection from victimization after complaint\n\nYou are not alone — speak up immediately!"
        ]
    },

    # ─── GRIEVANCES & ADMINISTRATION ─────────────────────────────────────────
    {
        "tag": "grievance",
        "patterns": [
            "complaint", "grievance", "problem in college", "how to file complaint",
            "who to contact for complaint", "student grievance", "raise complaint",
            "report issue", "ombudsman", "RTI"
        ],
        "responses": [
            "📣 Filing a Grievance / Complaint:\n\n**Step 1 – Internal Mechanism:**\n• Talk to your Class Teacher / Faculty Advisor first\n• Escalate to Head of Department (HOD)\n• Then to Dean of Student Affairs / Principal\n\n**Step 2 – Formal Complaint:**\n• Fill the Student Grievance Form (available at the admin office or student portal)\n• Submit to the Student Grievance Redressal Cell (SGRC)\n\n**Step 3 – External:**\n• **UGC Grievance Portal:** grievance.ugc.ac.in\n• **National Student Helpline:** 14417\n• **AICTE Grievance (for technical colleges):** aicte-grievance.in\n• **RTI Application** – for information from government colleges\n\n**Types of Grievances:**\n📋 Academic (marks, evaluation) | 💰 Financial (fees) | 🏠 Hostel | 🚌 Transport | 🤝 Faculty behavior\n\n💡 Keep a copy of all complaints submitted and note the acknowledgment receipt number."
        ]
    },

    # ─── CAREER GUIDANCE ──────────────────────────────────────────────────────
    {
        "tag": "career_guidance",
        "patterns": [
            "career guidance", "what career to choose", "career options after btech",
            "career options after bsc", "what to do after college", "career counseling",
            "best career in tech", "which field to choose", "IT or core",
            "best jobs", "career advice"
        ],
        "responses": [
            "🎯 Career Guidance:\n\n**After B.Tech (CS/IT):**\n💻 Software Developer/Engineer (most common)\n📊 Data Scientist / ML Engineer\n☁️ Cloud/DevOps Engineer\n🔒 Cybersecurity Analyst\n🎮 Game Developer\n📱 Mobile App Developer\n🏛️ Government IT jobs (UPSC, SSC, Bank PO)\n\n**After B.Tech (Core — Mech/Civil/ECE):**\n🏗️ Core engineering roles (BHEL, L&T, ISRO)\n📡 Electronics / VLSI / Embedded Systems\n🛣️ Civil (PWD, NHAI, urban planning)\n🎓 M.Tech → Research/Academia\n💼 MBA → Management roles\n\n**After B.Sc / Arts / Commerce:**\n📈 Finance, Banking, Accounting (CA/CFA/CMA)\n📚 Education / Teaching\n🌐 Digital Marketing / Content\n⚖️ Law (LLB after graduation)\n🏛️ Civil Services (IAS/IPS — UPSC)\n\n💡 Your career is shaped by: Skills + Experience + Networking. Start early!\nVisit: LinkedIn, Glassdoor, AmbitionBox for real job insights."
        ]
    },

    # ─── FACULTY & DEPARTMENTS ────────────────────────────────────────────────
    {
        "tag": "faculty",
        "patterns": [
            "faculty", "professors", "teachers", "who teaches", "faculty details",
            "department faculty", "contact faculty", "faculty list", "faculty qualifications",
            "visiting faculty", "assistant professor"
        ],
        "responses": [
            "👨‍🏫 Faculty & Academic Staff:\n\n**Faculty Designations:**\n• Assistant Professor (Entry level)\n• Associate Professor (Mid-level)\n• Professor / Senior Professor\n• HOD (Head of Department)\n• Dean (Academic / Research / Students)\n\n**Qualifications:**\n• Minimum: Master's degree (M.Tech/M.Sc/MBA) + NET/GATE\n• Preferred: PhD in relevant field\n• Industry experience valued in technical colleges\n\n**How to Contact Faculty:**\n📧 College email (typically name@collegename.edu.in)\n🏢 During office hours (posted on department notice board)\n📋 Faculty cabin hours usually 8 AM – 5 PM\n\n**Finding Faculty Info:**\n• College website → Academics → Departments → Faculty Directory\n• Student portal → Course page → Faculty contact\n\n💡 Build good relationships with faculty — they are key references for internships, research, and recommendation letters!"
        ]
    },

    # ─── ONLINE LEARNING ──────────────────────────────────────────────────────
    {
        "tag": "online_learning",
        "patterns": [
            "online courses", "NPTEL", "MOOC", "Coursera", "online certificate",
            "e-learning", "distance learning", "correspondence", "online degree",
            "free courses", "Swayam", "edX", "Udemy for students"
        ],
        "responses": [
            "🖥️ Online Learning Resources for College Students:\n\n**Free Indian Platforms:**\n📚 **SWAYAM** (swayam.gov.in) — Government of India; free courses from IITs/IIMs; NPTEL courses earn actual college credits\n📺 **NPTEL** (nptel.ac.in) — Engineering & Science courses by IIT/IISc professors; proctored exams for certificates\n📖 **NDLI** (ndl.gov.in) — National Digital Library; free textbooks & research papers\n\n**Global Platforms:**\n🎓 **Coursera** — Audit free; certificates with financial aid\n🎓 **edX** — MIT, Harvard courses; audit free\n🎓 **Khan Academy** — Math, Science fundamentals\n💻 **freeCodeCamp** — Web development, completely free\n🔧 **Google Skill Boost** — Cloud, Data, AI certifications\n\n**Paid (Worth it):**\n• **Udemy** — Affordable, practical skills (often <₹500 in sale)\n• **LinkedIn Learning** — Professional development\n\n💡 NPTEL courses can replace internal elective subjects in many AICTE-affiliated colleges — ask your HOD!"
        ]
    },

    # ─── ANTI-DRUG & DISCIPLINE ───────────────────────────────────────────────
    {
        "tag": "rules_regulations",
        "patterns": [
            "college rules", "discipline rules", "code of conduct", "dress code",
            "rules for students", "college regulations", "can I smoke in college",
            "mobile phone in class", "discipline committee", "misconduct"
        ],
        "responses": [
            "📋 Student Code of Conduct — General Rules:\n\n**Academic Discipline:**\n✅ Maintain 75%+ attendance\n✅ Submit assignments on time\n✅ No cheating / malpractice in exams → rustication risk\n✅ Mobile phones typically prohibited during lectures\n\n**Campus Conduct:**\n🚫 Smoking, alcohol, drugs — strictly prohibited; leads to expulsion\n🚫 Ragging — zero tolerance, criminal charges\n🚫 Eve teasing / sexual harassment — ICC complaint, expulsion\n👗 Dress code in many colleges — formal/semi-formal; ID card mandatory\n\n**Hostel Rules:**\n• No unauthorized guests\n• Lights-out timings for juniors\n• No damage to property\n\n**Punishment Scale:**\n1. Warning letter → 2. Fine → 3. Suspension → 4. Rustication → 5. Expulsion\n\n**Disciplinary Committee:**\nAny misconduct is heard by the Discipline Committee. Students have the right to present their side.\n\n💡 Read the college's Student Handbook given at admission — it contains all official rules."
        ]
    },

    # ─── MENTAL HEALTH ────────────────────────────────────────────────────────
    {
        "tag": "mental_health",
        "patterns": [
            "stress", "mental health", "anxiety", "depression", "feel sad",
            "exam stress", "college pressure", "struggling", "counselor",
            "I am stressed", "feeling overwhelmed", "mental health support",
            "psychology help", "career anxiety"
        ],
        "responses": [
            "💙 Mental Health & Well-being Support:\n\nFirst — it's completely okay to feel stressed. College life can be overwhelming.\n\n**Common Challenges Students Face:**\n• Exam pressure & academic stress\n• Homesickness (especially in hostels)\n• Relationship & social pressures\n• Career uncertainty\n• Financial stress\n\n**What You Can Do:**\n✅ **Talk to someone** — Friend, family, or trusted faculty mentor\n✅ **College Counselor** — Most colleges have a Student Counseling Center (free, confidential)\n✅ **Student Mentor Program** — Senior mentors assigned to freshers\n✅ **Physical activity** — Exercise genuinely reduces stress hormones\n✅ **Sleep well** — 7–8 hours is non-negotiable for brain function\n\n**National Helplines (India):**\n📞 **iCall:** 9152987821 (Mon–Sat, 8 AM – 10 PM)\n📞 **Vandrevala Foundation:** 1860-2662-345 (24/7)\n📞 **NIMHANS:** 080-46110007\n\n🌟 Seeking help is a sign of strength, not weakness. You matter!"
        ]
    },

    # ─── ABOUT THE BOT ────────────────────────────────────────────────────────
    {
        "tag": "about_bot",
        "patterns": [
            "who are you", "what are you", "about you", "what can you do",
            "how do you work", "tell me about yourself", "are you a bot",
            "what is this", "help me", "what questions can I ask"
        ],
        "responses": [
            "🤖 I'm **SmartCollegeBot** — your AI-powered college assistant!\n\nI can help you with:\n📋 **Admissions** — Process, eligibility, documents, dates\n💰 **Fees & Scholarships** — Fee structure, financial aid, education loans\n📚 **Courses** — Programs available, duration, syllabus\n📅 **Academics** — Exams, results, attendance, backlogs\n🏠 **Campus Life** — Hostel, cafeteria, transport, sports, clubs\n💼 **Career** — Placements, internships, higher education, guidance\n⚖️ **Student Rights** — Anti-ragging, grievances, mental health\n\nJust type your question naturally — I understand plain English! 😊\n\nExample questions:\n• 'How do I apply for admission?'\n• 'What is the fee for B.Tech?'\n• 'How do I clear my backlogs?'\n• 'What clubs can I join?'"
        ]
    },

    # ─── UNKNOWN ──────────────────────────────────────────────────────────────
    {
        "tag": "unknown",
        "patterns": [],
        "responses": [
            "🤔 I'm not sure I understood that. Could you rephrase your question?\n\nI can help with: Admissions, Fees, Courses, Exams, Results, Hostel, Library, Placements, Scholarships, Clubs & Events, Career Guidance, and more!\n\nTry asking something like:\n• 'How to apply for admission?'\n• 'What is the scholarship procedure?'\n• 'Tell me about hostel facilities'",
            "Hmm, I didn't quite catch that! 😅 Could you be more specific?\n\nI'm best at answering questions about college — admissions, academics, facilities, placements, and student life. Give it another shot!",
        ]
    }
]
