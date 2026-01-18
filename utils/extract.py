from pypdf import PdfReader
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatOpenAI(
    model="google/gemma-2-9b-it",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
)

def extract_text(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text() + "\n"
    return text


def extract_claims(text):
    prompt = f"""
    You are extracting claims for a professional fact-checking system.

    VERY IMPORTANT RULES:
    - DO NOT extract atomic or micro-level facts.
    - GROUP related facts within the same paragraph into ONE coherent claim.
    - Each claim should represent a complete, standalone assertion suitable for fact-checking.
    - Prefer 1 claim per section or paragraph.
    - If multiple numbers support the same idea, merge them.
    - DO NOT include introductions, conclusions, questions, or commentary.
    - DO NOT say things like "Here are the facts" or "Let me know if..." or "Here are the factual claims..."
    - DO NOT ask questions.

    BAD EXAMPLES (do NOT do this):
    ❌ "Bitcoin is trading at $42,500"
    ❌ "ETF inflows are negative"

    GOOD EXAMPLE:
    ✅ "As of January 2026, Bitcoin is trading around $42,500 with declining institutional interest and negative ETF inflows."

    TASK:
    Extract ONLY high-level factual claims from the text below.

    OUTPUT FORMAT:
    - Numbered list
    - Maximum 1–2 claims per section
    - Each claim should be self-contained and meaningful

    TEXT:
    {text}
    """

    response = llm.invoke(prompt)

    claims = response.content.split("\n")
    claims = claims[1:]
    return [c.strip() for c in claims if c.strip()]