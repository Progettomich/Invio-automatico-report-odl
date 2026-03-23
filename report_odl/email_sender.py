# report_odl/email_sender.py
import requests
import logging
from config import CC_EMAILS, GMAIL_MITTENTE, GMAIL_APP_PASSWORD, MAIL_SEND_ENDPOINT, API_ENDPOINT

# Configurazione logging base
logging.basicConfig(
    filename="odl_report.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def send_report(nome_tecnico, email_destinatario, html_body, subject="Report ODL settimanale"):
    """
    Invia il report HTML al tecnico tramite richiesta POST all'API o via email SMTP.
    
    Parametri:
        nome_tecnico (str): nome del tecnico destinatario
        email_destinatario (str): indirizzo email del tecnico
        html_body (str): corpo del report in formato HTML
        subject (str): oggetto della mail (default="Report ODL settimanale")
    
    Ritorna:
        bool: True se l'invio è andato a buon fine, False altrimenti
    """

    email_endpoint_url = f"{API_ENDPOINT}{MAIL_SEND_ENDPOINT}"

    # 1️⃣ Corpo della richiesta POST (ad esempio a un endpoint interno di invio email)
    payload = {
        "to": email_destinatario,         # destinatario principale
        "cc": CC_EMAILS,                  # copie conoscenza
        "subject": subject,
        "text": f"Buongiorno {nome_tecnico}, in allegato il report ODL settimanale.",  # testo alternativo
        "html": html_body                  # corpo HTML del report
    }

    try:
        # 2️⃣ Esempio invio via API POST (sostituire URL_API_INVIOMAIL con l'endpoint reale)
        API_ENDPOINT = f"{API_ENDPOINT}{MAIL_SEND_ENDPOINT}"
        response = requests.post(email_endpoint_url, json=payload, timeout=10)
        response.raise_for_status()  # genera eccezione se codice HTTP != 200

        logging.info(f"Report inviato correttamente a {nome_tecnico} ({email_destinatario})")
        return True

    except requests.exceptions.RequestException as e:
        logging.error(f"Errore invio report a {nome_tecnico} ({email_destinatario}): {e}")
        return False
