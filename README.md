🩺 MedSense: AI-Powered Medical Report Analyser
Privacy-Preserving Clinical Data Extraction, Structuring & RAG Simplification
🌐 Live Web PortalExperience the live application hosted on Streamlit Cloud:👉 https://medsense-analyser-lisa.streamlit.app
📌 Executive SummaryModern clinical laboratory reports (e.g., Complete Blood Counts, Metabolic Panels, Lipid Profiles) present complex diagnostic metrics laden with technical jargon, abbreviations, and numerical ranges. Non-specialist patients frequently experience severe cognitive burden and health-related anxiety while awaiting physician consultations.MedSense bridges this health literacy gap by providing an end-to-end, privacy-preserving AI pipeline. It ingests PDF and scanned lab reports, scrubs sensitive Personally Identifiable Information (PII) on the local host, extracts clinical entities using Natural Language Processing, evaluates biomarkers against standardized biological reference intervals, and synthesizes grounded plain-English summaries using Retrieval-Augmented Generation (RAG) powered by ChromaDB.
✨ Key Features
🔒 Local Privacy-Preserving Engine: Simulates PII de-identification (names, contact details, ages) directly on the local machine prior to any downstream language model processing.
👁️ Automated Entity Extraction & Parsing: Employs OCR (Tesseract) and Named Entity Recognition (spaCy) to transform unstructured documents into structured, machine-readable datasets.
📊 Interactive Biomarker Triage: Automatically cross-references patient values against clinical reference bounds, categorizing indicators with visual alert badges (NORMAL vs. FLAGGED).
🧠 Grounded RAG Knowledge Base: Indexes standardized biomarker definitions, associated organ systems, and etiology into ChromaDB vector embeddings (all-MiniLM-L6-v2) to eliminate hallucinations.💬 Clinical Literacy Chatbot: Enables follow-up queries where non-technical patient questions are matched to medical concepts via semantic vector search.🏗️ System Architecture & Workflow[ Patient Lab Report (PDF / Image) ]
                 │
                 ▼
    ┌───────────────────────────┐
    │  1. Ingestion & Privacy   │ ──► Local PII Redaction
    └─────────────┬─────────────┘
                  │
                  ▼
    ┌───────────────────────────┐
    │ 2. Text Extraction & NER  │ ──► OCR (Tesseract) + spaCy NER
    └─────────────┬─────────────┘
                  │
                  ▼
    ┌───────────────────────────┐
    │  3. Biomarker Structuring │ ──► Threshold Evaluation & Flagging
    └─────────────┬─────────────┘
                  │
                  ▼
    ┌───────────────────────────┐
    │ 4. ChromaDB Vector Engine │ ──► Semantic Retrieval (MiniLM-L6-v2)
    └─────────────┬─────────────┘
                  │
                  ▼
    ┌───────────────────────────┐
    │   5. Streamlit Portal     │ ──► Structured Table, AI Summary, Q&A
    └───────────────────────────┘
📁 Repository Structuremedical-report-analyser/
├── app.py                            # Streamlit web application & UI logic
├── clinical_reference_database.csv   # Structured clinical knowledge base (65+ biomarkers)
├── requirements.txt                  # Environment dependencies
├── README.md                         # Project documentation & architecture overview
└── .gitignore                        # Git ignore specifications
🚀 Quickstart & Local Installation1. Clone the Repositorygit clone https://github.com/lisaanjali/medical-report-analyser.git
cd medical-report-analyser
2. Set Up a Virtual Environment (Optional but Recommended)python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
3. Install Dependenciespip install -r requirements.txt
4. Launch the Streamlit Portalstreamlit run app.py
Open your browser and navigate to http://localhost:8501.🛠️ Technology StackLayerTools & LibrariesFrontend FrameworkStreamlitCore RuntimePython 3.10+Data ManipulationPandas, NumPyVector DatabaseChromaDB (Local Persistent Storage)Embeddings ModelHuggingFace Sentence-Transformers (all-MiniLM-L6-v2)Text ProcessingRegular Expressions, Presidio simulated masking⚖️ Clinical DisclaimerNotice: This application is developed strictly for educational, academic research, and health literacy purposes. It does not perform clinical diagnosis, staging, or medical prescription. Always consult a certified medical practitioner or physician regarding diagnostic interpretations and therapeutic decisions.
