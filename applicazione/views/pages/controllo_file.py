import math
import time
from pathlib import Path
from typing import Union
import io
import pandas as pd
import streamlit as st

from applicazione import App
from applicazione.config import ListaPagine
from applicazione.config import percorsi
from struttura.strutturaC1 import FileC1Repository, FileC1, ControlloFileC1
from struttura.strutturaC2 import FileC2Repository, FileC2, ControlloFileC2
from struttura.strutturaC3 import FileC3Repository, FileC3, ControlloFileC3
from struttura.strutturaResult import Result, display_errore, display_successo



class PaginaControllo(App):
    def __init__(self):
        super().__init__()

        storage_path = Path(percorsi.get_storage())
        self.percorso_file_c1 = storage_path / "file_c1.txt"
        self.percorso_file_c2 = storage_path / "file_c2.txt"
        self.percorso_file_c3 = storage_path / "file_c3.txt"
        self.struttura_selezionata = self.session.state.files.codice_struttura_selezionata
        self.anno_selezionato = self.session.state.files.anno_selezionato
        self.mese_selezionato = self.session.state.files.mese_selezionato

        self.is_error = self.session.state.page.is_error

        self.errore_controllo = False
        # st.write(self.struttura_selezionata)
        # st.stop()

        if self.current_page == ListaPagine.CONTROLLO_FILE and (
                not self.percorso_file_c1.exists()
                or not self.percorso_file_c2.exists()
                or not self.percorso_file_c3.exists()
                or self.struttura_selezionata is None
                or self.anno_selezionato is None
                or self.mese_selezionato is None):
            if self.session.state.page.loading:
                self.session.stop_loading()

            st.error('Caricare prima i File')

            with st.spinner(f"Reindirizzamento a '{ListaPagine.CARICAMENTO_FILE.page_model.title}' tra 10 secondi...",
                            show_time=True):
                time.sleep(10)
                # st.switch_page(ListaPagine.CARICAMENTO_FILE.page_model.path)
            self.session.switch_page(ListaPagine.CARICAMENTO_FILE)

    def reset_pagina_corrente(self, tipo_file):
        if tipo_file == 'file_c1':
            self.session.state.files.pagina_corrente_file_c1 = 1
        elif tipo_file == 'file_c2':
            self.session.state.files.pagina_corrente_file_c2 = 1
        elif tipo_file == 'file_c3':
            self.session.state.files.pagina_corrente_file_c3 = 1

    def set_pagina_corrente(self, tipo_file):
        """Callback per impostare un valore specifico nella sessione."""
        # st.session_state[key_sessione_pagina] = valore
        nuova_pagina = st.session_state[tipo_file]

        if tipo_file == 'file_c1':
            self.session.state.files.pagina_corrente_file_c1 = nuova_pagina
        elif tipo_file == 'file_c2':
            self.session.state.files.pagina_corrente_file_c2 = nuova_pagina
        elif tipo_file == 'file_c3':
            self.session.state.files.pagina_corrente_file_c3 = nuova_pagina

    def incrementa_pagina(self, tipo_file):
        """Callback per il bottone 'Successivo'."""
        # st.session_state[key_sessione_pagina] += 1
        nuova_pagina = 0
        if tipo_file == 'file_c1':
            self.session.state.files.pagina_corrente_file_c1 += 1
            nuova_pagina = self.session.state.files.pagina_corrente_file_c1
        elif tipo_file == 'file_c2':
            self.session.state.files.pagina_corrente_file_c2 += 1
            nuova_pagina = self.session.state.files.pagina_corrente_file_c2

        elif tipo_file == 'file_c3':
            self.session.state.files.pagina_corrente_file_c3 += 1
            nuova_pagina = self.session.state.files.pagina_corrente_file_c3

        st.session_state[tipo_file] = nuova_pagina


    def decrementa_pagina(self, tipo_file):
        """Callback per il bottone 'Precedente'."""
        # st.session_state[key_sessione_pagina] -= 1
        nuova_pagina  = 0
        if tipo_file == 'file_c1':
            self.session.state.files.pagina_corrente_file_c1 -= 1
            nuova_pagina = self.session.state.files.pagina_corrente_file_c1
        elif tipo_file == 'file_c2':
            self.session.state.files.pagina_corrente_file_c2 -= 1
            nuova_pagina = self.session.state.files.pagina_corrente_file_c2
        elif tipo_file == 'file_c3':
            self.session.state.files.pagina_corrente_file_c3 -= 1
            nuova_pagina = self.session.state.files.pagina_corrente_file_c3

        st.session_state[tipo_file] = nuova_pagina

    def download_excel(self, tipo_file):
        lista_record = None
        file_name = None
        sheet_name = None
        if tipo_file == 'file_c1':
            lista_record = self.session.state.files.file_c1
            file_name = "dati_export_c1.xlsx"
            sheet_name = "Dati C1"
        if tipo_file == 'file_c2':
            lista_record = self.session.state.files.file_c2
            file_name = "dati_export_c2.xlsx"
            sheet_name = "Dati C2"
        if tipo_file == 'file_c3':
            lista_record = self.session.state.files.file_c3
            file_name = "dati_export_c3.xlsx"
            sheet_name = "Dati C3"
            # st.write(tipo_file)
            # self.session.state.files.lista_record_c1 = lista_record
            #
        df = pd.DataFrame(lista_record)
        download_excel = "📤 Scarica dati Excel"
        # file_name = "dati_export_c1.xlsx"
        with open(file_name, 'wb') as f:
            with pd.ExcelWriter(f, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name=sheet_name)
        #
        st.download_button(
            label=download_excel,
            data=open(file_name, 'rb'),
            file_name=file_name,
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        )
        open(file_name, "wb").close()
            # print(self.session.state.files.lista_record_c1)
            # st.write(self.session.state.files.lista_record_c1)
            # st.stop()

    def mostra_tabella_record(self, dati, campi_da_escludere=None):
        if campi_da_escludere is None:
            campi_da_escludere = []
        df_originale = pd.DataFrame(dati)

        df_visualizzato = df_originale.drop(columns=campi_da_escludere)

        st.dataframe(df_visualizzato)



    def control_file(self, file_path, _repository: Union[FileC1Repository, FileC2Repository, FileC3Repository]):
        repo = _repository

        # controllo_result = repo.controlla_file(file_path)
        # if controllo_result.is_failure():
        #     return controllo_result

        oggetto_result = repo.carica_da_file(file_path)
        if oggetto_result.is_failure():
            # display_errore(oggetto_result)
            self.session.state.page.is_error = True
            if self.session.state.page.loading:
                self.session.stop_loading()
                st.rerun()

            st.error(oggetto_result.errore)
            with st.expander('info'):
                st.warning(oggetto_result.info)

            if st.button('Torna a Caricamento File', type="secondary"):
                self.session.switch_page(ListaPagine.CARICAMENTO_FILE)

            st.stop()

        file: Union[FileC1, FileC2] = oggetto_result.risultato
        return Result.success(file)



    def render_tab_c1(self, file_path):

        if not self.session.state.files.file_c1:
            with st.spinner('Controllo file in corso...'):
                self.session.state.files.pagina_corrente_file_c1 = 1
                repo = FileC1Repository()
                result_file = self.control_file(file_path, repo)

                if result_file.is_failure():
                    self.session.state.page.is_error = True
                    # st.write(result_file)
                    st.error(result_file.errore)
                    for errore in result_file.info:
                        with st.expander(f"{errore['messaggio']}"):
                            st.warning(f"Valore ricevuto: **{errore['dettagli']}**")
                else:
                    file: FileC1 = result_file.risultato
                    validatore = ControlloFileC1(file).controllo()

                    if validatore.is_failure():
                        self.session.state.page.is_error = True

                        if validatore.info == 'LISTA_ERRORI':
                            st.error('Errore durante il controllo del file C1')
                            lista_errori = validatore.errore
                            # st.write(lista_errori)
                            for errore in lista_errori:
                                with st.expander(f"Errore riga: **{errore['riga']}**"):
                                    st.error(errore['messaggio'])
                                    st.warning(f"Valore ricevuto: *'{errore['valore']}'*")
                        else:
                            st.error(validatore.errore)
                            st.warning(validatore.info[0])

                            with st.expander('Mostra errori'):
                                for errore in validatore.info[1]:
                                    with st.expander(f"Errore riga: **{errore['riga']}**"):
                                        st.error(errore['messaggio'])
                                        st.warning(f"Valore ricevuto: *'{errore['valore']}'*")

                    else:
                        self.session.state.page.is_error = False

                        st.success("Nessun errore riscontrato durante i controllo del File C1")
                        self.session.state.files.file_c1 = file.records
                        st.rerun()

        else:
            self.mostra_file_c(
                tipo_file='file_c1',
                campi_da_escludere=['uuid', 'campo_vuoto']
            )

    def render_tab_c2(self, file_path):

        if not self.session.state.files.file_c2:
            with st.spinner('Controllo file in corso...'):
                self.session.state.files.pagina_corrente_file_c2 = 1
                repo = FileC2Repository()
                result_file = self.control_file(file_path, repo)

                if result_file.is_failure():
                    self.session.state.page.is_error = True

                    # st.write(result_file)
                    st.error(result_file.errore)
                    for errore in result_file.info:
                        with st.expander(f"{errore['messaggio']}"):
                            st.warning(f"Valore ricevuto: **{errore['dettagli']}**")
                else:
                    file: FileC2 = result_file.risultato
                    validatore = ControlloFileC2(file).controllo()

                    if validatore.is_failure():
                        self.session.state.page.is_error = True

                        if validatore.info == 'LISTA_ERRORI':
                            st.error('Errore durante il controllo del file C2')
                            lista_errori = validatore.errore
                            # st.write(lista_errori)
                            for errore in lista_errori:
                                with st.expander(f"Errore riga: **{errore['riga']}**"):
                                    st.error(errore['messaggio'])
                                    st.warning(f"Valore ricevuto: *'{errore['valore']}'*")
                        else:
                            st.error(validatore.errore)
                            st.warning(validatore.info[0])

                            with st.expander('Mostra errori'):
                                for errore in validatore.info[1]:
                                    with st.expander(f"Errore riga: **{errore['riga']}**"):
                                        st.error(errore['messaggio'])
                                        st.warning(f"Valore ricevuto: *'{errore['valore']}'*")

                    else:



                        self.session.state.page.is_error = False

                        st.success("Nessun errore riscontrato durante i controllo del File C2")
                        self.session.state.files.file_c2 = file.records
                        st.rerun()

        else:
            self.mostra_file_c(
                tipo_file='file_c2',
                campi_da_escludere=['uuid', 'campo_vuoto']
            )

    def render_tab_c3(self, file_path):

        if not self.session.state.files.file_c3:
            with st.spinner('Controllo file in corso...'):
                self.session.state.files.pagina_corrente_file_c3 = 1
                repo = FileC3Repository()
                result_file = self.control_file(file_path, repo)

                if result_file.is_failure():
                    self.session.state.page.is_error = True

                    # st.write(result_file)
                    st.error(result_file.errore)
                    for errore in result_file.info:
                        with st.expander(f"{errore['messaggio']}"):
                            st.warning(f"Valore ricevuto: **{errore['dettagli']}**")
                else:
                    file: FileC3 = result_file.risultato
                    validatore = ControlloFileC3(file).controllo()

                    if validatore.is_failure():
                        self.session.state.page.is_error = True

                        if validatore.info == 'LISTA_ERRORI':
                            st.error('Errore durante il controllo del file C3')
                            lista_errori = validatore.errore
                            # st.write(lista_errori)
                            for errore in lista_errori:
                                with st.expander(f"Errore riga: **{errore['riga']}**"):
                                    st.error(errore['messaggio'])
                                    st.warning(f"Valore ricevuto: *'{errore['valore']}'*")
                        else:
                            st.error(validatore.errore)
                            st.warning(validatore.info[0])

                            with st.expander('Mostra errori'):
                                for errore in validatore.info[1]:
                                    with st.expander(f"Errore riga: **{errore['riga']}**"):
                                        st.error(errore['messaggio'])
                                        st.warning(f"Valore ricevuto: *'{errore['valore']}'*")

                    else:
                        self.session.state.page.is_error = False

                        st.success("Nessun errore riscontrato durante i controllo del File C3")
                        self.session.state.files.file_c3 = file.records
                        st.rerun()

        else:
            self.mostra_file_c(
                tipo_file='file_c3',
                campi_da_escludere=['uuid']
            )



    def mostra_file_c(self, tipo_file, campi_da_escludere):
        key_session_file = None
        pagina_corrente = None
        if tipo_file == 'file_c1':
            if not self.session.state.files.file_c1:
                st.warning('Dati non trovati in sessione')
            else:
                key_session_file = self.session.state.files.file_c1
                pagina_corrente = self.session.state.files.pagina_corrente_file_c1
        if tipo_file == 'file_c2':
            if not self.session.state.files.file_c2:
                st.warning('Dati non trovati in sessione')
            else:
                key_session_file = self.session.state.files.file_c2
                pagina_corrente = self.session.state.files.pagina_corrente_file_c2

        if tipo_file == 'file_c3':
            if not self.session.state.files.file_c3:
                st.warning('Dati non trovati in sessione')
            else:
                key_session_file = self.session.state.files.file_c3
                pagina_corrente = self.session.state.files.pagina_corrente_file_c3

        tutte_le_righe = key_session_file
        totale_righe = len(tutte_le_righe)

        col1, col2 = st.columns([1, 1])
        with col1:
            righe_per_pagina = st.selectbox(
                'Righe per pagina',
                options=[50, 100, 200, 500, 1000],
                index=1,
                key=f"select_righe_{tipo_file}",
                on_change=self.reset_pagina_corrente,
                args=(tipo_file,)
            )
        totale_pagine = math.ceil(totale_righe / righe_per_pagina) if righe_per_pagina > 0 else 1

        with col2:
            st.number_input(
                f"Vai alla pagina (1-{totale_pagine})",
                min_value=1,
                max_value=totale_pagine,
                value=pagina_corrente,
                key=tipo_file,
                on_change=self.set_pagina_corrente,
                args=(tipo_file,)
            )

        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            st.button('⬅️ Precedente',
                      use_container_width=True,
                      disabled=(pagina_corrente <= 1),
                      key=f"prec_{tipo_file}",
                      on_click=self.decrementa_pagina,
                      args=(tipo_file,))
        with col2:
            st.markdown(
                f"<h4 style='text-align: center;'>Pagina {pagina_corrente} di {totale_pagine}</h4>",
                unsafe_allow_html=True)

        with col3:
            st.button('Successivo ➡️',
                      use_container_width=True,
                      disabled=(pagina_corrente >= totale_pagine),
                      key=f"succ_{tipo_file}",
                      on_click=self.incrementa_pagina,
                      args=(tipo_file,))

        st.divider()

        start_index = (pagina_corrente - 1) * righe_per_pagina
        end_index = start_index + righe_per_pagina
        righe_da_mostrare = tutte_le_righe[start_index:end_index]

        with st.container(horizontal=True, border=False):
            st.subheader(f"Visualizzando righe da {start_index + 1} a {min(end_index, totale_righe)}")
            self.download_excel(tipo_file)

        righe_formattate = [riga.dati for riga in righe_da_mostrare]

        lista_record = [vars(record) for record in righe_formattate]


        if tipo_file == 'file_c1':
            self.session.state.files.lista_record_c1 = lista_record
        if tipo_file == 'file_c2':
            self.session.state.files.lista_record_c2 = lista_record
        if tipo_file == 'file_c3':
            self.session.state.files.lista_record_c3 = lista_record


        self.mostra_tabella_record(lista_record, campi_da_escludere=campi_da_escludere)



    def mostra_confirm_dialog(self):
        @st.dialog('Conferma di voler procedere', on_dismiss="ignore")
        def dialog(item = None):
            st.write('Confermi di voler procedere con il caricamento su DataBase?')
            with st.container(horizontal=True, horizontal_alignment="right"):
                # if st.button('Annulla'):
                #     pass
                if st.button('Procedi', type='primary'):
                    self.session.state.page.show_confirm_modal = False
                    self.session.nuova_operazione('CARICAMENTO_SU_DATABASE')
                    st.rerun()

        dialog()




    def show(self):
        risultato_operazione = self.session.state.risultato_operazione
        if risultato_operazione is not None:
            if risultato_operazione.is_failure():
                self.session.state.risultato_operazione = None
                # st.error(risultato_operazione.errore)
                display_errore(risultato_operazione)

            if risultato_operazione.is_success():
                self.session.state.risultato_operazione = None
                # st.success(risultato_operazione.risultato)
                display_successo(risultato_operazione)

        if self.session.state.page.show_confirm_modal:
            self.mostra_confirm_dialog()


        with st.container(horizontal=True, horizontal_alignment="center", vertical_alignment="center"):
            st.header('CONTROLLO')
            if self.session.state.files.upload_su_database:
                st.info('Upload su DataBase già avvenuto')
            with st.container():
                upload_db = st.button("Upload su database", type="primary", disabled=self.session.state.files.upload_su_database)

        with st.container(horizontal=True):
            st.markdown(f"**Struttura:** {self.session.state.files.nome_struttura_selezionata} | {self.session.state.files.codice_struttura_selezionata}")
            st.markdown(f"**Prestazione:** {self.session.state.files.nome_prestazione_selezionata} | {self.session.state.files.codice_prestazione_selezionata}")
            st.markdown(f"**Anno:** {self.session.state.files.anno_selezionato}")
            st.markdown(f"**Mese:** {self.session.state.files.mese_selezionato}")

        if upload_db:
            if self.session.state.page.is_error:
                st.error('Errore con i File Caricati')
                st.stop()
            if self.is_error:
                st.warning('Il caricamento non può essere eseguito poichè i file non rispettano i controlli')
            else:
                # self.session.state.page.show_confirm_modal = True
                # st.rerun()
                self.session.nuova_operazione('CARICAMENTO_SU_DATABASE')

        with st.spinner('Caricamento...'):
            tab_1, tab_2, tab_3 = st.tabs(["File C1", "File C2", "File C3"])

        with tab_1:
            if not self.errore_controllo:
                self.render_tab_c1(self.percorso_file_c1)
        with tab_2:
            if not self.errore_controllo:
                self.render_tab_c2(self.percorso_file_c2)

        with tab_3:
            if not self.errore_controllo:
                self.render_tab_c3(self.percorso_file_c3)

    # def show_test(self):
    #     st.write('pagina controllo file')
    #     if st.button('vai a caricamento'):
    #         st.write('caricamento')
    #         self.session_manager.switch_page(ListaPagine.CARICAMENTO_FILE)

    def render(self):

        self.show()
        # st.write('CONTROLLO FILE')
        # if self.session_manager.check_loading():
        #     self.session_manager.stop_loading()
        #     st.rerun()


pagina = PaginaControllo()
pagina.render()
