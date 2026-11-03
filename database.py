import sqlite3

DB_NAME = "support_tickets.db"

def init_db():

    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tickets (
                ticket_id TEXT PRIMARY KEY,
                created_at TEXT,
                customer_name TEXT,
                contact_info TEXT,
                message TEXT,
                category TEXT,
                priority TEXT,
                status TEXT,
                reasoning TEXT,
                draft_response TEXT,
                escalation_reason TEXT,
                review_needed INTEGER
            )
        ''')
        conn.commit()

def insert_ticket(ticket: dict):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO tickets (
                ticket_id, created_at, customer_name, contact_info, message, 
                category, priority, status, reasoning, draft_response, 
                escalation_reason, review_needed
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            ticket['ticket_id'], ticket['created_at'], ticket.get('customer_name', 'Anonymous'),
            ticket.get('contact_info', ''), ticket['message'], ticket['category'],
            ticket['priority'], ticket['status'], ticket.get('reasoning', ''),
            ticket.get('draft_response', ''), ticket.get('escalation_reason', ''),
            1 if ticket.get('review_needed') else 0
        ))
        conn.commit()

def get_all_tickets() -> list:
    with sqlite3.connect(DB_NAME) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tickets ORDER BY created_at ASC")
        rows = cursor.fetchall()
        
        return [dict(row) for row in rows]

def update_ticket_action(ticket_id: str, status: str, draft_response: str, review_needed: bool):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE tickets 
            SET status = ?, draft_response = ?, review_needed = ?
            WHERE ticket_id = ?
        ''', (status, draft_response, 1 if review_needed else 0, ticket_id))
        conn.commit()

def delete_ticket(ticket_id: str):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tickets WHERE ticket_id = ?", (ticket_id,))
        conn.commit()