users = set()

def add_user(user_id: int):
    users.add(user_id)

def get_stats():
    return len(users)
