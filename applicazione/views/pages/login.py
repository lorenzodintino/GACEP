import streamlit as st
from applicazione.config import SessionManager, ListaPagine
from struttura.strutturaResult import Result, display_errore
from struttura.strutturaUtente import UtenteRepository, Utente
from enum import Enum




class PaginaLogin:
    def __init__(self):
        # self.session_manager = SessionManager()
        # self.key = SessionKeys()
        self.session = SessionManager()
        self.session.state.page.current_page = ListaPagine.LOGIN
        self.current_page = self.session.state.page.current_page

        # print(f"sono in: {self.current_page}")


        if self.session.state.user.logged_in and self.current_page == ListaPagine.LOGIN:
            self.session.switch_page(ListaPagine.CARICAMENTO_FILE)


    def check_current_page(self):
        if self.current_page == ListaPagine.LOGIN:
            return True
        return False

    def mostra_form_login(self):

        with st.container(horizontal=True, horizontal_alignment="center"):

            with st.container(horizontal_alignment="center", width=600):

                with st.form("Accedi all'App"):
                    st.subheader("Accedi all'App")
                    username = st.text_input('Username o Email', placeholder="Inserisci il tuo username o la tua email")
                    password = st.text_input("Password", type="password", placeholder="Inserisci la tua password")

                    st.write("")
                    with st.container(horizontal=True, horizontal_alignment="right"):
                        submit = st.form_submit_button('Accedi', type="primary", width=150)

                    if submit:
                        # self.session_manager.start_loading()
                        self.check_login(username, password)

                        repo = UtenteRepository()

                        auth_result = repo.autentica_utente(username, password)

                        utente = auth_result.risultato

                        self.session.state.user.utente_loggato = utente
                        self.session.state.user.logged_in = True
                        # self.session_manager.switch_page(ListaPagine.CARICAMENTO_FILE)
                        self.session.state.page.current_page = ListaPagine.CARICAMENTO_FILE
                        st.rerun()



    def check_login(self, username:str, password:str):
        if username is None or username == '':
            risultato = Result.failure('Inserire un Username o una Email', info='')
            display_errore(risultato)
            return
        if password is None or password == '':
            risultato = Result.failure('Inserire una Password', info='')
            display_errore(risultato)
            return
        return




    def show(self):
        if not self.check_current_page():
            st.rerun()

        self.mostra_form_login()


    def render(self):
        self.show()
        if self.session.state.page.loading:
            self.session.stop_loading()
            st.rerun()


pagina = PaginaLogin()
pagina.render()