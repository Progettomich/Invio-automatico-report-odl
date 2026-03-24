# Modulo per gestire i percorsi dei file in modo indipendente dal sistema operativo
import os
# Modulo per la manipolazione e l'analisi dei dati tabellari
import pandas as pd
# Modulo per la formattazione di date e orari
from datetime import datetime
# Motore di template per generare l'HTML dinamico separando la logica dalla grafica
from jinja2 import Environment, FileSystemLoader

def build_html_report(
    nome_tecnico: str,
    numero_odl: object,
    odl_tecnico: pd.DataFrame,
    rdi_desc: pd.DataFrame,
    rdi_asc: pd.DataFrame,
    grafico_odl_b64: str,
    grafico_rdi_b64: str
) -> str:
    """
    Costruisce il report HTML finale per un tecnico specifico combinando dati tabellari, 
    grafici in base64 e calcolando i KPI da inserire nel template Jinja2.
    """

    print(f"Costruzione report HTML per il tecnico: {nome_tecnico}")


    # Prepara la lista di dizionari per la tabella ODL nel template HTML
    odl_list = (
        # Sostituisce eventuali valori nulli (NaN) con stringhe vuote per evitare 
        # la fastidiosa scritta "NaN" all'interno della tabella HTML finale
        odl_tecnico.fillna("")
        
        # Rinomina le colonne del DataFrame in modo che combacino esattamente con i nomi 
        # delle variabili usate nel file template_report.html (es. odl.id_odl, odl.stato_odl)
        .rename(columns={
            "N_ODL": "id_odl",
            "DATA_ODL": "data_odl",
            "GIORNI_TRASCORSI": "giorni_trascorsi",
            "STATO_ODL": "stato_odl",
            "DESCRIZIONE_ODL": "descrizione_odl",
            "CAUSA_SOSPENSIONE": "causa_sospensione",
            "DESCRIZIONE_BENE": "descrizione_bene",
            "FORNITORE_APPARECCHIATURA": "fornitore",
        })
        
        # Converte il DataFrame in una lista di dizionari (un dizionario per ogni riga) 
        # pronta per essere iterata dal ciclo for nel template Jinja2
        .to_dict("records")
    )

    # Prepara la lista di dizionari per la tabella delle RDI discendenti (più recenti)
    # Sostituisce i NaN con stringhe vuote e converte il DataFrame in lista di record
    rdi_desc_list = rdi_desc.fillna("").to_dict("records")

    # Prepara la lista di dizionari per la tabella delle RDI ascendenti (più vecchie)
    # Sostituisce i NaN con stringhe vuote e converte il DataFrame in lista di record
    rdi_asc_list = rdi_asc.fillna("").to_dict("records")

    # Identifica il percorso assoluto della cartella corrente in cui si trova questo file Python
    cartella_corrente = os.path.dirname(os.path.abspath(__file__))
    
    # Inizializza l'ambiente Jinja2 dicendogli di cercare i template nella cartella corrente
    env = Environment(loader=FileSystemLoader(cartella_corrente))
    
    # Carica in memoria il file HTML che funge da scheletro per il report
    template = env.get_template("template_report.html")

    ODL_IN_CORSO=numero_odl["IN_CORSO"],
    ODL_SOSPESI=numero_odl["SOSPESO"],
    ODL_CHIUSI=numero_odl["CONCLUSO"],

    print(f"DEBUG: {ODL_IN_CORSO} ODL in corso, {ODL_SOSPESI} ODL sospesi, {ODL_CHIUSI} ODL chiusi."),

    # Inietta tutte le variabili e le liste calcolate all'interno del template HTML
    # La funzione .render() andrà a sostituire tutte le parentesi graffe {{ ... }} del file HTML
    html_finale = template.render(
        
        # Variabili per l'intestazione e i sottotitoli
        nome=nome_tecnico,
        data_gen=datetime.now().strftime("%d/%m/%Y %H:%M"),
        
        # Variabili per valorizzare le 4 card in verde in alto nel report
        IN_CORSO=ODL_IN_CORSO,
        SOSPESI=ODL_SOSPESI,
        CHIUSI=ODL_CHIUSI,

        RDI_NON_PRESI=len(rdi_desc_list), # Numero di RDI calcolato contando le righe della tabella
        
        # Immagini dei grafici passate sotto forma di stringhe codificate in Base64
        grafico_base64_odl=grafico_odl_b64,
        grafico_base64_rdi=grafico_rdi_b64,
        
        # Liste di dati passate al template per popolare dinamicamente le righe delle tabelle
        odl_list=odl_list,
        rdi_desc_list=rdi_desc_list,
        rdi_asc_list=rdi_asc_list,
    )

    # Ritorna la stringa completa contenente l'intero report formattato in HTML
    return html_finale
