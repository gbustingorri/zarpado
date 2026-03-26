import requests
from datetime import datetime

CLIENT_ID = "dfd197a058fba973cadf047044c0c1d1"
CLIENT_SECRET = "6869f03b8e9e57aa9a0d4ce02b345e0c"
BASE_URL = "https://api.finneg.com/api"

token = requests.get(f"{BASE_URL}/oauth/token", params={"client_id": CLIENT_ID, "client_secret": CLIENT_SECRET, "grant_type": "client_credentials"}).text.strip()
facturas = requests.get(f"{BASE_URL}/reports/analisisFacturaCompra", params={"ACCESS_TOKEN": token}).json()
hoy = datetime.today().strftime("%d-%m-%Y")

for f in facturas:
    if "1.15" in f.get("EMPRESA", "") and f.get("FECHA") == hoy:
        print(f["PROVEEDOR"], "|", f["COMPROBANTE"])