# Modulo per l'elaborazione e la pulizia dei dati grezzi ricevuti dall'API

import pandas as pd
from datetime import datetime, timedelta  
import numpy as np                        # numpy per calcoli sicuri

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
    "REPARTO",           # reparto che ha aperto la RDI (usato anche nel grafico a torta)
    "CLASSE"
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

        # Rimozione zeri iniziali nella colonna degli ID_ODL
        if 'N_ODL' in df.columns:
            df['N_ODL'] = df['N_ODL'].astype(str).str.lstrip('0')

        # Rimozione zeri iniziali nella colonna degli ID_RDI
        if 'N_RDI' in df.columns:
            df['N_RDI'] = df['N_RDI'].astype(str).str.lstrip('0')

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
        "REPARTO":           "REPARTO",        # usato anche nel grafico a torta
        "CLASSE":             "CLASSE"          # colonna per la classe di apparecchiatura
    }
    df = df.rename(columns=mappa_rinomina)

    # Rimozione zeri iniziali nella colonna degli ID_RDI
    if 'N_RDI' in df.columns:
        df['N_RDI'] = df['N_RDI'].astype(str).str.lstrip('0')

    # Mantieni solo le colonne definite in COLONNE_OUTPUT_RDI che esistono nel DataFrame
    colonne_presenti = [c for c in COLONNE_OUTPUT_RDI if c in df.columns]
    df = df[colonne_presenti]

    # Sostituisce i valori NaN con uno spazio per evitare
    # che nell'HTML appaia la scritta "NaN"
    df = df.fillna(" ")

    return df

# ============================================================
# PREVISIONI PROSSIMI GUASTI (TIME TO FAILURE per FAMIGLIA DI BENE)
# ============================================================
def predict_next_rdi(dati_rdi_massivi: list) -> pd.DataFrame:
    """
    Raggruppa per DESCRIZIONE_BENE e calcola il tempo medio tra i guasti 
    per ciascuna TIPOLOGIA di apparecchio.
    """
    if not dati_rdi_massivi or not isinstance(dati_rdi_massivi, list):
        return pd.DataFrame()

    df = pd.DataFrame(dati_rdi_massivi)

    col_data = "DATA_RDI" if "DATA_RDI" in df.columns else None
    col_desc = "DESCRIZIONE_BENE" if "DESCRIZIONE_BENE" in df.columns else None
    col_inv = "N_INVENTARIO" if "N_INVENTARIO" in df.columns else "ICH" if "ICH" in df.columns else None

    if not col_desc or not col_data:
        return pd.DataFrame()

    colonne_utili = [col_desc, col_data]
    if col_inv:
        colonne_utili.append(col_inv)
        
    df_pred = df[colonne_utili].copy()
    df_pred = df_pred.rename(columns={col_desc: "descrizione_bene"})
    
    if col_inv:
        df_pred = df_pred.rename(columns={col_inv: "ICH_originale"})
    else:
        df_pred["ICH_originale"] = "N/D"
    
    # Pulizia
    df_pred = df_pred.dropna(subset=["descrizione_bene", col_data])
    df_pred = df_pred[df_pred["descrizione_bene"].astype(str).str.strip() != ""]

    df_pred[col_data] = pd.to_datetime(df_pred[col_data], errors="coerce")
    df_pred = df_pred.dropna(subset=[col_data])

    # Ordiniamo cronologicamente PER DESCRIZIONE BENE
    df_pred = df_pred.sort_values(["descrizione_bene", col_data])

    # Calcolo giorni trascorsi tra un guasto e l'altro della stessa famiglia
    df_pred["DELTA_GIORNI"] = (
        df_pred.groupby("descrizione_bene")[col_data]
        .diff()
        .dt.total_seconds() / 86400
    )

    validi = df_pred.dropna(subset=["DELTA_GIORNI"]).copy()

    if validi.empty:
        return pd.DataFrame()

    # Calcolo statistiche principali
    stats = validi.groupby("descrizione_bene").agg(
        ultima_data_rdi=(col_data, "max"),
        intervallo_medio_giorni=("DELTA_GIORNI", "mean"),
        numero_intervalli=("DELTA_GIORNI", "count")
    ).reset_index()

    # Estraiamo informazioni pulite: Quante macchine ci sono? Qual è l'ultimo ICH guasto?
    dettagli = df_pred.sort_values(col_data).groupby("descrizione_bene").agg(
        ultimo_ich=("ICH_originale", "last"),
        qta_macchine=("ICH_originale", "nunique")
    ).reset_index()

    stats = pd.merge(stats, dettagli, on="descrizione_bene", how="left")

    # Previsione
    stats["data_prevista_prossima_rdi"] = (
        stats["ultima_data_rdi"] + pd.to_timedelta(stats["intervallo_medio_giorni"], unit="D")
    )

    stats = stats[stats["numero_intervalli"] >= 1].copy()

    # FILTRO TEMPORALE: Solo previsioni FUTURE
    oggi = pd.Timestamp(datetime.now().date())
    limite_passato = oggi
    limite_futuro = oggi + timedelta(days=730)
    
    stats = stats[
        (stats["data_prevista_prossima_rdi"] >= limite_passato) & 
        (stats["data_prevista_prossima_rdi"] <= limite_futuro)
    ].copy()

    stats = stats.sort_values("data_prevista_prossima_rdi", ascending=True)
    top5 = stats.head(5).copy()

    top5["intervallo_medio_giorni"] = top5["intervallo_medio_giorni"].round(1)

    return top5