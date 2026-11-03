# AI Customer Support System 

An intelligent customer support ticket management system built with Streamlit, Python, and Qwen3-Coder LLM. The system automates ticket classification, policy-based priority assignment, missing info detection, and response drafting while keeping human agents in the loop via a review dashboard.


Target User
This system is designed for **Customer Support Representatives and Managers** at small to medium e-commerce companies who need to triage incoming requests efficiently without replacing the human touch.


 Key Features
- Automated Classification: Classifies support queries into Delivery, Billing, Technical Support, or Other.
- Policy-Based Prioritization: Assigns Low, Medium, or High priority using strict company support policies.
- Missing Information Guard: Automatically requests missing details (e.g., Order IDs) and flags status as Waiting for Info.
- Security Escalation: Escalates abusive language, credential requests, or sensitive queries directly to human supervisors.
- Human-In-The-Loop Dashboard: Allows support representatives to review, edit, approve, escalate, or resolve tickets with dynamic metrics tracking.

 Architecture & Project Structure
AI Customer System/



 .env # API keys and environment variables

 config.py # Model and runtime configurations

 prompts.py # Structured JSON prompts for classification & policy rules

 llm.py # OpenAI API client wrapper

 helper.py # Ticket record formatting, unique ID generation, and dashboard metrics

 full_system.py # Core orchestration agent

 app.py # Streamlit dual-tab UI (Customer Portal + Agent Dashboard)

 PROJECT_PLAN.md # Design document

 TEST_RESULTS.md # Acceptance test results

 README.md # Documentation and setup guide

 database.py # SQLite database initialization and CRUD operations



 Setup & Execution Guide

 1. Prerequisites
- Python 3.8 or higher.
- A valid Hugging Face / Novita API Key for LLM access.

2. Installation
Install the required dependencies:
```bash
pip install streamlit openai python-dotenv

3. Environment Configuration
Create a .env file in the root folder and add your API key:
HF_API_KEY=your_huggingface_api_key_here

4. Running the Application
Launch the Streamlit web server:
streamlit run app.py


Usage Workflow
Customer Portal (Tab 1): Customers enter their name, contact info, and issue details. The system validates inputs and returns a unique Ticket ID (TCK-XXXX)

.
Agent Dashboard (Tab 2): Support agents view aggregated metrics, filter tickets by status or priority, review AI-generated reasoning, edit response drafts, and click Approve & Resolve or Escalate.
