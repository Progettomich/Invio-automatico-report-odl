# report_odl/processing.py
import pandas as pd
from datetime import datetime
from main import fetch_odl_per_responsabili

COLONNE_OUTPUT = [
    "id_odl",
    "stato_odl",
    "data_odl",
    "descrizione_odl",
    "causa_sospensione",
    "descrizione_bene",
    "fornitore",
    "giorni_trascorsi",
]


def process_data(dati_grezzi: dict) -> dict:
    """
    Riceve il dizionario restituito da fetch_odl_per_responsabili()
    { nome_tecnico: lista_di_record } e restituisce
    { nome_tecnico: DataFrame_filtrato_e_pulito }
    """

    risultati = {}

    for tecnico, records in dati_grezzi.items():

        # Se la risposta è vuota o non è una lista, salta
        if not records or not isinstance(records, list):
            print(f"[{tecnico}] Nessun dato disponibile, salto.")
            continue

        # Converto la lista di record in DataFrame
        df = pd.DataFrame(records)

        # --- NORMALIZZAZIONE COLONNE ---
        if 'tecnico' not in df.columns:
            df['tecnico'] = ''

        if 'DT_APERTURA' not in df.columns:
            df['DT_APERTURA'] = pd.NaT

        df['DT_APERTURA'] = pd.to_datetime(df['DT_APERTURA'], errors='coerce')

        oggi = pd.Timestamp(datetime.now().date())
        df['giorni_trascorsi'] = (oggi - df['DT_APERTURA']).dt.days

        # --- RINOMINA COLONNE ---
        df = df.rename(columns={
            "stato":       "stato_odl",
            "DT_APERTURA": "data_odl",
            "descrizione": "descrizioni_odl",
        })

        # --- FILTRA SOLO LE COLONNE CHE ESISTONO ---
        colonne_presenti = [c for c in COLONNE_OUTPUT if c in df.columns]
        df = df[colonne_presenti]

        if df.empty:
            print(f"[{tecnico}] DataFrame vuoto dopo il filtraggio, salto.")
            continue

        risultati[tecnico] = df
        print(f"[{tecnico}] {len(df)} record processati.")

    return risultati 


######Parte da eliminare una volta verificato che il processo funziona correttamente######
# 1. Chiamo il fetch per ottenere i dati grezzi
dati_grezzi = fetch_odl_per_responsabili()

# 2. Processo i dati
dati_processati = process_data(dati_grezzi)

# 3. Stampo i risultati per verificare
for tecnico, df in dati_processati.items():
    print(f"\n=== {tecnico} ===")
    print(df)
