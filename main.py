import streamlit as st
from dipendenti import gestisci_dipendenti
from fornitori import gestisci_fornitori
from contabilita import gestisci_contabilita
from appuntamenti import gestisci_appuntamenti
from todo import gestisci_todo

def main():
    st.set_page_config(page_title="Gestionale Aziendale", layout="wide")
    st.title("Gestionale Aziendale")

    menu = ["Dashboard", "Dipendenti", "Buste Paga", "Fornitori", "Contabilità", "Appuntamenti", "To-Do List"]
    choice = st.sidebar.selectbox("Sezioni", menu)

    if choice == "Dashboard":
        st.header("Dashboard riepilogativa")
        st.info("Qui sarà visualizzato il riepilogo dei dati principali")
    elif choice == "Dipendenti":
        gestisci_dipendenti()
    elif choice == "Buste Paga":
        st.info("Modulo Buste Paga in sviluppo")
    elif choice == "Fornitori":
        gestisci_fornitori()
    elif choice == "Contabilità":
        gestisci_contabilita()
    elif choice == "Appuntamenti":
        gestisci_appuntamenti()
    elif choice == "To-Do List":
        gestisci_todo()

if __name__ == "__main__":
    main()
