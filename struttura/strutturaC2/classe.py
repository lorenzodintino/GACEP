from typing import Union, List

from struttura import generate_getters_for
from struttura.strutturaC2 import DatiRecordC2Model, RecordC2Builder, DatiFileC2Model
from struttura.strutturaResult import Result, display_errore


@generate_getters_for(model=DatiRecordC2Model, data_attribute_name='dati')
class RecordC2:

    def __init__(self, dati: DatiRecordC2Model):
        if not isinstance(dati, DatiRecordC2Model):
            risultato = Result.failure("'dati' deve essere una istanza di DatiRecordC2Model")

            display_errore(risultato)
            raise

        self._dati = dati

    @classmethod
    def crea(cls, dati_input: Union[DatiRecordC2Model, RecordC2Builder]):
        if isinstance(dati_input, RecordC2Builder):
            build_result = dati_input.costruisci()

            if build_result.is_failure():
                return build_result

            dati_classe = build_result.risultato
        elif isinstance(dati_input, DatiRecordC2Model):
            dati_classe = dati_input
        else:
            risultato = Result.failure(f"'dati_input' deve essere una istanza di RecordC2Builder o DatiRecordC2Model")
            display_errore(risultato)
            raise

        nuova_classe = cls(dati_classe)
        return nuova_classe

    @property
    def dati(self) -> DatiRecordC2Model:
        """Restituisce il modello dati Pydantic sottostante."""
        return self._dati

    @property
    def dati_json(self) -> str:
        """Restituisce una rappresentazione JSON dei dati."""
        return self._dati.model_dump_json(indent=2)

    #     --- METODI GET ---

    @property
    def get_regione_addebitante(self):
        return self.dati.regione_addebitante

    @property
    def get_az_osp_inviante(self):
        return self.dati.az_osp_inviante

    @property
    def get_codice_struttura_erogatrice(self):
        return self.dati.codice_struttura_erogatrice

    @property
    def get_numero_ricetta(self):
        return self.dati.numero_ricetta

    @property
    def get_progressivo_riga_per_ricetta(self):
        return self.dati.progressivo_riga_per_ricetta

    @property
    def get_data(self):
        return self.dati.data

    @property
    def get_codifica_nomenclatore(self):
        return self.dati.codifica_nomenclatore

    @property
    def get_codice_prestazione(self):
        return self.dati.codice_prestazione

    @property
    def get_sesso_dell_utente(self):
        return self.dati.sesso_dell_utente

    @property
    def get_quantita(self):
        return self.dati.quantita

    @property
    def get_posizione_dell_utente_nei_confronti_del_ticket(self):
        return self.dati.posizione_dell_utente_nei_confronti_del_ticket

    @property
    def get_importo_ticket(self):
        return self.dati.importo_ticket

    @property
    def get_importo_totale(self):
        return self.dati.importo_totale

    @property
    def get_posizione_contabile(self):
        return self.dati.posizione_contabile

    @property
    def get_errori_anagrafici(self):
        return self.dati.errori_anagrafici

    @property
    def get_errori_residenza(self):
        return self.dati.errori_residenza

    @property
    def get_errori_prestazione(self):
        return self.dati.errori_prestazione

    @property
    def get_errori_ricetta(self):
        return self.dati.errori_ricetta

    @property
    def get_errori_record(self):
        return self.dati.errori_record

    @property
    def get_errori_importo(self):
        return self.dati.errori_importo

    @property
    def get_errori_quantita(self):
        return self.dati.errori_quantita

    @property
    def get_errori_data_prestazione(self):
        return self.dati.errori_data_prestazione

    @property
    def get_errori_ricetta_2(self):
        return self.dati.errori_ricetta_2

    @property
    def get_errore_riservato(self):
        return self.dati.errore_riservato

    @property
    def get_id(self):
        return self.dati.id

    @property
    def get_regione_iniziale_addebito(self):
        return self.dati.regione_iniziale_addebito

    @property
    def get_tipo_erogazione(self):
        return self.dati.tipo_erogazione

    @property
    def get_codice_disciplina_unita_operativa_erogatrice(self):
        return self.dati.codice_disciplina_unita_operativa_erogatrice

    @property
    def get_classe_priorita_prenotazione(self):
        return self.dati.classe_priorita_prenotazione

    @property
    def get_codice_esenzione(self):
        return self.dati.codice_esenzione

    @property
    def get_tipo_struttura(self):
        return self.dati.tipo_struttura

    @property
    def get_quota_compartecipazione_alla_spesa(self):
        return self.dati.quota_compartecipazione_alla_spesa

    @property
    def get_fatturato_al_lordo_ticket(self):
        return self.dati.fatturato_al_lordo_ticket

    @property
    def get_campo_vuoto(self):
        return self.dati.campo_vuoto

    @property
    def get_numero_fattura(self):
        return self.dati.numero_fattura

    @property
    def get_data_fattura(self):
        return self.dati.data_fattura

    @property
    def get_fatturato_al_netto_ticket(self):
        return self.dati.fatturato_al_netto_ticket

    @property
    def get_liquidato(self):
        return self.dati.liquidato

    @property
    def get_causa_mancata_liquidazione(self):
        return self.dati.causa_mancata_liquidazione

    @property
    def get_causa_parziale_liquidazione(self):
        return self.dati.causa_parziale_liquidazione

    @property
    def get_codice_prestazione_cur(self):
        return self.dati.codice_prestazione_cur

    @property
    def get_branca_specialistica(self):
        return self.dati.branca_specialistica

    @property
    def get_garanzia_tempi_massimi(self):
        return self.dati.garanzia_tempi_massimi

    @property
    def get_numero_sedute_cliniche(self):
        return self.dati.numero_sedute_cliniche

    @property
    def get_data_prenotazione(self):
        return self.dati.data_prenotazione

    @property
    def get_data_prima_disponibilita(self):
        return self.dati.data_prima_disponibilita

    @property
    def get_data_primo_appuntamento(self):
        return self.dati.data_primo_appuntamento

    @property
    def get_tipo_prestazione(self):
        return self.dati.tipo_prestazione





class FileC2:

    def __init__(self, dati: DatiRecordC2Model):
        self._dati = dati

        self._records_objects = [RecordC2(d) for d in self._dati.records]

    @classmethod
    def crea(cls, lista_record: List[RecordC2], nome_file: str = ''):
        lista_dati_model = [rec.dati for rec in lista_record]
        dati_file_model = DatiFileC2Model(records=lista_dati_model, nome_file=nome_file)
        return cls(dati_file_model)

    @property
    def records(self):
        return self._records_objects

    @property
    def dati(self):
        return self._dati

    @property
    def nome_file(self):
        return self._dati.nome_file

    def __len__(self):
        return len(self._records_objects)

    def __iter__(self):
        return iter(self._records_objects)
