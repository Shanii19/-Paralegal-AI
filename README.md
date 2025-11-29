# ⚖️ Paralegal AI - AI Legal Assistant

A powerful AI-powered legal assistant built with Streamlit and Groq API, designed to help with legal document drafting, research, client Q&A, document review, and general legal advice.

## 🌟 Features

- **📜 Document Drafting**: Generate professional legal documents with standard clauses
- **🔍 Legal Research**: Research legal concepts, precedents, and statutes
- **💬 Client Q&A**: Get clear answers to legal questions
- **🛡️ Document Review**: Analyze contracts for risks and loopholes (PDF upload supported, max 5MB)
- **🧠 General Legal Advice**: Comprehensive legal guidance

## 🚀 Live Demo

[Add your deployed URL here]

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- Groq API Key ([Get one here](https://console.groq.com))

### Local Setup

1. Clone the repository:
```bash
git clone https://github.com/Shanii19/-Paralegal-AI.git
cd -Paralegal-AI
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env.local` file in the root directory:
```bash
GROQ_API_KEY=your_groq_api_key_here
```

4. Run the application:
```bash
streamlit run app.py
```

## 🌐 Deployment on Streamlit Cloud

1. Push your code to GitHub (make sure `.env.local` is in `.gitignore`)

2. Go to [Streamlit Cloud](https://share.streamlit.io/)

3. Click "New app" and select your repository

4. Set up your secrets in Streamlit Cloud:
   - Go to App Settings → Secrets
   - Add your Groq API key:
   ```toml
   GROQ_API_KEY = "your_groq_api_key_here"
   ```

5. Deploy!

## 📋 Configuration

The app uses a custom Streamlit configuration in `.streamlit/config.toml`:
- Maximum upload size: 5MB
- Custom theme with legal aesthetic (teal/navy colors)

## 🔒 Security Notes

- Never commit your `.env.local` file
- Always use Streamlit Secrets for production deployment
- The app validates that queries are legal-related before processing

## 🎨 Design

Modern, professional legal aesthetic featuring:
- Glassmorphism design
- Teal and navy color scheme
- Smooth animations and transitions
- Responsive layout

## ⚠️ Disclaimer

This AI tool is for educational/hackathon purposes only. Always consult a qualified attorney for legal matters.

## 📝 License

MIT License

## 👨‍💻 Author

Created for hackathon purposes
