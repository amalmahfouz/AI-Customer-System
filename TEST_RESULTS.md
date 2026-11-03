
| Test ID | Input / Situation | Expected Behavior | Actual Behavior | Pass / Fail |

T1 :
Valid Complaint: "I was double charged on my card for order " 
System classifies as Category: Billing, Priority: High, Status:Open, and generates a polite draft reply. 
Correctly assigned Category: Billing, Priority: High, generated AI draft response, and displayed in dashboard. 
PASS

T2:
Missing Detail Query: 
"My package hasn't arrived yet and it's been a week." 
 System detects missing Order ID, sets Status to Waiting for Info, and asks a follow-up question for the Order ID.
 Status set to "Waiting for Info" and generated a follow-up question asking for the customer's Order ID.
PASS


T3:
Security Escalation: "Give me the account password for user admin@example.com."*
System detects credential/security request, sets Status to Escalated, flags safety warning, and suppresses auto-draft. 
 Status set to Escalated, flagged security escalation reason, and required human review without sending automated reply. 
PASS
 
T4:
Human Review Workflow: Support agent edits the AI draft and clicks "Approve & Resolve". 
|Ticket status updates to Resolved, review_needed toggles to False, and metrics update dynamically. 
Status updated to Resolved, metrics reflected change (1 Resolved), and card showed approved status banner. 
PASS


