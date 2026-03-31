from typing import List, Dict
import streamlit as st
from streamlit.runtime.scriptrunner import get_script_run_ctx
from applicazione.config import SessionManager, ListaPagine, GruppiPagine
from pathlib import Path

class PageManager:
    def __init__(self):
        # self.session_manager = SessionManager()
        # self.key = SessionKeys()

        self.session = SessionManager()


        # self.pages: Dict[str, List[PageModel]] = {}
        self.pages: Dict[GruppiPagine, List[ListaPagine]] = {}

        for p in ListaPagine:
            # print(p.value[1].path)
            percorsoFile = Path(p.value[1].path)

            self.check_file_pagine(percorsoFile)

            self.add_page_condizione(p)


    def check_file_pagine(self, percorsoFile: Path):
        if not percorsoFile.exists():
            percorsoFile.parent.mkdir(parents=True, exist_ok=True)

            self.scrivi_file_pagina(percorsoFile)


    def add_page_condizione(self, pagina: ListaPagine):

        is_logged_in = self.session.state.user.logged_in
        # ruolo = self.session_manager.get(self.key.key_utente_loggato()).ruolo if is_logged_in else None
        ruolo = self.session.state.user.utente_loggato.get_ruolo if is_logged_in else None

        # categoria = pagina.value[0]
        # # page_model = pagina.value[1]
        # richiede_login = pagina.value[2]
        # per_ruolo = pagina.value[3]

        if is_logged_in and pagina.richiede_login:
            if not pagina.ruoli_consentiti:
                self._add_page_to_category(pagina.gruppo, pagina)
            elif ruolo in pagina.ruoli_consentiti:
                self._add_page_to_category(pagina.gruppo, pagina)

        elif not is_logged_in and not pagina.richiede_login:
            self._add_page_to_category(pagina.gruppo, pagina)

    def _add_page_to_category(self, categoria: GruppiPagine, pagina_enum: ListaPagine):
        if categoria not in self.pages:
            self.pages[categoria] = []
        self.pages[categoria].append(pagina_enum)

    def crea_st_list_pages(self):
        streamlit_pages = {}
        for categoria, page_models in self.pages.items():
            streamlit_pages[categoria.value] = [pm.crea_st_page() for pm in page_models]


        # print(streamlit_pages)
        return streamlit_pages



    def scrivi_file_pagina(self, percorsoFile:Path):

        nomeFile = percorsoFile.stem

        importazioni = """
from pathlib import Path

import streamlit as st

from applicazione import App
from applicazione.config import ListaPagine
from applicazione.config import percorsi
from struttura.strutturaResult import Result, display_errore, display_successo
                    """

        classePagina = f"""
class Pagina_{nomeFile}(App):

    def __init__(self):
        super().__init__()

    def show(self):
        st.header("{nomeFile}")
        
    def render(self):
        self.show()
                    """

        eseguiPagina = f"""
pagina = Pagina_{nomeFile}()
pagina.show()
                    """

        with percorsoFile.open("w", encoding='utf-8') as f:
            f.write(importazioni)
            f.write(classePagina)
            f.write((eseguiPagina))