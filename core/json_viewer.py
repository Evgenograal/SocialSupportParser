import os
import json

def get_json_files(folder):
    files = []

    for root, _, filenames in os.walk(folder):
        for filename in filenames:
            if filename.lower().endswith(".json"):
                files.append(os.path.join(root, filename))
        
        return files
    
def load_json_file(file_path):
    with open(file_path, "r", encoding = "utf-8") as f:
        return json.load(f)