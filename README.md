# 🚗 SmartDiag - AI-Powered Auto Diagnostic Assistant

SmartDiag is a local, AI-driven diagnostic tool that helps users understand OBD2 car error codes. By matching AI-generated diagnostic reports with a local database of repair tutorials, it provides an interactive and highly accurate troubleshooting experience.

## ✨ Key Features

- **Intelligent Diagnostics:** Uses advanced prompt engineering to extract standard OBD2 definitions, physical check recommendations, and exact defective parts.
- **Automated Video Mapping:** Parses the AI's output using Regular Expressions (Regex) to automatically trigger the correct tutorial video for the identified sensor (e.g., MAF, O2, EGR).
- **Privacy-First Architecture (Edge AI):** Built using **Ollama** to run large language models (LLMs) 100% locally. No vehicle diagnostic data or user queries are sent to third-party cloud APIs. This eliminates data leakage risks and ensures strict data privacy.
- **Interactive UI:** Built entirely in Python using Streamlit for a seamless user experience.

## 🛠️ Tech Stack

- **Language:** Python
- **Frontend:** Streamlit
- **AI Engine:** Ollama (Local LLM Inference)
- **Logic:** Regular Expressions (Regex) for text extraction and logic routing.

## 🚀 How to Run Locally

1. Clone the repository: `git clone https://github.com/your-username/SmartDiag.git`
2. Create a virtual environment: `python -m venv venv` and activate it.
3. Install dependencies: `pip install -r requirements.txt`
4. Ensure Ollama is running locally with your preferred model downloaded (e.g., `ollama pull llama3.1` or `phi3`).
5. Run the app: `streamlit run app.py`

## 🔮 Future Improvements

- Implement a persistent local database for diagnostic history.
- Explore Differential Privacy techniques if usage telemetry is ever collected.
