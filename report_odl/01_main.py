import requests

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
    """
    Recupera i report ODL per una lista di responsabili/tecnici.

    Parametri:
        base_url  : URL dell'API
        user      : username per l'autenticazione
        password  : password per l'autenticazione
        stati     : stati degli ODL da filtrare (stringa separata da virgole)
        date_from : data di inizio filtro (formato YYYY-MM-DD)
        limit     : numero massimo di record per pagina
        page      : numero di pagina
        responsabili : lista di nomi tecnici (se None usa la lista di default)

    Ritorna:
        dict con i risultati per ogni tecnico { nome_tecnico: data_risposta }
    """

    if responsabili is None:
        responsabili = [
            "Addamo FEDERICO" # Lascia solo lui per fare il test
        ]
    risultati = {}

    for responsabile in responsabili:
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
