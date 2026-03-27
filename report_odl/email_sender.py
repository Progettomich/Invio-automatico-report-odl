# Libreria per effettuare chiamate HTTP verso le API
import requests

# Libreria per registrare log di errori e successi su file
import logging

# Importazione delle costanti di configurazione per email e API
from config import CC_EMAILS, MAIL_SEND_ENDPOINT, API_ENDPOINT, API_USER, API_PASS

# Configurazione del sistema di logging
logging.basicConfig(
    filename="odl_report.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def send_report(nome_tecnico, email_destinatario, email_cc, html_body, subject="Report ODL settimanale", allegati=None):
    """
    Invia il report HTML al tecnico tramite richiesta POST all'API.
    """
    # Costruisce l'URL completo dell'endpoint per l'invio email
    email_endpoint_url = f"{API_ENDPOINT}{MAIL_SEND_ENDPOINT}?user={API_USER}&password={API_PASS}"

    # Costruisce il corpo della richiesta POST con tutti i dati necessari per l'invio
    payload = {
        "to": email_destinatario,  
        "cc": email_cc,           
        "subject": subject,        
        "text": f"Buongiorno {nome_tecnico}, in allegato il report ODL settimanale.",
        "html": html_body         
    }

    # Se passiamo degli allegati dalla funzione principale, li aggiungiamo al JSON
    if allegati:
        payload["attachments"] = allegati

    print(f"Prepared email. To: {email_destinatario}, CC: {email_cc}, Subject: {subject}")

    try:
        # Invia il report tramite chiamata POST all'endpoint email dell'API
        # json=payload converte automaticamente il dizionario in formato JSON
        response = requests.post(email_endpoint_url, json=payload, timeout=10)

        # Se il server risponde con un codice di errore HTTP, genera un'eccezione
        response.raise_for_status()

        # Registra nel log il successo dell'invio
        print(f"Report inviato correttamente a {nome_tecnico} ({email_destinatario})")
        logging.info(f"Report inviato correttamente a {nome_tecnico} ({email_destinatario})")
        return True

    except requests.exceptions.RequestException as e:
        # Registra nel log l'errore con i dettagli del tecnico e il messaggio di errore
        print(f"[{nome_tecnico}] Invio email fallito con errore: {e}")
        logging.error(f"Errore invio report a {nome_tecnico} ({email_destinatario}): {e}")
        return False