
from scheduler import schedule_report

def main():
    # inizializza il report
    print("Generazione report...")
    
    # avvia lo scheduler per la generazione e invio automatico dei report ogni settimana
    scheduler.schedule_report()
    
    # il programma rimane in esecuzione per permettere allo scheduler di funzionare
    print("Report completato.")

if __name__ == "__main__":
    main()

"""
Modulo report_odl
Contiene tutti i moduli per gestire:
- fetch dei dati ODL
- elaborazione e KPI
- generazione report HTML
- invio email
- scheduling automatico
"""
