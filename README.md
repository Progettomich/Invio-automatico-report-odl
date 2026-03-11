# Invio-automatico-report-ODL
Generatore report settimanale automatico scritto in Python

## Descrizione del progetto
Questo progetto Python automatizza l'invio dei report degli Ordini di Lavoro (ODL) ai tecnici. 
Scarica i dati da un'API interna, li elabora filtrando per tecnico, genera report HTML con tabelle e grafici, e invia email settimanali automaticamente.

## Struttura del repository

odl-report-automation/
│
├── report_odl/
│ ├── init.py # Trasforma la cartella in modulo Python
│ ├── config.py # Configurazioni API, email e tecnici
│ ├── api.py # Funzioni per GET/POST API
│ ├── processing.py # Elaborazione dati e filtro per tecnico
│ ├── html_report.py # Generazione report HTML e grafici
│ ├── email_sender.py # Invio email o POST HTML
│ └── scheduler.py # Programmazione esecuzione settimanale
├── Dockerfile # Containerizzazione
├── requirements.txt # Librerie Python necessarie
├── README.md # Descrizione progetto
└── main.py # Avvio esecuzione
