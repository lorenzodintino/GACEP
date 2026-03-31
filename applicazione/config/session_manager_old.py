import os
import shutil
from typing import Any, Union
import streamlit.components.v1 as components

import streamlit as st
from pydantic import BaseModel

from applicazione.config import ListaPagine, percorsi


class SessionKeys(BaseModel):

    @staticmethod
    def key_is_error() -> str:
        return 'is error'

    @staticmethod
    def key_loading() -> str:
        return 'loading'

    @staticmethod
    def key_current_page() -> str:
        return 'current_page'

    @staticmethod
    def key_logged_in() -> str:
        return 'logged_in'

    @staticmethod
    def key_utente_loggato() -> str:
        return 'utente_loggato'

    @staticmethod
    def key_file_c1() -> str:
        return 'file_c1'

    @staticmethod
    def key_file_c2() -> str:
        return 'file_c2'

    @staticmethod
    def key_file_c3() -> str:
        return 'file_c3'

    @staticmethod
    def key_pagina_file_corrente() -> str:
        return 'pagina_file_corrente'

    @staticmethod
    def key_upload_c1() -> str:
        return 'upload_c1'

    @staticmethod
    def key_upload_c2() -> str:
        return 'upload_c2'

    @staticmethod
    def key_upload_c3() -> str:
        return 'upload_c3'

    @staticmethod
    def key_operazione() -> str:
        return 'operazione'

    @staticmethod
    def key_risultato_operazione() -> str:
        return 'risultato_operazione'

    @staticmethod
    def key_flag_pagina() -> str:
        return 'flag_pagina'

    @staticmethod
    def key_struttura_selezionata() -> str:
        return 'struttura_selezionata'

    @staticmethod
    def key_anno_selezionato() -> str:
        return 'anno_selezionato'

    @staticmethod
    def key_mese_selezionato() -> str:
        return 'mese_selezionato'


class SessionManager:

    def __init__(self):
        self.key = SessionKeys()
        self.initialize_state()

    # @staticmethod
    def initialize_state(self):
        if self.key.key_is_error() not in st.session_state:
            st.session_state[self.key.key_is_error()] = False

        if self.key.key_loading() not in st.session_state:
            st.session_state[self.key.key_loading()] = False

        if self.key.key_logged_in() not in st.session_state:
            st.session_state[self.key.key_logged_in()] = False

        if self.key.key_utente_loggato() not in st.session_state:
            st.session_state[self.key.key_utente_loggato()] = None

        if self.key.key_current_page() not in st.session_state:
            st.session_state[self.key.key_current_page()] = ListaPagine.CARICAMENTO_FILE

        # ________________________________________________________________________________________________
        if self.key.key_file_c1() not in st.session_state:
            st.session_state[self.key.key_file_c1()] = None
        if self.key.key_file_c2() not in st.session_state:
            st.session_state[self.key.key_file_c2()] = None
        if self.key.key_file_c3() not in st.session_state:
            st.session_state[self.key.key_file_c3()] = None
        if self.key.key_pagina_file_corrente() not in st.session_state:
            st.session_state[self.key.key_pagina_file_corrente()] = 1
        if self.key.key_upload_c1() not in st.session_state:
            st.session_state[self.key.key_upload_c1()] = None
        if self.key.key_upload_c2() not in st.session_state:
            st.session_state[self.key.key_upload_c2()] = None
        if self.key.key_upload_c3() not in st.session_state:
            st.session_state[self.key.key_upload_c3()] = None
        if self.key.key_operazione() not in st.session_state:
            st.session_state[self.key.key_operazione()] = None
        if self.key.key_risultato_operazione() not in st.session_state:
            st.session_state[self.key.key_risultato_operazione()] = None
        if self.key.key_flag_pagina() not in st.session_state:
            st.session_state[self.key.key_flag_pagina()] = False
        if self.key.key_struttura_selezionata() not in st.session_state:
            st.session_state[self.key.key_struttura_selezionata()] = None
        if self.key.key_anno_selezionato() not in st.session_state:
            st.session_state[self.key.key_anno_selezionato()] = None
        if self.key.key_mese_selezionato() not in st.session_state:
            st.session_state[self.key.key_mese_selezionato()] = None

    @staticmethod
    def get( key: Union[str, SessionKeys], default: Any = None):
        # if key == self.key.key_risultato_operazione():
        #     risultato = st.session_state.get(key, default)
        #     st.session_state[key] = None
        #     return risultato

        risultato = st.session_state.get(key, default)
        return risultato

    @staticmethod
    def set(key: Union[str, SessionKeys], value: Any):
        st.session_state[key] = value

    @staticmethod
    def delete(key: Union[str, SessionKeys]):
        if key in st.session_state:
            del st.session_state[key]

    @staticmethod
    def check(key: Union[str, SessionKeys]):
        if key in st.session_state:
            if st.session_state[key] is not None:
                return True
        return False

    @property
    def session(self):
        return st.session_state

    # @property
    def logout(self):
        for k in st.session_state:
            self.delete(k)
        self.initialize_state()

    def check_loading(self):
        return self.get(self.key.key_loading())

    # @property
    def start_loading(self):
        self.set(self.key.key_loading(), True)

    # @property
    def stop_loading(self):
        self.set(self.key.key_loading(), False)

    def switch_page(self, page: ListaPagine):
        self.set(self.key.key_is_error(), False)
        self.start_loading()
        if self.get(self.key.key_current_page()) != page:
            self.set(self.key.key_flag_pagina(), False)

        if page == ListaPagine.CARICAMENTO_FILE:
            self.reset_pagina_carica_file()

        # print(f"pagina attuale: {self.get(self.key.key_current_page())}")
        self.set(self.key.key_current_page(), page)
        self.set(self.key.key_operazione(), None)
        # print(f"switch a: {self.get(self.key.key_current_page())}")
        st.switch_page(page.page_model.path)
        # st.rerun()

    def nuova_operazione(self, operazione: str):
        self.set(self.key.key_operazione(), operazione)
        self.start_loading()
        st.rerun()

    def termina_operazione(self):
        self.set(self.key.key_operazione(), None)
        self.stop_loading()
        st.rerun()

    def reset_pagina_carica_file(self):
        self.set(self.key.key_file_c1(), None)
        self.set(self.key.key_file_c2(), None)
        self.set(self.key.key_file_c3(), None)

        self.set(self.key.key_upload_c1(), None)
        self.set(self.key.key_upload_c2(), None)
        self.set(self.key.key_upload_c3(), None)

        self.set(self.key.key_struttura_selezionata(), None)
        self.set(self.key.key_anno_selezionato(), None)
        self.set(self.key.key_mese_selezionato(), None)

        storage = percorsi.get_storage()
        if os.path.exists(storage):
            try:
                # os.remove(storage)
                shutil.rmtree(storage)
                # print(f"✔️ File '{storage}' esistente eliminato con successo.")
            except OSError as e:
                # print(f"❌ Errore durante l'eliminazione del file: {e}")
                return

        os.mkdir(storage)
        with open(f"{storage}demo.txt", "w") as f:
            f.write("")

        # print(f"✔️ File '{storage}demo.txt' creato con successo.")


    def loading_on(self, element_id:str = 'contenitore-loading', class_name:str = 'd-none'):
        js_code = f"""
        <script>
            var element = document.getElementById("{element_id}");
            if (element) {{
                element.classList.remove("{class_name}");
            }}
            console.log("ON");
        </script>
        """

        components.html(js_code, height=0)


    def loading_off(self, element_id: str = 'contenitore-loading', class_name: str = 'd-none'):
        js_code = f"""
        <script>
            var element = document.getElementById("{element_id}");
            if (element) {{
                element.classList.add("{class_name}");
            }}
            console.log("OFF");
        </script>
        """

        components.html(js_code, height=0)
