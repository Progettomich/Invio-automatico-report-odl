# Invio-automatico-report-ODL
Generatore report giornaliero automatico scritto in Python

## Descrizione del progetto
Questo progetto Python automatizza l'invio dei report degli Ordini di Lavoro (ODL) ai tecnici. 
Scarica i dati da un'API interna, li elabora filtrando per tecnico, genera report HTML con tabelle e grafici, e invia email settimanali automaticamente.

## Struttura del repository

odl-report-automation/
 1. [Richiamo dei dati tramite l'API](api.py)
 2. [Filtraggio dei Dati](processing.py)
 3. [Creazione pagina HTML](html_report.py)
 4. [Richiesta Body mail](email_sender.py)
 5. [Invio periodico](scheduler.py)
    
