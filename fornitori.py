import streamlit as st
import pandas as pd
import sqlite3

conn = sqlite3.connect("database.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS fornitori (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_azienda TEXT,
    partita_iva TEXT,
    indirizzo TEXT,
    email TEXT,
    telefono TEXT,
    persona_riferimento TEXT
)
""")
conn.commit()

def gestisci_fornitori():
    st.header("Gestione Fornitori")
    df = pd.read_sql("SELECT * FROM fornitori", conn)
    st.dataframe(df, use_container_width=True)

    st.subheader("Aggiungi nuovo fornitore")
    nome_azienda = st.text_input("Nome Azienda")
    partita_iva = st.text_input("Partita IVA")
    indirizzo = st.text_input("Indirizzo")
    email = st.text_input("Email")
    telefono = st.text_input("Telefono")
    persona_riferimento = st.text_input("Persona di riferimento")

    if st.button("Salva Fornitore"):
        if nome_azienda:
            c.execute("INSERT INTO fornitori (nome_azienda,partita_iva,indirizzo,email,telefono,persona_riferimento) VALUES (?,?,?,?,?,?)",
                      (nome_azienda, partita_iva, indirizzo, email, telefono, persona_riferimento))
            conn.commit()
            st.success("Fornitore aggiunto!")
        else:
            st.error("Inserisci almeno il nome dell'azienda")
