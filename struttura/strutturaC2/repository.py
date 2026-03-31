import os
from typing import List, Dict, Any
import streamlit as st

from struttura.strutturaC2 import FileC2, RecordC2Builder, RecordC2, DatiRecordC2Model
from struttura.strutturaResult import Result, display_errore

from mysql.connector import Error
from struttura.strutturaDB import get_connection
from mysql.connector import MySQLConnection

DEFINIZIONE_CAMPI = [
    ("regione_addebitante", 0, 3),
    ("az_osp_inviante", 3, 6),
    ("codice_struttura_erogatrice", 6, 12),
    ("numero_ricetta", 12, 28),
    ("progressivo_riga_per_ricetta", 28, 30),
    ("data", 30, 38),
    ("codifica_nomenclatore", 38, 39),
    ("codice_prestazione", 39, 46),
    ("quantita", 46, 49),
    ("posizione_dell_utente_nei_confronti_del_ticket", 49, 51),
    ("importo_ticket", 51, 58),
    ("importo_totale", 58, 66),
    ("posizione_contabile", 66, 67),
    ("errori_anagrafici", 67, 68),
    ("errori_residenza", 68, 69),
    ("errori_prestazione", 69, 70),
    ("errori_ricetta", 70, 71),
    ("errori_record", 71, 72),
    ("errori_importo", 72, 73),
    ("errori_quantita", 73, 74),
    ("errori_data_prestazione", 74, 75),
    ("errori_ricetta_2", 75, 76),
    ("errore_riservato", 76, 77),
    ("id", 77, 97),
    ("regione_iniziale_addebito", 97, 100),
    ("tipo_erogazione", 100, 102),
    ("codice_disciplina_unita_operativa_erogatrice", 102, 105),
    ("classe_priorita_prenotazione", 105, 106),
    ("codice_esenzione", 106, 112),
    ("tipo_struttura", 112, 113),
    ("quota_compartecipazione_alla_spesa", 113, 121),
    ("fatturato_al_lordo_ticket", 121, 129),
    ("campo_vuoto", 129, 137),
    ("numero_fattura", 137, 157),
    ("data_fattura", 157, 165),
    ("fatturato_al_netto_ticket", 165, 173),
    ("liquidato", 173, 181),
    ("causa_mancata_liquidazione", 181, 182),
    ("causa_parziale_liquidazione", 182, 183),
    ("garanzia_tempi_massimi", 183, 184),
    ("numero_sedute_cliniche", 184, 187),
    ("data_prenotazione", 187, 195),
    ("data_prima_disponibilita", 195, 203),
    ("data_primo_appuntamento", 203, 211),
    ("tipo_prestazione", 211, 212),
]

LUNGHEZZA_ATTESA = 212

valori_per_posizione_dell_utente_nei_confronti_del_ticket = {
    '01': {
        'messaggio': 'esente totale'
    },
    '02': {
        'messaggio': 'non esente'
    }
}


def estrai_dati_riga(record_riga: str, conteggio):
    """Estrae i dati da una riga e li restituisce come dizionario."""
    if len(record_riga) != LUNGHEZZA_ATTESA:
        risultato = Result.failure(f'La lunghezza della riga {conteggio} non è valida',
                                   info=f"Attesa: {LUNGHEZZA_ATTESA}, Ricevuta: {len(record_riga)}")
        # display_errore(risultato)
        return risultato

    dati_estratti = {
        nome: record_riga[inizio:fine].strip()  # Usiamo .strip() per pulire gli spazi
        for nome, inizio, fine in DEFINIZIONE_CAMPI
    }
    return Result.success(dati_estratti)


def crea_record_da_stringa(riga_dati: str, conteggio) -> Result:
    """Factory che crea un oggetto RecordC2 partendo da una stringa."""
    # try:
    estrazione_result = estrai_dati_riga(riga_dati, conteggio)
    if estrazione_result.is_failure():
        return estrazione_result

    dati_estratti = estrazione_result.risultato

    builder = RecordC2Builder()

    # Popolamento dinamico del builder
    for nome_campo, valore in dati_estratti.items():

        # if nome_campo == 'progressivo_riga_per_ricetta':
        #     if valore == '99':
        #         st.write('valore 99')

        # if nome_campo == 'posizione_dell_utente_nei_confronti_del_ticket':
        #     if valore in valori_per_posizione_dell_utente_nei_confronti_del_ticket:
        #         st.success(f"valore corretto: {valore}, significato: {valori_per_posizione_dell_utente_nei_confronti_del_ticket[valore]['messaggio']}")
        #     else:
        #         st.error(f"valore errato: {valore}")

        setter_method_name = f"set_{nome_campo}"
        if hasattr(builder, setter_method_name):
            getattr(builder, setter_method_name)(valore)

    record_result = RecordC2.crea(builder)

    if hasattr(record_result, 'is_failure') and record_result.is_failure():
        info_errore_originale = f"{record_result.errore}: {record_result.info}"

        return Result.failure(
            f"Errore nella validazione dei dati alla riga {conteggio}",
            info=info_errore_originale
        )

    return Result.success(record_result)

    # except (ValidationError, KeyError) as e:
    #     risultato =  Result.failure("Errore nella creazione del RecordC2 dalla stringa", info=str(e))
    #     display_errore(risultato)
    #     return


class FileC2Repository:

    def __init__(self):
        self.limite = 100
    def carica_da_file(self, file_path: str) -> Result:
        """
        Legge un file di testo, processa ogni riga per creare un oggetto RecordC2,
        e restituisce un oggetto FileC2 che li contiene tutti.
        """
        if not os.path.exists(file_path):
            return Result.failure(f"File non trovato al percorso: {file_path}")

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
                        # return Result.failure(
                        #     f"Errore nella lettura del file alla riga {n_riga}",
                        #     info=record_result.errore
                        # )
                        display_errore(record_result)
                        raise

                    lista_record_oggetti.append(record_result.risultato)

            # Se tutte le righe sono state processate con successo, crea l'oggetto FileC2
            nome_file = os.path.basename(file_path)
            oggetto_file_C2 = FileC2.crea(lista_record_oggetti, nome_file=nome_file)

            return Result.success(oggetto_file_C2)

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




    def caricamento_su_database(self, file:FileC2, tabella: str):
        # st.write(file)
        connessione:MySQLConnection = get_connection().risultato
        # st.write(file)

        if not file:
            st.warning('Nessun dato da caricare per File C2')
            return

        column_names = list(DatiRecordC2Model.model_fields.keys())

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

            # st.success(f"Caricamento File C2 su DataBase completato con successo")

            return Result.success(f"Caricamento File C2 su DataBase completato con successo")
        except Error as e:
            # st.error(f"Errore durante il caricamento dei dati File C2 su database: {e}")

            if connessione:
                connessione.rollback()
            return Result.failure(f"Errore durante il caricamento dei dati File C2 su database: {e}")

        finally:
            if cursor:
                cursor.close()
            if connessione and connessione.is_connected():
                connessione.close()
