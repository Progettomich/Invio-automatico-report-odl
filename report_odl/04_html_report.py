import os
import pandas as pd
from datetime import datetime
from jinja2 import Environment, FileSystemLoader

def build_html_report(tecnico: str, df_t: pd.DataFrame, grafico_b64: str) -> str:
    """
    Costruisce il report HTML leggendo il template esterno e iniettando i dati.
    """
    
    # 1. Calcola i totali per le card verdi in alto
    # Assicurati che 'stato' sia il nome corretto della colonna nel tuo DataFrame
    # Se la colonna si chiama diversamente (es. 'STATO_ODL'), cambialo qui sotto.
    colonna_stato = 'stato' 
    
    if colonna_stato in df_t.columns:
        conteggi_stato = df_t[colonna_stato].value_counts().to_dict()
    else:
        conteggi_stato = {}

    # 2. Converti il DataFrame in una lista di dizionari per far funzionare il ciclo nella tabella HTML
    # Riempiamo i valori vuoti (NaN) con una stringa vuota per non avere "NaN" stampati nell'HTML
    odl_list = df_t.fillna("").to_dict('records')

    # 3. Carica il file template_report.html
    # Usiamo os.path.dirname(__file__) per dire a Python di cercare l'HTML nella stessa cartella di questo script
    cartella_corrente = os.path.dirname(os.path.abspath(__file__))
    env = Environment(loader=FileSystemLoader(cartella_corrente))
    
    try:
        template = env.get_template('template_report.html')
    except Exception as e:
        return f"<h1>Errore: Impossibile trovare il file template_report.html</h1><p>{e}</p>"

    # 4. Inietta i dati nel template (Render)
    html_finale = template.render(
        nome=tecnico,
        data_gen=datetime.now().strftime("%d/%m/%Y %H:%M"),
        # I nomi a sinistra devono combaciare con i {{ NOME }} nel file HTML
        IN_CORSO=conteggi_stato.get("IN CORSO", 0),
        SOSPESI=conteggi_stato.get("SOSPESO", 0), # Potrebbe essere "SOSPESI" a seconda di come risponde l'API
        CHIUSI=conteggi_stato.get("CHIUSO", 0),   # Potrebbe essere "CHIUSI"
        RDI_NON_PRESI=conteggi_stato.get("RDI NON PRESI", 0),
        grafico_base64=grafico_b64,
        odl_list=odl_list
    )
    
    return html_finale
