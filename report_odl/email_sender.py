# Libreria per effettuare chiamate HTTP verso le API
import requests

# Libreria per registrare log di errori e successi su file
import logging

# Importazione delle costanti di configurazione per email e API
from config import CC_EMAILS, MAIL_SEND_ENDPOINT, API_ENDPOINT, API_USER, API_PASS


# Configurazione del sistema di logging:
# - salva i log nel file "odl_report.log"
# - registra tutti i messaggi di livello INFO e superiore
# - formato: data/ora - livello - messaggio
logging.basicConfig(
    filename="odl_report.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def send_report(nome_tecnico, email_destinatario, email_cc, html_body, subject="Report ODL settimanale"):
    """
    Invia il report HTML al tecnico tramite richiesta POST all'API o via email SMTP.
    
    Parametri:
        tecnico (str): nome del tecnico destinatario
        email_destinatario (str): indirizzo email del tecnico
        html_body (str): corpo del report in formato HTML
        subject (str): oggetto della mail (default="Report ODL settimanale")
    
    Ritorna:
        bool: True se l'invio è andato a buon fine, False altrimenti
    """

    # Costruisce l'URL completo dell'endpoint per l'invio email
    email_endpoint_url = f"{API_ENDPOINT}{MAIL_SEND_ENDPOINT}?user={API_USER}&password={API_PASS}"

    # Costruisce il corpo della richiesta POST con tutti i dati necessari per l'invio
    payload = {
        "to": email_destinatario,  # destinatario principale: email del tecnico
        "cc": email_cc,           # indirizzi in copia conoscenza definiti in config.py
        "subject": subject,        # oggetto della email
        "text": f"Buongiorno {nome_tecnico}, in allegato il report ODL settimanale.",  # testo alternativo per client che non supportano HTML
        "html": html_body          # corpo HTML del report con tabelle e grafici
    }

    print(f"Prepared email. To: {email_destinatario}, CC: {email_cc}, Subject: {subject}")

    try:
        # Invia il report tramite chiamata POST all'endpoint email dell'API
        # json=payload converte automaticamente il dizionario in formato JSON
        response = requests.post(email_endpoint_url, json=payload, timeout=10)

        # Se il server risponde con un codice di errore HTTP, genera un'eccezione
        response.raise_for_status()

        # Registra nel log il successo dell'invio
        
        logging.info(f"Report inviato correttamente a {nome_tecnico} ({email_destinatario})")
        return True

    except requests.exceptions.RequestException as e:
        # Registra nel log l'errore con i dettagli del tecnico e il messaggio di errore
        print(f"[{nome_tecnico}] Invio email fallito con errore: {e}")
        logging.error(f"Errore invio report a {nome_tecnico} ({email_destinatario}): {e}")
        return False