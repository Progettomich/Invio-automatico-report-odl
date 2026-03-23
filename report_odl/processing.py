
import pandas as pd
from datetime import datetime

COLONNE_OUTPUT = [
    "id_odl",
    "stato_odl",
    "data_odl",
    "descrizione_odl",
    "causa_sospensione",
    "descrizione_bene",
    "fornitore",
    "giorni_trascorsi"
]

COLONNE_OUTPUT_RDI = [
    "N_RDI",
    "DATA_RDI",
    "DESCRIZIONE_RDI",
    "APERTA_DA",         
    "DESCRIZIONE_BENE",
    "ICH",
    "REPARTO"
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

def process_rdi(dati_rdi: list) -> pd.DataFrame:
    
    # Riceve la lista globale degli RDI e la pulisce,
    # restituendo un DataFrame formattato per le tabelle HTML.
    
    if not dati_rdi or not isinstance(dati_rdi, list):
        return pd.DataFrame(columns=COLONNE_OUTPUT_RDI)
        
    df = pd.DataFrame(dati_rdi)
    
    # 1. Rinomina le chiavi JSON dell'API nelle chiavi che si aspetta il tuo HTML
   
    mappa_rinomina = {
        "N_RDI": "N_RDI",            
        "DATA_RDI": "DATA_RDI",  
        "DESCRIZIONE_RDI": "DESCRIZIONE_RDI",
        "APERTA DA": "APERTA_DA",
        "DESCRIZIONE_BENE": "DESCRIZIONE_BENE",           
        "N_INVETARIO": "ICH",           
        "REPARTO": "REPARTO"           # Questa è la colonna usata anche dal grafico a torta
    }
    
    # Rinomina le colonne solo se esistono nel DataFrame grezzo
    df = df.rename(columns=mappa_rinomina)

    # 3. Mantieni solo le colonne che servono all'HTML
    colonne_presenti = [c for c in COLONNE_OUTPUT_RDI if c in df.columns]
    df = df[colonne_presenti]
    
    # Riempi i valori vuoti (NaN) con una stringa vuota o un trattino
    df = df.fillna(" ")
    
    return df

