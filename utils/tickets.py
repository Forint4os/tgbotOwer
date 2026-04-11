from database.db import add_ticket


def create_ticket(user_id: int, username: str, category: str, text: str):
    """
    Создаёт тикет в базе данных и возвращает структуру тикета
    """

    ticket_id = add_ticket(user_id, username, category, text)

    return {
        "id": ticket_id,
        "user_id": user_id,
        "username": username,
        "category": category,
        "text": text
    }
