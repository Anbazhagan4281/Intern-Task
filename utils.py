import re

def search_files(keyword, files):
    result = []

    for f in files:
        if re.search(keyword, f["name"], re.IGNORECASE):
            result.append(f)

    return result