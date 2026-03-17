import streamlit as st
import pandas as pd
import requests
import json

# 1. Setup & Page Config
st.set_page_config(page_title="SCM Risk AI Scorecard", layout="wide")
st.title("📦 DC Risk & Resilience AI Scorecard")
st.markdown("Managerial Decision Support for Inbound/Outbound Rerouting")

# 2. Hugging Face API Configuration (Free Tier)
# In production, use st.secrets for the API Key
HF_API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
headers = {"Authorization": "Bearer YOUR_HF_TOKEN_HERE"} 

def query_llm(payload):
    response = requests.post(HF_API_URL, headers=headers, json=payload)
    return response.json()

# 3. Data Ingestion (Automatic from GitHub)
@st.cache_data
def load_internal_data():
    try:
        return pd.read_csv("distribution_centers.csv")
    except FileNotFoundError:
        return None

df = load_internal_data()

# 4. Main Interface
if df is not None:
    st.sidebar.success("✅ DC Master Data Loaded")
    st.sidebar.write(f"Total Sites: {len(df)}")
    
    news_headline = st.text_input("🚨 Enter Live News Headline / Weather Alert:", 
                                  placeholder="e.g., Major blizzard projected for the Northeast Corridor")

    if news_headline:
        if st.button("Run AI Risk Assessment"):
            st.subheader("Automated Site Impact Analysis")
            
            # This loop must be indented inside the button 'if'
            for index, row in df.iterrows():
                prompt = f"""
                [ROLE] Senior Supply Chain Risk Controller. 
                [DC] {row['name']} in {row['location']}. Criticality: {row['criticality']}. DOH: {row['avg_inventory_doh']}.
                [EVENT] {news_headline}
                [TASK] Provide a JSON response with: 'risk_score' (1-10), 'reasoning' (1 sentence), and 'action' (1 sentence).
                JSON:"""
                
                output = query_llm({"inputs": prompt, "parameters": {"max_new_tokens": 150}})
                
                with st.expander(f"{row['name']} - {row['location']}"):
                    st.write(output[0]['generated_text'].split("JSON:")[-1])
else:
    st.error("🚨 Error: 'distribution_centers.csv' not found in your GitHub repository. Please ensure the file is uploaded to the same folder as app.py.")
            # Your existing loop for AI analysis goes here...
        
        # We'll analyze each DC and display results
        for index, row in df.iterrows():
            # Build the prompt using the template we drafted
            prompt = f"""
            [ROLE] Senior Supply Chain Risk Controller. 
            [DC] {row['name']} in {row['location']}. Criticality: {row['criticality']}. DOH: {row['avg_inventory_doh']}.
            [EVENT] {news_headline}
            [TASK] Provide a JSON response with: 'risk_score' (1-10), 'reasoning' (1 sentence), and 'action' (1 sentence).
            JSON:"""
            
            # Call the AI
            output = query_llm({"inputs": prompt, "parameters": {"max_new_tokens": 150}})
            
            # Display Logic (Simplification for MVP)
            with st.expander(f"{row['name']} - Location: {row['location']}"):
                col1, col2 = st.columns([1, 4])
                # In a real app, you'd parse the JSON here. For now, we show the raw AI thought:
                col1.metric("Risk Score", "Calculating...") 
                st.write(output[0]['generated_text'].split("JSON:")[-1])

else:
    st.info("Please upload your `distribution_centers.csv` and enter a headline to begin.")
