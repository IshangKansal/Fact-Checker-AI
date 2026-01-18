# AI Fact-Checking Web App

This project is a **Fact-Checking Web Application** built as part of an assessment.  
It ingests a PDF document, extracts factual claims, verifies them against **live web data**, and flags each claim as **Verified, Inaccurate, or False**, along with explanations and sources.

---

## 🚀 Features

- Upload a PDF via a simple Streamlit interface  
- Automatically extract high-level factual claims  
- Cross-check claims using live web search (Tavily)  
- Classify each claim as:
  - **Verified**
  - **Inaccurate** (outdated or partially wrong)
  - **False**
- Provide explanations, corrected information, and sources  
- Robust handling of LLM and API edge cases  

---

## 🛠️ Tech Stack

- **Frontend**: Streamlit  
- **Backend**: Python  
- **LLMs**:
  - OpenRouter (free/open models)
  - Gemini (optional fallback)
- **Search**: Tavily Web Search API  
- **Framework**: LangChain  

---

## 🧠 How It Works

1. **PDF Upload**  
   The user uploads a PDF through the Streamlit UI.

2. **Claim Extraction**  
   The app extracts *high-level, contextual claims* (not micro-facts) using an LLM.

3. **Claim Verification**  
   - Each claim is converted into a search-optimized query.
   - Tavily fetches live web evidence.
   - The LLM evaluates the claim against current data.

4. **Result Classification**  
   Each claim is labeled as **Verified**, **Inaccurate**, or **False**, with:
   - Explanation  
   - Correct information (if applicable)  
   - Source links  

---

## ▶️ Running Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

Create a .env file (for local development only):

```bash
OPENROUTER_API_KEY=your_key_here
TAVILY_API_KEY=your_key_here
GEMINI_API_KEY=optional
```

## 🌍 Deployment

The app is deployed using Streamlit Cloud.

Secrets are configured in:

```bash
Streamlit Cloud → App Settings → Secrets
```

Example:

```bash
OPENROUTER_API_KEY = "..."
TAVILY_API_KEY = "..."
```

## 📌 Notes

- The system is designed to verify claims against current real-world data, not historical context.

- If a claim was once true but is outdated, it is marked False.

- The architecture is model-agnostic and can be easily upgraded to stronger paid models if needed.

## 📹 Demo

A short demo video is included in the submission, showing:

- PDF upload

- Claim extraction

- Live verification results

## 📄 License

This project is for evaluation purposes only.