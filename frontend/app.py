import streamlit as st
import pandas as pd
import requests
import json
import time

st.title("🏥 Medical Note Structurer")

# Check if backend is running
backend_status = st.empty()
try:
    requests.get("http://localhost:8000/")
    backend_status.success("✅ Connected to backend server")
except requests.exceptions.ConnectionError:
    backend_status.error("❌ Backend server not running. Please start the backend server first.")
    st.info("Run this command in your backend directory: `uvicorn main:app --host 0.0.0.0 --port 8000`")

uploaded_file = st.file_uploader("Upload clinical notes CSV", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    
    # Display available columns
    st.write("Available columns in your CSV file:", df.columns.tolist())
    
    # Let user select which columns to use
    note_column = st.selectbox("Select the column containing medical notes:", df.columns)
    id_column = st.selectbox("Select the column containing patient IDs:", 
                            [col for col in df.columns if "id" in col.lower()] or df.columns)
    
    if st.button("Process Notes"):
        results = []
        
        with st.spinner("Extracting info from notes..."):
            for _, row in df.iterrows():
                # In the try-except block where you process notes:
                try:
                    response = requests.post("http://localhost:8000/extract/", data={"note": row[note_column]})
                    response.raise_for_status()  # Raise exception for HTTP errors
                    
                    try:
                        response_data = response.json()
                        extracted = response_data.get("structured", "")
                        
                        try:
                            structured = json.loads(extracted)
                        except json.JSONDecodeError:
                            st.warning(f"LLM didn't return valid JSON for patient {row[id_column]}. Using default values.")
                            structured = {"symptoms": "N/A", "diagnosis": "N/A", "medications": "N/A", "follow-up": "N/A"}
                    except json.JSONDecodeError:
                        st.error("Backend returned invalid JSON response. Check if Ollama is running properly.")
                        st.stop()
                        
                    results.append({
                        "patient_id": row[id_column],
                        **structured
                    })
                except requests.exceptions.ConnectionError:
                    st.error("❌ Connection to backend failed. Please ensure the backend server is running.")
                    st.stop()
                except requests.exceptions.HTTPError as e:
                    st.error(f"Backend error: {e}")
                    st.stop()
        
        if results:
            result_df = pd.DataFrame(results)
            st.success("Extraction complete!")
            st.dataframe(result_df)
            st.download_button("Download Structured Notes", result_df.to_csv(index=False), "structured_notes.csv", "text/csv")