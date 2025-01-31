# Функция поиска в Google Custom Search API
import requests
from configAPI import API_KEY, CSE_ID
from fastapi import HTTPException


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