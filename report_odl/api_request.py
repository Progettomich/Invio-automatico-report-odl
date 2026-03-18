import requests
# IMPORTANTE: Importa il dizionario dal tuo file di configurazione
from config import API_ENDPOINT, ODL_REPORT_ENDPOINT, RDI_ENDPOINT, TECNICI

# CHIAMATA API PER ODL
def fetch_odl_per_responsabili(
    user = "YOURUSER",
    password = "YOURPASSWORD",
    stati = "IN CORSO,SOSPESO,DA FARE,CONCLUSO",
    date_from = "2026-01-01",
    limit = 100,
    page = 1,
    responsabili = None
):
    
    print("Inizio fetch_odl_per_responsabili")

    endpoint_url = f"{API_ENDPOINT}{ODL_REPORT_ENDPOINT}"
    
    # SE NON PASSI NESSUNA LISTA, PRENDE AUTOMATICAMENTE I NOMI DAL CONFIG.PY!
    if responsabili is None:
        # list(TECNICI.keys()) prende solo i nomi ["Addamo FEDERICO", "PIETRAGALLA..."]
        responsabili = list(TECNICI.keys()) 

    risultati = {}

    for responsabile in responsabili:
        print(f"Elaborazione dati per responsabile: {responsabile}")

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
    endpoint_url,
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


# CHIAMATA API PER RDI asc
def fetch_rdi(
    user = "YOURUSER",
    password = "YOURPASSWORD", 
    limit = 10,
    page = 1,
    stato = "CREATA",
    orderBy = "asc"
):   

    endpoint_url = f"{API_ENDPOINT}{RDI_ENDPOINT}"

    print(f"Scaricando RDI da: {endpoint_url}")

    params = {
            "limit": limit,
            "page": page,
            "stato": stato,
            "orderBy": orderBy,
            "user": user,
            "password" : password
        }
    
    try:
        response = requests.get(endpoint_url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            # Estraiamo solo la chiave "recordset"
            if isinstance(data, dict) and "recordset" in data:
                recordset = data["recordset"]
                print(f"-> Trovati {len(recordset)} record RDI.")
                return recordset
            else:
                print("-> Nessun 'recordset' trovato nel JSON. L'API potrebbe aver cambiato formato.")
                return []
        else:
            print(f"Errore HTTP RDI: {response.status_code} - {response.text}")
            return []
            
    except requests.exceptions.RequestException as e:
        print(f"Errore di rete/chiamata API RDI: {e}")
        return []

