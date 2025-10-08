import streamlit as st
import pandas as pd
import sqlite3
from datetime import date

conn = sqlite3.connect("database.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS contabilita (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data TEXT,
    tipo TEXT,
    descrizione TEXT,
    importo REAL,
    stato TEXT,
    fornitore_cliente TEXT
)
""")
conn.commit()

def gestisci_contabilita():
    st.header("Contabilità")

    df = pd.read_sql("SELECT * FROM contabilita", conn)
    st.dataframe(df, use_container_width=True)

    st.subheader("Aggiungi transazione")
    data = st.date_input("Data", date.today())
    tipo = st.selectbox("Tipo", ["Fattura Fornitore", "Incasso", "Pagamento"])
    descrizione = st.text_input("Descrizione")
    importo = st.number_input("Importo", min_value=0.0)
    stato = st.selectbox("Stato", ["Pagato", "Non Pagato"])
    fornitore_cliente = st.text_input("Fornitore/Cliente")

    if st.button("Salva transazione"):
        if descrizione and importo>0:
            c.execute("INSERT INTO contabilita (data,tipo,descrizione,importo,stato,fornitore_cliente) VALUES (?,?,?,?,?,?)",
                      (str(data), tipo, descrizione, importo, stato, fornitore_cliente))
            conn.commit()
            st.success("Transazione salvata!")
        else:
            st.error("Compila tutti i campi obbligatori")
