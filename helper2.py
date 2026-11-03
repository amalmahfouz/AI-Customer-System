import json
import re
from datetime import datetime


def clean_json_response(response_str: str) -> dict:
  if not response_str:
    return {}

  cleaned = re.sub(r"```(?:json)?", "", response_str, flags=re.IGNORECASE)
  cleaned = cleaned.replace("```", "").strip()

  try:
    return json.loads(cleaned)
  except Exception as e:
    print(f" failed while loading JSON : {e}")
    return {
        "category": "Other",
        "priority": "Low",
        "status": "Escalated",
        "reasoning": "failed  JSON .",
        "missing_info_question": None,
        "draft_response": None,
        "escalation_reason": "problem with chatting  .",
        "review_needed": True,
    }


def generate_ticket_id(existing_tickets: list) -> str:
    base_number = 1001
    if not existing_tickets:
        return f"TCK-{base_number}"
    
    existing_ids = []
    for ticket in existing_tickets:
        tid = ticket.get("ticket_id", "")
        if tid.startswith("TCK-"):
            try:
                num = int(tid.split("-")[1])
                existing_ids.append(num)
            except ValueError:
                pass

    if existing_ids:
        next_number = max(existing_ids) + 1
    else:
        next_number = base_number + len(existing_tickets)

    return f"TCK-{next_number}"


def create_ticket_record(ticket_id: str,customer_name: str,contact_info: str,message: str,agent_analysis: dict,) -> dict:
  now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

  status = agent_analysis.get("status", "Open")
  draft = agent_analysis.get("draft_response")

  if (
      status == "Waiting for Info"
      and agent_analysis.get("missing_info_question")
  ):
    draft = f"Draft Follow-up Question:\n{agent_analysis.get('missing_info_question')}"

  return {
      "ticket_id": ticket_id,
      "created_at": now_str,
      "customer_name": customer_name if customer_name else "Anonymous",
      "contact_info": contact_info if contact_info else "Not provided",
      "message": message,
      "category": agent_analysis.get("category", "Other"),
      "priority": agent_analysis.get("priority", "low"),
      "status": status,
      "reasoning": agent_analysis.get("reasoning", ""),
      "draft_response": draft,
      "escalation_reason": agent_analysis.get("escalation_reason"),
      "review_needed": agent_analysis.get("review_needed", True),
  }


def calculate_dashboard_metrics(tickets: list) -> dict:
  total = len(tickets)
  open_count = sum(1 for t in tickets if t.get("status") == "Open")
  waiting_count = sum(
      1 for t in tickets if t.get("status") == "Waiting for Info"
  )
  escalated_count = sum(1 for t in tickets if t.get("status") == "Escalated")
  resolved_count = sum(1 for t in tickets if t.get("status") == "Resolved")

  return {
      "total": total,
      "open": open_count,
      "waiting": waiting_count,
      "escalated": escalated_count,
      "resolved": resolved_count,
  }