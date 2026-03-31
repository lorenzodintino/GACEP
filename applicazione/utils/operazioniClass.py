import time
from pathlib import Path

import streamlit as st

from applicazione.config import SessionManager, ListaPagine, percorsi
from struttura.strutturaC1 import FileC1, FileC1Repository
from struttura.strutturaC2 import FileC2, FileC2Repository
from struttura.strutturaC3 import FileC3, FileC3Repository
from struttura.strutturaResult import Result, display_errore


class OperazioniRouter:
    def __init__(self):
        # self.session_manager = SessionManager()
        # self.key = SessionKeys()
        self.session = SessionManager()
        self.operazione = self.session.state.operazione
        self.operazione_db = None

    def check_operazione(self):
        # with st.spinner('Caricamento...'):
        if self.operazione is not None:
            if self.operazione == 'SALVATAGGIO_FILE':
                with st.spinner('Salvataggio file...'):
                    file_c1 = self.session.state.files.upload_c1
                    file_c2 = self.session.state.files.upload_c2
                    file_c3 = self.session.state.files.upload_c3

                    try:
                        storage_path = Path(percorsi.get_storage())
                        storage_path.mkdir(parents=True, exist_ok=True)

                        (storage_path / "file_c1.txt").write_bytes(file_c1.getvalue())
                        (storage_path / "file_c2.txt").write_bytes(file_c2.getvalue())
                        (storage_path / "file_c3.txt").write_bytes(file_c3.getvalue())

                        st.toast("File salvati correttamente", icon=":material/check_box:", duration='long')
                        # self.session.termina_operazione()

                        self.session.switch_page(ListaPagine.CONTROLLO_FILE)

                    except Exception as e:
                        self.session.termina_operazione()
                        risultato = Result.failure(e)
                        display_errore(risultato)
                        return

            if self.operazione == 'CARICAMENTO_SU_DATABASE':
                tabella_c1 = st.secrets['tabelle']['tab_c1']
                tabella_c2 = st.secrets['tabelle']['tab_c2']
                tabella_c3 = st.secrets['tabelle']['tab_c3']
                with st.spinner('Caricamento su DataBase in corso...'):
                    # time.sleep(2)

                    file_c1: FileC1 = self.session.state.files.file_c1
                    file_c2: FileC2 = self.session.state.files.file_c2
                    file_c3: FileC3 = self.session.state.files.file_c3

                    from applicazione.utils import OperazioneDB
                    self.operazione_db = OperazioneDB()

                    with st.spinner('Svuoto tabelle...'):
                        self.operazione_db.svuota_tabella(tabella_c1)
                        self.operazione_db.svuota_tabella(tabella_c2)
                        self.operazione_db.svuota_tabella(tabella_c3)

                    with st.spinner('Upload C1...'):
                        repo = FileC1Repository()
                        caricamento_db = repo.caricamento_su_database(file_c1, tabella_c1)
                    with st.spinner('Upload C2...'):
                        repo = FileC2Repository()
                        caricamento_db = repo.caricamento_su_database(file_c2, tabella_c2)
                    with st.spinner('Upload C3...'):
                        repo = FileC3Repository()
                        caricamento_db = repo.caricamento_su_database(file_c3, tabella_c3)

                    # st.stop()

                    risultato = Result.success('Caricamento su db completato')

                    self.session.state.files.upload_su_database = True
                    self.session.termina_operazione(risultato)

            if self.operazione == 'CARICAMENTO_FILE_TEST':
                self.session.switch_page(ListaPagine.CONTROLLO_FILE)
                return
            if self.operazione == 'TEST_OPERAZIONE':
                self.session.start_loading()
                time.sleep(10)
                self.session.termina_operazione('test finito')
                self.session.stop_loading()
                self.session.switch_page(ListaPagine.CARICAMENTO_FILE)
                return
