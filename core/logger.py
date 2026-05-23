import threading

log_lock = threading.Lock()

def write_to_log_file(log_path, text):
    with log_lock:
        with open(log_path, 'a', encoding = 'utf-8') as f:
            f.write(text + '\n')