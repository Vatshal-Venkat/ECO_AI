from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from mock_teamcenter import get_mock_eco
from gemini_client import ask_gemini

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Teamcenter ECO PoC running"}

@app.get("/eco/{change_id}/summarize")
def summarize_eco(change_id: str):
    eco = get_mock_eco(change_id)

    prompt = f"""
    Summarize this ECO clearly:
    Title: {eco['title']}
    Description: {eco['description']}
    """

    summary = ask_gemini(prompt)
    return {"eco_id": change_id, "summary": summary}

@app.get("/eco/{change_id}/impact")
def impact_eco(change_id: str):
    eco = get_mock_eco(change_id)

    prompt = f"""
    Perform impact analysis based on this BOM:
    {eco['bom']}
    """

    impact = ask_gemini(prompt)
    return {"eco_id": change_id, "impact_analysis": impact}
