# 🕵️ CrimeDNA-X — AI-Powered Behavioral Crime Linkage

CrimeDNA-X is a behavioral crime linkage and investigation support system that helps investigators identify similar crime patterns and get explainable investigation recommendations. It uses **Adaptive Behavioral Crime Signatures (ABCS)** to match crimes based on behavior, not just basic details.

---
## Why I Built This
Most crime analytics tools focus on:
- who
- what
- where
- when  
But in real investigations, **how** the crime was committed (the offender's behavior) is often more important for linking cases.
I built CrimeDNA-X to:
- Detect patterns across crimes using behavioral signatures.
- Surface similar past cases when a new FIR is entered.
- Provide clear, explainable reasoning behind each match.
- Keep an audit trail for accountability and transparency.
## What It Does
- **Adaptive Behavioral Crime Signatures (ABCS)**
  - Converts each crime into a behavioral "fingerprint" (MO, entry method, target type, timing, etc.).
  - Uses these signatures to find similar crimes, even if basic details differ.
- **Similar Crime Pattern Matching**
  - When a new case is entered, the system:
    - Computes its behavioral signature.
    - Finds the most similar past cases.
    - Shows a similarity score and key matching features.
- **Explainable Investigation Recommendations**
  - Suggests likely connections between cases.
  - Highlights shared behavioral traits.
  - Provides simple, human‑readable explanations for why cases are linked.
- **Audit Trail**
  - Logs key events (queries, matches, recommendations).
  - Uses hash‑chaining to make the log tamper‑evident.
## Tech Stack
- Python
- Streamlit (UI + session state)
- Similarity / matching logic for behavioral signatures
- SHA‑256 hashing (for audit log)
## How to Run Locally
1. Clone the repo:
   ```bash
   git clone https://github.com/Praveena-Loganathan/CrimeDNA-X-AI-Crime-Analytics
   cd CrimeDNA-X-AI-Crime-Analytics
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   (At minimum, you need `streamlit` and any ML / similarity libs you use.)
3. Run the app:
   ```bash
   streamlit run app.py
   ```
4. Open in browser:
   ```text
   http://localhost:8501
   ```
## How to Use the Demo
1. Choose role: **Investigator** or **Supervisor**.
2. Enter case details (or select a sample case).
3. The system:
   - Computes the behavioral signature.
   - Finds similar past cases.
   - Shows similarity scores and explanations.
4. Review recommended links between cases.
5. Check the **Audit Log** and verify the chain if needed.
## Future Work
If I had more time, I would add:
- Integration with a real KSP crime database.
- More advanced ML models for signature learning.
- Map-based visualization of linked crimes.
- Role-based access control and secure backend.
- Deployment on Zoho Catalyst.
## Note
This is a hackathon prototype. The matching logic and explanations are simplified for the demo. The goal is to show how behavioral signatures and explainable AI can support investigations, not to replace human judgment.
## Author
Built by the team'CogniCore' as a hackathon project for the AI-Driven Crime Analytics & Visualization Platform challenge.
