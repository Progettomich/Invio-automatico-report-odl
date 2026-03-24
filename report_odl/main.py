# Punto di ingresso principale dell'applicazione
# Avvia lo scheduler che gestisce l'invio automatico dei report settimanali

# Importa la funzione che avvia lo scheduler dal file scheduler.py
from scheduler import schedule_report


def main():
    # Messaggio di avvio dell'applicazione
    print("Avvio gnerazione report ODL...")

    # Avvia lo scheduler che esegue automaticamente il report ogni lunedì alle 08:00
    # Questa funzione contiene un loop infinito — il programma rimane in esecuzione
    # finché non viene fermato manualmente
    schedule_report()

    # Questo messaggio viene stampato solo se lo scheduler viene fermato
    print("Generazione e invio report ODL completata.")


# Punto di ingresso dello script
# Questo blocco garantisce che main() venga eseguita solo quando
# il file viene avviato direttamente, non quando viene importato da un altro file
if __name__ == "__main__":
    main()