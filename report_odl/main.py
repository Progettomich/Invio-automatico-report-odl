# Punto di ingresso principale dell'applicazione
# Avvia lo scheduler che gestisce l'invio automatico dei report settimanali
# Punto di ingresso principale dell'applicazione
# Avvia lo scheduler che gestisce l'invio automatico dei report settimanali

# Importa la funzione che avvia lo scheduler dal file scheduler.py
# Importa la funzione che avvia lo scheduler dal file scheduler.py
from scheduler import schedule_report


def main():
    # Messaggio di avvio dell'applicazione
    # Messaggio di avvio dell'applicazione
    print("Starting the application...")

    # Avvia lo scheduler che esegue automaticamente il report ogni lunedì alle 08:00
    # Questa funzione contiene un loop infinito — il programma rimane in esecuzione
    # finché non viene fermato manualmente

    # Avvia lo scheduler che esegue automaticamente il report ogni lunedì alle 08:00
    # Questa funzione contiene un loop infinito — il programma rimane in esecuzione
    # finché non viene fermato manualmente
    schedule_report()

    # Questo messaggio viene stampato solo se lo scheduler viene fermato

    # Questo messaggio viene stampato solo se lo scheduler viene fermato
    print("Application finished.")


# Punto di ingresso dello script
# Questo blocco garantisce che main() venga eseguita solo quando
# il file viene avviato direttamente, non quando viene importato da un altro file

# Punto di ingresso dello script
# Questo blocco garantisce che main() venga eseguita solo quando
# il file viene avviato direttamente, non quando viene importato da un altro file
if __name__ == "__main__":
    main()
