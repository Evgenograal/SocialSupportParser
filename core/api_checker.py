from openai import OpenAI

def check_api_key(api_key, base_url, model):
    try:
        client = OpenAI(api_key=api_key, base_url=base_url)
        client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role":"user",
                    "content":"test"
                }
            ],
            max_tokens=1
        )

        return True

    except Exception:
        return False