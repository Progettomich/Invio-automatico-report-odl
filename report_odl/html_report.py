# Libreria per gestire i percorsi dei file in modo compatibile con tutti i sistemi operativi
import os

# Libreria per la gestione dei dati in formato tabellare
import pandas as pd

# Libreria per lavorare con date e ore
from datetime import datetime

# Libreria per il motore di template HTML (Jinja2)
# Permette di separare il codice Python dall'HTML
from jinja2 import Environment, FileSystemLoader


def build_html_report(
    nome_tecnico: str,
    odl_tecnico: pd.DataFrame,
    rdi_desc: pd.DataFrame,
    rdi_asc: pd.DataFrame,
    grafico_odl_b64: str,
    grafico_rdi_b64: str
) -> str:
    """
    Costruisce il report HTML leggendo il template esterno e iniettando i dati.
    Il parametro grafico_b64 è opzionale: se non viene passato, il grafico non verrà mostrato.
    """

    # 1. Calcola i totali per le card dei conteggi in alto nel report
    # Conta quanti ODL ci sono per ogni stato (IN CORSO, SOSPESO, ecc.)
    # Assicurati che 'STATO_ODL' sia il nome corretto della colonna nel DataFrame
    colonna_stato = 'STATO_ODL'

    if colonna_stato in odl_tecnico.columns:
        # Crea un dizionario { "IN CORSO": 5, "SOSPESO": 2, ... }
        conteggi_stato = odl_tecnico[colonna_stato].value_counts().to_dict()
    else:
        # Se la colonna non esiste, usa un dizionario vuoto per evitare errori
        conteggi_stato = {}

    # 2. Converti il DataFrame ODL in una lista di dizionari
    # Questo formato è necessario per iterare i dati nel template HTML
    # fillna("") sostituisce i valori NaN con stringa vuota per evitare
    # che nell'HTML appaia la scritta "NaN"
    odl_list = odl_tecnico.fillna("").to_dict('records')

    # 3. Carica il file template_report.html dalla stessa cartella di questo script
    # os.path.dirname(__file__) restituisce il percorso della cartella corrente
    # in modo che funzioni correttamente su qualsiasi computer
    cartella_corrente = os.path.dirname(os.path.abspath(__file__))

    # Crea l'ambiente Jinja2 puntando alla cartella dove si trova il template
    env = Environment(loader=FileSystemLoader(cartella_corrente))

    try:
        # Carica il file template_report.html
        template = env.get_template('template_report.html')
    except Exception as e:
        # Se il file template non viene trovato, restituisce un HTML di errore
        return f"<h1>Errore: Impossibile trovare il file template_report.html</h1><p>{e}</p>"

    # 4. Inietta i dati nel template e genera l'HTML finale
    # Ogni variabile passata qui diventa disponibile nel file template_report.html
    html_finale = template.render(
        grafico_base64_odl=grafico_odl_b64,  # grafico a barre degli ODL in formato base64
        grafico_base64_rdi=grafico_rdi_b64,  # grafico a torta delle RDI in formato base64
        odl_list=odl_list,                   # lista degli ODL del tecnico
        rdi_desc_list=rdi_desc,              # lista RDI in ordine decrescente
        rdi_asc_list=rdi_asc,               # lista RDI in ordine crescente
    )

    # Restituisce la stringa HTML completa pronta per essere inviata via email
    return html_finale