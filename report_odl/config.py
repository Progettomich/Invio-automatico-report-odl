# Libreria per leggere le variabili di ambiente dal sistema operativo
import os

# Libreria per caricare le variabili dal file .env
from dotenv import load_dotenv

# Carica le variabili definite nel file .env nell'ambiente di sistema
# Deve essere chiamata prima di qualsiasi os.getenv()
load_dotenv()


# --- Configurazione API ---
# Legge le credenziali di accesso all'API dal file .env
# In questo modo le credenziali non sono scritte in chiaro nel codice
API_USER = os.getenv("API_USER")   # username per autenticazione API
API_PASS = os.getenv("API_PASS")   # password per autenticazione API

# Indirizzo IP del server su cui gira l'API, letto dal file .env
API_BASE = os.getenv("API_BASE")

# URL base completo dell'API, costruito unendo l'indirizzo IP e il percorso fisso
API_ENDPOINT = f"{API_BASE}/api/v1/zMaintenance"

# Percorsi specifici dei singoli endpoint dell'API
RDI_ENDPOINT = "/rdi"              # endpoint per le Richieste Di Intervento
ODL_REPORT_ENDPOINT = "/report/odl" # endpoint per i report degli Ordini Di Lavoro
MAIL_SEND_ENDPOINT = "/email"       # endpoint per l'invio delle email tramite API
NUMERO_ODL_ENDPOINT = "/odl/number"     # endpoint per scaricare il numero di ODL conclusi per ciascun responsabile

# Data di inizio del filtro per il recupero dei dati storici
DATE_FROM = "2026-01-01"


# --- Lista tecnici e relative email ---
# Dizionario che associa il nome di ogni tecnico alla sua email aziendale
# Viene usato per filtrare i dati per tecnico e per inviare i report
TECNICI = {
    "Addamo Federico":       "federico.addamo@humanitas.it",
    # "Urbina Zabaleta Maria": "m.urbinazabaleta@humanitas.it",
    # "Pietragalla Canio":     "c.pietragalla@humanitas.it",
    # "Galimberti Carlo":      "c.galimberti@humanitas.it",
    # "Rizzo Alessandro":      "a.rizzo@humanitas.it",
    # "Ghilardotti Gilberto":  "g.ghilardotti@humanitas.it",
    # "Valentino Angelo":      "a.valentino@humanitas.it"
}

# --- Lista stati che possono avere gli ODL ---
# Viene usata per filtrare gli ODL in base al loro stato (es. "IN CORSO", "CONCLUSO", "SOSPESO")
STATI = {
    "IN CORSO",
    "CONCLUSO",
    "SOSPESO"
}


# Indirizzi email in copia conoscenza (CC) per ogni report inviato
CC_EMAILS = "sabrina.tapiabarzola@humanitas.it, federico.giacchibonetta@humanitas.it"