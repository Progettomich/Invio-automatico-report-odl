# report_odl/scheduler.py

import schedule  # libreria semplice per scheduling
import time
from datetime import datetime
from report_odl.01_main import fetch_odl_per_responsabili
from report_odl.02_processing import process_data
from report_odl.04_html_report import build_html
from report_odl.05_email_sender import send_report
from report_odl.config import TECNICI

def run_weekly_report():
    """
    Funzione principale che viene eseguita dal scheduler.
    Scarica i dati ODL, elabora i report per ciascun tecnico e invia le email.
    """

    # 1️⃣ Scarica tutti gli ODL tramite la funzione API
    df_all = fetch_odl_per_responsabili

    # 2️⃣ Elabora i dati e ritorna un dizionario {tecnico: df_tecnico}
    tecnici_dict = process_data(df_all)

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

    schedule.every().monday.at("08:00").do(run_weekly_report)

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

