
from pathlib import Path

import streamlit as st

from applicazione import App
from applicazione.config import ListaPagine
from applicazione.config import percorsi
from struttura.strutturaResult import Result, display_errore, display_successo
                    
class Pagina_storico_caricamenti(App):

    def __init__(self):
        super().__init__()

    def show(self):
        st.header("Storico caricamenti su DataBase")

        tab_1, tab_2, tab_3 = st.tabs(["File C1", "File C2", "File C3"])
        with tab_1:
            pass
        with tab_2:
            pass
        with tab_3:
            pass

    def render(self):
        self.show()
                    
pagina = Pagina_storico_caricamenti()
pagina.show()
                    