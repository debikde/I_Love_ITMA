# Функция поиска в Google Custom Search API
import requests
from fastapi import HTTPException
API_KEY = "AIzaSyA_Q_6OQPxLu17RXYZ3xZuC6Lpc3BZ9eD8"
CSE_ID = "c056f5f6858d2413b"

def google_search(query: str):
    search_url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={API_KEY}&cx={CSE_ID}"
    response = requests.get(search_url)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error with Google search API.")
    results = response.json().get('items', [])

    sources = []
    contexts = []

    # Собираем ссылки и текстовые фрагменты из результатов
    for result in results:
        if 'link' in result and 'snippet' in result:
            sources.append(result['link'])
            contexts.append(result['snippet'])

    return contexts, sources