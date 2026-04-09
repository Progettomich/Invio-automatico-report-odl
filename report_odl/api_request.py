# api_request.py

# Libreria per effettuare chiamate HTTP verso le API
import requests

# Importazione delle costanti di configurazione: endpoint API, credenziali e lista tecnici
from config import API_ENDPOINT, ODL_REPORT_ENDPOINT, RDI_ENDPOINT, TECNICI, API_USER, API_PASS, NUMERO_ODL_ENDPOINT, PROFILI

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
                #timeout =60, # timeout di 60 secondi per evitare di fare collassare il server per la mole di dati cheisti all'api
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
    limit=10,
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

    risultati = {}

    # Estraiamo tutti i profili unici dal dizionario PROFILI in config.py
    # Usando set() eliminiamo i duplicati (es. avremo solo {"tecnici", "ferri", "freddo", "altro"})
    profili_unici = set(PROFILI.values())

    print(f"Scaricando RDI da: {endpoint_url} per i profili: {profili_unici}")

    # Facciamo una chiamata API per ogni PROFILO, non per ogni tecnico!
    for profile in profili_unici:
        print(f"Richiesta API RDI per il profilo: {profile}")

        # Parametri da passare nell'URL della richiesta GET
        params = {
            "user": user,         # username per autenticazione
            "password": password, # password per autenticazione
            "limit": limit,       # numero massimo di record da ricevere
            "page": page,         # numero di pagina (paginazione)
            "stato": stato,       # filtra per stato RDI (es. "creata")
            "orderBy": orderBy,   # ordinamento: "asc" = crescente, "desc" = decrescente
            "profile": profile    # filtra per tipo di profilo del responsabile 
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
                    print(f"-> Trovati {len(recordset)} record RDI per il profilo '{profile}'.")
                    
                    risultati[profile] = recordset
                else:
                
                    risultati[profile] = []
            else:
                # In caso di errore HTTP stampa il codice e il messaggio di errore
                print(f"Errore HTTP RDI: {response.status_code} - {response.text}")
                risultati[profile] = []

        except requests.exceptions.RequestException as e:
            # Gestisce errori di rete (timeout, connessione rifiutata, ecc.)
            print(f"Errore di rete/chiamata API RDI: {e}")
            risultati[profile] = []

    
    return risultati

# ============================================================
# NUOVA CHIAMATA API: ANDAMENTO YTD PER GRAFICO AD AREE
# ============================================================
def fetch_dati_andamento_ytd_per_persona(tecnico, user=None, password=None):
    """
    Scarica gli ODL dell'anno corrente e dell'anno precedente per un singolo tecnico,
    fermandosi alla data odierna (YTD), al fine di generare il grafico comparativo.
    Non altera in alcun modo i dati delle altre chiamate.
    """
    if user is None:
        user = API_USER
    if password is None:
        password = API_PASS

    print(f"[{tecnico}] Inizio fetch dati andamento YTD...")

    # Usa lo stesso endpoint reportistico degli ODL
    endpoint_url = f"{API_ENDPOINT}{ODL_REPORT_ENDPOINT}"
    
    oggi = datetime.today()
    anno_corr = oggi.year
    anno_prec = anno_corr - 1
    
    inizio_corr = f"{anno_corr}-01-01"
    inizio_prec = f"{anno_prec}-01-01"
    fine_corr = oggi.strftime('%Y-%m-%d')
    
    # Gestione anni bisestili per l'anno precedente
    try:
        fine_prec = oggi.replace(year=anno_prec).strftime('%Y-%m-%d')
    except ValueError:
        fine_prec = oggi.replace(year=anno_prec, day=28).strftime('%Y-%m-%d')

    # Status e parametri base (limit alto per evitare paginazione)
    stati_richiesti = "IN CORSO,SOSPESO,DA FARE,CONCLUSO"
    limit_massimo = 2000

    params_corrente = {
        "user": user,
        "password": password,
        "limit": limit_massimo,
        "page": 1,
        "stato": stati_richiesti,
        "tecnico": tecnico,
        "dateFrom": inizio_corr,
        "dateTo": fine_corr
    }

    params_precedente = {
        "user": user,
        "password": password,
        "limit": limit_massimo,
        "page": 1,
        "stato": stati_richiesti,
        "tecnico": tecnico,
        "dateFrom": inizio_prec,
        "dateTo": fine_prec
    }

    risultato_corrente = []
    risultato_precedente = []

    try:
        # Chiamata API Anno Corrente
        resp_corr = requests.get(endpoint_url, params=params_corrente, timeout=15)
        if resp_corr.status_code == 200:
            data_corr = resp_corr.json()
            if isinstance(data_corr, dict) and "data" in data_corr and "recordset" in data_corr["data"]:
                risultato_corrente = data_corr["data"]["recordset"]

        # Chiamata API Anno Precedente
        resp_prec = requests.get(endpoint_url, params=params_precedente, timeout=15)
        if resp_prec.status_code == 200:
            data_prec = resp_prec.json()
            if isinstance(data_prec, dict) and "data" in data_prec and "recordset" in data_prec["data"]:
                risultato_precedente = data_prec["data"]["recordset"]

    except requests.exceptions.RequestException as e:
        print(f"[{tecnico}] Errore API durante andamento YTD: {e}")

    return risultato_corrente, risultato_precedente