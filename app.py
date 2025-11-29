import streamlit as st
import os
from groq import Groq
from dotenv import load_dotenv
from fpdf import FPDF
from pypdf import PdfReader

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="Paralegal AI",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load Environment Variables
load_dotenv(".env.local")

# Try to get API key from environment first, then from Streamlit secrets
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    try:
        GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
    except:
        pass

# Initialize Groq Client
if not GROQ_API_KEY:
    st.error("🚨 GROQ_API_KEY not found! Please set it in .env.local (local) or Streamlit Secrets (cloud).")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)

# Initialize Session State for Persistence
if "chat_history" not in st.session_state:
    st.session_state.chat_history = ""

# --- 2. CUSTOM CSS (Modern Legal Aesthetic) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&family=Playfair+Display:wght@600;700;800&display=swap');
    
    /* Main Background - Modern Dark */
    .stApp {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1d2e 50%, #0f1419 100%);
        color: #e5e7eb;
        font-family: 'Inter', sans-serif;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(10, 14, 39, 0.95) 0%, rgba(15, 20, 25, 0.95) 100%);
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(20, 184, 166, 0.15);
    }

    /* Glassmorphism Card Style */
    .glass-card {
        background: rgba(26, 29, 46, 0.5);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-radius: 20px;
        border: 1px solid rgba(20, 184, 166, 0.2);
        padding: 32px;
        margin-bottom: 24px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5), 0 0 0 1px rgba(20, 184, 166, 0.1);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .glass-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 20px 60px -10px rgba(20, 184, 166, 0.3);
        border-color: rgba(20, 184, 166, 0.4);
    }

    /* Headers */
    h1 {
        font-family: 'Playfair Display', serif;
        font-weight: 800;
        letter-spacing: -0.03em;
    }
    
    h2, h3 {
        color: #f9fafb;
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        letter-spacing: -0.02em;
    }
    
    /* Custom Button Styling - Teal Gradient */
    .stButton > button {
        background: linear-gradient(135deg, #14b8a6 0%, #0d9488 100%);
        color: #ffffff;
        border: none;
        border-radius: 12px;
        padding: 16px 32px;
        font-size: 0.95rem;
        font-weight: 600;
        font-family: 'Inter', sans-serif;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 20px rgba(20, 184, 166, 0.4);
        width: 100%;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(20, 184, 166, 0.6);
        background: linear-gradient(135deg, #0d9488 0%, #0f766e 100%);
    }

    /* Input Fields */
    .stTextArea textarea {
        background-color: rgba(15, 20, 30, 0.8);
        color: #f3f4f6;
        border: 1.5px solid rgba(20, 184, 166, 0.25);
        border-radius: 14px;
        font-size: 1rem;
        font-family: 'Inter', sans-serif;
        padding: 16px;
        transition: all 0.3s ease;
    }
    .stTextArea textarea:focus {
        border-color: #14b8a6;
        box-shadow: 0 0 0 3px rgba(20, 184, 166, 0.2);
        background-color: rgba(15, 20, 30, 0.95);
    }
    
    /* File Uploader */
    .stFileUploader {
        background: rgba(20, 184, 166, 0.05);
        border-radius: 14px;
        padding: 24px;
        border: 2px dashed rgba(20, 184, 166, 0.3);
        transition: all 0.3s ease;
    }
    .stFileUploader:hover {
        border-color: #14b8a6;
        background: rgba(20, 184, 166, 0.1);
    }
    
    /* Custom file uploader text */
    [data-testid="stFileUploader"] label {
        color: #14b8a6 !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
    }
    
    [data-testid="stFileUploader"] small {
        color: #9ca3af !important;
        font-size: 0.85rem !important;
    }

    /* Success Message */
    .stSuccess {
        background-color: rgba(20, 184, 166, 0.15);
        border-left: 4px solid #14b8a6;
        color: #d1fae5;
        border-radius: 10px;
    }
    
    /* Download Button - Cyan */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #06b6d4 0%, #0891b2 100%) !important;
        box-shadow: 0 4px 20px rgba(6, 182, 212, 0.4) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 16px 32px !important;
        font-size: 0.95rem !important;
        font-weight: 600 !important;
        font-family: 'Inter', sans-serif !important;
        letter-spacing: 0.5px !important;
        text-transform: uppercase !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    .stDownloadButton > button:hover {
        box-shadow: 0 8px 30px rgba(6, 182, 212, 0.6) !important;
        transform: translateY(-2px) !important;
        background: linear-gradient(135deg, #0891b2 0%, #0e7490 100%) !important;
    }

    /* Responsiveness */
    @media (max-width: 768px) {
        .stApp { padding: 10px; }
        h1 { font-size: 2.5rem !important; }
        .glass-card { padding: 20px; }
        .stButton > button { padding: 14px 24px; font-size: 0.9rem; }
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR ---
with st.sidebar:
    st.markdown("""
        <div style='text-align: center; padding: 20px 0;'>
            <h2 style='font-size: 1.8rem; margin: 0; color: #14b8a6; font-family: "Playfair Display", serif;'>⚖️ Paralegal AI</h2>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    st.write("Select a legal function below:")
    
    mode = st.radio(
        "Mode",
        ["📜 Document Drafting", "🔍 Legal Research", "💬 Client Q&A", "🛡️ Document Review", "🧠 General Legal Advice"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown("""
        <div style='text-align: center; padding: 20px 10px; font-style: italic; color: #14b8a6; font-size: 1.1rem; font-family: "Playfair Display", serif;'>
            "Elevate your justice"
        </div>
    """, unsafe_allow_html=True)

# --- 4. MAIN CONTENT ---

# Header
st.markdown("""
    <div style='text-align: center; padding: 60px 20px 40px;'>
        <h1 style='font-size: 4.2rem; background: linear-gradient(135deg, #14b8a6 0%, #06b6d4 50%, #0ea5e9 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 16px;'>
            AI Legal Assistant
        </h1>
        <p style='font-size: 1.2rem; color: #9ca3af; font-weight: 400; letter-spacing: 0.5px;'>Your intelligent partner for professional legal tasks</p>
    </div>
""", unsafe_allow_html=True)

# Dynamic Instructions
instructions = {
    "📜 Document Drafting": "Describe the document you need drafted (e.g., 'NDA for a freelance designer'). I will provide a comprehensive draft.",
    "🔍 Legal Research": "Enter a legal topic or question. I will research precedents, statutes, and case law summaries for you.",
    "💬 Client Q&A": "Ask a legal question as if you were a client. I will provide a clear, professional answer with legal context.",
    "🛡️ Document Review": "Upload a PDF contract or paste the text below. I will analyze it for risks, loopholes, and unfair terms.",
    "🧠 General Legal Advice": "Ask me anything about law, procedures, or legal definitions. I'm here to help."
}

st.markdown(f"""
    <div class="glass-card">
        <h3 style="margin-bottom: 16px; color: #14b8a6; font-size: 1.5rem; display: flex; align-items: center; gap: 12px;">
            {mode.split(' ')[0]} <span style="color: #f9fafb; font-weight: 600;">{mode.split(' ', 1)[1]}</span>
        </h3>
        <p style="font-size: 1.05rem; color: #d1d5db; line-height: 1.7;">{instructions[mode]}</p>
    </div>
""", unsafe_allow_html=True)

# Input Area
user_input = ""
uploaded_file_content = ""

if mode == "🛡️ Document Review":
    # Custom styling for file uploader - hide all default text
    st.markdown("""
        <style>
        /* Hide ALL default file uploader text */
        [data-testid="stFileUploader"] label {
            display: none !important;
        }
        
        [data-testid="stFileUploader"] section small {
            display: none !important;
        }
        
        [data-testid="stFileUploader"] section p {
            display: none !important;
        }
        
        [data-testid="stFileUploader"] section div[data-testid="stMarkdownContainer"] {
            display: none !important;
        }
        
        /* Style the dropzone */
        [data-testid="stFileUploader"] section[data-testid="stFileUploaderDropzone"] {
            border: 2px dashed rgba(20, 184, 166, 0.3) !important;
            background: rgba(20, 184, 166, 0.05) !important;
            border-radius: 14px !important;
            padding: 40px 20px !important;
            text-align: center !important;
        }
        
        [data-testid="stFileUploader"] section[data-testid="stFileUploaderDropzone"]:hover {
            border-color: #14b8a6 !important;
            background: rgba(20, 184, 166, 0.1) !important;
        }
        
        /* Add custom upload icon and text */
        [data-testid="stFileUploader"] section[data-testid="stFileUploaderDropzone"]::before {
            content: "📎 Upload PDF Contract";
            display: block;
            font-size: 1rem;
            font-weight: 600;
            color: #14b8a6;
            margin-bottom: 8px;
        }
        

        </style>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("upload", type="pdf", label_visibility="collapsed")
    
    if uploaded_file is not None:
        # Check file size (5MB = 5 * 1024 * 1024 bytes)
        if uploaded_file.size > 5 * 1024 * 1024:
            st.error("⚠️ File size exceeds 5MB limit. Please upload a smaller file.")
        else:
            try:
                reader = PdfReader(uploaded_file)
                for page in reader.pages:
                    uploaded_file_content += page.extract_text() + "\n"
                st.success(f"✅ PDF loaded successfully! ({len(reader.pages)} pages)")
                with st.expander("View Extracted Text"):
                    st.text(uploaded_file_content[:1000] + "..." if len(uploaded_file_content) > 1000 else uploaded_file_content)
            except Exception as e:
                st.error(f"Error reading PDF: {e}")

user_input = st.text_area("Input", height=200, placeholder="Type your detailed query here or paste text...", label_visibility="collapsed")

# Combine inputs for review
final_input = user_input
if mode == "🛡️ Document Review" and uploaded_file_content:
    if user_input.strip():
        final_input = f"User Query: {user_input}\n\nDocument Content:\n{uploaded_file_content}"
    else:
        final_input = f"Please review this document:\n{uploaded_file_content}"

# Logic for Groq Prompts
def generate_prompt(mode, input_text):
    # Strict System Instruction
    base_prompt = """You are an expert AI Legal Assistant. Your sole purpose is to provide professional legal assistance.
    
    CRITICAL INSTRUCTION:
    1. Analyze the user's input.
    2. If the input is NOT related to law, legal documents, court procedures, contracts, rights, or legal advice, you MUST REFUSE to answer.
    3. In that case, reply ONLY with: "⚠️ I am sorry, but this bot is designed exclusively for legal purposes. Please ask a question related to law, courts, or legal documents."
    4. Do not provide any other information or answer the non-legal question.
    
    If the input IS legal-related, proceed as follows:
    """
    
    if mode == "📜 Document Drafting":
        return base_prompt + f"Draft a professional legal document based on this request: '{input_text}'. Ensure it includes all standard clauses, definitions, and is formatted correctly."
    elif mode == "🔍 Legal Research":
        return base_prompt + f"Conduct legal research on: '{input_text}'. Provide a detailed summary of relevant legal concepts, precedents, statutes, or regulations. Cite sources where applicable (simulated)."
    elif mode == "💬 Client Q&A":
        return base_prompt + f"Answer this client question in simple, clear, and empathetic terms, while maintaining legal accuracy: '{input_text}'"
    elif mode == "🛡️ Document Review":
        return base_prompt + f"Review the following legal text for risks, loopholes, ambiguities, and unfair terms. Provide a bulleted list of issues and recommendations: '{input_text}'"
    elif mode == "🧠 General Legal Advice":
        return base_prompt + f"Provide a comprehensive answer to this legal query: '{input_text}'"
    
    return input_text

# PDF Generator Function
def create_pdf(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Simple sanitization for latin-1 (FPDF limitation)
    replacements = {
        '\u2018': "'", '\u2019': "'", '\u201c': '"', '\u201d': '"', 
        '\u2013': '-', '\u2014': '-', '\u2022': '*'
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    
    # Split lines to handle basic wrapping
    for line in text.split('\n'):
        try:
            pdf.multi_cell(0, 10, line.encode('latin-1', 'replace').decode('latin-1'))
        except:
            pdf.multi_cell(0, 10, "Error encoding line.")
            
    return pdf.output(dest='S').encode('latin-1')

# Action Button
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    generate_btn = st.button("🚀 Generate Response", use_container_width=True)

# --- 5. RESPONSE GENERATION ---
if generate_btn:
    if not final_input.strip():
        st.warning("⚠️ Please enter some text or upload a file first.")
    else:
        # Placeholder for loading animation
        with st.empty():
            st.markdown("""
                <div style="text-align: center; padding: 50px;">
                    <p style="font-size: 1.5rem; color: #14b8a6; font-weight: 600; animation: pulse 1.5s infinite;">
                        ⚡ Analyzing Legal Data...
                    </p>
                </div>
                <style>
                    @keyframes pulse {
                        0% { opacity: 0.5; }
                        50% { opacity: 1; }
                        100% { opacity: 0.5; }
                    }
                </style>
            """, unsafe_allow_html=True)
            
            try:
                # Build Prompt
                final_prompt = generate_prompt(mode, final_input)
                
                # Call Groq API
                chat_completion = client.chat.completions.create(
                    messages=[
                        {
                            "role": "user",
                            "content": final_prompt,
                        }
                    ],
                    model="llama-3.3-70b-versatile", 
                    temperature=0.5,
                    max_tokens=2048,
                )
                
                response_text = chat_completion.choices[0].message.content
                
                # Save to session state
                st.session_state.chat_history = response_text
                
            except Exception as e:
                st.error(f"An error occurred: {e}")

# Display Result (Persistent)
if st.session_state.chat_history:
    st.markdown("""<div class="glass-card"><h3 style="color: #14b8a6; font-size: 1.5rem;">📝 AI Legal Assistant Analysis</h3></div>""", unsafe_allow_html=True)
    st.markdown(st.session_state.chat_history)
    
    # PDF Download for Drafting
    if mode == "📜 Document Drafting":
        try:
            pdf_bytes = create_pdf(st.session_state.chat_history)
            col_dl_1, col_dl_2, col_dl_3 = st.columns([1, 2, 1])
            with col_dl_2:
                st.download_button(
                    label="📄 Save as PDF",
                    data=pdf_bytes,
                    file_name="legal_draft.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
        except Exception as e:
            st.error(f"Could not generate PDF: {e}")
    
    # Optional: Clear button
    if st.button("Clear Result"):
        st.session_state.chat_history = ""
        st.rerun()

# Footer
st.markdown("""
    <div style='text-align: center; margin-top: 100px; padding: 30px 20px; border-top: 1px solid rgba(20, 184, 166, 0.2);'>
        <p style='color: #6b7280; font-size: 0.9rem;'>⚠️ Disclaimer: This AI tool is for educational/hackathon purposes only. Always consult a qualified attorney.</p>
    </div>
""", unsafe_allow_html=True)
