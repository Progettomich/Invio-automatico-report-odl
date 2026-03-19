import os
import pandas as pd
from datetime import datetime
from jinja2 import Environment, FileSystemLoader


def build_html_report(nome_tecnico: str, odl_tecnico: pd.DataFrame, rdi_desc: pd.DataFrame, rdi_asc: pd.DataFrame, grafico_odl_b64: str, grafico_rdi_b64: str) -> str:
    """
    Costruisce il report HTML leggendo il template esterno e iniettando i dati.
    Il parametro grafico_b64 è opzionale: se non viene passato, il grafico non verrà mostrato.
    """
    
    # 1. Calcola i totali per le card verdi in alto
    # Assicurati che 'stato' sia il nome corretto della colonna nel tuo DataFrame
    # Se la colonna si chiama diversamente (es. 'STATO_ODL'), cambialo qui sotto.
    colonna_stato = 'STATO_ODL' 
    
    if colonna_stato in odl_tecnico.columns:
        conteggi_stato = odl_tecnico[colonna_stato].value_counts().to_dict()
    else:
        conteggi_stato = {}

    # 2. Converti il DataFrame in una lista di dizionari per far funzionare il ciclo nella tabella HTML
    # Riempiamo i valori vuoti (NaN) con una stringa vuota per non avere "NaN" stampati nell'HTML
    odl_list = odl_tecnico.fillna("").to_dict('records')

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
        # ... (le tue altre variabili) ...
        grafico_base64_odl=grafico_odl_b64,  # <- Il grafico a barre
        grafico_base64_rdi=grafico_rdi_b64,  # <- Il grafico a torta
        odl_list=odl_list,
        rdi_desc_list=rdi_desc,
        rdi_asc_list=rdi_asc,
    )
    return html_finale
