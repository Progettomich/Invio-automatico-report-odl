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
from config import API_USER, API_PASS

# Importazione delle funzioni per la generazione dei grafici
from graph import genera_grafico_plotly, genera_grafico_torta_rdi, grafico_to_base64


def run_weekly_report():
    """
    Funzione principale che viene eseguita dal scheduler.
    Scarica i dati ODL, elabora i report per ciascun tecnico e invia le email.
    """
    print("Esecuzione funzione Run Weekly Report iniziata.")

    # 1. Scarica tutti gli ODL per ogni tecnico tramite l'API
    print("Scarico gli ODL per i tecnici.")
    df_all = fetch_odl_per_responsabili(API_USER, API_PASS)

    # Controllo credenziali — da rimuovere in produzione
    print(f"Credenziali: user={API_USER}, pass={API_PASS}")

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

    # 5. Per ciascun tecnico costruisce il report HTML e lo invia via email
    for tecnico, df_tecnico in tecnici_dict.items():

        # Recupera l'email del tecnico dal dizionario TECNICI in config.py
        email_dest = TECNICI.get(tecnico, "")

        # Se l'email non è presente nel config, salta questo tecnico
        if not email_dest:
            print(f"[{tecnico}] Email non trovata nel config, salto.")
            continue

        # Costruisce il corpo HTML del report con tabelle e grafici
        html_body = build_html_report(tecnico, df_tecnico)

        # Invia il report all'email del tecnico
        send_report(tecnico, email_dest, html_body)


def schedule_report():
    """
    Schedula l'esecuzione automatica della funzione run_weekly_report()
    ogni LUNEDÌ alle 08:00.
    """

    # --- MODALITÀ TEST: esegue ogni minuto per verificare il funzionamento ---
    schedule.every(1).minutes.do(run_weekly_report)

    # --- MODALITÀ PRODUZIONE: ogni lunedì alle 08:00 ---
    # Decommentare quando il codice è pronto e commentare la riga sopra
    # schedule.every().monday.at("08:00").do(run_weekly_report)

    print(f"[{datetime.now()}] Scheduler avviato: report automatici ogni Lunedì alle 08:00")

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
