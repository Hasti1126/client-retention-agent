import streamlit as st
import requests
import json
from datetime import datetime

# Page config
st.set_page_config(
    page_title="Client Retention AI Agent",
    page_icon="🤖",
    layout="wide"
)

# Title
st.markdown("# 🤖 AI-Powered Client Retention Engine")
st.markdown("**Powered by ML (84.3% Detection) + Strands Agents**")

# API Configuration
API_URL = "http://localhost:8080"

def invoke_agent(prompt):
    """Call the agent API"""
    try:
        response = requests.post(
            f"{API_URL}/invocations",
            json={"input": {"prompt": prompt}},
            timeout=30
        )
        return response.json() if response.status_code == 200 else {"error": response.status_code}
    except Exception as e:
        return {"error": str(e)}

# Sidebar
st.sidebar.title("🎯 Features")
page = st.sidebar.radio("Select", ["Dashboard", "Single Client", "Batch Analysis", "Recommendations"])

# ==================== DASHBOARD ====================
if page == "Dashboard":
    st.header("Executive Dashboard")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Accuracy", "83.8%", "↑")
    col2.metric("Detection Rate", "84.3%", "↑")
    col3.metric("False Alarms", "16.3%", "↓")
    col4.metric("Threshold", "0.42", "Optimized")
    
    st.divider()
    
    col1, col2 = st.columns(2)
    with col1:
        st.info("📈 Model: XGBoost + Neural Network\n\n8 Features analyzed across 5 dimensions")
    with col2:
        st.success("💰 ROI: 685% (Example: $100K saved + $30K upsell + $58.5K time savings)")

# ==================== SINGLE CLIENT ====================
elif page == "Single Client":
    st.header("Analyze Single Client")
    
    with st.form("client_analysis"):
        col1, col2 = st.columns(2)
        
        with col1:
            client_id = st.text_input("Client ID", "CLT_001")
            sentiment = st.slider("Communication Sentiment", -1.0, 1.0, -0.3, 0.1)
            payment = st.slider("Payment Timeliness (days)", -30.0, 30.0, -5.0, 1.0)
            utilization = st.slider("Service Utilization", 0.0, 1.0, 0.45, 0.05)
        
        with col2:
            satisfaction = st.slider("Response Satisfaction", 0.0, 1.0, 0.6, 0.1)
            ticket_freq = st.slider("Ticket Frequency Trend", 0.5, 3.0, 1.5, 0.1)
            contract_trend = st.slider("Contract Value Trend", -0.5, 0.5, -0.1, 0.05)
            engagement = st.slider("Contact Engagement", 0.0, 1.0, 0.4, 0.1)
        
        escalation = st.slider("Escalation Frequency", 0.0, 1.0, 0.2, 0.1)
        
        submitted = st.form_submit_button("🔍 Analyze Risk")
    
    if submitted:
        prompt = f"""Assess churn risk for {client_id}:
        sentiment={sentiment}, payment_days={payment}, utilization={utilization*100}%,
        satisfaction={satisfaction}, ticket_trend={ticket_freq}, contract_trend={contract_trend},
        engagement={engagement}, escalation={escalation}
        
        Provide risk score, level, and top 3 recommendations."""
        
        with st.spinner("Analyzing..."):
            result = invoke_agent(prompt)
        
        st.json(result)

# ==================== BATCH ANALYSIS ====================
elif page == "Batch Analysis":
    st.header("Analyze Multiple Clients")
    
    if st.button("📊 Analyze Sample Portfolio (10 Clients)"):
        prompt = """Analyze and prioritize these 10 clients by churn risk:
        Client A: sentiment=0.8, payment=+2, util=85%, satisfaction=0.9, ticket_freq=0.8, contract_trend=+0.15
        Client B: sentiment=-0.5, payment=-10, util=40%, satisfaction=0.4, ticket_freq=2.0, contract_trend=-0.15
        Client C: sentiment=0.2, payment=-3, util=60%, satisfaction=0.7, ticket_freq=1.2, contract_trend=0
        ... (7 more similar clients)
        
        Show total at-risk count, distribution by risk level, and top 3 to prioritize."""
        
        with st.spinner("Analyzing portfolio..."):
            result = invoke_agent(prompt)
        
        st.json(result)

# ==================== RECOMMENDATIONS ====================
elif page == "Recommendations":
    st.header("Retention Strategy Generator")
    
    risk_level = st.selectbox("Risk Level", ["critical", "high", "medium", "low"])
    client_value = st.number_input("Annual Contract Value ($)", 5000, 500000, 50000)
    
    factors = st.multiselect(
        "Risk Factors",
        ["communication_sentiment", "payment_timeliness", "service_utilization",
         "response_satisfaction", "ticket_frequency_trend"],
        default=["communication_sentiment", "payment_timeliness"]
    )
    
    if st.button("💰 Generate Retention Plan"):
        factors_str = ", ".join(factors)
        prompt = f"""Generate retention recommendations for a {risk_level} risk client 
        with risk factors: {factors_str}. Annual contract value: ${client_value}.
        
        Provide: (1) top 3 actions, (2) success probability for each, (3) estimated ROI"""
        
        with st.spinner("Generating plan..."):
            result = invoke_agent(prompt)
        
        st.json(result)

st.sidebar.divider()
st.sidebar.write(f"**Server Status:** {'✅ Connected' if requests.get(f'{API_URL}/ping').status_code == 200 else '❌ Disconnected'}")
