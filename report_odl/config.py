# report_odl/config.py

# --- Configurazione API ---
API_BASE = "http://10.38.169.149:3500/api/v1/zMaintenance/rdi"
API_USER = "fgiacchibonetta"
API_PASS = "Humanitas1!"
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
