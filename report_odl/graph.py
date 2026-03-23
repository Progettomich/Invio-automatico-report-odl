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
    "SOSPESI":  "#f59e0b",  # arancione
    "IN CORSO": "#009FE3",  # blu
    "DA FARE":  "#ef4444",  # rosso
}

# Ordine fisso con cui gli stati vengono mostrati nel grafico a barre
ORDINE_STATI = ["CONCLUSO", "SOSPESO", "IN CORSO", "DA FARE"]


# ============================================================
# GRAFICO A BARRE — Distribuzione ODL per stato
# ============================================================
def genera_grafico_plotly(df):
    """Genera grafico Plotly ordinato per ORDINE_STATI"""

    # Verifica che la colonna STATO esista nel DataFrame
    if "STATO" not in df.columns:
        raise ValueError("La colonna 'STATO' non è presente nel DataFrame")

    # Conta quanti ODL ci sono per ogni stato
    stato_counts = df["STATO"].value_counts()

    # Filtra e ordina gli stati secondo ORDINE_STATI
    # (esclude stati non presenti nei dati)
    stati_ordinati = [stato for stato in ORDINE_STATI if stato in stato_counts.index]
    counts_ordinati = [stato_counts.get(stato, 0) for stato in stati_ordinati]

    # Crea il grafico a barre con Plotly
    fig = go.Figure(data=[
        go.Bar(
            x=stati_ordinati,                                      # asse X: nomi degli stati
            y=counts_ordinati,                                     # asse Y: numero di ODL
            marker_color=[COLOR_MAP[stato] for stato in stati_ordinati],  # colore per ogni barra
            text=[f'{int(c)}' for c in counts_ordinati],           # numero mostrato sopra ogni barra
            textposition='outside',                                # posizione del numero
            textfont=dict(size=14, family="Arial Black")           # stile del testo
        )
    ])

    # Impostazioni grafiche del layout
    fig.update_layout(
        title="Distribuzione degli ODL per Stato",
        xaxis_title="Stato ODL",
        yaxis_title="Numero di ODL",
        width=800,
        height=500,
        font=dict(family="Arial", size=12)
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
        width=800,
        height=400,
        showlegend=True,
        # Legenda posizionata in basso al centro
        legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5)
    )
    return fig


# ============================================================
# CONVERSIONE GRAFICO IN BASE64
# Converte un grafico Plotly in immagine PNG codificata in base64
# per poterla incorporare direttamente nell'HTML della email
# ============================================================
def grafico_to_base64(fig):
    """Converte qualsiasi grafico Plotly in base64 per HTML"""

    # Esporta il grafico come immagine PNG in memoria
    img_bytes = fig.to_image(format="png", width=800, height=400)

    # Codifica l'immagine in base64 e la converte in stringa
    img_base64 = base64.b64encode(img_bytes).decode('utf-8')

    # Restituisce la stringa nel formato corretto per essere
    # usata direttamente come src di un tag <img> nell'HTML
    return f"data:image/png;base64,{img_base64}"
