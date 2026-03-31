import os
import shutil
from typing import Any, Union, Optional
import streamlit.components.v1 as components
from struttura.strutturaUtente import Utente
from struttura.strutturaC1 import FileC1
from struttura.strutturaC2 import FileC2
from struttura.strutturaC3 import FileC3
from struttura.strutturaResult import Result

import streamlit as st
from pydantic import BaseModel, Field, ConfigDict

from applicazione.config import ListaPagine, percorsi


class UserState(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)


    logged_in: bool = False
    utente_loggato: Optional[Utente] = None


class PageState(BaseModel):

    # model_config = ConfigDict(arbitrary_types_allowed=True)



    current_page: ListaPagine = ListaPagine.CARICAMENTO_FILE
    loading: bool = False
    is_error: bool = False
    flag_pagina: bool = False

    show_confirm_modal:bool = False


class FileUploadState(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)



    file_c1: Optional[FileC1] = None
    file_c2: Optional[FileC2] = None
    file_c3: Optional[FileC3] = None
    upload_c1: Optional[Any] = None
    upload_c2: Optional[Any] = None
    upload_c3: Optional[Any] = None
    pagina_corrente_file_c1: Optional[int] = None
    pagina_corrente_file_c2: Optional[int] = None
    pagina_corrente_file_c3: Optional[int] = None
    codice_struttura_selezionata: Optional[str] = None
    nome_struttura_selezionata: Optional[str] = None
    codice_prestazione_selezionata: Optional[str] = None
    nome_prestazione_selezionata: Optional[str] = None
    anno_selezionato: Optional[str] = None
    mese_selezionato: Optional[str] = None
    upload_su_database: Optional[bool] = False


class AppState(BaseModel):
    user: UserState = Field(default_factory=UserState)
    page: PageState = Field(default_factory=PageState)
    files: FileUploadState = Field(default_factory=FileUploadState)

    operazione: Optional[str] = None
    risultato_operazione: Optional[Result] = None