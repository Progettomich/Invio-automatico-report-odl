import requests
# IMPORTANTE: Importa il dizionario dal tuo file di configurazione
from config import TECNICI

def fetch_odl_per_responsabili(
    base_url="http://10.38.169.149:3500/api/v1/zMaintenance/REPORT/ODL",
    user="YOURUSER",
    password="YOURPASSWORD",
    stati="IN CORSO,SOSPESO,DA FARE,CONCLUSO",
    date_from="2026-01-01",
    limit=100,
    page=1,
    responsabili=None
):
    
    # SE NON PASSI NESSUNA LISTA, PRENDE AUTOMATICAMENTE I NOMI DAL CONFIG.PY!
    if responsabili is None:
        # list(TECNICI.keys()) prende solo i nomi ["Addamo FEDERICO", "PIETRAGALLA..."]
        responsabili = list(TECNICI.keys()) 

    risultati = {}

    for responsabile in responsabili:
        # ... [IL RESTO DEL TUO CODICE RIMANE IDENTICO A PRIMA] ...
        params = {
            "limit": limit,
            "page": page,
            "stato": stati,
            "tecnico": responsabile,
            "dateFrom": date_from,
        }

        print(f"Richiesta per tecnico: {responsabile}")
        try:
            response = requests.get(
    base_url,
    params=params,
    timeout=10,
    auth=(user, password)
)
            print("URL chiamata:", response.url)

            if response.status_code == 200:
                data = response.json()
                print("Numero record ricevuti:", len(data) if isinstance(data, list) else "non è una lista")
                risultati[responsabile] = data
            else:
                print("Errore HTTP:", response.status_code, response.text)
                risultati[responsabile] = None

        except requests.exceptions.RequestException as e:
            print("Errore di rete/chiamata:", e)
            risultati[responsabile] = None

        print("-" * 50)

    return risultati
