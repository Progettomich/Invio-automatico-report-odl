# Libreria per la gestione dello scheduling automatico dei task
import schedule

# Libreria per gestire le pause nel loop dello scheduler
import time

# Libreria per lavorare con date e ore
from datetime import datetime

# Importazione delle funzioni per il recupero dei dati dall'API
from api_request import fetch_odl_per_responsabili, fetch_rdi

# Importazione delle funzioni per l'elaborazione dei dati ODL e RDI
from processing import process_data
from processing import process_rdi

# Importazione della funzione per la costruzione del report HTML
from html_report import build_html_report

# Importazione della funzione per l'invio delle email
from email_sender import send_report

# Importazione della lista tecnici e delle credenziali API dal file di configurazione
from config import TECNICI
from config import API_USER, API_PASS, CC_EMAILS

# Importazione delle funzioni per la generazione dei grafici
from graph import genera_grafico_plotly, genera_grafico_torta_rdi, grafico_to_base64


def scheduled_report_steps():
    """
    Funzione principale che viene eseguita dal scheduler.
    Scarica i dati ODL, elabora i report per ciascun tecnico e invia le email.
    """
    print("Esecuzione funzione Run Weekly Report iniziata.")

    # 1. Scarica tutti gli ODL per ogni tecnico tramite l'API
    print("Scarico gli ODL per i tecnici.")
    df_all = fetch_odl_per_responsabili(API_USER, API_PASS)

    # 2. Scarica le RDI in ordine crescente (le più vecchie prima)
    print("Scarico RDI ascendenti")
    rdi_asc = fetch_rdi(user=API_USER, password=API_PASS, limit=10, page=1, stato="creata", orderBy="asc")

    # Scarica le RDI in ordine decrescente (le più recenti prima)
    print("Scarico RDI discendenti")
    rdi_desc = fetch_rdi(user=API_USER, password=API_PASS, limit=10, page=1, stato="creata", orderBy="desc")

    # 3. Elabora i dati ODL grezzi e li organizza per tecnico
    # Restituisce un dizionario { nome_tecnico: DataFrame }
    print("Elaboro dati relativi agli ODL")
    tecnici_dict = process_data(df_all)

    # 4. Elabora i dati RDI grezzi e li converte in DataFrame puliti
    print("Elaboro i dati relativi alle RDI ascendenti")
    df_rdi_asc = process_rdi(rdi_asc)

    print("Elaboro i dati relativi alle RDI discendenti")
    df_rdi_desc = process_rdi(rdi_desc)

    # Generazione grafici RDI
    print(f"Generazione grafici RDI in corso.")
    grafico_rdi_raw = genera_grafico_torta_rdi(df_rdi_desc)
    grafico_rdi = grafico_to_base64(grafico_rdi_raw)

    # 5. Per ciascun tecnico costruisce il report HTML e lo invia via email
    for tecnico, df_tecnico in tecnici_dict.items():

        # Recupera l'email del tecnico dal dizionario TECNICI in config.py
        email_dest = TECNICI.get(tecnico, "")

        # Se l'email non è presente nel config, salta questo tecnico
        if not email_dest:
            print(f"[{tecnico}] Email non trovata nel config, salto.")
            continue

        # Generazione grafici personalizzati
        print(f"[{tecnico}] generazione grafico ODL in corso.")
        grafico_odl_raw = genera_grafico_plotly(df_tecnico)
        grafico_odl = grafico_to_base64(grafico_odl_raw)

        # Costruisce il corpo HTML del report con tabelle e grafici
        print(f"[{tecnico}] generazione report HTML in corso.")
        html_body = build_html_report(tecnico, df_tecnico, df_rdi_desc, df_rdi_asc, grafico_odl, grafico_rdi)

        # Invia il report all'email del tecnico
        print(f"[{tecnico}] Report e grafici creati: invio email in corso.")
        send_report(tecnico, email_dest, CC_EMAILS, html_body)


def schedule_report():
    """
    Schedula l'esecuzione automatica della funzione scheduled_report_steps().
    """

    # --- MODALITÀ TEST: esegue ogni minuto per verificare il funzionamento ---
    schedule.every(1).minutes.do(scheduled_report_steps)

    # --- MODALITÀ PRODUZIONE: ogni lunedì alle 08:00 ---
    # Decommentare quando il codice è pronto e commentare la riga sopra
    # schedule.every().monday.at("08:00").do(scheduled_report_steps)

    print(f"[{datetime.now()}] Scheduler avviato: report automatici attivi")

    # Loop infinito che controlla ogni 30 secondi se è ora di eseguire il task
    # time.sleep(30) evita di sovraccaricare la CPU con controlli continui
    while True:
        schedule.run_pending()  # esegue i task in scadenza
        time.sleep(30)          # attende 30 secondi prima del prossimo controllo


# Avvio manuale per test
# Questo blocco viene eseguito solo quando il file viene avviato direttamente
if __name__ == "__main__":
    print("Avvio manuale per TEST immediato...")
    schedule_report()