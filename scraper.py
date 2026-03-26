import requests
import json
import os
from datetime import datetime

CLIENT_ID = "dfd197a058fba973cadf047044c0c1d1"
CLIENT_SECRET = "6869f03b8e9e57aa9a0d4ce02b345e0c"
BASE_URL = "https://api.finneg.com/api"
TELEGRAM_TOKEN = "8741240506:AAEzOumxhDw2M_nk4GUySuKH158mfNnSxMU"
TELEGRAM_CHAT_ID = "8600326009"
REGISTRO_FILE = "facturas_notificadas.json"

MIS_LOCALES = [
    "1.10 Belgrains Local Ruta 205",
    "1.11 Belgrains Local Azul",
    "1.13 Belgrains Local Mar Del Plata",
    "1.14 Belgrains Local Alvear",
    "1.15 Belgrains Local Villa Gesell",
]

TODOS_LOS_PROVEEDORES = [
    "AHRENS MARIO ALBERTO", "BEYCO SA", "BINGO FUEL WINES SOCIEDAD ANONIMA",
    "CASOLO FEDERICO MIGUEL", "COMBUSTIBLES LA PERLA S.A.", "COTIGNOLA ANDREA",
    "DESTRO GABRIEL ALEJANDRO", "DISTRIBUCIONES JULIO MORRONE E HIJO S. A.",
    "DOMINGUEZ KARINA PAOLA", "EMEZETA S. A.", "FINCA BALCARCE SA",
    "FRIGO PAT S.A.", "GARCIA HERMANOS AGROINDUSTRIAL SRL", "Greco Horacio Hugo",
    "HIJOS DE J.M. LUBERRIAGA S.A.", "ILARI CLAUDIA FIORELLA",
    "INSTITUCION SALESIANA NUESTRA SEÑORA DE LUJAN", "LA AGRICOLA S A",
    "Le Gurie Sociedad Anonima", "LOPEZ WALTER RICARDO", "MANNELLI JORGE",
    "MARCONI MARIA EMILIA", "OLIVE&CO S.R.L.", "PASTURAS DE CAZON S.R.L.",
    "PDB S R L", "QUESADA COM E IND S R L", "REGINALD LEE S A",
    "SALDIVIA GERARDO JOSE", "SALOMON JULIO ANDRES", "TOTAL REFRIGERACION",
    "COMERCIAL DEL MAR S A", "DE LA TORRE LEONARDO EMMANUEL", "DI LULLO BRENDA LINA",
    "OLMEDO SUAREZ TOMAS", "PANACITY MDQ SRL", "PAYWAY SAU",
    "PEREZ ROCIO MICAELA MERCEDES", "RAMUNDO GUSTAVO JAVIER", "SERIN SA",
    "VILLORIA CAROLINA SOLEDAD", "WAM ENTERTAINMENT COMPANY S. A.",
    "GALLO PEDRO", "CARIATI MARIA SILVINA",
    "COOP ELECTRICA CREDITO VIVIENDA Y OTROS SERVICIOS PUBLICOS DE VILLA GESELL",
    "JUAMPI S A", "MONTENEGRO NESTOR ARMANDO", "SAIZAR NESTOR EDUARDO",
    "VILLA GESELL TELEVISION COMUNITARIA S A", "WEST PALM SA", "ZALDIVAR MANUEL IGNACIO",
    "VALDIVIA NICOLAS LEANDRO"
]

def cargar_registro():
    if not os.path.exists(REGISTRO_FILE):
        return {}
    with open(REGISTRO_FILE, "r") as f:
        return json.load(f)

def guardar_registro(registro):
    with open(REGISTRO_FILE, "w") as f:
        json.dump(registro, f)

def obtener_token():
    url = f"{BASE_URL}/oauth/token"
    params = {"client_id": CLIENT_ID, "client_secret": CLIENT_SECRET, "grant_type": "client_credentials"}
    return requests.get(url, params=params).text.strip()

def obtener_facturas(token):
    url = f"{BASE_URL}/reports/analisisFacturaCompra"
    return requests.get(url, params={"ACCESS_TOKEN": token}).json()

def filtrar_mis_facturas(facturas):
    hoy = datetime.today().strftime("%d-%m-%Y")
    vistas = set()
    mis_facturas = []
    for f in facturas:
        tid = f.get("TRANSACCIONID")
        proveedor = f.get("PROVEEDOR", "")
        fecha = f.get("FECHA", "")
        empresa = f.get("EMPRESA", "")
        if (proveedor in TODOS_LOS_PROVEEDORES
                and fecha == hoy
                and empresa in MIS_LOCALES
                and tid not in vistas):
            vistas.add(tid)
            mis_facturas.append(f)
    return mis_facturas

def enviar_telegram(mensaje):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "text": mensaje, "parse_mode": "Markdown"})

def main():
    print(f"Ejecutando: {datetime.now().strftime('%d-%m-%Y %H:%M')}")
    registro = cargar_registro()
    hoy = datetime.today().strftime("%d-%m-%Y")

    # Limpiar registros de días anteriores
    registro = {k: v for k, v in registro.items() if v == hoy}

    token = obtener_token()
    facturas = obtener_facturas(token)
    mis_facturas = filtrar_mis_facturas(facturas)

    nuevas = 0
    for f in mis_facturas:
        tid = str(f["TRANSACCIONID"])
        if tid not in registro:
            mensaje = (
                f"🧾 *Nueva factura de proveedor*\n"
                f"📅 Fecha: {f['FECHA']}\n"
                f"🏪 Local: {f['EMPRESA']}\n"
                f"🏭 Proveedor: {f['PROVEEDOR']}\n"
                f"📄 Comprobante: {f['COMPROBANTE']}\n"
                f"💰 Total: ${f['TOTAL']:,.2f}\n"
                f"📋 Estado: {f['SITUACION']}"
            )
            enviar_telegram(mensaje)
            registro[tid] = hoy
            nuevas += 1
            print(f"Notificada: {f['COMPROBANTE']}")

    guardar_registro(registro)
    print(f"Nuevas facturas notificadas: {nuevas}")
    print("Listo!")

main()