# AI-Driven DC Risk & Resilience Scorecard
**Course Project: AI in Supply Chain Management**

## Project Overview
This application serves as a managerial decision-support tool to evaluate real-time risks to Distribution Centers (DCs). It uses a Large Language Model (LLM) to synthesize unstructured news data with internal DC constraints (Capacity, Criticality, and Days on Hand).

## Setup Instructions
1. **Data:** Ensure the `distribution_centers.csv` is in the root directory.
2. **Environment:** Install dependencies via `pip install -r requirements.txt`.
3. **API Key:** You must provide a Hugging Face User Access Token (Free Tier) in the `app.py` headers.
4. **Execution:** Run locally using `streamlit run app.py` or access via the Deployment URL.

## Known Limitations & Constraints (Free-Tier)
- **Latency:** As a free-tier inference model, response times may vary (3-10 seconds per DC analysis).
- **Context Window:** The model is optimized for single-event analysis; processing a month's worth of news at once may exceed token limits.
- **Data Privacy:** This MVP uses a public inference endpoint. In a Fortune 500 context, a Private VPC deployment would be required.

## Managerial Impact
The tool transitions risk management from reactive to proactive by providing a **Recommended Action** for each site based on its specific operational buffer (DOH).
