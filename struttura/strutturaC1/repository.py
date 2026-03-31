import os
from typing import List, Dict, Any
import streamlit as st
from struttura.strutturaC1 import FileC1, RecordC1Builder, RecordC1, DatiRecordC1Model
from struttura.strutturaResult import Result, display_errore
import mysql.connector
from mysql.connector import Error
from struttura.strutturaDB import get_connection
from mysql.connector import MySQLConnection


DEFINIZIONE_CAMPI = [
    ("regione_addebitante", 0, 3),
    ("az_osp_inviante", 3, 6),
    ("codice_struttura_erogatrice", 6, 12),
    ("medico_prescrittore", 12, 28),
    ("cognome_dell_utente", 28, 58),
    ("nome_dell_utente", 58, 78),
    ("campo_vuoto", 78, 94),
    ("codice_fiscale_dell_utente", 94, 110),
    ("sesso_dell_utente", 110, 111),
    ("data_di_nascita_dell_utente", 111, 119),
    ("provincia_e_comune_di_residenza", 119, 125),
    ("usl_di_residenza", 125, 128),
    ("progressivo_riga_per_ricetta", 128, 130),
    ("id", 130, 150),
]

LUNGHEZZA_ATTESA = 150


def estrai_dati_riga(record_riga: str, conteggio):
    """Estrae i dati da una riga e li restituisce come dizionario."""
    if len(record_riga) != LUNGHEZZA_ATTESA:
        risultato = Result.failure(f'La lunghezza della riga {conteggio} non è valida. File C1',
                                   info=f"Attesa: {LUNGHEZZA_ATTESA}, Ricevuta: {len(record_riga)}")
        # display_errore(risultato)
        return risultato

    dati_estratti = {
        nome: record_riga[inizio:fine].strip()  # Usiamo .strip() per pulire gli spazi
        for nome, inizio, fine in DEFINIZIONE_CAMPI
    }
    return Result.success(dati_estratti)


def crea_record_da_stringa(riga_dati: str, conteggio) -> Result:
    """Factory che crea un oggetto RecordC1 partendo da una stringa."""
    # try:
    estrazione_result = estrai_dati_riga(riga_dati, conteggio)
    if estrazione_result.is_failure():
        return estrazione_result

    dati_estratti = estrazione_result.risultato
    builder = RecordC1Builder()

    # Popolamento dinamico del builder
    for nome_campo, valore in dati_estratti.items():

        setter_method_name = f"set_{nome_campo}"
        if hasattr(builder, setter_method_name):
            getattr(builder, setter_method_name)(valore)

    record_result = RecordC1.crea(builder)

    if hasattr(record_result, 'is_failure') and record_result.is_failure():
        info_errore_originale = f"{record_result.errore}: {record_result.info}"

        return Result.failure(
            f"Errore nella validazione dei dati alla riga {conteggio}",
            info=info_errore_originale
        )

    return Result.success(record_result)

    # except (ValidationError, KeyError) as e:
    #     risultato =  Result.failure("Errore nella creazione del RecordC1 dalla stringa", info=str(e))
    #     display_errore(risultato)
    #     return


class FileC1Repository:
    def carica_da_file(self, file_path: str) -> Result:
        """
        Legge un file di testo, processa ogni riga per creare un oggetto RecordC1,
        e restituisce un oggetto FileC1 che li contiene tutti.
        """
        if not os.path.exists(file_path):
            risultato = Result.failure(f"File non trovato al percorso: {file_path}")
            display_errore(risultato)
            st.stop()

        lista_record_oggetti = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                conteggio = 0
                for n_riga, riga in enumerate(f, 1):
                    conteggio += 1
                    # Ignora righe vuote o composte solo da spazi
                    if not riga.strip():
                        continue

                    # Usa la factory per creare il singolo record
                    record_result = crea_record_da_stringa(riga.strip('\n'), n_riga)

                    if record_result.is_failure():
                        # Se anche una sola riga fallisce, interrompiamo e segnaliamo l'errore

                        return Result.failure(
                            f"Errore nella lettura del file alla riga {n_riga}",
                            info=record_result.info
                        )
                        # display_errore(record_result)
                        # raise

                    lista_record_oggetti.append(record_result.risultato)

            # Se tutte le righe sono state processate con successo, crea l'oggetto FileC1
            nome_file = os.path.basename(file_path)
            oggetto_file_c1 = FileC1.crea(lista_record_oggetti, nome_file=nome_file)

            return Result.success(oggetto_file_c1)

        except Exception as e:
            return Result.failure("Errore imprevisto durante l'apertura o la lettura del file", info=str(e))

    def controlla_file(self, file_path: str):

        if not os.path.exists(file_path):
            return Result.failure(f"File non trovato al percorso: {file_path}")

        lista_errori: List[Dict[str, Any]] = []

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for n_riga, riga in enumerate(f, 1):
                    if not riga.strip():
                        continue

                    record_result = crea_record_da_stringa(riga.strip('\n'), n_riga)

                    if record_result.is_failure():
                        errore_dettagliato = {
                            'riga': n_riga,
                            'messaggio': record_result.errore,
                            'dettagli': record_result.info
                        }

                        lista_errori.append(errore_dettagliato)

            if lista_errori:
                return Result.failure(
                    f"Caricamento fallito. Trovati {len(lista_errori)} record errati nel file.",
                    info=lista_errori
                )
            else:
                return Result.success("Il file è stato controllato e risulta valido")

        except Exception as e:
            return Result.failure("Errore imprevisto durante la lettura del file", info=str(e))




    def caricamento_su_database(self, file:FileC1, tabella: str):
        # st.write(file)
        connessione:MySQLConnection = get_connection().risultato
        # st.write(file)

        if not file:
            st.warning('Nessun dato da caricare per File C1')
            return

        column_names = list(DatiRecordC1Model.model_fields.keys())

        data_tuples = []
        for record in file:
            tuple_values = tuple(getattr(record.dati, col) for col in column_names)
            data_tuples.append(tuple_values)

        columns_sql = ", ".join([f"`{c}`" for c in column_names])
        placeholders_sql = ", ".join(["%s"] * len(column_names))
        query = f"INSERT INTO {tabella} ({columns_sql}) VALUES ({placeholders_sql})"

        if connessione is None:
            return

        cursor = None
        try:
            cursor = connessione.cursor()
            cursor.executemany(query, data_tuples)

            connessione.commit()

            # st.success(f"Caricamento File C1 su DataBase completato con successo")

            return Result.success(f"Caricamento File C1 su DataBase completato con successo")
        except Error as e:
            # st.error(f"Errore durante il caricamento dei dati File C1 su database: {e}")

            if connessione:
                connessione.rollback()
            return Result.failure(f"Errore durante il caricamento dei dati File C1 su database: {e}")

        finally:
            if cursor:
                cursor.close()
            if connessione and connessione.is_connected():
                connessione.close()
