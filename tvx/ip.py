import requests

def investigate_ip(ip):
    url = f"http://ip-api.com/json/{ip}"
    data = requests.get(url).json()

    for k, v in data.items():
        print(f"[+] {k}: {v}")
