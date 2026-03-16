# report_odl/html_report.py
import pandas as pd
import matplotlib.pyplot as plt
import base64
from io import BytesIO

def build_html(tecnico, df_tecnico):
    """
    Costruisce la pagina HTML del report per un singolo tecnico, includendo:
    - Tabelle degli ODL filtrati
    - Grafici a torta e a barre in formato base64
    - KPI principali (ODL in corso, sospesi, da fare)

    Parametri:
        tecnico (str): nome del tecnico destinatario
        df_tecnico (pd.DataFrame): DataFrame contenente solo gli ODL del tecnico

    Ritorna:
        str: stringa HTML completa pronta per invio via email o visualizzazione
    """

    # 1️⃣ Calcolo KPI principali
    num_in_corso = (df_tecnico['stato odl'] == 'IN CORSO').sum()
    num_sospesi = (df_tecnico['stato odl'] == 'SOSPESO').sum()
    num_da_fare = (df_tecnico['stato odl'] == 'DA FARE').sum()

    # 2️⃣ Generazione grafico a torta (stato ODL)
    fig1, ax1 = plt.subplots()
    ax1.pie(
        [num_in_corso, num_sospesi, num_da_fare],
        labels=['IN CORSO', 'SOSPESO', 'DA FARE'],
        autopct='%1.1f%%',
        colors=['#4CAF50', '#FF9800', '#F44336']
    )
    ax1.set_title('Distribuzione ODL per stato odl')

    # Salvataggio grafico in memoria come base64
    buffer1 = BytesIO()
    plt.savefig(buffer1, format='png', bbox_inches='tight')
    buffer1.seek(0)
    img_pie = base64.b64encode(buffer1.getvalue()).decode()
    plt.close(fig1)  # chiude il grafico per non sovraccaricare la memoria

    # 3️⃣ Generazione grafico a barre (giorni trascorsi)
    fig2, ax2 = plt.subplots()
    df_tecnico['giorni_trascorsi'].plot(kind='bar', ax=ax2, color='#2196F3')
    ax2.set_xlabel('ODL')
    ax2.set_ylabel('Giorni trascorsi')
    ax2.set_title('Giorni trascorsi dall\'apertura degli ODL')

    # Salvataggio grafico in memoria come base64
    buffer2 = BytesIO()
    plt.savefig(buffer2, format='png', bbox_inches='tight')
    buffer2.seek(0)
    img_bar = base64.b64encode(buffer2.getvalue()).decode()
    plt.close(fig2)

    # 4️⃣ Generazione tabella HTML
    # Manteniamo solo le colonne principali
    df_tabella = df_tecnico[['id_odl', 'tecnico', 'stato', 'DT_APERTURA', 'giorni_trascorsi']]
    tabella_html = df_tabella.to_html(index=False, classes='table table-striped')

    # 5️⃣ Creazione della stringa HTML finale
    html = f"""
    <html>
        <head>
            <style>
                .table {{border-collapse: collapse; width: 100%;}}
                .table th, .table td {{border: 1px solid #ddd; padding: 8px; text-align: left;}}
                .table th {{background-color: #f2f2f2;}}
            </style>
        </head>
        <body>
            <h2>Report ODL - {tecnico}</h2>
            <p><strong>ODL in corso:</strong> {num_in_corso} |
               <strong>ODL sospesi:</strong> {num_sospesi} |
               <strong>ODL da fare:</strong> {num_da_fare}</p>

            <h3>Grafico Stato ODL</h3>
            <img src="data:image/png;base64,{img_pie}" />

            <h3>Giorni trascorsi dall'apertura</h3>
            <img src="data:image/png;base64,{img_bar}" />

            <h3>Dettaglio ODL</h3>
            {tabella_html}
        </body>
    </html>
    """
    return html
