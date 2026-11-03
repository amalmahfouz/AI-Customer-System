from prompts import build_support_agent_prompt
from llm import ask_llm
from helper2 import ( clean_json_response, generate_ticket_id, create_ticket_record)

def process_new_ticket(customer_name: str, contact_info: str, message: str, existing_tickets: list) -> dict:
   
    cleaned_msg = message.strip() if message else ""
    if len(cleaned_msg) < 10:
        return {
            "status": "error",
            "message": "عذراً، يجب أن تحتوي الرسالة على 10 أحرف على الأقل لشرح المشكلة بشكل واضح."
        }
    

    ticket_id = generate_ticket_id(existing_tickets)
    

    system_prompt, user_prompt = build_support_agent_prompt(
        customer_name=customer_name,
        message=cleaned_msg,
        contact_info=contact_info
    )
    
    raw_response = ask_llm(system_prompt, user_prompt)
    
  
    agent_analysis = clean_json_response(raw_response)
    

    ticket_record = create_ticket_record(
        ticket_id=ticket_id,
        customer_name=customer_name,
        contact_info=contact_info,
        message=cleaned_msg,
        agent_analysis=agent_analysis
    )
    
    return {
        "status": "success",
        "ticket": ticket_record
    }