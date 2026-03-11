# report_odl/processing.py
import pandas as pd
from datetime import datetime

def process_data(df):
    """
    Elabora i dati ODL calcolando KPI e giorni trascorsi,
    filtrando i dati per ciascun tecnico.

    Parametri:
        df (pd.DataFrame): DataFrame contenente tutti gli ODL scaricati

    Ritorna:
        dict: dizionario con chiave=nome tecnico, valore=DataFrame filtrato
    """

    # 1️⃣ Normalizza eventuali colonne mancanti
    # Se il DataFrame non contiene la colonna 'tecnico' o 'DT_APERTURA', crea colonne vuote
    if 'tecnico' not in df.columns:
        df['tecnico'] = ''
    if 'DT_APERTURA' not in df.columns:
        df['DT_APERTURA'] = pd.NaT

    # 2️⃣ Converte la colonna delle date in formato datetime
    df['DT_APERTURA'] = pd.to_datetime(df['DT_APERTURA'], errors='coerce')

    # 3️⃣ Calcola il numero di giorni trascorsi dall'apertura dell'ODL
    oggi = pd.Timestamp(datetime.now().date())
    df['giorni_trascorsi'] = (oggi - df['DT_APERTURA']).dt.days

    # 4️⃣ Calcola i KPI per ciascun tecnico
    # Creiamo un dizionario che conterrà i DataFrame filtrati per tecnico
    tecnici_dict = {}

    # Otteniamo la lista dei tecnici presenti nei dati
    tecnici_presenti = df['tecnico'].dropna().unique()

    for tecnico in tecnici_presenti:
        # Filtra i dati solo per il tecnico corrente
        df_tecnico = df[df['tecnico'] == tecnico].copy()

        # Conta ODL per stato
        df_tecnico['num_in_corso'] = (df_tecnico['stato'] == 'IN CORSO').sum()
        df_tecnico['num_sospesi'] = (df_tecnico['stato'] == 'SOSPESO').sum()
        df_tecnico['num_da_fare'] = (df_tecnico['stato'] == 'DA FARE').sum()

        # Inserisce il DataFrame filtrato nel dizionario
        tecnici_dict[tecnico] = df_tecnico

    # 5️⃣ Restituisce il dizionario con tutti i tecnici
    return tecnici_dict
