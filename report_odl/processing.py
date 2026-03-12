# report_odl/processing.py
import pandas as pd
from datetime import datetime

def process_data(df: pd.DataFrame) -> dict:
    """
    Filtra i dati per ciascun tecnico (fisso) e
    restituisce solo le colonne richieste.
    Ritorna: dict {nome_tecnico: DataFrame_filtrato}
    """

    # --- NORMALIZZAZIONE COLONNE DI BASE ---

    # Se per qualche motivo la colonna 'tecnico' non esiste, la creo vuota
    # (evita errori quando faccio i filtri più avanti)
    if 'tecnico' not in df.columns:
        df['tecnico'] = ''

    # Se la colonna di apertura ODL non esiste, la creo come colonna di date vuote
    if 'DT_APERTURA' not in df.columns:
        df['DT_APERTURA'] = pd.NaT

    # Converto la colonna 'DT_APERTURA' in formato datetime
    # errors='coerce' trasforma i valori non validi in NaT (valore nullo per le date)
    df['DT_APERTURA'] = pd.to_datetime(df['DT_APERTURA'], errors='coerce')

    # Calcolo la data di oggi
    oggi = pd.Timestamp(datetime.now().date())

    # Aggiungo una colonna 'giorni_trascorsi' = differenza in giorni tra oggi e DT_APERTURA
    df['giorni_trascorsi'] = (oggi - df['DT_APERTURA']).dt.days

    # Dizionario che conterrà i risultati per ogni tecnico
    # chiave = nome tecnico, valore = DataFrame filtrato e pulito
    risultati = {}

    # --------------------------------------------------
    # 1) TECNICO: ADDAMO FEDERICO
    # --------------------------------------------------
    # Filtra il DataFrame solo con le righe dove 'tecnico' è "ADDAMO FEDERICO"
    df_addamo = df[df['tecnico'] == "ADDAMO FEDERICO"].copy()

    # Controllo: se non ci sono righe per questo tecnico, salto
    if not df_addamo.empty:
        # Rinomino le colonne per allinearle ai nomi che ti servono in output
        # 'stato' -> 'stato_odl', 'DT_APERTURA' -> 'data_odl', 'descrizione' -> 'descrizioni_odl'
        df_addamo = df_addamo.rename(columns={
            "stato": "stato_odl",
            "DT_APERTURA": "data_odl",
            "descrizione": "descrizioni_odl"
        })

        # Elenco delle colonne che vuoi tenere per l'output
        colonne_addamo = [
            "id_odl",
            "stato_odl",
            "data_odl",
            "descrizioni_odl",
            "causa_sospensione",
            "descrizione_bene",
            "fornitore"
        ]

        # Mi assicuro di tenere solo le colonne che esistono davvero nel DataFrame
        colonne_addamo = [c for c in colonne_addamo if c in df_addamo.columns]

        # Seleziono solo quelle colonne
        df_addamo = df_addamo[colonne_addamo]

        # Salvo il DataFrame nel dizionario, con chiave = nome tecnico
        risultati["ADDAMO FEDERICO"] = df_addamo

    # --------------------------------------------------
    # 2) TECNICO: PIETRAGALLA CANIO
    # --------------------------------------------------
    df_pietragalla = df[df['tecnico'] == "PIETRAGALLA CANIO"].copy()
    if not df_pietragalla.empty:
        df_pietragalla = df_pietragalla.rename(columns={
            "stato": "stato_odl",
            "DT_APERTURA": "data_odl",
            "descrizione": "descrizioni_odl"
        })
        colonne_pietragalla = [
            "id_odl",
            "stato_odl",
            "data_odl",
            "descrizioni_odl",
            "causa_sospensione",
            "descrizione_bene",
            "fornitore"
        ]
        colonne_pietragalla = [c for c in colonne_pietragalla if c in df_pietragalla.columns]
        df_pietragalla = df_pietragalla[colonne_pietragalla]
        risultati["PIETRAGALLA CANIO"] = df_pietragalla

    # --------------------------------------------------
    # 3) TECNICO: URBINA ZABALETA MARIA
    # --------------------------------------------------
    df_urbina = df[df['tecnico'] == "URBINA ZABALETA MARIA"].copy()
    if not df_urbina.empty:
        df_urbina = df_urbina.rename(columns={
            "stato": "stato_odl",
            "DT_APERTURA": "data_odl",
            "descrizione": "descrizioni_odl"
        })
        colonne_urbina = [
            "id_odl",
            "stato_odl",
            "data_odl",
            "descrizioni_odl",
            "causa_sospensione",
            "descrizione_bene",
            "fornitore"
        ]
        colonne_urbina = [c for c in colonne_urbina if c in df_urbina.columns]
        df_urbina = df_urbina[colonne_urbina]
        risultati["URBINA ZABALETA MARIA"] = df_urbina

    # --------------------------------------------------
    # 4) TECNICO: GALIMBERTI CARLO
    # --------------------------------------------------
    df_galimberti = df[df['tecnico'] == "GALIMBERTI CARLO"].copy()
    if not df_galimberti.empty:
        df_galimberti = df_galimberti.rename(columns={
            "stato": "stato_odl",
            "DT_APERTURA": "data_odl",
            "descrizione": "descrizioni_odl"
        })
        colonne_galimberti = [
            "id_odl",
            "stato_odl",
            "data_odl",
            "descrizioni_odl",
            "causa_sospensione",
            "descrizione_bene",
            "fornitore"
        ]
        colonne_galimberti = [c for c in colonne_galimberti if c in df_galimberti.columns]
        df_galimberti = df_galimberti[colonne_galimberti]
        risultati["GALIMBERTI CARLO"] = df_galimberti

    # --------------------------------------------------
    # 5) TECNICO: RIZZO ALESSANDRO
    # --------------------------------------------------
    df_rizzo = df[df['tecnico'] == "RIZZO ALESSANDRO"].copy()
    if not df_rizzo.empty:
        df_rizzo = df_rizzo.rename(columns={
            "stato": "stato_odl",
            "DT_APERTURA": "data_odl",
            "descrizione": "descrizioni_odl"
        })
        colonne_rizzo = [
            "id_odl",
            "stato_odl",
            "data_odl",
            "descrizioni_odl",
            "causa_sospensione",
            "descrizione_bene",
            "fornitore"
        ]
        colonne_rizzo = [c for c in colonne_rizzo if c in df_rizzo.columns]
        df_rizzo = df_rizzo[colonne_rizzo]
        risultati["RIZZO ALESSANDRO"] = df_rizzo

    # --------------------------------------------------
    # 6) TECNICO: GHILARDOTTI GILBERTO
    # --------------------------------------------------
    df_ghilardotti = df[df['tecnico'] == "GHILARDOTTI GILBERTO"].copy()
    if not df_ghilardotti.empty:
        df_ghilardotti = df_ghilardotti.rename(columns={
            "stato": "stato_odl",
            "DT_APERTURA": "data_odl",
            "descrizione": "descrizioni_odl"
        })
        colonne_ghilardotti = [
            "id_odl",
            "stato_odl",
            "data_odl",
            "descrizioni_odl",
            "causa_sospensione",
            "descrizione_bene",
            "fornitore"
        ]
        colonne_ghilardotti = [c for c in colonne_ghilardotti if c in df_ghilardotti.columns]
        df_ghilardotti = df_ghilardotti[colonne_ghilardotti]
        risultati["GHILARDOTTI GILBERTO"] = df_ghilardotti

    # --------------------------------------------------
    # 7) TECNICO: VALENTINO ANGELO
    # --------------------------------------------------
    df_valentino = df[df['tecnico'] == "VALENTINO ANGELO"].copy()
    if not df_valentino.empty:
        df_valentino = df_valentino.rename(columns={
            "stato": "stato_odl",
            "DT_APERTURA": "data_odl",
            "descrizione": "descrizioni_odl"
        })
        colonne_valentino = [
            "id_odl",
            "stato_odl",
            "data_odl",
            "descrizioni_odl",
            "causa_sospensione",
            "descrizione_bene",
            "fornitore"
        ]
        colonne_valentino = [c for c in colonne_valentino if c in df_valentino.columns]
        df_valentino = df_valentino[colonne_valentino]
        risultati["VALENTINO ANGELO"] = df_valentino

    # Ritorno il dizionario con un DataFrame per ogni tecnico
    return risultati
