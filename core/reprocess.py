import os

from core.process_processing import (process_single_file)

import shutil

def get_failed_files(log_file_path):
    failed_files = []

    with open(log_file_path, 'r', encoding = "utf-8") as f:
        for line in f:
            line = line.strip()

            if "ошибка" in line.lower():
                
                filename = (line.split(" - ")[0])
                failed_files.append(filename)
    return failed_files

def reprocess_failed_files(input_dir, output_dir, log_file_path, log_callback, progress_callback):
    
    failed_files = get_failed_files(log_file_path)
    files_to_process = []

    for root, _, filenames in os.walk(input_dir):
        for f in failed_files:
            if f in filenames:
                files_to_process.append(os.path.join(root, f))
    
    total = len(files_to_process)

    completed = 0

    retry_log = os.path.join(output_dir, "retry_log.txt")

    with open(retry_log, 'w', encoding = 'utf-8') as f:
        f.write("=== RETRY LOG ===\n")

    failed_output_dir = os.path.join(output_dir, "failed_files_retry")

    os.makedirs(failed_output_dir, exist_ok = True)

    for file_path in files_to_process:
        filename, success, message = (
            process_single_file(
                file_path,
                input_dir,
                output_dir,
                log_callback,
                retry_log
            )
        )

        completed += 1

        progress_callback(completed, total)

        if success:
            log_callback(f"✓ успешная повторная обработка: {filename}")

        else: 
            log_callback(f"✗ ошибка: {filename}: {message}")
            try:
                shutil.copy2(file_path, os.path.join(failed_output_dir, filename))
            except Exception as copy_error:
                log_callback(f"Ошибка копирования файла:{filename}: {copy_error}")
    
    log_callback("=== ПОВТОРНАЯ ОБРАБОТКА ГОТОВА ===")