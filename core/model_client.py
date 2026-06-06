import threading
import time
from openai import OpenAI
from core.settings import get_settings

clients = []

for key in get_settings("api_keys", []):
    clients.append(
        OpenAI(base_url = get_settings("base_url"), api_key = key)
    )

client_index = 0
client_lock = threading.Lock()

def get_client():
    global client_index

    with client_lock:
        client = clients[client_index]

        client_index = (client_index + 1) % len(clients)
    
    return client 

def call_model(prompt, filename, log_callback):
    for attemp in range(get_settings("max_retries", 10)):
        try:
            client = get_client()

            completion = (
                client.chat.completions.create(
                    model = get_settings("model"),
                    messages = [
                        {
                            'role': 'user',
                            'content': prompt
                        }
                    ],
                    temperature = 0.1,
                    response_format = {
                        "type": 'json_object'
                    }
                )
            )
        
            return completion

        except Exception as e:
            error = str(e)

            if("429" in error or "rate" in error.lower()):
                wait_time = (attemp + 1) * 5
            
                log_callback(f"{filename}: ждём, время обработки: {wait_time} секунд")

                time.sleep(wait_time)

                continue

    raise Exception("Предел попыток")