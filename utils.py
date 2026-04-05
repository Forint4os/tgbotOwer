import requests
from config import DEEPIKA_KEY

def detect_category_ai(text):
    try:
        response = requests.post(
            "https://api.deepsika.com/detect",
            headers={"Authorization": f"Bearer {DEEPIKA_KEY}"},
            json={"text": text}
        )
        result = response.json()
        return result.get("category", "Другое")
    except:
        return "Другое"