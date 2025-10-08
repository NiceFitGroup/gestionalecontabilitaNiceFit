import streamlit as st
import pandas as pd
import sqlite3
from datetime import date, timedelta
import matplotlib.pyplot as plt

# -------------------------------
# CONFIGURAZIONE APP
# -------------------------------
st.set_page_config(page_title="Gestionale Palestre", page_icon="💼", layout="wide")

# Colori per palestra
PALESTRE = {
    "NEXUS": "#cce0ff",       # blu chiaro
    "ELISIR": "#f5f5dc",      # beige chiaro
    "YOUNIQUE": "#e6ccff",    # viola chiaro
    "AVENUE": "#a7dcd1",      # azzurro ottanio chiaro
}

# Connessione DB
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
# FUNZIONI DI SUPPORTO
# -------------------------------
def inserisci_transazione(data, descrizione, importo, tipo, stato, fornitore_cliente, palestra):
    c.execute("INSERT INTO transazioni (data, descrizione, importo, tipo, stato, fornitore_cliente, palestra) VALUES (?, ?, ?, ?, ?, ?, ?)",
              (data, descrizione, importo, tipo, stato, fornitore_cliente, palestra))
    conn.commit()

def carica_transazioni():
    df = pd.read_sql_query("SELECT * FROM transazioni", conn)
    return df

def elimina_transazione(id_):
    c.execute("DELETE FROM transazioni WHERE id = ?", (id_,))
    conn.commit()

def aggiorna_transazione(id_, stato_nuovo):
    c.execute("UPDATE transazioni SET stato = ? WHERE id = ?", (stato_nuovo, id_))
    conn.commit()

# -------------------------------
# INTERFACCIA GRAFICA
# -------------------------------
st.title("Gestionale Contabile Palestre")
st.markdown("#### by Beatrice Ronconi — Consulenza & Gestione Palestre")
�
