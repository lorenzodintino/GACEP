
import streamlit as st
from applicazione.config import SessionKeys, SessionManager, ListaPagine
from applicazione import App
                    
class Pagina_nuova(App):

    def __init__(self):
        super().__init__()

    def show(self):
        st.title("nuova")
                    
pagina = Pagina_nuova()
pagina.show()
                    