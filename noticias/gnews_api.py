import os
import requests
from dotenv import load_dotenv

load_dotenv()
GNEWS_API_KEY = os.getenv("GNEWS_API_KEY")

def buscar_noticias(limit=5):
    url = f"https://gnews.io/api/v4/search?q=artificial%20intelligence&lang=en&max={limit}&apikey={GNEWS_API_KEY}"

    response = requests.get(url)

    if response.status_code != 200:
        print("❌ Erro ao buscar no GNews:", response.text)
        return []

    data = response.json()
    return [
        {
            "titulo": item["title"],
            "descricao": item["description"],
            "url": item["url"]
        }
        for item in data.get("articles", [])
    ]
