
from pathlib import Path
import tomllib
import os.path
import streamlit as st
import toml
from applicazione import App
from applicazione.config import ListaPagine
from applicazione.config import percorsi
from struttura.strutturaResult import Result, display_errore, display_successo
from struttura.strutturaDB import sincronizza_tabella
from struttura.strutturaUtente import DatiUtenteModel, UtenteBuilder, Utente
from struttura.strutturaC1 import DatiRecordC1Model
from struttura.strutturaC2 import DatiRecordC2Model
from struttura.strutturaC3 import DatiRecordC3Model
class Pagina_configurazione(App):

    def __init__(self):
        super().__init__()
        self.secrets_file_path = os.path.join(".streamlit", "secrets.toml")

        try:
            with open(self.secrets_file_path, "r") as f:
                self.secrets = toml.load(f)
        except FileNotFoundError:
            st.error(f"File '{self.secrets_file_path}' non trovato. Assicurati che il file esista.")
            st.stop()
        except toml.TomlDecodeError:
            st.error(
                f"Errore nella decodifica del file '{self.secrets_file_path}'. Assicurati che sia formattato correttamente.")
            st.stop()



    def db_config(self):
        modelli = [
            DatiUtenteModel,
            DatiRecordC1Model,
            DatiRecordC2Model,
            DatiRecordC3Model,
        ]
        tabelle = [
            'streamlit_utenti',
            'streamlit_c1',
            'streamlit_c2',
            'streamlit_c3',
        ]

        campi_unici = [
            ['username', 'email', 'telefono', 'codice_fiscale'],
            ['uuid'],
            ['uuid'],
            ['uuid'],
        ]

        for i in range(len(modelli)):
            db_result = sincronizza_tabella(
                model=modelli[i],
                table_name=tabelle[i],
                unique_fields=campi_unici[i]
            )

    def form_edit_secrets_file(self):
        with st.form('Modifica secrets'):
            st.subheader('Modifica `secrets.toml`')

            updated_secrets = {}

            for section, values in self.secrets.items():
                with st.expander(f"Sezione: `{section}`"):
                    # st.markdown(f"##### Sezione: `{section}`")
                    updated_secrets[section] = {}
                    for key, value in values.items():
                        new_value = st.text_input(f"Valore per `{key}`", value=value, key=f"{section}_{key}")
                        updated_secrets[section][key] = new_value

            submitted = st.form_submit_button('Salva Modifiche')
            if submitted:
                try:
                    with open(self.secrets_file_path, "w") as f:
                        toml.dump(updated_secrets, f)
                    st.success('File secrets.toml aggiornato con successo')
                    st.info("Riavvia la tua applicazione per applicare le modifiche")
                except Exception as e:
                    st.error(f"Si è verificato un errore durante l'aggiornamento del file secrets.toml : {e}")

        st.subheader("Contenuto attuale di `secrets.toml`")
        st.warning(
            "Questo è il contenuto al momento del caricamento della pagina. Potrebbe essere necessario un riavvio dell'app.")
        with st.expander(''):
            st.json(st.secrets.to_dict())


    def show(self):
        st.header("Configurazione")

        with st.container(horizontal=True):
            db_config = st.button('DB Config', type="primary")
            if st.button("Refresh"):
                st.rerun()

        # st.write(st.secrets['tabelle']['tab_c1'])
        st.divider()
        with st.spinner('Caricamento...'):
            if db_config:
                self.db_config()
                st.success('Database aggiornato con successo')

        with st.container(border=False):
            self.form_edit_secrets_file()

        
    def render(self):
        self.show()
                    
pagina = Pagina_configurazione()
pagina.show()
                    