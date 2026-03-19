# main.py

from scheduler import schedule_report


def main():
    # Setup logging and startup application
    print("Starting the application...")
    
    # EXECUTE MAIN FUNCTION
    schedule_report()
    
    # Log completion of the application
    print("Application finished.")

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
