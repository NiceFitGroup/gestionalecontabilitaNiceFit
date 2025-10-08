import streamlit as st
import pandas as pd
import sqlite3
from datetime import date

conn = sqlite3.connect("database.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS appuntamenti (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data TEXT,
    ora TEXT,
    titolo TEXT,
    descrizione TEXT
)
""")
conn.commit()

def gestisci_appuntamenti():
    st.header("Calendario Appuntamenti")
    df = pd.read_sql("SELECT * FROM appuntamenti ORDER BY data", conn)
    st.dataframe(df, use_container_width=True)

    st.subheader("Aggiungi appuntamento")
    data = st.date_input("Data", date.today())
    ora = st.text_input("Ora (HH:MM)")
    titolo = st.text_input("Titolo")
    descrizione = st.text_area("Descrizione")

    if st.button("Salva appuntamento"):
        if titolo:
            c.execute("INSERT INTO appuntamenti (data,ora,titolo,descrizione) VALUES (?,?,?,?)",
                      (str(data), ora, titolo, descrizione))
            conn.commit()
            st.success("Appuntamento salvato!")
        else:
            st.error("Inserisci il titolo")
