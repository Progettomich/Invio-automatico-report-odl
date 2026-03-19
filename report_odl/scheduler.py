# report_odl/scheduler.py

import schedule
import time
from datetime import datetime

from api_request import fetch_odl_per_responsabili, fetch_rdi
from processing import process_data
from processing import process_rdi
from html_report import build_html_report
from email_sender import send_report
from config import TECNICI
from config import API_USER, API_PASS

from graph import genera_grafico_plotly, genera_grafico_torta_rdi, grafico_to_base64

def run_weekly_report():
    """
    Funzione principale che viene eseguita dal scheduler.
    Scarica i dati ODL, elabora i report per ciascun tecnico e invia le email.
    """
    print("Esecuzione funzione Run Weekly Report iniziata.")

    # 1️⃣ Scarica tutti gli ODL tramite la funzione API

    print("Scarico gli ODL per i tecnico.")
    df_all = fetch_odl_per_responsabili(API_USER, API_PASS)

    print("Scarico RDI ascendenti")
    rdi_asc = fetch_rdi(user=API_USER, password=API_PASS, limit=10, page=1, stato="CREATA", orderBy="asc")

    print("Scarico RDI discendenti")
    rdi_desc = fetch_rdi(user=API_USER, password=API_PASS, limit=10, page=1, stato="CREATA", orderBy="desc")

    # 2️⃣ Elabora i dati e ritorna un dizionario {tecnico: df_tecnico}
    print("Elaboro dati relativi agli ODL")
    tecnici_dict = process_data(df_all)
     
    # Elabora i dati per gli rdi 
    print("Elaboro i dati relativi alle RDI ascendenti")
    df_rdi_asc = process_rdi(rdi_asc)

    print("Elaboro i dati relativi alle RDI discendenti")
    df_rdi_desc = process_rdi(rdi_desc)

    # 3️⃣ Per ciascun tecnico costruisce e invia il report
    for tecnico, df_tecnico in tecnici_dict.items():
        # Genera il corpo HTML del report
        html_body = build_html_report(tecnico, df_tecnico)

        # Recupera l'email destinazione dal config (TECNICI è un dict: {nome: email})
        email_dest = TECNICI.get(tecnico, "")

        # Invia il report con la funzione di invio
        send_report(tecnico, email_dest, html_body)

def schedule_report():
    """
    Schedula l'esecuzione automatica della funzione run_weekly_report()
    ogni LUNEDÌ alle 08:00.
    
    Usa la libreria 'schedule' per controllare continuamente il tempo.
    """

    # ### Imposta lo scheduling ###
    # schedule.every().monday.at("08:00").do(run_weekly_report)
    # Questo dice: ogni lunedì alle 08:00 esegui la funzione run_weekly_report()

    schedule.every().minute.do(run_weekly_report)  # <-- Per test, esegue ogni minuto

    print(f"[{datetime.now()}] Scheduler avviato: report automatici ogni Lunedì alle 08:00")

    # ### Loop infinito per controllare lo scheduler ###
    # La libreria 'schedule' richiede un ciclo costante per controllare
    # quando deve partire il job.
    while True:
        schedule.run_pending()  # controlla se è ora di eseguire qualcosa
        time.sleep(30)         # aspetta 30 secondi per non sovraccaricare la CPU

if __name__ == "__main__":
    print("Avvio manuale per TEST immediato...")
    # Invece di chiamare schedule_report(), chiamo direttamente la funzione
    run_weekly_report() 

