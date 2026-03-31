from enum import Enum

import streamlit as st
from pydantic import BaseModel, Field, field_validator

from applicazione.config import percorsi
from struttura.strutturaUtente import Ruolo


class PageModel(BaseModel):
    path: str = Field(...)
    title: str = Field(...)

    # icon: Optional[str] = Field(default=None)

    @field_validator("path")
    @classmethod
    def add_base_path(cls, valore_fornito: str) -> str:
        base_path = percorsi.get_pages()
        full_path = base_path + valore_fornito
        return full_path.replace('\\', '/')

    def crea_st_page(self):
        return st.Page(self.path, title=self.title)


class GruppiPagine(Enum):
    SERVIZI = "Servizi"
    PROFILO = "Profilo"
    CONFIG = "Config"
    ALTRO = "Altro"
    LOGOUT = 'Esci'


class ListaPagine(Enum):
    LOGIN = (GruppiPagine.PROFILO, PageModel(path="login.py", title="Pagina Login"), False, [])
    CONFIG = (GruppiPagine.CONFIG, PageModel(path="configurazione.py", title="Configurazione"), True, [Ruolo.SUPERADMIN])

    # ESEGUI_OPERAZIONE = (GruppiPagine.ALTRO,PageModel(path='esegui_operazione.py', title='Esegui Operazione'), True, [])
    CARICAMENTO_FILE = (GruppiPagine.SERVIZI, PageModel(path="carica_file.py", title="Caricamento File"), True, [])
    CONTROLLO_FILE = (GruppiPagine.SERVIZI, PageModel(path="controllo_file.py", title="Controllo File"), True, [])
    STORICO_CARICAMENTI = (GruppiPagine.SERVIZI, PageModel(path="storico_caricamenti.py", title="Storico Caricamenti"), True,[])
    PROFILO = (GruppiPagine.PROFILO, PageModel(path='profilo.py', title="Il mio Profilo"), True, [])
    # ALTRO = (GruppiPagine.SERVIZI, PageModel(path='altro.py', title='Pagina Altro'), True, [Ruolo.SUPERADMIN])

    LOGOUT = (GruppiPagine.LOGOUT, PageModel(path='logout.py', title='Logout'), True, [])

    # DEMO = (categoria della pagina, modello pagina, se bisogna essere loggati per vederla, ruolo utente che puo vederla: [] = tutti oppure [Ruolo.1, Ruolo.2] = solo chi puo vedere)

    @property
    def gruppo(self):
        return self.value[0]

    @property
    def page_model(self):
        return self.value[1]

    @property
    def richiede_login(self):
        return self.value[2]

    @property
    def ruoli_consentiti(self):
        return self.value[3]

    def crea_st_page(self):
        return self.page_model.crea_st_page()


    @classmethod
    def get_page_by_title(cls, titolo:str):
        titolo_da_cercare_lower = titolo.lower()

        for page_enum in cls:
            if page_enum.page_model.title.lower() == titolo_da_cercare_lower:
                return page_enum

        return None




