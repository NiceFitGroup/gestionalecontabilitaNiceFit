import streamlit as st
import pandas as pd
import sqlite3

conn = sqlite3.connect("database.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS dipendenti (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    cognome TEXT,
    data_inizio TEXT,
    data_fine TEXT,
    tipo_contratto TEXT,
    telefono TEXT,
    email TEXT
)
""")
conn.commit()

def gestisci_dipendenti():
    st.header("Gestione Dipendenti")

    df = pd.read_sql("SELECT * FROM dipendenti", conn)
    st.dataframe(df, use_container_width=True)

    st.subheader("Aggiungi nuovo dipendente")
    nome = st.text_input("Nome")
    cognome = st.text_input("Cognome")
    data_inizio = st.date_input("Data inizio contratto")
    data_fine = st.date_input("Data fine contratto")
    tipo_contratto = st.selectbox("Tipo contratto", ["Determinato", "Indeterminato", "Part-time"])
    telefono = st.text_input("Telefono")
    email = st.text_input("Email")

    if st.button("Salva Dipendente"):
        if nome and cognome:
            c.execute("INSERT INTO dipendenti (nome,cognome,data_inizio,data_fine,tipo_contratto,telefono,email) VALUES (?,?,?,?,?,?,?)",
                      (nome, cognome, str(data_inizio), str(data_fine), tipo_contratto, telefono, email))
            conn.commit()
            st.success("Dipendente aggiunto!")
        else:
            st.error("Compila almeno Nome e Cognome")
