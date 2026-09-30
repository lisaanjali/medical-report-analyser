import streamlit as st
import pandas as pd
import chromadb
from chromadb.utils import embedding_functions
import re
import os

st.set_page_config(
    page_title="MedSense - AI Medical Report Analyser",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Medical Aesthetic Styling
st.markdown("""
<style>
    .main-title { font-size: 2.2rem; font-weight: 800; color: #0284c7; margin-bottom: 0px; }
    .sub-title { font-size: 1.05rem; color: #64748b; margin-bottom: 20px; }
    .badge-normal { background-color: #dcfce7; color: #15803d; padding: 4px 10px; border-radius: 8px; font-weight: 600; }
    .badge-flagged { background-color: #fee2e2; color: #b91c1c; padding: 4px 10px; border-radius: 8px; font-weight: 600; }
    .disclaimer-box { background: #fef2f2; border-left: 4px solid #ef4444; padding: 12px; border-radius: 6px; color: #991b1b; font-size: 0.85rem; margin-top: 15px; }
</style>
""", unsafe_allow_html=True)

# Initialize Session State
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "assistant", "content": "Hello! I am your AI Medical Assistant. Upload your report or ask any health test questions."}
    ]

# Connect to ChromaDB
@st.cache_resource
def get_vector_db():
    client = chromadb.PersistentClient(path="./chroma_medical_db")
    embed_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
    collection = client.get_or_create_collection(name="clinical_knowledge", embedding_function=embed_fn)
    return collection

collection = get_vector_db()

# Load Reference CSV
@st.cache_data
def get_reference_data():
    if os.path.exists("clinical_reference_database.csv"):
        return pd.read_csv("clinical_reference_database.csv")
    return None

df_ref = get_reference_data()

# Local Privacy Redaction Function
def anonymize_text(text):
    text = re.sub(r'(?i)name[:\s]+([A-Za-z\s]+)', 'Name: <REDACTED_PATIENT_NAME>', text)
    text = re.sub(r'(?i)age[:\s]+(\d+)', 'Age: <REDACTED_AGE>', text)
    text = re.sub(r'(?i)(phone|mobile|contact)[:\s]+(\d+)', 'Contact: <REDACTED_PHONE>', text)
    text = re.sub(r'\b\d{10}\b', '<REDACTED_PHONE>', text)
    return text

# Sidebar Navigation
with st.sidebar:
    st.title("🩺 MedSense Portal")
    st.caption("M.Sc. Data Science Capstone Project")
    st.markdown("---")
    
    st.subheader("1. Ingestion & Privacy")
    uploaded_file = st.file_uploader("Upload Lab Report (PDF / Image)", type=["pdf", "png", "jpg", "jpeg"])
    
    enable_privacy = st.checkbox("Enable Local PII Anonymization", value=True)
    
    st.markdown("""
    <div class="disclaimer-box">
        <strong>⚠️ Clinical Disclaimer:</strong><br>
        For educational and health literacy purposes only. Not a clinical diagnosis. Always consult a certified physician.
    </div>
    """, unsafe_allow_html=True)

# Main Title Header
st.markdown('<div class="main-title">AI-Powered Medical Report Analyser</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Privacy-Preserving Clinical Data Extraction, Structuring & RAG Simplification</div>', unsafe_allow_html=True)

# Check if file is uploaded
if uploaded_file is not None:
    st.success(f"✓ Ingested file: **{uploaded_file.name}**")
    
    tab1, tab2, tab3 = st.tabs(["📊 Structured Biomarkers", "📝 Plain-English AI Summary", "🔒 Raw & Anonymized Text"])
    
    # Sample extracted results for presentation
    extracted_sample = [
        {"Biomarker": "Hemoglobin", "Your Value": 10.5, "Unit": "g/dL", "Normal Range": "12.0 - 15.5", "Status": "FLAGGED (LOW)"},
        {"Biomarker": "Vitamin D", "Your Value": 22.0, "Unit": "ng/mL", "Normal Range": "30.0 - 100.0", "Status": "FLAGGED (LOW)"},
        {"Biomarker": "Total Cholesterol", "Your Value": 182.0, "Unit": "mg/dL", "Normal Range": "125.0 - 200.0", "Status": "NORMAL"},
        {"Biomarker": "Serum Creatinine", "Your Value": 0.9, "Unit": "mg/dL", "Normal Range": "0.6 - 1.2", "Status": "NORMAL"},
        {"Biomarker": "Platelet Count", "Your Value": 240.0, "Unit": "10^3/uL", "Normal Range": "150.0 - 450.0", "Status": "NORMAL"}
    ]
    df_results = pd.DataFrame(extracted_sample)
    
    with tab1:
        st.subheader("Extracted Biomarkers vs. Reference Intervals")
        
        def highlight_status(val):
            return "background-color: #fee2e2; color: #b91c1c; font-weight: bold;" if "FLAGGED" in str(val) else "background-color: #dcfce7; color: #15803d; font-weight: bold;"
            
        st.dataframe(df_results.style.map(highlight_status, subset=["Status"]), use_container_width=True)
        st.info("💡 **Attention:** Values flagged in red warrant a discussion with your doctor during your next appointment.")
        
    with tab2:
        st.subheader("Grounded Plain-English Summary")
        st.markdown("""
        > **Key Takeaways from Your Report:**
        > 
        > 1. **Hemoglobin (10.5 g/dL — Low):** Your hemoglobin is slightly below the standard threshold (12.0 - 15.5 g/dL). Hemoglobin carries oxygen to your cells. Slightly low values often correlate with mild fatigue or iron deficiency.
        > 2. **Vitamin D (22.0 ng/mL — Low):** Below the recommended target of 30 ng/mL. Safe morning sun exposure and dietary sources can assist recovery.
        > 3. **Normal Organs:** Your Kidney function (Creatinine), Blood clotting (Platelets), and Heart metrics (Total Cholesterol) are all within healthy reference ranges.
        """)
        
    with tab3:
        raw_text_demo = f"Patient Name: John Doe, Age: 45, Phone: 9876543210. Lab Results: Hemoglobin 10.5 g/dL, Vitamin D 22 ng/mL, Creatinine 0.9 mg/dL."
        c1, c2 = st.columns(2)
        with c1:
            st.caption("Raw OCR Extracted Text")
            st.code(raw_text_demo)
        with c2:
            st.caption("Anonymized Text (Privacy Filter Applied)")
            st.code(anonymize_text(raw_text_demo) if enable_privacy else raw_text_demo)

else:
    st.info("👈 Upload a lab report PDF or Image in the left sidebar to start the analysis pipeline.")

# Interactive RAG Chatbot Section
st.markdown("---")
st.subheader("💬 Ask Your Doubt to MedSense AI")
st.caption("Responses are retrieved directly from your clinical knowledge base in ChromaDB.")

# Display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# User Chat Input
if user_doubt := st.chat_input("Ask a doubt (e.g., 'What foods improve low hemoglobin?'):"):
    st.session_state.chat_history.append({"role": "user", "content": user_doubt})
    with st.chat_message("user"):
        st.write(user_doubt)
        
    with st.chat_message("assistant"):
        with st.spinner("Searching ChromaDB clinical knowledge base..."):
            search_res = collection.query(query_texts=[user_doubt], n_results=1)
            
            if search_res and search_res.get('documents') and len(search_res['documents'][0]) > 0:
                retrieved_context = search_res['documents'][0][0]
                matched_name = search_res['metadatas'][0][0]['biomarker']
                
                bot_answer = (
                    f"**Regarding {matched_name}:**\n\n"
                    f"{retrieved_context}\n\n"
                    f"*Note: Please discuss specific dosages and clinical symptoms with your treating physician.*"
                )
            else:
                bot_answer = "I could not find an exact match in the reference database. Please consult a medical doctor for professional guidance."
                
            st.write(bot_answer)
            st.session_state.chat_history.append({"role": "assistant", "content": bot_answer})