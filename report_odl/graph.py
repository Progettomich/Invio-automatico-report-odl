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

    # 6. Impostazioni del layout (GRAFICO A BARRE)
    fig.update_layout(
        title=dict(
            text="Distribuzione degli ODL per stato",
            x=0.5,           # Posiziona al centro (50% della larghezza)
            xanchor='center' # Assicura che l'ancoraggio sia centrale
        ),
        xaxis=dict(
            title="Stato ODL",
            type='category' # Forza l'asse a testo per evitare vuoti
        ),
        yaxis=dict(
            title="Numero di ODL",
            range=[0, max(counts_ordinati) * 1.2 if counts_ordinati and max(counts_ordinati) > 0 else 5]
        ),
        width=420,
        height=500,                            # <-- Stessa altezza del grafico a torta! (era 450)
        margin=dict(l=40, r=20, t=40, b=180),  # <-- Margine inferiore allineato (era 120)
        font=dict(family="Arial", size=11),
        plot_bgcolor='#f4f7fb',                # Colore di sfondo opzionale per uniformità visiva
    )

    return fig


# ============================================================
# GRAFICO A TORTA — Distribuzione RDI per reparto
# ============================================================
def genera_grafico_torta_rdi(df_rdi_desc):
    """
    Genera grafico a torta per la distribuzione RDI per reparto.
    Mostra i primi 5 reparti in ordine decrescente; i restanti vengono sommati 
    in un'unica categoria "Altro".
    """

    colonna_reparto = "REPARTO" 

    # 1. Sicurezza: Se il DataFrame è vuoto o manca la colonna, grafico vuoto
    if df_rdi_desc.empty or colonna_reparto not in df_rdi_desc.columns:
        fig = go.Figure()
        fig.update_layout(title="Nessun RDI disponibile per il grafico a torta", width=800, height=400)
        return fig

    # 2. CONTEGGIO DEI REPARTI E ORDINAMENTO
    # df.value_counts() raggruppa, conta e ordina in automatico dal più grande al più piccolo
    reparti_counts = df_rdi_desc[colonna_reparto].fillna("Sconosciuto").value_counts()

    # 3. FILTRO "TOP 5" E RAGGRUPPAMENTO "ALTRO"
    numero_massimo_fette = 10

    # Controlla se abbiamo più di 5 reparti totali
    if len(reparti_counts) > numero_massimo_fette:
        # Prende i primi 5 (i più grandi)
        top_reparti = reparti_counts.head(numero_massimo_fette)
        
        # Somma i valori di tutti gli altri reparti (dal 6° in poi)
        somma_altri = reparti_counts.iloc[numero_massimo_fette:].sum()
        
        # Aggiunge la categoria "Altro" al nostro blocco dei Top 5
        top_reparti["Altro"] = somma_altri
        
        reparti_da_graficare = top_reparti
    else:
        # Se ci sono 5 reparti o meno, li usiamo tutti senza fare "Altro"
        reparti_da_graficare = reparti_counts

    # 4. ESTRAZIONE DATI PER IL GRAFICO E TRONCAMENTO AGGRESSIVO
    raw_labels = reparti_da_graficare.index.tolist()
    values = reparti_da_graficare.values.tolist()
    
    # TRUCCO: Plotly fa la legenda su 2 colonne SOLO SE (Testo1 + Testo2) < LarghezzaGrafico.
    # Tronchiamo in modo aggressivo a MAX 20 caratteri e usiamo "..." per indicare il taglio.
    max_chars = 20
    labels = []
    for label in raw_labels:
        if len(label) > max_chars:
            labels.append(label[:max_chars] + "..")
        else:
            # Riempiamo gli spazi vuoti con spazi invisibili o lo lasciamo così
            labels.append(label)

    # 5. CREAZIONE GRAFICO A TORTA
    fig = go.Figure(data=[
        go.Pie(
            labels=labels,
            values=values,
            textinfo='percent',  
            insidetextorientation='radial',
            marker=dict(line=dict(color='#ffffff', width=2)) 
        )
    ])

    # 6. IMPOSTAZIONI LAYOUT
    fig.update_layout(
        title=dict(
            text="Distribuzione RDI Non Presi per Reparto",
            x=0.5,
            xanchor='center'
        ),
        width=480,     # <-- Allarghiamo ancora a 480 per dare ulteriore respiro alle due colonne
        height=500, 
        showlegend=True,
        margin=dict(t=40, b=180, l=10, r=10), 
        legend=dict(
            orientation="h",       # Legenda orizzontale
            yanchor="top", 
            y=-0.1,                # Posizionata sotto la torta
            xanchor="center", 
            x=0.5, 
            font=dict(size=9), 
            traceorder="normal"
        )
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