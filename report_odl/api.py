import requests
import pandas as pd
import logging

logging.basicConfig(
    filename="odl_report.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

API_BASE = "http://10.38.169.149:3500/api/v1/zMaintenance/rdi"
API_USER = "**********"
API_PASS = "**********"
DATE_FROM = "2026-01-01"

def fetch_tutti_odl(limit=100, page=1):
    all_odl = []

    # 1) ADDAMO FEDERICO
    params = {
        "user": API_USER,
        "password": API_PASS,
        "limit": limit,
        "page": page,
        "stato": "IN CORSO,SOSPESO,DA FARE,CONCLUSO",
        "tecnico": "ADDAMO FEDERICO",
        "dateFrom": DATE_FROM
    }
    resp = requests.get(API_BASE, params=params)
    resp.raise_for_status()
    data = resp.json()
    if data and "records" in data:
        all_odl.extend(data["records"])
        logging.info(f"ADDAMO FEDERICO: {len(data['records'])} record")

    # 2) PIETRAGALLA CANIO
    params = {
        "user": API_USER,
        "password": API_PASS,
        "limit": limit,
        "page": page,
        "stato": "IN CORSO,SOSPESO,DA FARE,CONCLUSO",
        "tecnico": "PIETRAGALLA CANIO",
        "dateFrom": DATE_FROM
    }
    resp = requests.get(API_BASE, params=params)
    resp.raise_for_status()
    data = resp.json()
    if data and "records" in data:
        all_odl.extend(data["records"])
        logging.info(f"PIETRAGALLA CANIO: {len(data['records'])} record")

    # 3) URBINA ZABALETA MARIA
    params = {
        "user": API_USER,
        "password": API_PASS,
        "limit": limit,
        "page": page,
        "stato": "IN CORSO,SOSPESO,DA FARE,CONCLUSO",
        "tecnico": "URBINA ZABALETA MARIA",
        "dateFrom": DATE_FROM
    }
    resp = requests.get(API_BASE, params=params)
    resp.raise_for_status()
    data = resp.json()
    if data and "records" in data:
        all_odl.extend(data["records"])
        logging.info(f"URBINA ZABALETA MARIA: {len(data['records'])} record")

    # 4) GALIMBERTI CARLO
    params = {
        "user": API_USER,
        "password": API_PASS,
        "limit": limit,
        "page": page,
        "stato": "IN CORSO,SOSPESO,DA FARE,CONCLUSO",
        "tecnico": "GALIMBERTI CARLO",
        "dateFrom": DATE_FROM
    }
    resp = requests.get(API_BASE, params=params)
    resp.raise_for_status()
    data = resp.json()
    if data and "records" in data:
        all_odl.extend(data["records"])
        logging.info(f"GALIMBERTI CARLO: {len(data['records'])} record")

    # 5) RIZZO ALESSANDRO
    params = {
        "user": API_USER,
        "password": API_PASS,
        "limit": limit,
        "page": page,
        "stato": "IN CORSO,SOSPESO,DA FARE,CONCLUSO",
        "tecnico": "RIZZO ALESSANDRO",
        "dateFrom": DATE_FROM
    }
    resp = requests.get(API_BASE, params=params)
    resp.raise_for_status()
    data = resp.json()
    if data and "records" in data:
        all_odl.extend(data["records"])
        logging.info(f"RIZZO ALESSANDRO: {len(data['records'])} record")

    # 6) GHILARDOTTI GILBERTO
    params = {
        "user": API_USER,
        "password": API_PASS,
        "limit": limit,
        "page": page,
        "stato": "IN CORSO,SOSPESO,DA FARE,CONCLUSO",
        "tecnico": "GHILARDOTTI GILBERTO",
        "dateFrom": DATE_FROM
    }
    resp = requests.get(API_BASE, params=params)
    resp.raise_for_status()
    data = resp.json()
    if data and "records" in data:
        all_odl.extend(data["records"])
        logging.info(f"GHILARDOTTI GILBERTO: {len(data['records'])} record")

    # 7) VALENTINO ANGELO
    params = {
        "user": API_USER,
        "password": API_PASS,
        "limit": limit,
        "page": page,
        "stato": "IN CORSO,SOSPESO,DA FARE,CONCLUSO",
        "tecnico": "VALENTINO ANGELO",
        "dateFrom": DATE_FROM
    }
    resp = requests.get(API_BASE, params=params)
    resp.raise_for_status()
    data = resp.json()
    if data and "records" in data:
        all_odl.extend(data["records"])
        logging.info(f"VALENTINO ANGELO: {len(data['records'])} record")

    df = pd.DataFrame(all_odl)
    logging.info(f"Totale ODL recuperati: {len(df)}")
    return df
