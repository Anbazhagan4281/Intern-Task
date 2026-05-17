import os
from datetime import datetime

def scan_folder(path):
    files = []

    try:
        for file in os.listdir(path):
            full_path = os.path.join(path, file)

            if os.path.isfile(full_path):

                if "." in file:
                    file_type = file.split('.')[-1]
                else:
                    file_type = "unknown"

                modified_time = datetime.fromtimestamp(
                    os.path.getmtime(full_path)
                ).strftime("%Y-%m-%d %H:%M")

                files.append({
                    "name": file,
                    "size": os.path.getsize(full_path),
                    "type": file_type,
                    "modified": modified_time,
                    "path": full_path   
                })

    except PermissionError:
        print("Permission denied")

    except FileNotFoundError:
        print("Folder not found")

    return files