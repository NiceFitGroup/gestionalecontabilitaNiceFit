import streamlit as st
import pandas as pd
import sqlite3
from datetime import date, timedelta

conn = sqlite3.connect("database.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS todo (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    attivita TEXT,
    scadenza TEXT,
    completata INTEGER
)
""")
conn.commit()

def gestisci_todo():
    st.header("To-Do List")
    df = pd.read_sql("SELECT * FROM todo", conn)
    st.dataframe(df, use_container_width=True)

    st.subheader("Aggiungi attività")
    attivita = st.text_input("Attività")
    scadenza = st.date_input("Scadenza", date.today())
    completata = 0

    if st.button("Salva attività"):
        if attivita:
            c.execute("INSERT INTO todo (attivita,scadenza,completata) VALUES (
