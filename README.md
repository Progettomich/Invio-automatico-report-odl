# Invio-automatico-report-ODL

Generatore report giornaliero automatico scritto in Python

## Descrizione del progetto

Questo progetto Python automatizza l'invio dei report degli Ordini di Lavoro (ODL) ai tecnici.
Scarica i dati da un'API interna, li elabora filtrando per tecnico, genera report HTML con tabelle e grafici, e invia email giornaliere automaticamente.

## Struttura del repository

1.  [Connessione e richiamo dei dati dalla API](api.py)
2.  [Elaborazione dei dati](processing.py)
3.  [Generazione dell'HTML](html_report.py)
4.  [Invio email](email_sender.py)
5.  [Ripetizione periodica](scheduler.py)
