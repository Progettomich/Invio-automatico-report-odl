
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
    "ADDAMO FEDERICO",
    "PIETRAGALLA CANIO",
    "URBINA ZABALETA MARIA",
    "GALIMBERTI CARLO",
    "RIZZO ALESSANDRO",
    "GHILARDOTTI GILBERTO",
    "VALENTINO ANGELO"
]

API_BASE = "http://10.38.169.149:3500/api/v1/zMaintenance/report/odl"
API_USER = "il_tuo_user"
API_PASS = "la_tua_password"
DATE_FROM = "2026-01-01"


def fetch_odl_tecnico(tecnico, limit=100):
    """
    Scarica tutti gli ODL per un singolo tecnico, gestendo la paginazione.
    Ritorna un DataFrame con gli ODL di quel tecnico.
    """
    all_odl = []

    # prima chiamata per capire quante pagine ci sono (se l'API lo espone)
    params = {
        "user": API_USER,
        "password": API_PASS,
        "limit": limit,
        "page": 1,
        "stato": "IN CORSO,SOSPESO,DA FARE,CONCLUSO",
        "tecnico": tecnico,            # ← singolo tecnico
        "dateFrom": DATE_FROM          # ← stringa corretta
    }

    response = requests.get(API_BASE, params=params)
    data = response.json()

    if not data or "records" not in data:
        logging.warning(f"Nessun dato restituito per il tecnico {tecnico}")
        return pd.DataFrame()

    all_odl.extend(data["records"])
    total_pages = data.get("totalPages", 1)

    # dalla pagina 2 fino all’ultima con un ciclo for
    for page in range(2, total_pages + 1):
        params["page"] = page
        response = requests.get(API_BASE, params=params)
        data = response.json()

        if not data or "records" not in data:
            break

        all_odl.extend(data["records"])

    df = pd.DataFrame(all_odl)
    # opzionale: aggiungo una colonna con il nome del tecnico
    if not df.empty:
        df["tecnico"] = tecnico

    return df


def fetch_tutti_odl_tecnici(limit=100):
    """
    Cicla su tutti i tecnici con un for e concatena i DataFrame.
    """
    df_list = []

    for tecnico in TECNICI_LIST:
        logging.info(f"Scarico ODL per il tecnico: {tecnico}")
        df_tecnico = fetch_odl_tecnico(tecnico, limit=limit)
        if not df_tecnico.empty:
            df_list.append(df_tecnico)

    if df_list:
        return pd.concat(df_list, ignore_index=True)
    else:
        return pd.DataFrame()
