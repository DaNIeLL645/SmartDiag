# 🚗 SmartDiag - AI-Powered Auto Diagnostic Assistant

SmartDiag is a local, AI-driven diagnostic tool that helps users understand OBD2 car error codes. By matching AI-generated diagnostic reports with a local database of repair tutorials, it provides an interactive, secure, and highly accurate troubleshooting experience.

## ✨ Key Features

- **Intelligent Diagnostics:** Uses advanced prompt engineering to extract standard OBD2 definitions, physical check recommendations, and exact defective parts.
- **Secure User Authentication:** Features a custom login and registration system. Passwords are encrypted using salted hashing via **Bcrypt** to ensure data security.
- **Persistent Diagnostic History:** Utilizes a local **SQLite** relational database to securely store and manage user-specific search history and identified defective parts (Access Control).
- **Automated Video Mapping:** Parses the AI's output using Regular Expressions (Regex) to automatically trigger the correct tutorial video for the identified sensor (e.g., MAF, O2, EGR).
- **Privacy-First Architecture (Edge AI):** Built using **Ollama** to run large language models (LLMs) 100% locally. No vehicle diagnostic data or user queries are sent to third-party cloud APIs, eliminating data leakage risks.
- **Interactive UI:** Built entirely in Python using Streamlit with secure session state management.

## 🛠️ Tech Stack

- **Language:** Python
- **Frontend:** Streamlit
- **AI Engine:** Ollama (Local LLM Inference - Phi-3 / Llama 3.1)
- **Database & Security:** SQLite3, Bcrypt (Password Hashing)
- **Logic:** Regular Expressions (Regex) for text extraction and logic routing.

## 🚀 How to Run Locally

1. Clone the repository: `git clone https://github.com/your-username/SmartDiag.git`
2. Create a virtual environment: `python -m venv venv` and activate it.
3. Install dependencies: `pip install -r requirements.txt`
4. Ensure Ollama is running locally with your preferred model downloaded (e.g., `ollama pull phi3`).
5. Run the app: `streamlit run app.py`
   _(Note: The `database.db` file and required tables will be generated automatically upon the first run)._

## 🔮 Future Improvements

- Explore **Differential Privacy** techniques if usage telemetry is ever collected, ensuring individual queries cannot be reconstructed.
- Implement **Federated Learning** concepts to improve diagnostic prompt accuracy across multiple local nodes without centralizing raw user data.
