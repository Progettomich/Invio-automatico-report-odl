import requests

# Endpoint base (senza parametri)
BASE_URL = "http://10.38.169.149:3500/api/v1/zMaintenance/REPORT/ODL"

# Credenziali e parametri fissi
USER = "fgiacchibonetta"
PASSWORD = "Humanitas1!"
STATI = "IN CORSO,SOSPESO,DA FARE"
DATE_FROM = "2026-01-01"
LIMIT = 100
PAGE = 1

# Lista responsabili (tecnici)
responsabili = [
    "Addamo FEDERICO",
    "PIETRAGALLA CANIO",
    "URBINA ZABALETA MARIA",
    "GALIMBERTI CARLO",
    "RIZZO ALESSANDRO",
    "GHILARDOTTI GILBERTO",
    "VALENTINO ANGELO",
]

for responsabile in responsabili:
    # Costruisco i query params: requests si occupa di fare l'URL encoding
    params = {
        "user": USER,
        "password": PASSWORD,
        "limit": LIMIT,
        "page": PAGE,
        "stato": STATI,
        "tecnico": responsabile,
        "dateFrom": DATE_FROM,
    }

    print(f"Richiesta per tecnico: {responsabile}")
    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        print("URL chiamata:", response.url)

        if response.status_code == 200:
            data = response.json()  # oppure response.text se non è JSON
            # Qui puoi lavorare con 'data', salvarlo, stamparlo, ecc.
            print("Numero record ricevuti:", len(data) if isinstance(data, list) else "non è una lista")
        else:
            print("Errore HTTP:", response.status_code, response.text)
    except requests.exceptions.RequestException as e:
        print("Errore di rete/chiamata:", e)

    print("-" * 50)
