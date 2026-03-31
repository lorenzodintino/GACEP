import streamlit as st
from applicazione import App

# from applicazione.config import SessionKeys,SessionManager,ListaPagine
from applicazione.config import SessionManager


class PaginaLogout(App):
    def __init__(self):
        super().__init__()
        self.session.logout()

        # self.session_manager = SessionManager()
        # self.key = SessionKeys()
        # self.session_manager.set(self.key.key_current_page(), ListaPagine.LOGOUT)
        # self.current_page = self.session_manager.get(self.key.key_current_page())
        #
        # if self.session_manager.get(self.key.key_logged_in()):
        #     self.session_manager.logout()
        #     st.rerun()
        #     # self.session_manager.switch_page(ListaPagine.LOGIN)



    def show(self):
        st.write('LOGOUT')


pagina = PaginaLogout()
pagina.show()