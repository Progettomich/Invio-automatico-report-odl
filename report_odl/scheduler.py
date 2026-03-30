# Libreria per la gestione dello scheduling automatico dei task
import schedule

# Libreria per gestire le pause nel loop dello scheduler
import time

# Libreria per lavorare con date e ore
from datetime import date, datetime

# Libreria per gestire i percorsi dei file
import os

# Importazione delle funzioni per il recupero dei dati dall'API
from api_request import fetch_numero_odl, fetch_odl_per_responsabili, fetch_rdi

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

    today_date = datetime.today().strftime('%Y-%m-%d')
    first_day_date = f"{date.today().year}-01-01"

    # 1. Scarica tutti gli ODL per ogni tecnico tramite l'API
    print("Scarico gli ODL per i tecnici.")
    df_all = fetch_odl_per_responsabili(API_USER, API_PASS, first_day_date, today_date)

    # 1. Scarica tutti gli ODL per ogni tecnico tramite l'API
    print("Scarico numero ODL per i tecnici.")
    df_num_odl = fetch_numero_odl(API_USER, API_PASS, first_day_date, today_date)

    # 2. Scarica le RDI in ordine crescente (le più vecchie prima)
    print("Scarico RDI ascendenti")
    rdi_asc = fetch_rdi(user=API_USER, password=API_PASS, limit=10, page=1, stato="creata", orderBy="asc")

    # Scarica le RDI in ordine decrescente (le più recenti prima)
    print("Scarico RDI discendenti")
    rdi_desc = fetch_rdi(user=API_USER, password=API_PASS, limit=10, page=1, stato="creata", orderBy="desc")

    # 3. Elabora i dati ODL grezzi e li organizza per tecnico
    print("Elaboro dati relativi agli ODL")
    tecnici_dict = process_data(df_all)

    # 4. Elabora i dati RDI grezzi e li converte in DataFrame puliti
    print("Elaboro i dati relativi alle RDI ascendenti")
    df_rdi_asc = process_rdi(rdi_asc)

    print("Elaboro i dati relativi alle RDI discendenti")
    df_rdi_desc = process_rdi(rdi_desc)

    # Generazione grafici RDI (crea la stringa Base64 pura)
    print(f"Generazione grafici RDI in corso.")
    grafico_rdi_raw = genera_grafico_torta_rdi(df_rdi_desc)
    grafico_rdi_b64 = grafico_to_base64(grafico_rdi_raw) # <--- Ora è Base64 puro

    # ----------------------------------------------------
    # NUOVO: Crea una cartella "report_locali" se non esiste
    # ----------------------------------------------------
    output_dir = "report_locali"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 5. Per ciascun tecnico costruisce il report HTML e lo invia via email
    for tecnico, df_tecnico in tecnici_dict.items():

        # Recupera l'email del tecnico dal dizionario TECNICI in config.py
        email_dest = TECNICI.get(tecnico, "")

        if not email_dest:
            print(f"[{tecnico}] Email non trovata nel config, salto.")
            continue

        num_odl_tecnico = df_num_odl.get(tecnico)

        # Generazione grafico ODL (crea la stringa Base64 pura)
        print(f"[{tecnico}] generazione grafico ODL in corso.")
        grafico_odl_raw = genera_grafico_plotly(num_odl_tecnico)
        grafico_odl_b64 = grafico_to_base64(grafico_odl_raw) 

        # Costruisce il corpo HTML del report passando le stringhe cid al posto delle stringhe base64 lunghissime
        print(f"[{tecnico}] generazione report HTML in corso.")
        html_body = build_html_report(
            nome_tecnico=tecnico, 
            numero_odl=num_odl_tecnico, 
            odl_tecnico=df_tecnico, 
            rdi_desc=df_rdi_desc, 
            rdi_asc=df_rdi_asc, 
            grafico_odl_b64="cid:grafico_odl.png",  
            grafico_rdi_b64="cid:grafico_rdi.png"  
        )

                # ----------------------------------------------------
        # Salvataggio del file HTML locale (per debugging)
        # ----------------------------------------------------
        nome_file = f"{tecnico.replace(' ', '_')}_report.html"
        percorso_file = os.path.join(output_dir, nome_file)
        
        # Sostituiamo i riferimenti 'cid:' con le stringhe Base64 complete per la visualizzazione offline nel browser
        html_locale = html_body.replace(
            "cid:grafico_odl.png", 
            f"data:image/png;base64,{grafico_odl_b64}"
        ).replace(
            "cid:grafico_rdi.png", 
            f"data:image/png;base64,{grafico_rdi_b64}"
        )
        
        # Salviamo la versione modificata (html_locale) e non html_body
        with open(percorso_file, "w", encoding="utf-8") as file_html:
            file_html.write(html_locale)
        print(f"[{tecnico}] Report salvato in locale con grafici visibili in: {percorso_file}")

        # ----------------------------------------------------
        # MODIFICA: Preparazione della lista allegati
        # ----------------------------------------------------
        miei_allegati = [
            {
                "filename": "grafico_odl.png",
                "content": grafico_odl_b64,
                "encoding": "base64",
                "cid": "grafico_odl.png"  # Collega l'allegato al tag HTML <img src="cid:grafico_odl.png">
            },
            {
                "filename": "grafico_rdi.png",
                "content": grafico_rdi_b64,
                "encoding": "base64",
                "cid": "grafico_rdi.png"  # Collega l'allegato al tag HTML <img src="cid:grafico_rdi.png">
            }
        ]

        # Invia il report all'email del tecnico includendo gli allegati
        print(f"[{tecnico}] Report e grafici creati: invio email in corso.")
        send_report(
            nome_tecnico=tecnico, 
            email_destinatario=email_dest, 
            email_cc=CC_EMAILS, 
            html_body=html_body,
            allegati=miei_allegati # <-- Passiamo l'array di allegati
        )

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

    while True:
        schedule.run_pending()
        time.sleep(30)

# Avvio manuale per test
if __name__ == "__main__":
    print("Avvio manuale per TEST immediato...")
    scheduled_report_steps() # <-- Chiamiamo direttamente la funzione per fare un test istantaneo, invece di aspettare il minuto