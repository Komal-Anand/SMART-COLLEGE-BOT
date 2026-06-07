# SmartCollegeBot 🎓

An **NLP & ML-Based College Assistant Chatbot** — B.Tech Pre-Final Year Project (CSM355)

---

## 🚀 How to Run

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start the App
```bash
streamlit run app.py
```

The app opens at `http://localhost:8501`

---

## 🔐 Demo Login Credentials

| Username | Password | Role |
|----------|----------|------|
| `admin` | `admin123` | Admin |
| `student1` | `student123` | Student |
| `demo` | `demo123` | Student |

---

## 📁 Project Structure

```
smartcollegebot/
├── app.py            # Main Streamlit application
├── dataset.py        # Intent dataset (37 intents, 400+ patterns)
├── model_utils.py    # NLP preprocessing + ML model training
├── auth.py           # User authentication & registration
├── chat_logger.py    # Chat history & analytics logging
├── model.pkl         # Trained model (auto-generated)
├── users.json        # User database (auto-generated)
├── chat_history.json # Chat logs (auto-generated)
└── requirements.txt
```

---

## 🧠 Technical Stack

| Component | Technology |
|-----------|-----------|
| **Frontend** | Streamlit (Python) |
| **NLP Preprocessing** | Custom (Regex tokenizer, Suffix stemmer, Stopword removal) |
| **Feature Extraction** | TF-IDF Vectorizer (n-gram: 1–3, max 8000 features) |
| **ML Algorithm** | Logistic Regression (multinomial, LBFGS solver) |
| **Model Evaluation** | 5-fold Cross-validation |
| **Authentication** | SHA-256 hashed passwords, JSON-based user store |
| **Logging** | JSON-based chat history with intent & confidence tracking |

---

## 💬 Topics the Bot Covers

- **Admissions** – Process, eligibility, documents, dates
- **Fees & Scholarships** – Fee structure, NSP/government scholarships, education loans
- **Courses** – Programs, duration, syllabus, credit system
- **Academics** – Exam schedule, results, attendance policy, backlogs
- **Campus Life** – Hostel, cafeteria, transport, sports, Wi-Fi
- **Career** – Placements, internships, higher education (GRE/GMAT/MS)
- **Student Services** – Library, medical, clubs & fests
- **Student Rights** – Anti-ragging, grievance mechanism, mental health
- **Career Guidance** – Post-graduation paths, job sectors, certifications

---

## 🛡️ Admin Features

- 📊 Analytics Dashboard (intent stats, daily activity, confidence metrics)
- 👥 User Management (add/delete users, reset passwords)
- 🔍 Low-Confidence Log viewer (for dataset improvement)
- 🧠 Model Inspector (test queries, view intent probabilities)

---

## 📊 Model Performance

- **Training samples:** ~2,600 (with data augmentation)
- **Intents:** 37 categories
- **Cross-validation accuracy:** ~70% (general NLP for unseen paraphrases)
- **High-confidence queries:** 85–96% accuracy on trained patterns

---

*Submitted by: Komal Anand | Reg. No.: 12311189 | LPU, Phagwara*
