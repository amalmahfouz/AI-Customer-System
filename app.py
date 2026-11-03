import streamlit as st
from helper2 import calculate_dashboard_metrics
from full_system import process_new_ticket
import database as db

# Initialize Database 
db.init_db()


st.set_page_config(
    page_title="TechGear Support Hub",
    layout="wide"
)


st.markdown("""
    <style>
    /* Global modern font */
    .stApp {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Box Card styling with Blue Hover effect */
    div[data-testid="stExpander"] {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        transition: all 0.3s ease-in-out;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
        margin-bottom: 15px;
    }
    
    div[data-testid="stExpander"]:hover {
        border-color: #2563eb !important;
        box-shadow: 0 4px 12px rgba(37,99,235,0.15) !important;
    }

    /* Modern Buttons */
    .stButton>button {
        border-radius: 6px;
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)

# header 
st.title("TechGear Support Hub")

# tabs
tab_customer, tab_agent = st.tabs(["Customer Portal", "Agent Review Dashboard"])


# Customer Portal
with tab_customer:
    st.subheader("Submit a New Support Ticket")
    st.write("Please fill out the form below. Your request will be routed automatically.")
    
    with st.form(key="ticket_submission_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            cust_name = st.text_input("Customer Name (Optional)", placeholder="e.g., Amal mahfouz")
        with col2:
            cust_contact = st.text_input("Contact Info (Optional)", placeholder="amal@example.com")
            
        cust_message = st.text_area("Message / Issue Description *", placeholder="Describe your issue in detail (at least 10 characters)...", height=120)
        
        submit_button = st.form_submit_button(label="Submit Ticket")
        
    if submit_button:
        with st.spinner("Analyzing request and generating ticket via AI..."):
            
            # Fetch existing tickets directly from DB to generate a unique sequential ID
            current_tickets = db.get_all_tickets()
            
            result = process_new_ticket(
                customer_name=cust_name,
                contact_info=cust_contact,
                message=cust_message,
                existing_tickets=current_tickets
            )
            
            if result["status"] == "error":
                st.error(f"Error: {result['message']}")
            else:
                new_ticket = result["ticket"]
                
                # insert
                db.insert_ticket(new_ticket)
                
                st.success(f"Success! Your ticket has been created. Reference ID: {new_ticket['ticket_id']}")
                
                with st.expander("View Submitted Details", expanded=True):
                    st.write(f"**Ticket ID:** {new_ticket['ticket_id']}")
                    st.write(f"**Initial Category:** {new_ticket['category']}")
                    st.write(f"**Current Status:** {new_ticket['status']}")


#  support team Dashboard
with tab_agent:
    st.subheader("Human Review & Approval Board")
    
    # Fetch all tickets  from the database
    all_tickets = db.get_all_tickets()
    
   
    metrics = calculate_dashboard_metrics(all_tickets)
    m_col1, m_col2, m_col3, m_col4, m_col5 = st.columns(5)
    
    m_col1.metric("Total Tickets", metrics["total"])
    m_col2.metric("Open", metrics["open"])
    m_col3.metric("Waiting for Info", metrics["waiting"])
    m_col4.metric("Escalated", metrics["escalated"])
    m_col5.metric("Resolved", metrics["resolved"])
    
    st.divider()
    
    f_col1, f_col2 = st.columns(2)
    with f_col1:
        status_filter = st.selectbox("Filter by Status:", ["All", "Open", "Waiting for Info", "Escalated", "Resolved"])
    with f_col2:
        priority_filter = st.selectbox("Filter by Priority:", ["All", "High", "Medium", "Low"])
        
    filtered_tickets = all_tickets
    if status_filter != "All":
        filtered_tickets = [t for t in filtered_tickets if t.get("status") == status_filter]
    if priority_filter != "All":
        filtered_tickets = [t for t in filtered_tickets if t.get("priority") == priority_filter]
        
    st.write(f"Showing **{len(filtered_tickets)}** ticket(s):")
    
    # Tickets Review
    if not filtered_tickets:
        st.info("No tickets match the current filters.")
    else:
        for ticket in reversed(filtered_tickets):
            ticket_id = ticket["ticket_id"]
            
            with st.expander(f"{ticket_id} | Priority: {ticket['priority']} | Category: {ticket['category']} | Status: {ticket['status']}"):
                col_left, col_right = st.columns([1, 1])
                
                with col_left:
                    st.markdown("### Message Details")
                    st.write(f"**Customer:** {ticket['customer_name']} ({ticket['contact_info']})")
                    st.write(f"**Created At:** {ticket['created_at']}")
                    st.write("**Original Message:**")
                    st.info(f"\"{ticket['message']}\"")
                    st.write("**AI Reasoning:**")
                    st.caption(ticket['reasoning'])
                    
                    if ticket.get("escalation_reason"):
                        st.error(f"Escalation Reason: {ticket['escalation_reason']}")

                with col_right:
                    st.markdown("### Response & Actions")
                    
                    if ticket.get("status") == "Resolved":
                        st.success("Approved and Sent to Customer")
                    else:
                        st.warning("Automated Draft - Requires Human Approval")
                        
                    edited_draft = st.text_area(
                        "Final Response (Editable):",
                        value=ticket.get("draft_response") or "",
                        key=f"draft_{ticket_id}",
                        height=150
                    )
                    
                    b_col1, b_col2, b_col3 = st.columns(3)
                    
                    with b_col1:
                        if st.button("Approve & Close", key=f"approve_{ticket_id}"):
                            # Update database
                            db.update_ticket_action(ticket_id, "Resolved", edited_draft, False)
                            st.rerun()
                            
                    with b_col2:
                        if st.button("Escalate Ticket", key=f"esc_{ticket_id}"):
                            # Escalate in database
                            db.update_ticket_action(ticket_id, "Escalated", edited_draft, False)
                            st.rerun()
                            
                    with b_col3:
                        if st.button("Delete Ticket", key=f"del_{ticket_id}"):
                            # Delete from database
                            db.delete_ticket(ticket_id)
                            st.rerun()