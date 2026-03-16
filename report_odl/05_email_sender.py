# report_odl/email_sender.py
import requests
import logging
from report_odl.config import CC_EMAILS, GMAIL_MITTENTE, GMAIL_APP_PASSWORD

# Configurazione logging base
logging.basicConfig(
    filename="odl_report.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def send_report(tecnico, email_destinatario, html_body, subject="Report ODL settimanale"):
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

    # 1️⃣ Corpo della richiesta POST (ad esempio a un endpoint interno di invio email)
    payload = {
        "to": email_destinatario,         # destinatario principale
        "cc": CC_EMAILS,                  # copie conoscenza
        "subject": subject,
        "text": f"Buongiorno {tecnico}, in allegato il report ODL settimanale.",  # testo alternativo
        "html": html_body                  # corpo HTML del report
    }

    try:
        # 2️⃣ Esempio invio via API POST (sostituire URL_API_INVIOMAIL con l'endpoint reale)
        URL_API_INVIOMAIL = "https://example.com/api/send_email"
        response = requests.post(URL_API_INVIOMAIL, json=payload, timeout=10)
        response.raise_for_status()  # genera eccezione se codice HTTP != 200

        logging.info(f"Report inviato correttamente a {tecnico} ({email_destinatario})")
        return True

    except requests.exceptions.RequestException as e:
        logging.error(f"Errore invio report a {tecnico} ({email_destinatario}): {e}")
        return False
