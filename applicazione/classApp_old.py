import streamlit as st

from applicazione.config import SessionKeys, SessionManager, ListaPagine
from applicazione.utils import PageManager, OperazioniRouter, OperazioneDB


class App:

    def __init__(self):
        self.session_manager = SessionManager()

        self.session_manager.initialize_state()
        self.key = SessionKeys()

        self.current_page: ListaPagine = self.session_manager.get(self.key.key_current_page())

        self.page_manager = PageManager()

        self.is_loading = self.session_manager.get(self.key.key_loading())

        self.primary_color = st.get_option("theme.primaryColor")
        self.overlay_color = "rgba(255,255,255,0.5)" if st.get_option("theme.base") == "light" else "rgba(0,0,0,0.5)"

        self.check_operazione = OperazioniRouter()

        self.operazione_db = OperazioneDB()

        self.logo = './static/logo/logo-asl.png'

        st.logo(self.logo, icon_image=self.logo, size="large")
        # st.image(self.logo, caption="logo asl pescara")

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

        st.set_page_config(
            layout="wide"
        )

        self.overlay_css = f"""
                <style>
                .overlay {{
                    position:fixed;
                    top:0;
                    left:0;
                    width:100vw;
                    height:100vh;
                    background-color:{self.overlay_color};
                    z-index:9999;
                    cursor:wait;
                    display: flex;
                    justify-content:center;
                    align-items:center;
                }}
                
                
                .loader {{
                  width: 48px;
                  height: 48px;
                  border-radius: 50%;
                  display: inline-block;
                  border-top: 3px solid {self.primary_color};
                  border-right: 3px solid transparent;
                  box-sizing: border-box;
                  animation: rotation 1s linear infinite;
                }}
                
                @keyframes rotation {{
                  0% {{
                    transform: rotate(0deg);
                  }}
                  100% {{
                    transform: rotate(360deg);
                  }}
                }} 
                
                
                .d-none{{
                    display:none;
                }}
                </style>
                """

        self.overlay_html = """
        <div id="contenitore-loading" class="d-none">
            <div class="overlay">
                <span class="loader"></span>
            </div>
        </div>
        """

    def mostra_loading(self):
        # if self.is_loading:
        if True:
            # print('caricamento si')
            st.markdown(self.overlay_css, unsafe_allow_html=True)
            st.markdown(self.overlay_html, unsafe_allow_html=True)
        # print('caricamento no')

    def check_page(self, pagina: ListaPagine):
        if self.current_page == pagina:
            print('sono nella pagina giusta')
        else:
            print('sono nella pagina sbagliata')

    def run(self):
        # print('\n\n')
        self.mostra_loading()

        self.check_operazione.check_operazione()

        lista_pagine = self.page_manager.crea_st_list_pages()

        # st.write(lista_pagine)

        pg = st.navigation(lista_pagine, position="sidebar")

        # print(f"pg: {pg}")
        # print(f"-"*30)
        # print(f"self.current_page: {self.current_page}")
        # print(f"-"*30)
        #
        # print(f"pg.title: {pg.title}")
        # print(f"self.current_page.page_model.title: {self.current_page.page_model.title}")

        if self.current_page.page_model.title != pg.title:
            self.session_manager.switch_page(ListaPagine.get_page_by_title(pg.title))
            # print(f"devo cambiare pagina da {pg.title} a {self.current_page.page_model.title}")
            # self.session_manager.switch_page(ListaPagine.get_page_by_title(pg.title))
            # st.switch_page(self.current_page.page_model.path)
            # st.rerun()

        is_logged_in = self.session_manager.get(self.key.key_logged_in())

        if not is_logged_in:
            if ListaPagine.get_page_by_title(pg.title).richiede_login:
                st.switch_page(ListaPagine.LOGIN.page_model.path)
        else:
            if self.current_page == ListaPagine.LOGIN:
                self.session_manager.switch_page(ListaPagine.LOGIN)
                st.switch_page(ListaPagine.CARICAMENTO_FILE.page_model.path)

        # st.write(pg.title)
        # if not self.is_loading:
        pg.run()

        # if self.is_loading:
        #     self.session_manager.stop_loading()
        #     st.rerun()

        with st.expander('SESSION'):
            st.json(self.session_manager.session)
