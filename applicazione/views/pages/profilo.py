import time

import streamlit as st
from applicazione.config import SessionKeys, SessionManager,ListaPagine, ColoriCSS


class PaginaProfilo:
    def __init__(self):
        self.css = ColoriCSS()
        self.session_manager = SessionManager()
        self.key = SessionKeys()
        self.current_page = self.session_manager.get(self.key.key_current_page())
        self.utente = self.session_manager.get(self.key.key_utente_loggato())

        self.custom_css()



    def etichetta_basic(self, testo:str ='', bordo:bool = False, key_css = ''):
        with st.container(border=bordo, gap="small", width=200):
            # st.write(f"{label}:")
            # with st.container():
            #     st.write(testo)
            st.text_input("Stato", value=testo, label_visibility="visible", key=f'{key_css}')

    def show(self):
        st.header('PROFILO')


        with st.container(border=False, horizontal_alignment="center"):
            st.subheader("Dati account:")
            with st.container(horizontal=True):
                stato = "ATTIVO" if self.utente.get_stato_attivo else "NON ATTIVO"
                key_css = "utente_stato_success" if self.utente.get_stato_attivo else "utente_stato_error"
                self.etichetta_basic(stato, True, key_css)
        st.warning('prova')
        st.write(self.utente.dati)

    def render(self):
        self.show()
        if self.session_manager.check_loading():
            self.session_manager.stop_loading()
            st.rerun()


    def custom_css(self):
        st.markdown(f"""
        <style>
        
        .st-key-utente_stato_success > div > div input {{
           {self.css.success()}
        }}
        
        .st-key-utente_stato_error > div > div input{{
            {self.css.error()}
        }}
        
        .st-key-utente_stato_warning > div > div input{{
            {self.css.warning()}
        }}
        
        
        
        </style>
        """, unsafe_allow_html=True)







pagina = PaginaProfilo()
pagina.render()