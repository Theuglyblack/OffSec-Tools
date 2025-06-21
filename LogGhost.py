import os
import psutil
import time
from datetime import datetime

def detect_hidden_processes():
    print("[*] Buscando procesos ocultos o sin nombre...")
    for proc in psutil.process_iter(['pid', 'name']):
        if not proc.info['name']:
            print(f"[!] Proceso oculto detectado: PID {proc.info['pid']}")

def detect_anomalous_files(base_path="/"):
    print("[*] Escaneando timestamps de archivos...")
    for root, dirs, files in os.walk(base_path):
        for name in files:
            try:
                path = os.path.join(root, name)
                stat = os.stat(path)
                create_time = datetime.fromtimestamp(stat.st_ctime)
                if create_time.year < 2000 or create_time > datetime.now():
                    print(f"[!] Timestamp anómalo: {path} -> {create_time}")
            except Exception:
                continue

def main():
    detect_hidden_processes()
    detect_anomalous_files("/home" if os.name != 'nt' else "C:\\Users")

if __name__ == "__main__":
    main()
