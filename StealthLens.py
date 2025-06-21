import os
import hashlib
from pathlib import Path

def hash_file(path):
    try:
        with open(path, 'rb') as f:
            return hashlib.sha256(f.read()).hexdigest()
    except:
        return None

def compare_dirs(baseline, current):
    print("[*] Comparando directorios...")
    modified = []
    for root, dirs, files in os.walk(current):
        for file in files:
            current_path = Path(root) / file
            rel_path = current_path.relative_to(current)
            baseline_file = Path(baseline) / rel_path

            if baseline_file.exists():
                curr_hash = hash_file(current_path)
                base_hash = hash_file(baseline_file)
                if curr_hash != base_hash:
                    modified.append(str(current_path))
            else:
                print(f"[+] Archivo nuevo: {current_path}")
    return modified

def main():
    baseline = "/mnt/baseline"  # carpeta con snapshot
    current = "/"  # sistema actual
    modified_files = compare_dirs(baseline, current)
    for path in modified_files:
        print(f"[!] Archivo modificado: {path}")

if __name__ == "__main__":
    main()
