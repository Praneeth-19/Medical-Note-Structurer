from fastapi import FastAPI, Form
import requests

app = FastAPI()

def query_llama(prompt: str):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "llama2", "prompt": prompt, "stream": False},
            timeout=30  # Add a timeout
        )
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
        return response.json()["response"].strip()
    except requests.exceptions.RequestException as e:
        # Handle network errors, timeouts, etc.
        print(f"Error connecting to Llama2 service: {e}")
        # You might want to raise a FastAPI HTTPException here to return a proper error to the client
        # from fastapi import HTTPException
        # raise HTTPException(status_code=503, detail=f"Error connecting to Llama2 service: {e}")
        return "Error: Could not connect to Llama2 service."
    except KeyError:
        # Handle cases where 'response' key is missing in the JSON
        print(f"Error: 'response' key not found in Llama2 output. Full response: {response.text}")
        # raise HTTPException(status_code=500, detail="Invalid response format from Llama2 service.")
        return "Error: Invalid response format from Llama2 service."
    except Exception as e:
        # Catch any other unexpected errors
        print(f"An unexpected error occurred in query_llama: {e}")
        # raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")
        return "Error: An unexpected error occurred."

@app.post("/extract/")
def extract_medical_info(note: str = Form(...)):
    prompt = (
        f"Extract the following from the doctor's note:\n"
        f"- Symptoms\n- Diagnosis\n- Medications\n- Follow-up Instructions\n"
        f"Return the output in JSON format.\n\nNote:\n{note}"
    )
    structured_data = query_llama(prompt)
    return {"structured": structured_data}