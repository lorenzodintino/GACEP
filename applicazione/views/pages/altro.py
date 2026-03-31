import streamlit as st
from applicazione.config import SessionKeys, SessionManager, ListaPagine
from applicazione import App


class PaginaAltro(App):

    def __init__(self):
        super().__init__()

    def show(self):
        st.title("ALTRO")




pagina = PaginaAltro()
pagina.show()