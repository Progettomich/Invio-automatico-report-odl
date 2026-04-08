# scheduler.py

# Libreria per la gestione dello scheduling automatico dei task
import schedule

# Libreria per gestire le pause nel loop dello scheduler
import time

# Libreria per lavorare con date e ore
from datetime import datetime

# Libreria per gestire i percorsi dei file
import os

# Importazione delle funzioni per il recupero dei dati dall'API
from api_request import fetch_numero_odl, fetch_odl_per_responsabili, fetch_rdi, fetch_dati_andamento_ytd_per_persona

# Importazione delle funzioni per l'elaborazione dei dati
from processing import process_data, process_rdi, predict_next_rdi, elabora_ytd_odl

# Importazione della funzione per la costruzione del report HTML
from html_report import build_html_report

# Importazione della funzione per l'invio delle email
from email_sender import send_report

# Importazione della lista tecnici e delle credenziali API dal file di configurazione
from config import TECNICI, PROFILI, API_USER, API_PASS, CC_EMAILS

# Importazione delle funzioni per la generazione dei grafici
from graph import genera_grafico_plotly, genera_grafico_torta_rdi, genera_grafico_torta_apparecchiature, grafico_to_base64, crea_grafico_ytd

def scheduled_report_steps():
    """
    Funzione principale che viene eseguita dal scheduler.
    Scarica i dati ODL, elabora i report per ciascun tecnico e invia le email.
    """
    print("Esecuzione funzione Run Weekly Report iniziata.")

    today_date = datetime.today().strftime('%Y-%m-%d')
    first_day_date = f"{datetime.today().year}-01-01"

    # 1. Scarica tutti gli ODL per ogni tecnico tramite l'API
    print("Scarico gli ODL per i tecnici.")
    df_all = fetch_odl_per_responsabili(API_USER, API_PASS, first_day_date, today_date)

    # 1. Scarica numero ODL per ogni tecnico tramite l'API
    print("Scarico numero ODL per i tecnici.")
    df_num_odl = fetch_numero_odl(API_USER, API_PASS, first_day_date, today_date)

    # 2. Scarica le RDI (le chiamate ora restituiscono un dizionario diviso per profili)
    print("Scarico RDI ascendenti (per tabelle, limit 10)")
    rdi_asc_tutti = fetch_rdi(user=API_USER, password=API_PASS, limit=10, page=1, stato="creata", orderBy="asc")

    print("Scarico RDI discendenti (per tabelle, limit 10)")
    rdi_desc_tutti = fetch_rdi(user=API_USER, password=API_PASS, limit=10, page=1, stato="creata", orderBy="desc")

    # 2.1 Scarica le RDI massivamente per i grafici a torta (solo RDI aperte/create)
    print("Scarico RDI massivo per GRAFICO TORTA (limit 10000)")
    rdi_grafico_tutti = fetch_rdi(user=API_USER, password=API_PASS, limit=10000, page=1, stato="CREATA", orderBy="desc")

    # NUOVO: 2.2 Scarica lo STORICO RDI (Piano B: due chiamate separate con limite 150.000)
    print("Scarico RDI massivo per PREVISIONI GUASTI (stato: CREATA)")
    rdi_storico_create = fetch_rdi(user=API_USER, password=API_PASS, limit=150000, page=1, stato="CREATA", orderBy="desc")
    
    print("Scarico RDI massivo per PREVISIONI GUASTI (stato: CHIUSA CON ODL)")
    rdi_storico_chiuse = fetch_rdi(user=API_USER, password=API_PASS, limit=150000, page=1, stato="CHIUSA CON ODL", orderBy="desc")

    # 3. Elabora i dati ODL grezzi e li organizza per tecnico
    print("Elaboro dati relativi agli ODL")
    tecnici_dict = process_data(df_all)

    # ----------------------------------------------------
    # NUOVO: Crea una cartella "report_locali" se non esiste
    # ----------------------------------------------------
    output_dir = "report_locali"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 5. Per ciascun tecnico costruisce il report HTML e lo invia via email
    for tecnico, df_tecnico in tecnici_dict.items():

        # =====================================================================
        # 1° CONTROLLO DI SICUREZZA: Email esistente
        # =====================================================================
        email_dest = TECNICI.get(tecnico, "")
        if not email_dest:
            print(f"[{tecnico}] ⚠️ SALTO: Email non trovata nel config.")
            continue

        # =====================================================================
        # 2° CONTROLLO DI SICUREZZA: Il tecnico ha almeno un ODL nell'anno?
        # =====================================================================
        # df_tecnico è il DataFrame estratto in precedenza da process_data()
        # Se è vuoto o None, significa che il tecnico non ha ODL attivi/storici recenti.
        if df_tecnico is None or df_tecnico.empty:
            print(f"[{tecnico}] ⚠️ SALTO: Nessun ODL trovato per questo periodo. (Nuovo tecnico o nessun ticket assegnato)")
            continue

        # =====================================================================
        # 3° CONTROLLO DI SICUREZZA: Controlliamo che l'API non abbia fallito
        # =====================================================================
        num_odl_tecnico = df_num_odl.get(tecnico)
        if not isinstance(num_odl_tecnico, dict) or not num_odl_tecnico:
            print(f"[{tecnico}] ⚠️ SALTO: Nessun conteggio ODL (dizionario vuoto). Dati insufficienti per generare i grafici.")
            continue

        # Se supera tutti e tre i controlli, significa che il tecnico è "sano" 
        # e ha dati su cui lavorare. Procediamo con la grafica!
        print(f"\n[{tecnico}] ✅ Controllo superato. Generazione report in corso...")

        # Generazione grafico ODL (Codice che hai già)
        grafico_odl_raw = genera_grafico_plotly(num_odl_tecnico)
        grafico_odl_b64 = grafico_to_base64(grafico_odl_raw) 
        
        # ... RESTO DEL TUO CODICE CHE SCARICA LE RDI E CREA I GRAFICI ... 

        # ====================================================================
        # --- NUOVO GRAFICO YTD: Estrazione dati e creazione immagine isolata
        # ====================================================================
        print(f"[{tecnico}] Scarico dati e genero grafico andamento YTD ad aree.")
        anno_corr = datetime.today().year
        anno_prec = anno_corr - 1
        
        inizio_corr = f"{anno_corr}-01-01"
        inizio_prec = f"{anno_prec}-01-01"
        fine_corr = datetime.today().strftime('%Y-%m-%d')
        
        try:
            fine_prec = datetime.today().replace(year=anno_prec).strftime('%Y-%m-%d')
        except ValueError: # Sicurezza per gli anni bisestili
            fine_prec = datetime.today().replace(year=anno_prec, day=28).strftime('%Y-%m-%d')
            
        # 1. Chiamata API
        json_corr, json_prec = fetch_dati_andamento_ytd_per_persona(tecnico, API_USER, API_PASS)
        # 2. Elaborazione Pandas
        df_corr = elabora_ytd_odl(json_corr, inizio_corr, fine_corr)
        df_prec = elabora_ytd_odl(json_prec, inizio_prec, fine_prec)
        # 3. Creazione immagine
        grafico_ytd_raw = crea_grafico_ytd(df_prec, df_corr)
        grafico_ytd_b64 = grafico_to_base64(grafico_ytd_raw)
        # ====================================================================

        # Trova il profilo del tecnico per pescare solo le sue RDI
        profilo_tecnico = PROFILI.get(tecnico)

        # Recupera le RDI specifiche per quel profilo (per tabelle HTML)
        rdi_asc_personali = rdi_asc_tutti.get(profilo_tecnico, []) if profilo_tecnico else []
        rdi_desc_personali = rdi_desc_tutti.get(profilo_tecnico, []) if profilo_tecnico else []
        
        # Recupera le RDI specifiche per quel profilo (per Grafico a Torta)
        rdi_grafico_personali = rdi_grafico_tutti.get(profilo_tecnico, []) if profilo_tecnico else []
        
        # Recupera lo storico (create + chiuse) e lo unisce!
        storico_create = rdi_storico_create.get(profilo_tecnico, []) if profilo_tecnico else []
        storico_chiuse = rdi_storico_chiuse.get(profilo_tecnico, []) if profilo_tecnico else []
        
        rdi_storico_personali = storico_create + storico_chiuse

        # Stampa di controllo: vediamo quante ne ha trovate in totale
        print(f"[{tecnico}] DEBUG STORICO: Trovate {len(rdi_storico_personali)} RDI storiche totali.")

        print(f"[{tecnico}] Elaboro i dati relativi alle RDI (Profilo: {profilo_tecnico})")
        df_rdi_asc = process_rdi(rdi_asc_personali)
        df_rdi_desc = process_rdi(rdi_desc_personali)
        
        # Processa il DataFrame specifico e massivo per il grafico
        df_rdi_grafico = process_rdi(rdi_grafico_personali)

        # Processa lo storico completo per le classi per le apparecchiature
        df_rdi_storico = process_rdi(rdi_storico_personali)

        # ----------------------------------------------------
        # NUOVO: Calcolo previsioni prossime RDI (Top 5)
        # ----------------------------------------------------
        df_previsioni = None
        
        if profilo_tecnico == "tecnici":
            print(f"[{tecnico}] Profilo 'tecnici' rilevato: Calcolo previsioni prossimi guasti in corso.")
            df_previsioni = predict_next_rdi(rdi_storico_personali)
        else:
            print(f"[{tecnico}] Profilo '{profilo_tecnico}' rilevato: Salto il calcolo delle previsioni.")
        
        # Generazione grafico classe apparecchiature
        print(f"[{tecnico}] Generazione grafico apparecchiature in corso.")
        grafico_app_raw = genera_grafico_torta_apparecchiature(df_rdi_storico)
        grafico_app_b64 = grafico_to_base64(grafico_app_raw)

        # Generazione grafici RDI per lo specifico tecnico
        print(f"[{tecnico}] Generazione grafici RDI in corso.")
        grafico_rdi_raw = genera_grafico_torta_rdi(df_rdi_grafico)
        grafico_rdi_b64 = grafico_to_base64(grafico_rdi_raw)

        # Costruisce il corpo HTML del report
        print(f"[{tecnico}] generazione report HTML in corso.")
        html_body = build_html_report(
            nome_tecnico=tecnico, 
            numero_odl=num_odl_tecnico, 
            odl_tecnico=df_tecnico, 
            rdi_desc=df_rdi_desc, 
            rdi_asc=df_rdi_asc, 
            grafico_odl_b64="cid:grafico_odl.png",  
            grafico_rdi_b64="cid:grafico_rdi.png",
            grafico_app_b64="cid:grafico_app.png",
            grafico_ytd_b64="cid:grafico_ytd.png",
            previsioni_rdi=df_previsioni
        )

        # ----------------------------------------------------
        # Salvataggio del file HTML locale (per debugging)
        # ----------------------------------------------------
        nome_file = f"{tecnico.replace(' ', '_')}_report.html"
        percorso_file = os.path.join(output_dir, nome_file)
        
        html_locale = html_body.replace(
            "cid:grafico_odl.png", 
            f"data:image/png;base64,{grafico_odl_b64}"
        ).replace(
            "cid:grafico_rdi.png", 
            f"data:image/png;base64,{grafico_rdi_b64}"
        ).replace(
            "cid:grafico_app.png", 
            f"data:image/png;base64,{grafico_app_b64}"
        ).replace(
            # --- NUOVO GRAFICO YTD: Aggiunto al debug locale ---
            "cid:grafico_ytd.png", 
            f"data:image/png;base64,{grafico_ytd_b64}"
        )
        
        with open(percorso_file, "w", encoding="utf-8") as file_html:
            file_html.write(html_locale)
        print(f"[{tecnico}] Report salvato in locale con grafici visibili in: {percorso_file}")

        # ----------------------------------------------------
        # Preparazione della lista allegati
        # ----------------------------------------------------
        miei_allegati = [
            {
                "filename": "grafico_odl.png",
                "content": grafico_odl_b64,
                "encoding": "base64",
                "cid": "grafico_odl.png"
            },
            {
                "filename": "grafico_rdi.png",
                "content": grafico_rdi_b64,
                "encoding": "base64",
                "cid": "grafico_rdi.png"
            },
            {
                "filename": "grafico_app.png",
                "content": grafico_app_b64,
                "encoding": "base64",
                "cid": "grafico_app.png"
            },
            # --- NUOVO GRAFICO YTD: Aggiunto all'elenco allegati dell'email ---
            {
                "filename": "grafico_ytd.png",
                "content": grafico_ytd_b64,
                "encoding": "base64",
                "cid": "grafico_ytd.png"
            }
        ]

        # Invia il report all'email
        print(f"[{tecnico}] Report e grafici creati: invio email in corso.")
        send_report(
            nome_tecnico=tecnico, 
            email_destinatario=email_dest, 
            email_cc=CC_EMAILS, 
            html_body=html_body,
            allegati=miei_allegati
        )

def schedule_report():
    """Schedula l'esecuzione automatica."""
    schedule.every(1).minutes.do(scheduled_report_steps)
    # schedule.every().monday.at("08:00").do(scheduled_report_steps)
    print(f"[{datetime.now()}] Scheduler avviato: report automatici attivi")

    while True:
        schedule.run_pending()
        time.sleep(30)

if __name__ == "__main__":
    print("Avvio manuale per TEST immediato...")
    scheduled_report_steps()