MESSAGES = []
MSG_COUNTER = 1

def add_message(from_user, to_user, category, text):
    global MSG_COUNTER
    msg = [MSG_COUNTER, from_user, category, text, "🆕"]
    MESSAGES.append(msg)
    MSG_COUNTER += 1
    return msg[0]

def get_messages_for_admin(admin_id):
    return [msg for msg in MESSAGES if msg[1] == admin_id or msg[1] != admin_id]

def get_messages_by_category(admin_id, category):
    return [msg for msg in MESSAGES if msg[2] == category]

def get_message_by_id(msg_id):
    for msg in MESSAGES:
        if msg[0] == msg_id:
            return msg
    return None

def update_message_status(msg_id, status):
    msg = get_message_by_id(msg_id)
    if msg:
        msg[4] = status

def get_stats(admin_id):
    total = len(MESSAGES)
    new = len([m for m in MESSAGES if m[4] == "🆕"])
    done = len([m for m in MESSAGES if m[4] == "✅"])
    categories = []
    for cat in ["💼 Работа", "💰 Выплата", "🤝 Коллаб", "⚠️ Ошибки", "🆘 Поддержка", "👤 Личное", "📌 Другое"]:
        count = len([m for m in MESSAGES if m[2] == cat])
        categories.append((cat, count))
    return total, new, done, categories