from tavily import TavilyClient
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
import json
import re

load_dotenv()

llm = ChatOpenAI(
    model="google/gemma-2-9b-it",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
)

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def build_search_query(claim):
    prompt = f"""
    Convert the claim into a concise search query.

    RULES:
    - Max 200 characters
    - Keep entities, numbers, dates
    - Remove filler words
    - Do NOT rewrite meaning

    CLAIM:
    {claim}

    Output ONLY the query.
    """

    response = llm.invoke(prompt)
    query = response.content.strip()

    if not query or len(query) < 10:
        query = " ".join(claim.split()[:20])

    return query[:200]



def clean_json(text):
    if not text:
        return None
    text = re.sub(r"```json|```", "", text).strip()
    match = re.search(r"\{.*\}", text, re.DOTALL)
    return match.group() if match else None

def verify_claim(claim, search_query):
    search_results = tavily.search(
        query=search_query,
        max_results=5
    )

    evidence_text = "\n\n".join(
        [res["content"] for res in search_results.get("results", [])]
    )

    prompt = f"""
    You are a strict JSON-producing fact-checking system.

    CLAIM:
    "{claim}"

    WEB EVIDENCE:
    {evidence_text}

    Rules:
    - Output ONLY valid JSON
    - No markdown
    - No explanations outside JSON
    - You MUST always fill explanation and correct_info
    - If the claim is False:
    - Explain why it is false
    - Provide the correct, current information
    - Cite sources that support the correction
    - If the claim is Inaccurate:
    - Explain what part is outdated or wrong
    - Provide updated numbers or facts
    - Cite sources
    - If the claim is Verified:
    - Briefly confirm using evidence
    - Cite sources

    Output format:
    {{
    "claim": "{claim}",
    "status": "Verified | Inaccurate | False",
    "explanation": "",
    "correct_info": "",
    "sources": []
    }}
    """

    response = llm.invoke(prompt)

    cleaned = clean_json(response.content)

    if cleaned is None:
        return {
            "claim": claim,
            "status": "False",
            "explanation": "Model did not return valid JSON.",
            "correct_info": "",
            "sources": []
        }

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        return {
            "claim": claim,
            "status": "False",
            "explanation": "JSON parsing failed.",
            "correct_info": "",
            "sources": []
        }