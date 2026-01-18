import streamlit as st
from utils.extract import extract_text, extract_claims
from utils.verify import verify_claim, build_search_query
import json

st.title("📘 AI Fact Checking Web App")

uploaded = st.file_uploader("Upload PDF", type=["pdf"])

if uploaded:
    with st.spinner("Extracting text..."):
        text = extract_text(uploaded)

    with st.spinner("Extracting claims..."):
        claims = extract_claims(text)

    st.subheader("Extracted Claims")
    st.write(claims)

    results = []

    with st.spinner("Verifying claims..."):
        for c in claims:
            res = build_search_query(c)
            result = verify_claim(c,res)
            results.append(result)

    st.subheader("Verification Results")
    st.json(results)

