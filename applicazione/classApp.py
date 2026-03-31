import streamlit as st

from applicazione.config import SessionManager, ListaPagine
from applicazione.utils import PageManager, OperazioniRouter, OperazioneDB


class App:

    def __init__(self):

        self.session = SessionManager()

        self.current_page: ListaPagine = self.session.state.page.current_page

        self.page_manager = PageManager()

        self.is_loading = self.session.state.page.loading

        self.primary_color = st.get_option("theme.primaryColor")

        self.check_operazione = OperazioniRouter()

        self.operazione_db = OperazioneDB()

        self.logo = './static/logo/logo-asl.png'

        st.logo(self.logo, icon_image=self.logo, size="large")

        st.markdown("""
                <style>



                header[data-testid="stHeader"] {
                    height: auto !important;

                }

                div[data-testid="stSidebarContent"] > div[data-testid="stSidebarNav"]{
                    margin-top:4rem !important;
                }

                img[data-testid="stSidebarLogo"] {
                    height: 6rem !important;
                    margin-top:4rem;
                }
                img[data-testid="stHeaderLogo"] {
                   height: 5rem !important;

                }

                </style>
                """, unsafe_allow_html=True)


    def run(self):
        with st.spinner('Caricamento...'):

            st.set_page_config(
                # page_title=,
                layout='wide',
            )


            self.check_operazione.check_operazione()

            lista_pagine = self.page_manager.crea_st_list_pages()


            pg = st.navigation(lista_pagine, position="sidebar")



            if self.current_page.page_model.title != pg.title:
                self.session.switch_page(ListaPagine.get_page_by_title(pg.title))


            is_logged_in = self.session.state.user.logged_in

            if not is_logged_in:
                if ListaPagine.get_page_by_title(pg.title).richiede_login:
                    st.switch_page(ListaPagine.LOGIN.page_model.path)
            else:
                if self.current_page == ListaPagine.LOGIN:
                    self.session.switch_page(ListaPagine.LOGIN)
                    st.switch_page(ListaPagine.CARICAMENTO_FILE.page_model.path)


            pg.run()



        # with st.expander('SESSION'):
        #     st.json(self.session.state)
        # with st.expander('C1'):
        #     st.write(self.session.state.files.file_c1)
