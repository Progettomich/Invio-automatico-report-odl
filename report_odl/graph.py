# Libreria per la creazione di grafici interattivi
import plotly.graph_objects as go

# Libreria per la gestione dei dati in formato tabellare
import pandas as pd

# Libreria per la codifica delle immagini in formato base64
import base64

# Libreria per gestire i dati binari in memoria senza salvare su disco
from io import BytesIO


# Dizionario che associa ogni stato ODL al suo colore nel grafico
# I colori sono in formato esadecimale
COLOR_MAP = {
    "CONCLUSO": "#038262",  # verde
    "SOSPESO":  "#f59e0b",  # arancione
    "IN CORSO": "#009FE3",  # blu
    "DA FARE":  "#ef4444",  # rosso
}

# Ordine fisso con cui gli stati vengono mostrati nel grafico a barre
ORDINE_STATI = ["CONCLUSO", "SOSPESO", "IN CORSO", "DA FARE"]


# ============================================================
# GRAFICO A BARRE — Distribuzione ODL per stato
# ============================================================
# ============================================================
# GRAFICO A BARRE — Distribuzione ODL per stato
# ============================================================
def genera_grafico_plotly(dati_conteggio_api):
    """
    Genera grafico Plotly ordinato per ORDINE_STATI utilizzando
    direttamente i totali pre-calcolati dall'API in formato dizionario.
    """

    # 1. Sicurezza: Se i dati non arrivano, creiamo un dizionario vuoto
    if not isinstance(dati_conteggio_api, dict):
        dati_conteggio_api = {}

    # 2. Mappatura: L'API restituisce i nomi con gli underscore ("IN_CORSO", "DA_FARE")
    # mentre noi vogliamo mostrarli con gli spazi ("IN CORSO", "DA FARE")
    chiavi_api = {
        "CONCLUSO": "CONCLUSO",
        "SOSPESO":  "SOSPESO",
        "IN CORSO": "IN_CORSO",   
        "DA FARE":  "DA_FARE"     
    }

    # 3. Costruiamo i dati basandoci strettamente sull'ORDINE_STATI
    stati_ordinati = ORDINE_STATI 
    
    # Andiamo a leggere i valori dal dizionario JSON dell'API. Se non c'è, mettiamo 0
    counts_ordinati = []
    for stato in stati_ordinati:
        chiave_esatta_api = chiavi_api[stato]
        valore = dati_conteggio_api.get(chiave_esatta_api, 0)
        counts_ordinati.append(valore)

    # 4. Creiamo la lista dei colori per le barre
    colori_ordinati = [COLOR_MAP.get(stato, "#cccccc") for stato in stati_ordinati]

    # 5. Creazione del grafico a barre
    fig = go.Figure(data=[
        go.Bar(
            x=stati_ordinati, 
            y=counts_ordinati, 
            marker_color=colori_ordinati,
            text=[f'{int(c)}' for c in counts_ordinati], 
            textposition='outside',
            textfont=dict(size=14, family="Arial Black")
        )
    ])

    # 6. Impostazioni del layout
    fig.update_layout(
        title="Distribuzione degli ODL per stato",
        xaxis=dict(
            title="Stato ODL",
            type='category' # Forza l'asse a testo per evitare vuoti
        ),
        yaxis=dict(
            title="Numero di ODL",
            range=[0, max(counts_ordinati) * 1.2 if counts_ordinati and max(counts_ordinati) > 0 else 5]
        ),
        width=420,
        height=420,
        margin=dict(l=40, r=20, t=40, b=40),
        font=dict(family="Arial", size=11)
    )

    return fig


# ============================================================
# GRAFICO A TORTA — Distribuzione RDI per reparto
# ============================================================
def genera_grafico_torta_rdi(df_rdi_desc):
    """Genera grafico a torta per la distribuzione RDI per reparto."""

    # Nome della colonna che contiene il reparto nel DataFrame RDI
    colonna_reparto = "REPARTO"  # <-- Cambia se nel JSON si chiama diversamente

    # Se il DataFrame è vuoto o manca la colonna reparto,
    # restituisce un grafico vuoto con messaggio
    if df_rdi_desc.empty or colonna_reparto not in df_rdi_desc.columns:
        fig = go.Figure()
        fig.update_layout(title="Nessun RDI disponibile per il grafico a torta", width=800, height=400)
        return fig

    # Conta quante RDI ci sono per ogni reparto
    # I valori mancanti vengono sostituiti con "Sconosciuto"
    reparti_counts = df_rdi_desc[colonna_reparto].fillna("Sconosciuto").value_counts()
    labels = reparti_counts.index.tolist()   # nomi dei reparti
    values = reparti_counts.values.tolist()  # numero di RDI per reparto

    # Crea il grafico a torta con Plotly
    fig = go.Figure(data=[
        go.Pie(
            labels=labels,
            values=values,
            textinfo='percent',                # mostra solo la percentuale nelle fette
            insidetextorientation='radial',    # testo orientato radialmente
            marker=dict(line=dict(color='#ffffff', width=2))  # bordo bianco tra le fette
        )
    ])

    # Impostazioni grafiche del layout
    fig.update_layout(
    title="Distribuzione RDI Non Presi per Reparto",
    width=420,
    height=420,
    showlegend=True,
    # Aggiungi un margine inferiore (b) più ampio per far respirare il grafico
    margin=dict(t=40, b=130, l=10, r=10), 
    legend=dict(orientation="h", yanchor="top", y=-0.1, xanchor="center", x=0.5, font=dict(size=10))
)
    return fig


# ============================================================
# CONVERSIONE GRAFICO IN BASE64
# Converte un grafico Plotly in immagine PNG codificata in base64
# per poterla incorporare direttamente nell'HTML della email
# ============================================================
def grafico_to_base64(fig):
    """Converte qualsiasi grafico Plotly in base64 puro (senza header html)"""

    # Esporta il grafico come immagine PNG in memoria
    img_bytes = fig.to_image(format="png")

    # Codifica l'immagine in base64 e la converte in stringa
    img_base64 = base64.b64encode(img_bytes).decode('utf-8')

    # Ritorna SOLO il codice, che l'API tradurrà in un file fisico
    return img_base64