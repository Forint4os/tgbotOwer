tickets = []
ticket_id = 0


def create_ticket(user_id: int, username: str, category: str, text: str):
    global ticket_id

    ticket_id += 1

    ticket = {
        "id": ticket_id,
        "user_id": user_id,
        "username": username,
        "category": category,
        "text": text,
        "answered": False
    }

    tickets.append(ticket)
    return ticket


def get_tickets():
    return tickets


def get_ticket_by_id(tid: int):
    for t in tickets:
        if t["id"] == tid:
            return t
    return None
