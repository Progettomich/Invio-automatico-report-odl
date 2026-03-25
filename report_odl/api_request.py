
# Libreria per effettuare chiamate HTTP verso le API
import requests

# Importazione delle costanti di configurazione: endpoint API, credenziali e lista tecnici
from config import API_ENDPOINT, ODL_REPORT_ENDPOINT, RDI_ENDPOINT, TECNICI, API_USER, API_PASS, NUMERO_ODL_ENDPOINT

from datetime import datetime

# ============================================================
# CHIAMATA API PER ODL
# Scarica gli Ordini Di Lavoro per ogni tecnico presente in TECNICI
# ============================================================
def fetch_odl_per_responsabili(
    user=None,
    password=None,
    date_from=datetime.today().strftime('%Y-%m-%d'),
    date_to=datetime.today().strftime('%Y-%m-%d'),
    order_by="asc",
    stati="IN CORSO,SOSPESO,DA FARE",
    limit=15,
    page=1,
    responsabili=None
):
    """
    Scarica gli ODL per ciascun responsabile dalla API.
    User e password vengono passati come query params (non come HTTP Basic Auth).
    Gli stati vengono passati come stringa unica con virgole reali nell'URL.
    """

    # Se le credenziali non vengono passate esplicitamente,
    # usa quelle definite nel file .env tramite config.py
    if user is None:
        user = API_USER
    if password is None:
        password = API_PASS

    print("Inizio fetch_odl_per_responsabili")

    # Costruisce l'URL completo dell'endpoint ODL unendo base URL e percorso specifico
    endpoint_url = f"{API_ENDPOINT}{ODL_REPORT_ENDPOINT}"

    # Se non viene passata una lista di responsabili,
    # usa automaticamente tutti i tecnici definiti in config.py
    if responsabili is None:
        responsabili = list(TECNICI.keys())

    # Dizionario che conterrà i risultati per ogni tecnico
    # chiave = nome tecnico, valore = dati ricevuti dall'API
    risultati = {}

    # Ciclo su ogni tecnico della lista per fare una chiamata API separata
    for responsabile in responsabili:
        print(f"Elaborazione dati per responsabile: {responsabile}")

        # Parametri da passare nell'URL della richiesta GET
        params = {
            "user": user,           # username per autenticazione
            "password": password,   # password per autenticazione
            "limit": limit,         # numero massimo di record da ricevere
            "page": page,           # numero di pagina (paginazione)
            "stato": stati,         # filtra per stato ODL (IN CORSO, SOSPESO, ecc.)
            "tecnico": responsabile, # filtra gli ODL per questo specifico tecnico
            "dateFrom": date_from,  # data di inizio del filtro
            "dateTo" : date_to, # data di fine del filtro (uguale a date_from per avere solo i dati di quel giorno)
            "orderBy": order_by,       # ordina i risultati in ordine crescente (più vecchi prima)
        }

        print(f"Richiesta per tecnico: {responsabile}")

        try:
            # Effettua la chiamata GET all'API con i parametri costruiti sopra
            response = requests.get(
                endpoint_url,
                params=params,
                timeout=10,  # timeout di 10 secondi per evitare attese infinite
            )
            print("URL chiamata:", response.url)

            # Se la risposta è positiva (codice 200), estrae i dati JSON
            if response.status_code == 200:
                data = response.json()
                print("Numero record ricevuti:", len(data) if isinstance(data, list)
                      else f"risposta ricevuta (formato: {type(data).__name__})")
                # Salva i dati nel dizionario dei risultati con il nome del tecnico come chiave
                risultati[responsabile] = data["data"]["recordset"] if isinstance(data, dict) and "data" in data and "recordset" in data["data"] else []
            else:
                # In caso di errore HTTP stampa il codice e il messaggio di errore
                print("Errore HTTP:", response.status_code, response.text)
                risultati[responsabile] = None

        except requests.exceptions.RequestException as e:
            # Gestisce errori di rete (timeout, connessione rifiutata, ecc.)
            print("Errore di rete/chiamata:", e)
            risultati[responsabile] = None

        print("-" * 50)

    # Restituisce il dizionario completo con i dati di tutti i tecnici
    return risultati


def fetch_numero_odl(
        user=None,
        password=None,
        date_from=datetime.today().strftime('%Y-%m-%d'),
        date_to=datetime.today().strftime('%Y-%m-%d'),
        stati=None,
        limit=7,
        page=1,
        responsabili=None
):
    """
    Scarica il numero di odl a seconda del responsabile e dello stato (conclusi, in corso, sospesi).
    """

    # Se le credenziali non vengono passate esplicitamente,
    # usa quelle definite nel file .env tramite config.py
    if user is None:
        user = API_USER
    if password is None:
        password = API_PASS

    print("Inizio fetch_numero_odl")

    # Costruisce l'URL completo dell'endpoint ODL unendo base URL e percorso specifico
    endpoint_url = f"{API_ENDPOINT}{NUMERO_ODL_ENDPOINT}"

    # Se non viene passata una lista di responsabili,
    # usa automaticamente tutti i tecnici definiti in config.py
    if responsabili is None:
        responsabili = list(TECNICI.keys())

    # Dizionario che conterrà i risultati per ogni tecnico
    # chiave = nome tecnico, valore = dati ricevuti dall'API
    risultati = {}


    # Ciclo su ogni tecnico della lista per fare una chiamata API separata
    for responsabile in responsabili:
        print(f"Richiesta numero ODL per responsabile: {responsabile}")

        # Parametri da passare nell'URL della richiesta GET
        params = {
            "user": user,           # username per autenticazione
            "password": password,   # password per autenticazione
            "limit": limit,         # numero massimo di record da ricevere
            "page": page,           # numero di pagina (paginazione)
            "tecnico": responsabile, # filtra gli ODL per questo specifico tecnico
            "dateFrom": date_from,  # data di inizio del filtro
            "dateTo" : date_to,       # data di fine del filtro (uguale a date_from per avere solo i dati di quel giorno)
        }

        print(f"Richiesta numero ODL per tecnico: {responsabile}")

        try:
            # Effettua la chiamata GET all'API con i parametri costruiti sopra
            response = requests.get(
                endpoint_url,
                params=params,
                timeout=10,  # timeout di 10 secondi per evitare attese infinite
            )
            print("URL chiamata:", response.url)

            # Se la risposta è positiva (codice 200), estrae i dati JSON
            if response.status_code == 200:
                data = response.json()
                print("Numero record ricevuti:", len(data) if isinstance(data, list)
                      else f"risposta ricevuta (formato: {type(data).__name__})")
                # Salva i dati nel dizionario dei risultati con il nome del tecnico come chiave
                risultati[responsabile] = data["data"]["recordset"][0] if isinstance(data, dict) and "data" in data and "recordset" in data["data"] and data["data"]["recordset"] else None
            else:
                # In caso di errore HTTP stampa il codice e il messaggio di errore
                print("Errore HTTP:", response.status_code, response.text)
                risultati[responsabile] = None

        except requests.exceptions.RequestException as e:
            # Gestisce errori di rete (timeout, connessione rifiutata, ecc.)
            print("Errore di rete/chiamata:", e)
            risultati[responsabile] = None

        print("-" * 50)

        

    # Restituisce il dizionario completo con i dati di tutti i tecnici
    return risultati


# ============================================================
# CHIAMATA API PER RDI
# Scarica le Richieste Di Intervento ordinate per data (asc o desc)
# ============================================================
def fetch_rdi(
    user=None,
    password=None,
    limit=100,
    page=1,
    stato="creata",
    orderBy="asc"
):
    # Se le credenziali non vengono passate esplicitamente,
    # usa quelle definite nel file .env tramite config.py
    if user is None:
        user = API_USER
    if password is None:
        password = API_PASS

    # Costruisce l'URL completo dell'endpoint RDI
    endpoint_url = f"{API_ENDPOINT}{RDI_ENDPOINT}"

    print(f"Scaricando RDI da: {endpoint_url}")

    # Parametri da passare nell'URL della richiesta GET
    params = {
        "user": user,         # username per autenticazione
        "password": password, # password per autenticazione
        "limit": limit,       # numero massimo di record da ricevere
        "page": page,         # numero di pagina (paginazione)
        "stato": stato,       # filtra per stato RDI (es. "creata")
        "orderBy": orderBy,   # ordinamento: "asc" = crescente, "desc" = decrescente
    }

    try:
        # Effettua la chiamata GET all'API con i parametri costruiti sopra
        response = requests.get(endpoint_url, params=params, timeout=10)
        print("URL chiamata RDI:", response.url)

        # Se la risposta è positiva (codice 200), estrae i dati JSON
        if response.status_code == 200:
            data = response.json()

            # L'API restituisce un dizionario con una chiave "recordset"
            # che contiene la lista effettiva dei record RDI
            if isinstance(data, dict) and "data" in data and "recordset" in data["data"]:
                recordset = data["data"]["recordset"]
                print(f"-> Trovati {len(recordset)} record RDI.")
                return recordset
            else:
                # Se la struttura della risposta è diversa dal previsto
                print("-> Nessun 'recordset' trovato nel JSON.")
                return []
        else:
            # In caso di errore HTTP stampa il codice e il messaggio di errore
            print(f"Errore HTTP RDI: {response.status_code} - {response.text}")
            return []

    except requests.exceptions.RequestException as e:
        # Gestisce errori di rete (timeout, connessione rifiutata, ecc.)
        print(f"Errore di rete/chiamata API RDI: {e}")
        return []