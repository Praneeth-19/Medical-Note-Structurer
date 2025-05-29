# Medical Note Structurer (LLaMA2)
This app helps healthcare professionals convert unstructured doctor notes into
## Features
- Extract symptoms, diagnosis, meds, follow-up
- Upload batch CSVs of clinical notes
- View and export structured results
- Streamlit frontend, FastAPI backend
## How to Use
1. Run Ollama: `ollama pull llama2`
2. Backend: `uvicorn backend.main:app --reload`
3. Frontend: `streamlit run frontend/app.py`
4. Upload notes and get structured data!
