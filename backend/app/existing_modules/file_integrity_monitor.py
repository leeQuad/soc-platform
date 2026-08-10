import hashlib
import os
import json


def calculate_hash(filepath: str) -> str:
    sha256 = hashlib.sha256()

    with open(filepath, "rb") as file:
        while chunk := file.read(4096):
            sha256.update(chunk)

    return sha256.hexdigest()


def scan_files(folder_to_monitor: str) -> dict:
    file_hashes = {}

    for filename in os.listdir(folder_to_monitor):
        filepath = os.path.join(folder_to_monitor, filename)

        if os.path.isfile(filepath):
            file_hashes[filename] = calculate_hash(filepath)

    return file_hashes


def load_old_hashes(hash_file: str) -> dict:
    if not os.path.exists(hash_file):
        return {}

    with open(hash_file, "r") as file:
        return json.load(file)


def save_hashes(hashes: dict, hash_file: str) -> None:
    with open(hash_file, "w") as file:
        json.dump(hashes, file, indent=4)


def run_integrity_check(folder_to_monitor: str, hash_file: str) -> dict:
    """
    Compares current file hashes against the last saved snapshot.

    Same detection logic as the original monitior1.py — just wrapped in
    a function that returns structured results instead of printing them,
    so it can be called from an API endpoint. Also persists the new
    snapshot to hash_file, exactly like the original script did.
    """
    old_hashes = load_old_hashes(hash_file)
    new_hashes = scan_files(folder_to_monitor)

    new_files = []
    changed_files = []
    deleted_files = []

    for file, hash_value in new_hashes.items():
        if file not in old_hashes:
            new_files.append(file)
        elif old_hashes[file] != hash_value:
            changed_files.append(file)

    for file in old_hashes:
        if file not in new_hashes:
            deleted_files.append(file)

    save_hashes(new_hashes, hash_file)

    return {
        "new_files": new_files,
        "changed_files": changed_files,
        "deleted_files": deleted_files,
    }


if __name__ == "__main__":
    FOLDER_TO_MONITOR = "monitored_files"
    HASH_FILE = "hashes.json"

    results = run_integrity_check(FOLDER_TO_MONITOR, HASH_FILE)

    for f in results["new_files"]:
        print(f"[NEW FILE] {f}")
    for f in results["changed_files"]:
        print(f"[CHANGED] {f}")
    for f in results["deleted_files"]:
        print(f"[DELETED] {f}")
