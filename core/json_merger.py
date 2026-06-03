import os
import shutil

def collect_json_files(json_dirs):
    json_map = {}

    for json_dir in json_dirs:
        for root, _, files in os.walk(json_dir):
            for file in files:
                if file.endswith(".json"):
                    name_without_ext = os.path.splitext(file)[0]

                    full_path = os.path.join(root, file)

                    json_map[name_without_ext] = full_path
    return json_map

def merge_json_to_md(md_dir, json_dirs, log_callback, progress_callback):
    json_map = collect_json_files(json_dirs)
    md_files = []

    for root, _, files in os.walk(md_dir):
        for file in files:
            if file.endswith(".md"):
                md_files.append(os.path.join(root, file))

    total = len(md_files)
    completed = 0

    copied = 0
    not_found = 0

    for md_path in md_files:
        md_name = os.path.splitext(os.path.basename(md_path))[0]        
        md_folder = os.path.dirname(md_path)

        if md_name in json_map:
            json_source = json_map[md_name]

            json_target = os.path.join(md_folder, md_name + ".json")

            try:
                shutil.copy2(json_source, json_target)

                copied += 1

                log_callback(f"✓ {md_name}.json скопирован")

            except Exception as e:
                log_callback(f"✗ Ошибка копирования {md_name}: {e}")
        
        else:
            not_found += 1

            log_callback(f"✗ JSON не найден: {md_name}")
        
        completed += 1

        progress_callback(completed, total)

    log_callback(f"\nСкопировано: {copied}")
    log_callback(f"Не найдено: {not_found}")
