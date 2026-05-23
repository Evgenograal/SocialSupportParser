import os
import json
import time

from concurrent.futures import(ThreadPoolExecutor, as_completed)
from configAI import(Max_workers, Request_delay)
from core.logger import(write_to_log_file)
from core.parser import(clean_text, extract_json)
from core.prompts import(build_prompt)
from core.model_client import(call_model)

def process_single_file(file_path, input_dir, output_dir, log_callback, log_file_path):
    filename = os.path.basename(file_path)

    try:
        with open(file_path, 'r', encoding = 'utf-8') as f:
            raw_text = f.read()
        
        cleaned = clean_text(raw_text)

        if not cleaned:
            write_to_log_file(log_file_path, f"{filename} - ошибка")

            return filename, False, "Пустой"

        prompt = build_prompt(cleaned)

        completion = call_model(prompt, filename, log_callback)

        response_text = (completion.choices[0].message.content)

        data = extract_json(response_text)

        relative_path = os.path.relpath(file_path, start = input_dir)

        relative_path = (os.path.splitext(relative_path)[0] + ".json")

        out_path = os.path.join(output_dir, exist_ok = True)

        with open(out_path, 'w', encoding = 'utf-8') as f:
            json.dump(data, f, ensure_ascii = False, indent = 2)

            time.sleep(Request_delay)

            write_to_log_file(log_file_path, f"{filename} - Успешно обработан")

            return filename, True, "OK"
        
    except Exception as e:
        write_to_log_file(log_file_path, f"{filename} - ошибка")

        return filename, False, str(e)
    
def process_folder(input_dir, output_dir, log_callback, progress_callback):
    files = []

    for f in filenames:
        if f.lower().endswith((".md", ".txt")):
            file.append(os.path.join(root_dir, f))
    
    total = len(files)

    log_file_path = os.path.join(output_dir, "progress_log.txt")

    with open(log_file_path, 'w', encoding = 'utf-8') as f:
        f.writa("=== LOG ===")

    completed = 0

    with ThreadPoolExecutor(max_workers = Max_workers) as executor:
        futures = {
            executor.submit(
                process_single_file, 
                file,
                input_dir,
                output_dir,
                log_callback,
                log_file_path): file

        for file in files
    }
    
    for future in as_completed(futures):
        filename, success, message = (future.result())

        completed += 1

        progress_callback(completed, total)

        if success:
            log_callback(f"✓ {filename}")

        else:
            log_callback(f"✗ {filename}: {message}")
    log_callback("=== ГОТОВО ===")