import os
from dotenv import load_dotenv

# Load variables from .env into the environment
load_dotenv()

# --- Configurazione API ---
API_BASE = os.getenv("API_BASE")
API_USER = os.getenv("API_USER")
API_PASS = os.getenv("API_PASS")
DATE_FROM = "2026-01-01"

# --- Lista tecnici e relative email ---
TECNICI = {
    "Addamo Federico": "f.addamo@humanitas.it",
    "Urbina Zabaleta Maria": "m.urbinazabaleta@humanitas.it",
    "Pietragalla Canio": "c.pietragalla@humanitas.it",
    "Galimberti Carlo": "c.galimberti@humanitas.it",
    "Rizzo Alessandro": "a.rizzo@humanitas.it",
    "Ghilardotti Gilberto": "g.ghilardotti@humanitas.it",
    "Valentino Angelo": "a.valentino@humanitas.it"
}

# --- Configurazione invio email ---
GMAIL_MITTENTE = "tuo.account@gmail.com"
GMAIL_APP_PASSWORD = "xxxx xxxx xxxx xxxx"
CC_EMAILS = "sabrina.tapiabarzola@humanitas.it, federico.giacchibonetta@humanitas.it"
