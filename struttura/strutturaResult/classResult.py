from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Any

import streamlit as st
from pydantic import Field


@dataclass
class Result:
    stato: bool = Field(default=True)
    risultato: Optional[Any] = Field(default=None)
    errore: Optional[str] = Field(default=None)
    info: Optional[str] = Field(default=None)
    timestamp: datetime = Field(default_factory=datetime.now)

    @classmethod
    def success(cls, risultato, info=None):
        return cls(stato=True, risultato=risultato, info=info)

    @classmethod
    def failure(cls, errore, info=None):
        return cls(stato=False, errore=errore, info=info)

    def is_success(self) -> bool:
        return self.stato

    def is_failure(self) -> bool:
        return not self.stato


def display_errore(risultato: Result, azione_suggerita:str = ''):
    st.session_state['app_state'].page.is_error = True
    @st.dialog("Errore", width="medium", on_dismiss="ignore")
    def show_error(risultato: Result):
        st.error(risultato.errore)
        if risultato.info is not None:
            with st.expander("Info"):
                st.warning(risultato.info)
                st.write(st.session_state['app_state'].page.is_error)

    if 'loading' in st.session_state and st.session_state['loading']:
        st.session_state['loading'] = False



    # st.rerun()
    show_error(risultato)
    st.stop()

def display_successo(risultato: Result, azione_suggerita:str = ''):
    @st.dialog("Successo", width="medium", on_dismiss="rerun")
    def show_success(risultato: Result):
        st.success(risultato.risultato)
        if risultato.info is not None:
            with st.expander("Info"):
                st.write(risultato.info)

    if 'loading' in st.session_state and st.session_state['loading']:
        st.session_state['loading'] = False

    show_success(risultato)

    st.stop()
