# Invio-automatico-report-ODL
Generatore report giornaliero automatico scritto in Python

## Descrizione del progetto
Questo progetto Python automatizza l'invio dei report degli Ordini di Lavoro (ODL) ai tecnici. 
Scarica i dati da un'API interna, li elabora filtrando per tecnico, genera report HTML con tabelle e grafici, e invia email settimanali automaticamente.

## Struttura del repository

odl-report-automation/
 1. [Richiamo_dei_dati_tramite_l'API](api.py)
 2. [Filtraggio_dei_Dati](processing.py)
 3. [Creazione_pagina_HTML](html_report.py)
 4. [Richiesta_Body_mail](email_sender.py)
 5. [Invio_periodico](scheduler.py)
    
