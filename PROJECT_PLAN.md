
Project Name:
   AI Customer Support Assistant (TechGear Support Hub)

Problem Statement:
     Customer support teams at e-commerce companies receive large volumes of unorganized messages daily. Sorting tickets manually, prioritizing urgent cases, and drafting accurate responses is repetitive, time-consuming, and prone to human error.


Realistic Example:
    A customer sends a message saying "My credit card was charged twice for order, refund me now!"
    - This urgent message might sit in an unread queue for hours without automated prioritization.


Target User:
   Customer Support Representatives and Support Managers at TechGear Store.


Goal:
    Automatically ingest incoming customer messages, categorize them, assign priority based on company policy, flag security risks or missing information, generate polite response drafts labeled for human review, and present them in an actionable dashboard.



Scope:

--WILL DO:
  1. Validate incoming customer messages and reject empty/overly short submissions.
  2. Generate unique ticket IDs (TCK-XXXX) and store tickets in an in-memory session store (or SQLite database).
  3. Classify messages into predefined categories (Delivery, Billing, Technical Support, Other) with supporting reasoning.
  4. Assign priority (Low, Medium, High) according to a strict company policy.
  5. Identify missing details (e.g., missing Order ID) and set ticket status to Waiting for Info.
  6. Generate polite proposed draft replies labeled strictly as Draft - human review required.
  7. Escalate sensitive requests (e.g., threats, password requests, credentials) without sending automated replies.
  8. Provide a human review dashboard allowing agents to edit, approve, reject, or resolve tickets.


--WILL NOT DO:
  1. Automatically send emails or messages directly to customers without human agent approval.
  2. Ask for sensitive user credentials, passwords, or full credit card numbers.


Example Out-of-Scope Request:
      "Here is my account password '123456', please log in and change my home address."

Input Contract
| Input Field | Required? | Type | Example Value | Handling Missing/Invalid Input |

Customer Name        No | String | "Amal Mh" | Defaults to "Anonymous Customer" if left blank. 
Contact Info         No | String | "AmalMH@example.com" | Optional field for reference. 
Customer Message    Yes | String | "My package hasn't arrived yet and it's been a week." | Rejects input if under 10 characters and displays a validation alert asking for more detail. 


Outputs Generated:

  1. Ticket Record Entry (TCK-XXXX).
  2. Category & Priority labels with clear explanation.
  3. Ticket Status (Open, Waiting for Info, Escalated, Resolved).
  4. Proposed Response Draft marked as "Draft - human review required".
  5. Actionable Support Dashboard with status update buttons for human agents.

Sample Output (Invented Data):
  Ticket ID: TCK-1002
  Customer: Amal Mh
  Category: Delivery
  Priority: Medium
  Status: Waiting for Info
  Draft Response:"Dear Amal, thank you for reaching out to TechGear Support. We would be happy to check your shipment status. Could you please provide your 4-digit Order ID?"


Workflow
Customer Submits Form -> Input Validation -> Generate Unique Ticket ID -> LLM Agent Evaluation

  - Path A (Missing Essential Data): Status set to "Waiting for Info" -> Specific follow-up query generated -> Added to Agent Dashboard.

  - Path B (Security / Policy Exception): Status set to "Escalated" -> Security alert flagged -> No automated draft sent.

  - Path C (Complete Valid Request): Classified into Category & Priority -> Response Draft created -> Added to Dashboard for Human Agent Approval/Resolution.



Agent Specification
Goal:
   Evaluate customer inquiries, enforce company categorization and priority policies, guard against security risks, and assist support agents with high-quality response drafts.


Allowed Actions:
1.classify_ticket 
2.assign_priority 
3.ask_for_info
4.draft_response
5.escalate
6.finish


Decision Rules:
  1. If message contains threats, harassment, or requests passwords/credentials -> Trigger [escalate].
  2. If message lacks required context (e.g., complaining about a delivery without an Order ID) -> Trigger [ask_for_info].
  3. If message is a valid complaint/query -> Trigger [classify_ticket] + [assign_priority] + [draft_response].

Permissions: Restricted to structured JSON outputs; no dynamic Python code execution.



 Data Preparation & Policy Rules
Supported Categories:
   Delivery: Shipping delays, tracking issues, wrong address.
   Billing: Double charges, refund requests, payment gateway errors.
   Technical Support: Defective products, warranty queries, setup help.
  Other: General inquiries outside standard business operations.


Priority Matrix:
  High: Double billing, damaged goods on arrival, escalated complaints.
  Medium: Delayed shipments, standard refund requests.
  Low: General product specification or setup questions.

Interface Sketch
Tab 1: Customer Portal (Submit Ticket)
  Customer Name & Contact Input Fields.
  Message Text Area.
  Submit Button.
  Submission Status Confirmation Card showing Ticket ID.

Tab 2: Agent Review Dashboard (Human-In-The-Loop)
   Ticket Metrics (Total, Open, Waiting, Escalated, Resolved).
   Filter by Status/Priority.
   Collapsible Ticket Cards displaying:
    - Original message + Metadata.
    - Category & Priority badges.
    - AI Draft Response text area (Editable).
    - Action Buttons: Approve & Resolve, Escalate, Delete.


Success Tests
|T1 - Valid Classification | 3 distinct messages assigned correct categories (Delivery, Billing, Technical Support).

|T2 -Missing Detail Handling|  Order query missing Order ID sets status to "Waiting for Info" and "asks a follow-up question".

|T3 - Security Escalation| Message asking for account password triggers "Escalated" status with safety warnings.

|T4 - Human Review Workflow| Agent can edit AI draft response and update status to "Resolved".

|T5 - Validation & Uniqueness| Blank/short form submission is blocked; consecutive submissions yield unique IDs (TCK-1001, TCK-1002).



Technology Plan
Known Concepts: Python, System Prompts, Agent Workflows, JSON parsing.

Self-Learned Tools:
  Streamlit: Forms (st.form), Tabs (st.tabs), Session State (st.session_state)
  SQLite / In-Memory State: Ticket records persistence.

;; Build Order
;; - Phase 1 (MVP): Form input validation + LLM Intent & Classification JSON parser + In-Memory Ticket store.
;; - Phase 2 (Dashboard & Review): Human Review Dashboard with status toggles (Approve, Escalate, Resolve).
;; -Phase 3 (Enhancements & Persistence): SQLite persistence layer + statistics metrics + safety rule enforcement.
