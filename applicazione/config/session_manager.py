import os
import shutil
from typing import Any, Union, Optional
import streamlit.components.v1 as components

import streamlit as st
from pydantic import BaseModel,Field

from applicazione.config import ListaPagine, percorsi
from .state_models import FileUploadState, AppState
from struttura.strutturaResult import Result


class SessionManager:

    def __init__(self, state_key: str = 'app_state'):
        self._state_key = state_key
        if self._state_key not in st.session_state:
            st.session_state[self._state_key] = AppState()

    @property
    def state(self) -> AppState:
        """Fornisce accesso all'oggetto AppState completo con type hinting"""
        return st.session_state[self._state_key]




    def logout(self):
        """Esegue il logout resettando l'intero stato dell'appp"""
        st.session_state[self._state_key] = AppState()
        st.rerun()


    def start_loading(self):
        self.state.page.loading = True

    def stop_loading(self):
        self.state.page.loading = False

    def switch_page(self, page:ListaPagine):
        self.state.page.is_error = False
        self.state.page.show_confirm_modal = False
        self.start_loading()

        if self.state.page.current_page != page:
            self.state.page.flag_pagina = False

        if page == ListaPagine.CARICAMENTO_FILE:
            self.reset_pagina_carica_file()


        self.state.page.current_page = page
        self.state.operazione = None
        st.switch_page(page.page_model.path)


    def nuova_operazione(self, operazione:str):
        self.state.operazione = operazione
        self.start_loading()
        st.rerun()

    def termina_operazione(self, risultato:Optional[Result] = None):
        self.state.operazione = None
        self.state.risultato_operazione = risultato
        self.stop_loading()
        st.rerun()


    def reset_pagina_carica_file(self):
        self.state.files = FileUploadState()


        storage = percorsi.get_storage()
        if os.path.exists(storage):
            try:
                shutil.rmtree(storage)
            except OSError as e:
                print(f"ERRORE DURANTE ELIMINAZIONE STORAGE: {e}")
                return

        os.mkdir(storage)
        with open(os.path.join(storage, 'demo.txt'), 'w') as f:
            f.write('inizializzato')