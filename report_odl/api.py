import requests
import pandas as pd
import logging

# configurazione del logging
logging.basicConfig(
    filename="odl_report.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# lista tecnici
TECNICI_LIST = [
    "Addamo FEDERICO",
    "PIETRAGALLA CANIO",
    "URBINA ZABALETA MARIA",
    "GALIMBERTI CARLO",
    "RIZZO ALESSANDRO",
    "GHILARDOTTI GILBERTO",
    "VALENTINO ANGELO"
]

API_BASE = "http://10.38.169.149:3500/api/v1/zMaintenance/rdi"
API_USER = "fgiacchibonetta"
API_PASS = "Humanitas1!"
DATE_FROM = "2026-01-01"

def fetch_tutti_odl(limit=100):

    all_odl = []
    page = 1

    while True:

        params = {
            "user": API_USER,
            "password": API_PASS,
            "limit": limit,
            "page": page,
            "stato": "IN CORSO,SOSPESO,DA FARE",
            "tecnico": ",".join(TECNICI_LIST),
            "dateFrom": DATE_FROM
        }

        response = requests.get(API_BASE, params=params)

        data = response.json()

        if not data or "records" not in data:
            break

        all_odl.extend(data["records"])

        total_pages = data.get("totalPages", page)

        if page >= total_pages:
            break

        page += 1

    df = pd.DataFrame(all_odl)

    return df
