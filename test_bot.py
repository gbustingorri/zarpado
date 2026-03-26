import requests
from datetime import datetime, timedelta

ACCESS_TOKEN = "334222fc-479d-4001-a2dd-933c50c74009"

hoy = datetime.today().strftime("%Y%m%d")
hace30 = (datetime.today() - timedelta(days=30)).strftime("%Y%m%d")

url = "https://go-prod.finneg.com/api/1/botdecompras-frontend-consumer-back/purchaseInvoices/EMPRESA_EMPRE01"
params = {
    "workspace": "BELGRAINS",
    "access_token": ACCESS_TOKEN,
    "pending": "true",
    "rejected": "false",
    "FechaDeEntregaDesde": hace30,
    "FechaDeEntregaHasta": hoy,
    "from": "BDC",
    "provider": ""
}

r = requests.get(url, params=params)
data = r.json()

# Ver las claves del objeto raíz
print("Claves del objeto:", list(data.keys()))

# Ver cuántos registros tiene cada clave
for k, v in data.items():
    if isinstance(v, list):
        print(f"{k}: {len(v)} registros")
    else:
        print(f"{k}: {v}")