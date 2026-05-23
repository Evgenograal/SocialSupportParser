import re
import json

def clean_text(text:str) -> str:
    lines = text.splitlines()
    cleaned_lines = []

    for line in lines:
        line = re.sub(r'https?://\\S+', '', line)

        line = line.strip()

        if line:
            cleaned_lines.append(line)
        
    return '\n'.join(cleaned_lines)

def extract_json(response_text: str):
    
    response_text = response_text.strip()
    response_text = re.sub(r'^```json', '', response_text)
    response_text = re.sub( r'^```', '', response_text ) 
    response_text = re.sub( r'```$', '', response_text ) 
    
    json_match = re.search( r'\\{.*\\}', response_text, re.DOTALL )

    if json_match:
        json_str = json_match.group(0)
    
    else:
        json_str = response_text

    return json.loads(json_str)