from typing import Optional

from struttura.strutturaC1 import FileC1, RecordC1
from struttura.strutturaResult import Result, display_errore
from applicazione.config import ListaPagine

valori_per_campo_sesso_dell_utente = {
    "1": {
        "messaggio": "Maschio"
    },
    "2": {
        "messaggio": "Femmina"
    }
}


class ControlloFileC1:
    def __init__(self, file: FileC1):
        self.record: Optional[RecordC1] = None
        self.fine_ricetta: bool = False
        self.lista_errori = []
        self.file: FileC1 = file
        self.riga = 0
        self.limite_massimo_errori = 100
        self.limite_raggiunto: bool = False

        # self.session_manager = SessionManager()
        # self.key = SessionKeys()

        from applicazione.config import SessionManager

        self.session = SessionManager()

    def _controllo_campi_obbligatori(self):
        if self.record.get_regione_addebitante != '130':
            self.lista_errori.append(
                {
                    "riga": self.riga,
                    "messaggio": f"Valore per il campo regione_addebitante obligatorio e deve essere uguale a 130",
                    "valore": self.record.get_regione_addebitante
                }
            )
            return
        if self.record.get_az_osp_inviante != '203':
            self.lista_errori.append(
                {
                    "riga": self.riga,
                    "messaggio": f"Valore per il campo azienda_ospedaliera_inviante è obligatorio e deve essere uguale a 203",
                    "valore": self.record.get_az_osp_inviante
                }
            )
            return
        if self.record.get_codice_struttura_erogatrice != self.session.state.files.codice_struttura_selezionata:

            self.lista_errori.append(
                {
                    "riga": self.riga,
                    "messaggio": f"Valore per il campo codice_struttura_erogatrice è obligatorio e deve essere uguale a {self.session.state.files.codice_struttura_selezionata}",
                    "valore": self.record.get_codice_struttura_erogatrice
                }
            )
            return
        if self.record.get_codice_fiscale_dell_utente == '':

            self.lista_errori.append(
                {
                    "riga": self.riga,
                    "messaggio": f"Valore per il campo codice_fiscale_dell_utente è obligatorio .",
                    "valore": self.record.get_codice_fiscale_dell_utente
                }
            )
            return
        if self.record.get_cognome_dell_utente == '':

            self.lista_errori.append(
                {
                    "riga": self.riga,
                    "messaggio": f"Valore per il campo cognome_dell_utente è obligatorio .",
                    "valore": self.record.get_cognome_dell_utente
                }
            )
            return
        if self.record.get_nome_dell_utente == '':

            self.lista_errori.append(
                {
                    "riga": self.riga,
                    "messaggio": f"Valore per il campo nome_dell_utente è obligatorio .",
                    "valore": self.record.get_nome_dell_utente
                }
            )
            return
        if self.record.get_provincia_e_comune_di_residenza == '':

            self.lista_errori.append(
                {
                    "riga": self.riga,
                    "messaggio": f"Valore per il campo provincia e comune è obligatorio .",
                    "valore": self.record.get_provincia_e_comune_di_residenza
                }
            )
            return
        if self.record.get_progressivo_riga_per_ricetta == '':

            self.lista_errori.append(
                {
                    "riga": self.riga,
                    "messaggio": f"Progressivo_riga_per_ricetta non valido .",
                    "valore": self.record.get_progressivo_riga_per_ricetta
                }
            )
            return
        if self.record.get_id == '':

            self.lista_errori.append(
                {
                    "riga": self.riga,
                    "messaggio": f"Valore identificativo ricetta non valido.",
                    "valore": self.record.get_id
                }
            )
            return
        

    def _controllo_limite_errori(self):
        if len(self.lista_errori) >= self.limite_massimo_errori:
            self.limite_raggiunto = True
        return

    def _controllo_se_fine_ricetta(self):
        if self.record.get_progressivo_riga_per_ricetta == '99':
            return True
        return False

    def _controllo_sesso_dell_utente(self):
        valore = self.record.get_sesso_dell_utente

        if not valore in valori_per_campo_sesso_dell_utente:
            self.lista_errori.append(
                {
                    "riga": self.riga,
                    "messaggio": f"Valore non atteso per campo 'sesso_dell_utente', valori attesi: {[v for v in valori_per_campo_sesso_dell_utente]}",
                    "valore": valore
                }
            )

        return

    def controllo(self):

        for record in self.file:
            self._controllo_limite_errori()
            if self.limite_raggiunto:
                break
            self.record = record
            self.riga += 1

            self.fine_ricetta = self._controllo_se_fine_ricetta()

            self._controllo_sesso_dell_utente()

            self._controllo_campi_obbligatori()

        if self.limite_raggiunto:
            risultato = Result.failure(
                f"Il File non può essere accettato poichè ha raggiunto la soglia massima di {self.limite_massimo_errori} errori",
                info=[f"Sono state controllate {self.riga} righe su un totale di {len(self.file.records)}",
                self.lista_errori]
            )

            return risultato

        if len(self.lista_errori) > 0:
            return Result.failure(
                self.lista_errori,
                info='LISTA_ERRORI'
            )
        return Result.success(f"File valido")
