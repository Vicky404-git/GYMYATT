import os
import json
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate

from prompts import (
    TT_GENERATE_PROMPT, 
    TT_REVIEW_PROMPT, 
    TT_ANALYZE_PROMPT,
    PROGRESS_ANALYZE_PROMPT,
    HOLISTIC_PLAN_PROMPT
)

load_dotenv()

_llm = ChatGroq(
    temperature=0.6,
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.3-70b-versatile",
)

# Add this helper function anywhere in ai_brain.py
def _clean_json_output(raw_text: str) -> str:
    """Strips markdown code blocks from LLM output so json.loads() doesn't crash."""
    cleaned = raw_text.strip()
    if cleaned.startswith("```json"):
        cleaned = cleaned[7:]
    elif cleaned.startswith("```"):
        cleaned = cleaned[3:]
    if cleaned.endswith("```"):
        cleaned = cleaned[:-3]
    return cleaned.strip()

def analyze_tt(csv_text: str) -> dict:
    prompt = PromptTemplate.from_template(TT_ANALYZE_PROMPT)
    chain = prompt | _llm
    try:
        raw_output = chain.invoke({"csv_data": csv_text}).content
        clean_output = _clean_json_output(raw_output)
        return json.loads(clean_output)
    except Exception as e:
        print("AI analysis error:", e)
        return {"score": None, "summary": "Failed to analyze training template.", "tags": []}

def analyze_progress(csv_text: str) -> dict:
    prompt = PromptTemplate.from_template(PROGRESS_ANALYZE_PROMPT)
    chain = prompt | _llm
    try:
        raw_output = chain.invoke({"csv_data": csv_text}).content
        clean_output = _clean_json_output(raw_output)
        return json.loads(clean_output)
    except Exception as e:
        print("AI progress analysis error:", e)
        return {"error": "Failed to parse log."}

def generate_tt(user_data: dict) -> str:
    prompt = PromptTemplate.from_template(TT_GENERATE_PROMPT)
    chain = prompt | _llm
    try:
        return chain.invoke(user_data).content.strip()
    except Exception as e:
        print("AI generation error:", e)
        return ""

def review_tt(csv_text: str) -> str:
    prompt = PromptTemplate.from_template(TT_REVIEW_PROMPT)
    chain = prompt | _llm
    try:
        return chain.invoke({"csv_data": csv_text}).content.strip()
    except Exception as e:
        print("AI review error:", e)
        return "Could not analyze the training template."

def analyze_tt(csv_text: str) -> dict:
    prompt = PromptTemplate.from_template(TT_ANALYZE_PROMPT)
    chain = prompt | _llm
    try:
        return json.loads(chain.invoke({"csv_data": csv_text}).content.strip())
    except Exception as e:
        print("AI analysis error:", e)
        return {"score": None, "summary": "Failed to analyze training template.", "tags": []}

def analyze_progress(csv_text: str) -> dict:
    prompt = PromptTemplate.from_template(PROGRESS_ANALYZE_PROMPT)
    chain = prompt | _llm
    try:
        return json.loads(chain.invoke({"csv_data": csv_text}).content.strip())
    except Exception as e:
        print("AI progress analysis error:", e)
        return {"error": "Failed to parse log."}

def generate_holistic_plan(metrics_str: str) -> str:
    prompt = PromptTemplate.from_template(HOLISTIC_PLAN_PROMPT)
    chain = prompt | _llm
    try:
        return chain.invoke({"metrics": metrics_str}).content.strip()
    except Exception as e:
        print("AI planning error:", e)
        return "Failed to generate plan."
