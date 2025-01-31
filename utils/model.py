import re
from langchain_gigachat import GigaChat

from utils.search import google_search

system_message = """
Ты — языковая модель, предназначенная исключительно для работы с запросами, связанными с Университетом ИТМО.
1. Ты не должен отвечать на запросы, которые не касаются Университета ИТМО."
"""
giga_chat = GigaChat(credentials="MzM2MjdkNTMtMzMyOS00N2NiLWFjY2UtYjNjYjIzYWFjNTgyOmRlMzBkOGRmLTg2ZTktNGZkNy1hMDU0LTI4ZWU3Y2U3NzQ5MQ==", verify_ssl_certs=False)
def extract_answer_options(query: str):
    matches = re.findall(r"(\d+)\.\s+([^\n]+)", query)
    return {int(num): text.strip() for num, text in matches}

def parse_model_response(model_response: str):
    match = re.match(r"^(\d+)\.\s*(.*)", model_response.strip())
    if match:
        answer_number = int(match.group(1))
        explanation = match.group(2).strip()
        return answer_number, explanation
    else:
        return None, model_response.strip()
def get_answer_from_model(query: str,  contexts: list):
    contexts = contexts[500:]
    try:
        if ("ИТМО" or "итмо" or "itmo" or "ITMO" or "Итмо") not in query:
            return 0, "Извините, я могу отвечать только на вопросы о Университете ИТМО."

        options = extract_answer_options(query)

        if options:
            prompt = f"{system_message}\n"
            prompt += (
                f"Ты получаешь вопрос с вариантами ответов. Твоя задача — выбрать правильный вариант и предоставить объяснение. "
                f"Ответ должен быть структурирован так:\n"
                f"- В первой строке ты указываешь номер правильного ответа (например, 1, 2, 3 или 4) Без знаков препинания\n"
                f"- В следующей строке ты даешь объяснение твоего ответа "
                f"Вопрос: {query}\nИнформация из сети:\n{contexts}\nВыберите правильный ответ из вариантов:\n"
            )
            for num, option in options.items():
                prompt += f"{num}. {option}\n"
            prompt += "Ответ:"


            model_response = giga_chat.predict(prompt)
            generated_text = model_response.strip()
            print(generated_text)
            answer_number, explanation = parse_model_response(generated_text)
            explanation += 'Ответ с помощью GigaChat'
            return answer_number, explanation

        prompt = f"Вопрос: {query}\nИнформация из сети: {contexts}\nОтвет:"
        reasoning = giga_chat.predict(prompt)
        return 0, reasoning.strip()

    except Exception as e:
        return 0, f"Ошибка: {str(e)}"


def check_model_knowledge(query: str):
    prompt = f"Вопрос: {query}\nОтвет:"
    model_response = giga_chat.predict(prompt)
    if "не знаю" in model_response or "не могу ответить" in model_response:
        return False
    return True


def main_agent(query: str):
    contexts = ' '
    sources = []
    if not check_model_knowledge(query):
        contexts, sources = google_search(query)
        sources = sources[:3]
        return get_answer_from_model(query, contexts)

    answer_number, explanation = get_answer_from_model(query, contexts)
    return answer_number, explanation, sources
