import requests
import json
import time

def ask_ollama(question, parameters):
    base_url = "http://10.xx.xx.xxx:xxxxx/api/chat"
    headers = {
        "Content-Type": "application/json"
    }

    data = {
        "model": model_name,
        "messages": [
            {
                "role": "user",
                "content": question + " Bitte antworte ausschließlich im JSON-Format mit den Feldern: answer.",
            }
        ],
        "stream": False,
        "format": "json",
        "options": {
            "temperature": parameters.get("temperature", 0.7),
            "top_p": parameters.get("top_p", 0.9),
            "repeat_penalty": parameters.get("repeat_penalty", 1.1),
        }
    }

    start_time = time.time()
    response = requests.post(base_url, json=data, headers=headers)
    duration = time.time() - start_time

    if response.status_code == 200:
        try:
            response_json = response.json()
            content_str = response_json["message"]["content"]
            content = json.loads(content_str)

            return (
                content.get("question", question),
                content.get("answer", ""),
                content.get("sources", []),
                round(duration, 2)
            )

        except (json.JSONDecodeError, KeyError) as e:
            raise ValueError(f"Fehler beim Parsen der Antwort: {e}\nAntworttext: {response.text}")
    else:
        raise ConnectionError(f"Fehlerhafte API-Antwort: {response.status_code} – {response.text}")


