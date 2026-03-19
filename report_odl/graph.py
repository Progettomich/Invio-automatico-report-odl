import plotly.graph_objects as go
import pandas as pd
import base64
from io import BytesIO

COLOR_MAP = {
    "CONCLUSO": "#038262",
    "SOSPESI": "#f59e0b", 
    "IN CORSO": "#009FE3",
    "DA FARE": "#ef4444",
}
ORDINE_STATI = ["CONCLUSO", "SOSPESO", "IN CORSO", "DA FARE"]

# Funzione per generare il grafico a barre per gli odl

def genera_grafico_plotly(df):
    """Genera grafico Plotly ordinato per ORDINE_STATI"""
    if "STATO" not in df.columns:
        raise ValueError("La colonna 'STATO' non è presente nel DataFrame")
    
    stato_counts = df["STATO"].value_counts()
    stati_ordinati = [stato for stato in ORDINE_STATI if stato in stato_counts.index]
    counts_ordinati = [stato_counts.get(stato, 0) for stato in stati_ordinati]
    
    fig = go.Figure(data=[
        go.Bar(
            x=stati_ordinati, 
            y=counts_ordinati,
            marker_color=[COLOR_MAP[stato] for stato in stati_ordinati],
            text=[f'{int(c)}' for c in counts_ordinati],
            textposition='outside',
            textfont=dict(size=14, family="Arial Black")
        )
    ])
    
    fig.update_layout(
        title="Distribuzione degli ODL per Stato",
        xaxis_title="Stato ODL",
        yaxis_title="Numero di ODL",
        width=800, 
        height=500,
        font=dict(family="Arial", size=12)
    )
    return fig

# Funzione per generare il grafico a torta per i reparti

def genera_grafico_torta_rdi(df_rdi_desc):
    """Genera grafico a torta per la distribuzione RDI per reparto."""
    colonna_reparto = "REPARTO" # <-- Cambia se nel JSON si chiama diversamente
    
    if df_rdi_desc.empty or colonna_reparto not in df_rdi_desc.columns:
        fig = go.Figure()
        fig.update_layout(title="Nessun RDI disponibile per il grafico a torta", width=800, height=400)
        return fig
    
    reparti_counts = df_rdi_desc[colonna_reparto].fillna("Sconosciuto").value_counts()
    labels = reparti_counts.index.tolist()
    values = reparti_counts.values.tolist()
    
    fig = go.Figure(data=[
        go.Pie(
            labels=labels, 
            values=values,
            textinfo='percent', # Mostra solo la percentuale nella fetta
            insidetextorientation='radial',
            marker=dict(line=dict(color='#ffffff', width=2))
        )
    ])
    
    fig.update_layout(
        title="Distribuzione RDI Non Presi per Reparto",
        width=800, height=400,
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5)
    )
    return fig

# Funzione per generare l'immagine dei grafici

def grafico_to_base64(fig):
    """Converte qualsiasi grafico Plotly in base64 per HTML"""
    img_bytes = fig.to_image(format="png", width=800, height=400)
    img_base64 = base64.b64encode(img_bytes).decode('utf-8')
    return f"data:image/png;base64,{img_base64}"
