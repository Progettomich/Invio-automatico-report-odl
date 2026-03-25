# Modulo per l'elaborazione e la pulizia dei dati grezzi ricevuti dall'API

import pandas as pd
from datetime import datetime


# Elenco delle colonne da mantenere nel DataFrame finale degli ODL
# Le colonne non presenti in questa lista vengono scartate
COLONNE_OUTPUT = [
    "N_RDI",            # identificativo univoco dell'RDI
    "N_ODL",            # identificativo univoco dell'ODL
    "STATO_ODL",        # stato corrente (IN CORSO, SOSPESO, ecc.)
    "DATA_ODL",         # data di apertura dell'ODL
    "DESCRIZIONE_ODL",  # descrizione del lavoro da fare
    "CAUSA_SOSPENSIONE", # motivo della sospensione (se presente)
    "DESCRIZIONE_BENE", # descrizione del bene su cui si lavora
    "FORNITORE_APPARECCHIATURA",        # fornitore coinvolto
    "GIORNI_TRASCORSI", # giorni trascorsi dall'apertura (calcolato)
    "RESPONSABILE",     # nome responsabile
]

# Elenco delle colonne da mantenere nel DataFrame finale delle RDI
COLONNE_OUTPUT_RDI = [
    "N_RDI",            # numero identificativo della RDI
    "DATA_RDI",         # data di creazione della RDI
    "DESCRIZIONE_RDI",  # descrizione della richiesta
    "APERTA_DA",        # nome di chi ha aperto la RDI
    "DESCRIZIONE_BENE", # descrizione del bene coinvolto
    "ICH",              # numero inventario del bene
    "REPARTO"           # reparto che ha aperto la RDI (usato anche nel grafico a torta)
]


# ============================================================
# ELABORAZIONE DATI ODL
# ============================================================
def process_data(dati_grezzi: dict) -> dict:
    """
    Riceve il dizionario restituito da fetch_odl_per_responsabili()
    { nome_tecnico: lista_di_record } e restituisce
    { nome_tecnico: DataFrame_filtrato_e_pulito }
    """

    # Dizionario che conterrà i DataFrame elaborati per ogni tecnico
    risultati = {}

    # Ciclo su ogni tecnico e i suoi dati grezzi
    for tecnico, records in dati_grezzi.items():

        # Se la risposta è vuota o non è una lista, salta questo tecnico
        if not records or not isinstance(records, list):
            print(f"[{tecnico}] Nessun dato disponibile, salto.")
            continue

        # Converte la lista di record (dizionari) in un DataFrame pandas
        df = pd.DataFrame(records)

        # --- NORMALIZZAZIONE COLONNE ---
        # Se la colonna 'tecnico' non esiste, la crea vuota per evitare errori
        if 'RESPONSABILE' not in df.columns:
            df['RESPONSABILE'] = ''

        # Se la colonna 'data_odl' non esiste, la crea con valori nulli
        if 'DATA_ODL' not in df.columns:
            df['DATA_ODL'] = pd.NaT

        # Converte la colonna data in formato datetime
        # errors='coerce' trasforma i valori non validi in NaT invece di dare errore
        df['DATA_ODL'] = pd.to_datetime(df['DATA_ODL'], errors='coerce')

        # Calcola i giorni trascorsi dall'apertura dell'ODL ad oggi
        oggi = pd.Timestamp(datetime.now().date())
        df['giorni_trascorsi'] = (oggi - df['DATA_ODL']).dt.days

        # --- FILTRA SOLO LE COLONNE CHE ESISTONO ---
        # Mantieni solo le colonne definite in COLONNE_OUTPUT che esistono nel DataFrame
        colonne_presenti = [c for c in COLONNE_OUTPUT if c in df.columns]
        df = df[colonne_presenti]

        # Se dopo il filtraggio il DataFrame è vuoto, salta questo tecnico
        if df.empty:
            print(f"[{tecnico}] DataFrame vuoto dopo il filtraggio, salto.")
            continue

        # Salva il DataFrame nel dizionario dei risultati
        risultati[tecnico] = df
        print(f"[{tecnico}] {len(df)} record processati.")

    return risultati


# ============================================================
# ELABORAZIONE DATI RDI
# ============================================================
def process_rdi(dati_rdi: list) -> pd.DataFrame:
    """
    Riceve la lista globale degli RDI e la pulisce,
    restituendo un DataFrame formattato per le tabelle HTML.
    """

    # Se la lista è vuota o non è una lista, restituisce un DataFrame vuoto
    # con le colonne corrette per evitare errori nei passaggi successivi
    if not dati_rdi or not isinstance(dati_rdi, list):
        return pd.DataFrame(columns=COLONNE_OUTPUT_RDI)

    # Converte la lista di record in un DataFrame pandas
    df = pd.DataFrame(dati_rdi)

    # Rinomina le colonne dall'API ai nomi usati nel resto del progetto
    # Solo le colonne presenti nel DataFrame vengono rinominate
    mappa_rinomina = {
        "N_RDI":             "N_RDI",
        "DATA_RDI":          "DATA_RDI",
        "DESCRIZIONE_RDI":   "DESCRIZIONE_RDI",
        "APERTA DA":         "APERTA_DA",       # nota: il nome originale ha uno spazio
        "DESCRIZIONE_BENE":  "DESCRIZIONE_BENE",
        "N_INVENTARIO":       "ICH",             # numero inventario rinominato in ICH
        "REPARTO":           "REPARTO"          # usato anche nel grafico a torta
    }
    df = df.rename(columns=mappa_rinomina)

    # Mantieni solo le colonne definite in COLONNE_OUTPUT_RDI che esistono nel DataFrame
    colonne_presenti = [c for c in COLONNE_OUTPUT_RDI if c in df.columns]
    df = df[colonne_presenti]

    # Sostituisce i valori NaN con uno spazio per evitare
    # che nell'HTML appaia la scritta "NaN"
    df = df.fillna(" ")

    return df