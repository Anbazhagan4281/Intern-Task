def generate_report(files):
    total = len(files)
    largest = max(files, key=lambda x: x["size"])

    ext_count = {}
    for f in files:
        ext = f["type"]
        ext_count[ext] = ext_count.get(ext, 0) + 1

    common = max(ext_count, key=ext_count.get)

    return {
        "total_files": total,
        "largest_file": largest["name"],
        "common_extension": common
    }