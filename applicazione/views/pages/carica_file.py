import streamlit as st

from applicazione import App
from struttura.strutturaResult import Result, display_errore
from struttura.strutturaUtente import Utente


class PaginaCaricaFile(App):
    def __init__(self):
        super().__init__()

        self.struttura_selezionata = None
        self.prestazione_selezionata = None
        self.anno_selezionato = None
        self.mese_selezionato = None
        self.opzioni_strutture = self._get_opzioni_strutture()
        self.opzioni_prestazioni = self._get_opzioni_prestazioni()

        # self.utente:Utente = self.session_manager.get(self.key.key_utente_loggato())
        self.utente: Utente = self.session.state.user.utente_loggato

        # if not self.opzioni_strutture:
        #     st.error("La query non ha restituito alcun risultato.")
        # else:
        #     st.write("--- INIZIO DEBUG ---")
        #     st.write("Il primo elemento della lista di strutture è:")
        #     primo_elemento = self.opzioni_strutture[0]
        #     st.write(primo_elemento)
        #     st.write(f"Il tipo del primo elemento è: {type(primo_elemento)}")
        #     st.write(f"Il numero di valori al suo interno è: {len(primo_elemento)}")
        #     st.write("--- FINE DEBUG ---")
        #
        # # Interrompiamo l'app qui per analizzare l'output del debug
        # st.stop()

    def _get_opzioni_strutture(self):
        sql = """SELECT codice, denominazione FROM strutture ORDER BY denominazione"""

        result: Result = self.operazione_db.query_select_all(query=sql).risultato

        # opzioni_strutture = {codice:denominazione for codice, denominazione in result}
        # st.write(opzioni_strutture)
        # st.write(len(opzioni_strutture))
        # st.stop()
        # return opzioni_strutture
        return result

    def _format_opzioni_strutture(self, opzione):
        codice, denominazione = opzione
        return f"{denominazione} (Cod: {codice})"

    def _get_opzioni_prestazioni(self):
        sql = """SELECT codice, tipo_prest FROM strutture_tipo_prestazione"""

        result: Result = self.operazione_db.query_select_all(query=sql).risultato

        # opzioni_prestazioni = {tipo_prestazione:codice for codice, tipo_prestazione in result}
        # st.write(opzioni_prestazioni)
        # st.stop()
        # return opzioni_prestazioni
        return result

    def _format_opzioni_prestazioni(self, opzione):
        codice, prestazione = opzione
        return f"{prestazione} (Cod: {codice})"

    @st.fragment
    def _caricamento_file(self):
        with st.container(
                border=True,
                horizontal=True,
                horizontal_alignment="distribute"
        ):
            file_c1 = st.file_uploader("File C1", type=['txt'])
            file_c2 = st.file_uploader("File C2", type=['txt'])
            file_c3 = st.file_uploader("File C3", type=['txt'])

        return file_c1, file_c2, file_c3

    def show(self):
        st.header('Carica i file C')

        placeholder = st.empty()

        # col1, col2, col3 = st.columns([3, 1.5, 2])
        col1, col2 = st.columns([4, 2])
        with col1:
            self.struttura_selezionata = st.selectbox(
                label="Strutture",
                options=self.opzioni_strutture,
                format_func=self._format_opzioni_strutture,
                index=None,
                placeholder="Seleziona una struttura",

            )
            self.prestazione_selezionata = st.selectbox(
                label="Prestazione",
                # options=self.opzioni_prestazioni.keys(),
                options=self.opzioni_prestazioni,
                format_func=self._format_opzioni_prestazioni,
                index=None,
                placeholder="Seleziona una prestazione",
            )
        with col2:
            self.anno_selezionato = st.selectbox(
                label="Anno",
                index=None,
                placeholder="Seleziona un anno",
                options=["2024", "2025"],

            )
            self.mese_selezionato = st.selectbox(
                        label='Mese',
                        index=None,
                        placeholder="Seleziona un mese",
                        options=["Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno", "Luglio", "Agosto", "Settembre",
                                 "Ottobre", "Novembre", "Dicembre"],

                    )
        # with col3:
        #     self.mese_selezionato = st.selectbox(
        #         label='Mese',
        #         index=None,
        #         placeholder="Seleziona un mese",
        #         options=["Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno", "Luglio", "Agosto", "Settembre",
        #                  "Ottobre", "Novembre", "Dicembre"],
        #
        #     )

        upload_file_c1, upload_file_c2, upload_file_c3 = self._caricamento_file()

        with st.container(horizontal=True, horizontal_alignment="center"):
            procedi_button = st.button("Procedi con questi file", width=300, type="primary")

        if procedi_button:
            with placeholder.container():
                with st.spinner('Caricamento...'):
                    if self.struttura_selezionata is None:
                        risultato = Result.failure('Per favore selezionare una struttura')
                        display_errore(risultato)
                        return
                    if self.anno_selezionato is None:
                        risultato = Result.failure('Per favore selezionare un Anno')
                        display_errore(risultato)
                        return
                    if self.mese_selezionato is None:
                        risultato = Result.failure('Per favore selezionare un Mese')
                        display_errore(risultato)
                        return
                    if upload_file_c1 is None or upload_file_c2 is None or upload_file_c3 is None:
                        risultato = Result.failure('Per favore caricare tutti i file')
                        display_errore(risultato)
                        return

                    codice_struttura = None
                    nome_struttura = None
                    if self.struttura_selezionata:
                        codice_struttura = self.struttura_selezionata[0]
                        nome_struttura = self.struttura_selezionata[1]
                    if codice_struttura:
                        codice_struttura = str(codice_struttura).zfill(6)
                    # st.write(codice_struttura)


                    codice_prestazione = None
                    nome_prestazione = None
                    if self.prestazione_selezionata:
                        codice_prestazione = self.prestazione_selezionata[0]
                        nome_prestazione = self.prestazione_selezionata[1]
                    if codice_prestazione:
                        codice_prestazione = str(codice_prestazione).zfill(6)
                    # st.write(codice_prestazione)
                    # st.stop()

                    # codice_struttura = self.opzioni_strutture[self.struttura_selezionata].zfill(6)
                    # self.session_manager.set(self.key.key_struttura_selezionata(), codice_struttura)
                    # self.session_manager.set(self.key.key_anno_selezionato(), self.anno_selezionato)
                    # self.session_manager.set(self.key.key_mese_selezionato(), self.mese_selezionato)
                    #
                    # self.session_manager.set(self.key.key_upload_c1(), upload_file_c1)
                    # self.session_manager.set(self.key.key_upload_c2(), upload_file_c2)
                    # self.session_manager.set(self.key.key_upload_c3(), upload_file_c3)
                    #
                    # self.session_manager.nuova_operazione('SALVATAGGIO_FILE')

                    self.session.state.files.nome_struttura_selezionata = nome_struttura
                    self.session.state.files.codice_struttura_selezionata = codice_struttura
                    self.session.state.files.nome_prestazione_selezionata = nome_prestazione
                    self.session.state.files.codice_prestazione_selezionata = codice_prestazione
                    self.session.state.files.anno_selezionato = self.anno_selezionato
                    self.session.state.files.mese_selezionato = self.mese_selezionato

                    self.session.state.files.upload_c1 = upload_file_c1
                    self.session.state.files.upload_c2 = upload_file_c2
                    self.session.state.files.upload_c3 = upload_file_c3

                    self.session.nuova_operazione('SALVATAGGIO_FILE')

            st.write('FINITO')

        if st.button('test'):
            # self.session_manager.nuova_operazione('TEST_OPERAZIONE')
            self.session.nuova_operazione('TEST_OPERAZIONE')

    def render(self):

        if self.session.state.operazione is None:
            self.show()
        # if self.session_manager.check_loading():
        #     self.session_manager.loading_off()

        # st.rerun()


pagina = PaginaCaricaFile()
pagina.render()
