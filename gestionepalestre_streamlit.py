import streamlit as st
import pandas as pd
import sqlite3
from datetime import date, timedelta
import matplotlib.pyplot as plt

# -------------------------------
# Configurazione pagina
# -------------------------------
st.set_page_config(page_title="Gestionale Contabile Palestre", layout="wide")

# -------------------------------
# Colori palestre
# -------------------------------
PALESTRE_COLORI = {
    "NEXUS": "#9EC9FF",      # blu chiaro
    "ELISIR": "#E8D9C0",     # beige
    "YOUNIQUE": "#D9B3FF",   # viola chiaro
    "AVENUE": "#A6DAD9"      # azzurro ottanio
}

# -------------------------------
# Connessione e creazione database
# -------------------------------
conn = sqlite3.connect("contabilita_palestre.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS transazioni (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data TEXT,
    descrizione TEXT,
    importo REAL,
    tipo TEXT,
    stato TEXT,
    fornitore_cliente TEXT,
    palestra TEXT
)
""")
conn.commit()

# -------------------------------
# Funzioni per database
# -------------------------------
def aggiungi_transazione(data, descrizione, importo, tipo, stato, fornitore_cliente, palestra):
    c.execute("""
    INSERT INTO transazioni (data, descrizione, importo, tipo, stato, fornitore_cliente, palestra)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (data, descrizione, importo, tipo, stato, fornitore_cliente, palestra))
    conn.commit()

def leggi_transazioni():
    df = pd.read_sql("SELECT * FROM transazioni ORDER BY data DESC", conn)
    return df

def elimina_transazione(id_):
    c.execute("DELETE FROM transazioni WHERE id = ?", (id_,))
    conn.commit()

# -------------------------------
# Interfaccia utente
# -------------------------------
st.title("Gestionale Contabile Palestre")
st.markdown("Versione web - Beatrice Ronconi")

tab1, tab2, tab3 = st.tabs(["Nuova registrazione", "Storico e filtri", "Riepilogo contabile"])

# -------------------------------
# TAB 1 - Inserimento dati
# -------------------------------
with tab1:
    st.header("Inserisci una nuova transazione")
    col1, col2, col3 = st.columns(3)
    with col1:
        data = st.date_input("Data", date.today())
        tipo = st.selectbox("Tipo", ["Fattura Fornitore", "Incasso", "Pagamento"])
        stato = st.selectbox("Stato", ["Pagato", "Non Pagato"])
    with col2:
        descrizione = st.text_input("Descrizione")
        importo = st.number_input("Importo (€)", min_value=0.0, step=0.01)
    with col3:
        if tipo == "Incasso":
            fornitore_cliente = st.text_input("Cliente")
        else:
            fornitore_cliente = st.text_input("Fornitore")
        palestra = st.selectbox("Palestra", list(PALESTRE_COLORI.keys()))

    if st.button("Salva transazione"):
        if descrizione and importo > 0 and fornitore_cliente:
            aggiungi_transazione(str(data), descrizione, importo, tipo, stato, fornitore_cliente, palestra)
            st.success("Transazione salvata con successo!")
        else:
            st.error("Compila tutti i campi obbligatori.")

# -------------------------------
# TAB 2 - Storico e filtri
# -------------------------------
with tab2:
    st.header("Storico delle transazioni")
    df = leggi_transazioni()

    if not df.empty:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            filtro_tipo = st.selectbox("Filtra per tipo", ["Tutti"] + df["tipo"].unique().tolist())
        with col2:
            filtro_stato = st.selectbox("Filtra per stato", ["Tutti"] + df["stato"].unique().tolist())
        with col3:
            filtro_palestra = st.selectbox("Filtra per palestra", ["Tutte"] + list(PALESTRE_COLORI.keys()))
        with col4:
            intervallo = st.selectbox("Periodo", ["Tutti", "Ultimi 30 giorni", "Ultimo trimestre"])

        df_filtrato = df.copy()
        if filtro_tipo != "Tutti":
            df_filtrato = df_filtrato[df_filtrato["tipo"] == filtro_tipo]
        if filtro_stato != "Tutti":
            df_filtrato = df_filtrato[df_filtrato["stato"] == filtro_stato]
        if filtro_palestra != "Tutte":
            df_filtrato = df_filtrato[df_filtrato["palestra"] == filtro_palestra]
        if intervallo != "Tutti":
            oggi = date.today()
            if intervallo == "Ultimi 30 giorni":
                limite = oggi - timedelta(days=30)
            elif intervallo == "Ultimo trimestre":
                limite = oggi - timedelta(days=90)
            df_filtrato = df_filtrato[pd.to_datetime(df_filtrato["data"]) >= pd.Timestamp(limite)]

        st.dataframe(df_filtrato, use_container_width=True)

        st.subheader("Elimina una transazione")
        id_da_eliminare = st.number_input("ID transazione", min_value=1, step=1)
        if st.button("Elimina transazione"):
            elimina_transazione(id_da_eliminare)
            st.success("Transazione eliminata con successo")
    else:
        st.info("Nessuna transazione presente. Inserisci una nuova registrazione nel tab precedente.")

# -------------------------------
# TAB 3 - Riepilogo contabile
# -------------------------------
with tab3:
    st.header("Riepilogo contabile")
    df = leggi_transazioni()

    if not df.empty:
        tot_incassi = df[df["tipo"] == "Incasso"]["importo"].sum()
        tot_pagamenti = df[df["tipo"].isin(["Fattura Fornitore", "Pagamento"])]["importo"].sum()
        saldo = tot_incassi - tot_pagamenti

        col1, col2, col3 = st.columns(3)
        col1.metric("Totale Incassi", f"€ {tot_incassi:,.2f}")
        col2.metric("Totale Pagamenti", f"€ {tot_pagamenti:,.2f}")
        col3.metric("Saldo Attuale", f"€ {saldo:,.2f}")

        st.subheader("Andamento incassi e pagamenti")
        df["data"] = pd.to_datetime(df["data"])
        incassi = df[df["tipo"] == "Incasso"].groupby("data")["importo"].sum()
        pagamenti = df[df["tipo"].isin(["Fattura Fornitore", "Pagamento"])].groupby("data")["importo"].sum()

        fig, ax = plt.subplots()
        ax.plot(incassi.index, incassi.values, label="Incassi", color="green")
        ax.plot(pagamenti.index, pagamenti.values, label="Pagamenti", color="red")
        ax.set_xlabel("Data")
        ax.set_ylabel("Importo (€)")
        ax.legend()
        st.pyplot(fig)
    else:
        st.info("Non ci sono dati per il riepilogo.")
