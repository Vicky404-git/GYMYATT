# 🏋️‍♂️ GYMYATT (v1.0)

> **"Sudo make me huge."**
> A terminal-native, hyper-pragmatic Personal Health Engine built for the budget-constrained, Indian hostel dev-bro. Zero hype. Zero fluff. Just pure gains and terminal scripts.

---

## 🚀 Core Features

*   **AI Training Template Engine:** Generates beginner-safe, compound-movement-focused 1-week workout routines and outputs them natively to structured CSV files.
*   **Automated Plan Review & Score:** Leverages Llama 3.3 (70B) to review existing routines, tag exercises by muscle groups, and assign a brutal, strict fitness score out of 10.
*   **Hostel-Friendly Holistic Planning:** Generates daily health, recovery, and nutrition roadmaps restricted strictly to high-protein, low-budget Indian hostel components (eggs, dal, roti, soy chunks, peanuts, milk). No exotic meats, no expensive avocados.
*   **Local Health Snapshot Logger:** Append weight, sleep duration, and calorie intake directly to local persistence layers (`csv`) safely handling unmeasured data (`idk`/`?`).

---

## 🛠️ Tech Stack & Architecture

*   **Language:** Python 3.12+
*   **Package Manager:** `uv` (Fast, modern alternative to pip)
*   **LLM Orchestration:** `LangChain` + `ChatGroq` (`llama-3.3-70b-versatile`)
*   **Database/Persistence:** Local Structured CSV (`data/my_tt.csv`, `data/health_log.csv`)
*   **Containerization:** `Dockerfile` ready for deployment

---

## 📦 Installation & Setup

Ensure you have Python and `uv` installed on your system. 

1. **Clone the repository:**
   ```
   https://github.com/Vicky404-git/GYMYATT.git
   cd GYMYATT
   ```

2. **Set up Environment Variables:**
Create a .env file in the root directory and append your Groq API key:

```
GROQ_API_KEY=gsk_your_actual_api_key_here
```
3. **Install Dependencies:**
`uv` will automatically manage the virtual environment and sync dependencies:
```
uv sync
```

## 🎮 How to Run
Execute the engine directly using `uv`:
```
uv run main.py
```


## System Menu Snapshot:
```
==================================
 🛠️ TERMINAL HEALTH ENGINE (v1.0)
==================================
--- Training Templates ---
1. AI Create TT
2. Review TT (Text)
3. Analyze TT (JSON Score)
--- Daily Engine ---
4. Calculate TDEE/Macros
5. Log Daily Health Snapshot
6. AI Analyze Health Log
7. Generate Holistic Day Plan (Hostel Diet)
8. Exit
```

## 🤝 Roadmap & Teammate Delegation
- AI Engine & Architecture: Maintained locally by @vicky-404 (Core engine, prompt constraints, formatting guards).

- Frontend/UI Team: Transitioning the CLI workflow into a modern interface using Google Project IDX.

- Database Team: Migration planned from local flat CSV files to a persistent PostgreSQL instance.
