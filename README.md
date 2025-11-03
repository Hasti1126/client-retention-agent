# NeuroNova: AI-Powered Client Retention & Growth Engine

**Project for SuperHack 2025 by SuperOps, Powered by AWS.**

* **Team:** NeuroNova
* **Team Leader:** Hasti Chopada
* **Hackathon Theme:** Building the Future of Agentic AI For IT Management
* **GitHub Repository:** `https://github.com/Hastil126/client-retention-agent`

---

## 🚀 Demo Video

Watch the full prototype demo on Loom:

**[https://www.loom.com/share/946e10e51bcc4ecda422b921ce197546](https://www.loom.com/share/946e10e51bcc4ecda422b921ce197546)**
[![NeuroNova Demo Video](https://cdn.loom.com/sessions/thumbnails/946e10e51bcc4ecda422b921ce197546-original.jpg)](https://www.loom.com/share/946e10e51bcc4ecda422b921ce197546)

---

## 🎯 Problem Statement & Vision

**Problem:** This project addresses the "AI-Powered Client Retention & Growth Engine" challenge.

**Idea:** NeuroNova is an autonomous AI agent designed to revolutionize how Managed Service Providers (MSPs) handle client relationships. It autonomously predicts churn risks and pinpoints growth opportunities before they become critical issues.

**Vision:** To create sustainable business growth for MSPs through AI-driven client intelligence, enabling them to thrive by fostering deeper, more valuable client relationships rather than relying on constant client acquisition.

## ✨ Key Features

The solution is built around four unique selling propositions (USPs):

1.  **MSP-Native Intelligence:**
    * Built specifically for MSP business models and client relationships.
    * Understands IT service delivery patterns and technical support dynamics.
    * Trained on MSP-specific success and failure indicators.

2.  **Predictive Relationship Health:**
    * Provides a 60-90 day early warning system for client issues.
    * Delivers real-time health scoring with confidence intervals.
    * Analyzes trends to show relationship trajectory over time.

3.  **ROI-Focused Growth Engine:**
    * Identifies high-probability upselling and cross-selling opportunities.
    * Calculates the potential revenue impact of recommended actions.
    * Optimizes client lifetime value (LTV) through strategic recommendations.

4.  **Self-Improving AI System:**
    * Learns from every client interaction and its outcome.
    * Adapts to each MSP's unique business patterns.
    * Continuously improves prediction accuracy over time.

### Core Functionality

* **Communication Intelligence:** Sentiment analysis across emails, chats, calls, and tickets.
* **Dashboard & Analytics:** An executive portfolio overview and deep-dive views for individual clients.
* **Smart Alert System:** Customizable, multi-channel notifications (Email, Slack, Teams) with priority-based routing.
* **AI Recommendation Engine:** Generates personalized retention strategies and action plans, each with a success probability score.

---

## 🛠️ Tech Stack & Architecture

### Technologies Used

| Category | Technology |
| :--- | :--- |
| **AI/ML Platform** | XGBoost, scikit-learn, TensorFlow |
| | Transformers (Hugging Face), spaCy, NLTK |
| | OpenAI GPT-4 API, LangChain framework |
| | MLflow, Apache Airflow |
| **Backend** | FastAPI (Python) |
| | PostgreSQL, Redis (caching) |
| | Celery + Redis (async tasks) |
| | Docker  |
| **Frontend** | React 18 + TypeScript |
| | Tailwind CSS + shadcn/ui |
| | Recharts + D3.js (charts) |
| | Zustand (state management) |
| **Infrastructure** | AWS (BedRock Agent Core, Strands) |
| | GitHub Actions (CI/CD) |
| **Security** | OAuth 2.0, JWT tokens |

### Architecture

The solution is built on a scalable, multi-layered architecture:

1.  **Frontend Layer:** React Dashboard and Mobile App.
2.  **API Gateway Layer:** Manages authentication, rate limiting, and load balancing.
3.  **AI Processing Engine:**
    * **NLP:** Sentiment Analysis.
    * **ML Models:** Risk Scoring & Churn Prediction.
    * **LLM Engine:** GPT-4 API + LangChain for generating recommendations.
    * **Recommendation Generator Engine**.
4.  **Data Storage Layer:** PostgreSQL, Redis Cache, ML Model Store.
5.  **Integration Layer:** Connects to MSP tools like Kaseya, Autotaske, Email APIs, and custom webhooks.

### AI/ML Pipeline

The AI model pipeline follows a clear process:
1.  **Data Sources:** Ingests data from PSA, RMM, Communication, and Usage Analytics.
2.  **Feature Engineering:** Includes data cleaning, feature extraction, normalization, and validation.
3.  **AI Models:**
    * Sentiment Analysis (NLP).
    * Churn Risk Prediction (ML).
    * Growth Opp Detection (ML).
    * Recommendation Generator (LLM).
4.  **Output Generation:** Produces risk scores, health metrics, recommendations, and explanations.

---

## 📊 Prototype Performance Report

The model's performance was optimized for accurately detecting clients who are likely to churn (high recall).

* **Model Accuracy:** 83.80%
* **Churn Detection Rate (Recall):** 84.3%
* **False Alarm Rate:** 16.3%

### Classification Report

| | precision | recall | f1-score | support |
| :--- | :--- | :--- | :--- | :--- |
| **No Churn** | 0.96 | 0.84 | 0.90 | 834 |
| **Churn** | 0.51 | 0.84 | 0.63 | 166 |
| **accuracy** | | | 0.84 | 1000 |
| **macro avg** | 0.74 | 0.84 | 0.76 | 1000 |
| **weighted avg**| 0.89 | 0.84 | 0.85 | 1000 |

### Confusion Matrix

| | Predicted: No Churn | Predicted: Churn |
| :--- | :--- | :--- |
| **Actual: No Churn** | 698 | 136 |
| **Actual: Churn** | 26 | 140 |

---

## 🖥️ Prototype Screenshots & Wireframes

### 1. Executive Dashboard (Prototype)
This is the main portfolio overview.
* **Portfolio Health:** Shows "Healthy," "At Risk," and "Critical" client counts.
* **Critical Alerts:** Highlights specific clients at high risk.
    * **Example: TechCorp Solutions**
        * **Status:** CRITICAL
        * **Health Score:** 25/100
        * **Risk:** 78% churn risk
        * **Risk Factors:** Payment delays, Low satisfaction, Underutilization
        * **AI Recommendation:** "Schedule Emergency QBR - Within 7 days (87% success rate)"
  <img width="1363" height="565" alt="image" src="https://github.com/user-attachments/assets/282e0cf8-8562-42aa-a305-199b6df59cf4" />


### 2. Client Detail View (Prototype)
A deep-dive into a specific client (e.g., TechCorp Solutions).
* **Key Metrics:**
    * **Churn Probability:** 78%
    * **Service Utilization:** 40%
    * **Support Tickets (30d):** 28
    * **Sentiment Score:** -0.6
    * **Last Contact:** 12 days ago
* **Risk Factor Breakdown:** Quantifies the impact of different issues (e.g., Payment Delays: -15pts, Low Satisfaction: -12pts).
* **AI Recommendations:** A list of prioritized actions.
    * **Example 1:** "Schedule Emergency QBR" (Success Rate: 87%).
    * **Example 2:** "Assign Dedicated Success Manager" (Success Rate: 81%).
    * **Example 3:** "Comprehensive Service Audit" (Success Rate: 76%).
<img width="1366" height="648" alt="image" src="https://github.com/user-attachments/assets/d3e96434-e82f-4c58-b761-670a6c9a135d" />

### 3. AI Recommendation Engine (Wireframe)
This view details the full, personalized action plan.
* **AI Reasoning:** Explains *why* the recommendation is being made (e.g., "Payment delays indicate...", "Recent support escalations...").
* **Action Plan:** Breaks actions into Immediate, Short-Term, and Long-Term strategies.
* **Predicted Outcomes:**
    * "Following this plan XX% chance... of retention"
    * "No action taken: XX% chance of retention"
    * "Estimated revenue saved: $XXX,000..."


<img width="1361" height="638" alt="image" src="https://github.com/user-attachments/assets/844e5069-323b-4603-9d18-23ed4344eb80" />
<img width="817" height="648" alt="image" src="https://github.com/user-attachments/assets/194ded66-31c1-453f-955d-35ea41c288a2" />


