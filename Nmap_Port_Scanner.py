import subprocess
import re
import json
import sys

if len(sys.argv) < 3:
    print("Использование: python3 nmap_scanner.py <host> <порты>")
    print("Пример: python3 nmap_scanner.py 127.0.0.1 8000,8080")
    sys.exit(1)
host=sys.argv[1]
ports=sys.argv[2]

def scan_ports(host, ports):
    try:
        test=subprocess.run(["nmap", "-p", ports, host], capture_output=True, text=True)
        pattern=r"(\d+)/tcp\s+(\w+)\s+(\S+)"
        text=re.findall(pattern, test.stdout)
        open_ports={}
        for fir, sec, thir in text:
            if sec=="open":
                open_ports[fir]=thir
        return open_ports
    except FileNotFoundError:
        return None

def save_json(data, filename):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def load_json(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            loaded=json.load(f)
            return loaded
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

result=scan_ports(host, ports)

if result is not None:
    save_json(result, "scan.json")
print(load_json("scan.json"))
