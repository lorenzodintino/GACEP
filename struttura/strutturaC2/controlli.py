from typing import Optional
import streamlit as st
from struttura.strutturaC2 import FileC2, RecordC2
from struttura.strutturaResult import Result, display_errore


valori_per_posizione_dell_utente_nei_confronti_del_ticket = {
    '01': {
        'messaggio': 'esente totale'
    },
    '02': {
        'messaggio': 'non esente'
    }
}


class ControlloFileC2:
    def __init__(self, file: FileC2):

        self.record: Optional[RecordC2] = None
        self.fine_ricetta: bool = False
        self.lista_errori = []
        self.file: FileC2 = file
        self.riga = 0
        self.limite_massimo_errori = 100
        self.limite_raggiunto: bool = False

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
        if self.record.get_numero_ricetta  == '':
            self.lista_errori.append(
                {
                    "riga": self.riga,
                    "messaggio": f"Valore per il campo anumero ricetta è obligatorio.",
                    "valore": self.record.get_numero_ricetta
                }
            )
            return
        if self.record.get_progressivo_riga_per_ricetta  == '':
            self.lista_errori.append(
                {
                    "riga": self.riga,
                    "messaggio": f"Valore per il campo  progressivo_riga_per_ricetta è obligatorio.",
                    "valore": self.record.get_progressivo_riga_per_ricetta
                }
            )
            return

        if self.record.get_data == '' and self.record.get_progressivo_riga_per_ricetta != '99':
            self.lista_errori.append(
                {
                    "riga": self.riga,
                    "messaggio": f"Valore per il campo  data è obligatorio.",
                    "valore": self.record.get_data
                }
            )
            return

        if self.record.get_codifica_nomenclatore == '' and self.record.get_progressivo_riga_per_ricetta!= '99':
            self.lista_errori.append(
                {
                    "riga": self.riga,
                    "messaggio": f"Valore per codifica_nomenclatore è obligatorio.",
                    "valore": self.record.get_codifica_nomenclatore
                }
            )
            return
        if self.record.get_codice_prestazione == '' and self.record.get_progressivo_riga_per_ricetta!= '99':
            self.lista_errori.append(
                {
                    "riga": self.riga,
                    "messaggio": f"Valore per codice_prestazione è obligatorio.",
                    "valore": self.record.get_codice_prestazione
                }
            )
            return
        if self.record.get_quantita == '0':
            self.lista_errori.append(
                {
                    "riga": self.riga,
                    "messaggio": f"Valore per quantità è obligatorio.",
                    "valore": self.record.get_quantita
                }
            )
            return
        if (self.record.get_posizione_dell_utente_nei_confronti_del_ticket != '01' and 
            self.record.get_posizione_dell_utente_nei_confronti_del_ticket != '02'):
            self.lista_errori.append(
                {
                    "riga": self.riga,
                    "messaggio": f"Valore per posizione_dell_utente_nei_confronti_del_ticket è errato.",
                    "valore": self.record.get_posizione_dell_utente_nei_confronti_del_ticket
                }
            )
            return
        if (self.record.get_progressivo_riga_per_ricetta == '99' and 
            self.record.get_importo_ticket  == '0'):
            self.lista_errori.append(
                {
                    "riga": self.riga,
                    "messaggio": f"Valore per importo ticket quando progressivo riga è 99 non può essere 0.",
                    "valore": self.record.get_progressivo_riga_per_ricetta
                }
            )
            return

        if (self.record.get_importo_totale == '0'):
            self.lista_errori.append(
                {
                    "riga": self.riga,
                    "messaggio": f"Valore per importo_totale non può essere 0.",
                    "valore": self.record.get_importo_totale
                }
            )
            return
        if (self.record.get_posizione_contabile == '' ): 
            self.lista_errori.append(
                {
                    "riga": self.riga,
                    "messaggio": f"Valore per posizione_contabile non può essere NULL.",
                    "valore": self.record.get_posizione_contabile
                }
            )
            return
        if (self.record.get_id == '' ): 
            self.lista_errori.append(
                {
                    "riga": self.riga,
                    "messaggio": f"Valore per campo ID non può essere NULL.",
                    "valore": self.record.get_id
                }
            )
            return
        if (self.record.get_posizione_contabile == '3' and
            self.record.get_regione_iniziale_addebito == ''): 
            self.lista_errori.append(
                {
                    "riga": self.riga,
                    "messaggio": f"Valore per campo regione iniziale di addebito in questo caso non può essere NULL.",
                    "valore": self.record.get_regione_iniziale_addebito
                }
            )
            return
        if (self.record.get_tipo_erogazione not in('A','P','D','S')): 
            self.lista_errori.append(
                {
                    "riga": self.riga,
                    "messaggio": f"Valore per campo Tipo erogazione non è corretto (A,P,D,S).",
                    "valore": self.record.get_tipo_erogazione
                }
            )
            return
        if (self.record.get_classe_priorita_prenotazione == '' and
            self.record.get_tipo_prestazione =='1'): 
            self.lista_errori.append(
                {
                    "riga": self.riga,
                    "messaggio": f"Valore per campo classe priorità prenotazione non può essere null se Tipo prestazione = 1 .",
                    "valore": self.record.get_classe_priorita_prenotazione
                }
            )
            return
        if (self.record.get_codice_esenzione == '' and
            self.record.get_tipo_erogazione =='S' and self.record.get_posizione_dell_utente_nei_confronti_del_ticket == '01' and
            self.record.get_progressivo_riga_per_ricetta == '99'):
            self.lista_errori.append(
                {
                    "riga": self.riga,
                    "messaggio": f"Valore per campo codice esenzione non può essere null se Tipo erogazione = 1  e ticket = 01.",
                    "valore": self.record.get_codice_esenzione
                }
            )
            return
        if (self.record.get_tipo_struttura == ''): 
            self.lista_errori.append(
                {
                    "riga": self.riga,
                    "messaggio": f"Valore per campo tipo struttura non può essere null ",
                    "valore": self.record.get_tipo_struttura
                }
            )
            return
        if (self.record.get_quota_compartecipazione_alla_spesa == '0' and
             self.record.get_progressivo_riga_per_ricetta == '99'):
            self.lista_errori.append(
                {
                    "riga": self.riga,
                    "messaggio": f"Valore per campo quota compartecipazione non può essere 0 per prog. riga 99 ",
                    "valore": self.record.get_quota_compartecipazione_alla_spesa
                }
            )
            return
        if (self.record.get_quota_compartecipazione_alla_spesa != '0' and
             self.record.get_progressivo_riga_per_ricetta != '99'):
            self.lista_errori.append(
                {
                    "riga": self.riga,
                    "messaggio": f"Valore per campo quota compartecipazione non può essere <> 0 per prog. riga <> 99 ",
                    "valore": self.record.get_quota_compartecipazione_alla_spesa
                }
            )
            return
        if (self.record.get_fatturato_al_lordo_ticket == '0' and
             self.record.get_progressivo_riga_per_ricetta == '99' and
             self.record.get_tipo_struttura != '1'):
            self.lista_errori.append(
                {
                    "riga": self.riga,
                    "messaggio": f"Valore per campo fatturato lordo non può essere 0 per tipo struttura diversa da 1 e prog. riga 99 ",
                    "valore": self.record.get_fatturato_al_lordo_ticket
                }
            )
            return  
        if (self.record.get_numero_fattura == '0' and
             self.record.get_progressivo_riga_per_ricetta == '99' ):
            self.lista_errori.append(
                {
                    "riga": self.riga,
                    "messaggio": f"Valore per campo numero fattura non può essere 0 per prog. riga 99 ",
                    "valore": self.record.get_numero_fattura
                }
            )
            return
        if (self.record.get_data_fattura== '0' and
             self.record.get_progressivo_riga_per_ricetta == '99'):
            self.lista_errori.append(
                {
                    "riga": self.riga,
                    "messaggio": f"Valore per campo data fattura non può essere 0 per prog. riga 99 ",
                    "valore": self.record.get_data_fattura
                }
            )
            return
        if (self.record.get_fatturato_al_netto_ticket== '0' and
             self.record.get_progressivo_riga_per_ricetta == '99' and
             self.record.get_tipo_struttura != '1'): 
            self.lista_errori.append(
                {
                    "riga": self.riga,
                    "messaggio": f"Valore per campo fatturato al netto del ticket non può essere 0 per prog. riga 99 e tipo strutture <> 1 ",
                    "valore": self.record.get_fatturato_al_netto_ticket
                }
            )
            return
        if (self.record.get_liquidato == '0' and
             self.record.get_progressivo_riga_per_ricetta == '99' ):
            self.lista_errori.append(
                {
                    "riga": self.riga,
                    "messaggio": f"Valore per campo liquidato non può essere 0 per prog. riga 99  ",
                    "valore": self.record.get_liquidato
                }
            )
            return
        if (self.record.get_causa_mancata_liquidazione == '0' and
             self.record.get_progressivo_riga_per_ricetta == '99' and
            self.record.get_tipo_struttura != '1'):  
            self.lista_errori.append(
                {
                    "riga": self.riga,
                    "messaggio": f"Valore per campo causa mancata liquidazione non può essere 0 per prog. riga 99 e tipo struttura <> 1 ",
                    "valore": self.record.get_causa_mancata_liquidazione
                }
            )
            return
        if (self.record.get_causa_parziale_liquidazione == '0' and
             self.record.get_progressivo_riga_per_ricetta == '99' and
            self.record.get_tipo_struttura != '1'):  
            self.lista_errori.append(
                {
                    "riga": self.riga,
                    "messaggio": f"Valore per campo causa parziale liquidazione non può essere 0 per prog. riga 99 e tipo struttura <> 1 ",
                    "valore": self.record.get_causa_parziale_liquidazione
                }
            )
            return
        if (self.record.get_data_prenotazione == '0' and
            self.record.get_tipo_erogazione in('A','D','S') and
            self.record.get_tipo_prestazione == '1' and
             self.record.get_progressivo_riga_per_ricetta != '99' ):
            self.lista_errori.append(
                {
                    "riga": self.riga,
                    "messaggio": f"Valore per campo data prenotazione deve essere valorizzata per prog. riga <> 99, tipo erogazione A D S e tipo prestazione 1",
                    "valore": self.record.get_data_prenotazione
                }
            )
            return
        if (self.record.get_data_prima_disponibilita == '0' and
            self.record.get_tipo_erogazione in('A','D','S') and
            self.record.get_tipo_prestazione == '1' and
             self.record.get_progressivo_riga_per_ricetta != '99' ):
            self.lista_errori.append(
                {
                    "riga": self.riga,
                    "messaggio": f"Valore per campo data prima disponibilità deve essere valorizzata per prog. riga <> 99, tipo erogazione A D S e tipo prestazione 1",
                    "valore": self.record.get_data_prima_disponibilita
                }
            )
            return
        if (self.record.get_data_primo_appuntamento == '0' and
            self.record.get_tipo_erogazione in('A','D','S') and
            self.record.get_tipo_prestazione == '1' and
             self.record.get_progressivo_riga_per_ricetta != '99' ):
            self.lista_errori.append(
                {
                    "riga": self.riga,
                    "messaggio": f"Valore per campo data primo appuntamento deve essere valorizzata per prog. riga <> 99, tipo erogazione A D S e tipo prestazione 1",
                    "valore": self.record.get_data_primo_appuntamento
                }
            )
            return
        if (self.record.get_tipo_prestazione not in('0','1','2') and self.record.get_progressivo_riga_per_ricetta != '99' ):
            self.lista_errori.append(
                {
                    "riga": self.riga,
                    "messaggio": f"Valore per campo tipo prestazione deve essere valorizzata 0 1 2",
                    "valore": self.record.get_tipo_prestazione
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

    def _controllo_importo_ticket(self):
        valore = self.record.get_importo_ticket
        zero = '0000,00'
        if self.fine_ricetta:

            if valore == zero:
                self.lista_errori.append(
                    {
                        "riga": self.riga,
                        "messaggio": f"Nella riga 99 (fine ricetta) il campo 'importo_ticket' non può essere a 0 ({zero})",
                        "valore": valore
                    }
                )
            pass
        else:
            if valore != zero:
                self.lista_errori.append(
                    {
                        "riga": self.riga,
                        "messaggio": f"Il campo 'importo_ticket' deve essere sempre valorizzato a: **{zero}** tranne che per la riga 99 (fine ricetta)",
                        "valore": valore
                    }
                )

    def _controllo_posizione_dell_utente_nei_confronti_del_ticket(self):
        valore = self.record.get_posizione_dell_utente_nei_confronti_del_ticket
        if self.fine_ricetta:
            if not valore in valori_per_posizione_dell_utente_nei_confronti_del_ticket:
                self.lista_errori.append(
                    {
                        "riga": self.riga,
                        "messaggio": f"Valore non atteso per campo 'posizione_dell_utente_nei_confronti_del_ticket', valori attesi: {[v for v in valori_per_posizione_dell_utente_nei_confronti_del_ticket]}",
                        "valore": valore
                    }
                )
        return


    def controllo(self):
        # return Result.success('')
        for record in self.file:

            self._controllo_limite_errori()
            if self.limite_raggiunto:
                break
            self.record = record
            # print(f"{self.record.get_quota_compartecipazione_alla_spesa} --- {self.record.get_progressivo_riga_per_ricetta} --- {self.record.get_posizione_dell_utente_nei_confronti_del_ticket}")
            self.riga += 1
            self.fine_ricetta = self._controllo_se_fine_ricetta()

            self._controllo_campi_obbligatori()

            self._controllo_posizione_dell_utente_nei_confronti_del_ticket()
            # self._controllo_importo_ticket()

        if self.limite_raggiunto:
            risultato = Result.failure(
                f"Il File non può essere accettato poichè ha raggiunto la soglia massima di {self.limite_massimo_errori} errori",
                info=[f"Sono state controllate {self.riga} righe su un totale di {len(self.file.records)}",
                self.lista_errori]
            )
            # display_errore(risultato)
            return risultato

        if len(self.lista_errori) > 0:
            return Result.failure(
                self.lista_errori,
                info='LISTA_ERRORI'
            )
        return Result.success(f"File valido")
