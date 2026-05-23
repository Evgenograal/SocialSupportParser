import threading
import time
from openai import OpenAI
from configAI import *

clients = []

for key in Api_keys:
    clients.append(
        OpenAI(base_url = Base_url, api_key = key)
    )

client_index = 0
client_lock = threading.Lock()

def get_client():
    global client_index

    with client_lock:
        client = clients[client_index]

        client_index = (client_index + 1) % len(client)
    
    return client 

def call_model(promt, filename, log_callback):
    for attemp in range(max_retries):
        try:
            client = get_client()

            completion = (
                client.chat.completions.create(
                    model = Model,
                    messages = [
                        {
                            'role': 'user',
                            'content': 'promt'
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
            
            log_callback(f"{filename}: ждём {wait_time}")

            time.sleep(wait_time)

            continue

    raise Exception("Предел попыток")