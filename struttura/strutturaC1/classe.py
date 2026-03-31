from typing import Union, List

from struttura import generate_getters_for
from struttura.strutturaC1 import DatiRecordC1Model, RecordC1Builder, DatiFileC1Model
from struttura.strutturaResult import Result, display_errore


@generate_getters_for(model=DatiRecordC1Model, data_attribute_name='dati')
class RecordC1:

    def __init__(self, dati: DatiRecordC1Model):
        if not isinstance(dati, DatiRecordC1Model):
            risultato = Result.failure("'dati' deve essere una istanza di DatiRecordC1Model")

            display_errore(risultato)
            raise

        self._dati = dati

    @classmethod
    def crea(cls, dati_input: Union[DatiRecordC1Model, RecordC1Builder]):
        if isinstance(dati_input, RecordC1Builder):
            build_result = dati_input.costruisci()

            if build_result.is_failure():
                return build_result

            dati_classe = build_result.risultato
        elif isinstance(dati_input, DatiRecordC1Model):
            dati_classe = dati_input
        else:
            risultato = Result.failure(f"'dati_input' deve essere una istanza di RecordC1Builder o DatiRecordC1Model")
            display_errore(risultato)
            raise

        nuova_classe = cls(dati_classe)
        return nuova_classe

    @property
    def dati(self) -> DatiRecordC1Model:
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
    def get_medico_prescrittore(self):
        return self.dati.medico_prescrittore

    @property
    def get_cognome_dell_utente(self):
        return self.dati.cognome_dell_utente

    @property
    def get_nome_dell_utente(self):
        return self.dati.nome_dell_utente

    @property
    def get_campo_vuoto(self):
        return self.dati.campo_vuoto

    @property
    def get_codice_fiscale_dell_utente(self):
        return self.dati.codice_fiscale_dell_utente

    @property
    def get_sesso_dell_utente(self):
        return self.dati.sesso_dell_utente

    @property
    def get_data_di_nascita_dell_utente(self):
        return self.dati.data_di_nascita_dell_utente

    @property
    def get_provincia_e_comune_di_residenza(self):
        return self.dati.provincia_e_comune_di_residenza

    @property
    def get_usl_di_residenza(self):
        return self.dati.usl_di_residenza

    @property
    def get_progressivo_riga_per_ricetta(self):
        return self.dati.progressivo_riga_per_ricetta

    @property
    def get_id(self):
        return self.dati.id


class FileC1:

    def __init__(self, dati: DatiRecordC1Model):
        self._dati = dati

        self._records_objects = [RecordC1(d) for d in self._dati.records]

    @classmethod
    def crea(cls, lista_record: List[RecordC1], nome_file: str = ''):
        lista_dati_model = [rec.dati for rec in lista_record]
        dati_file_model = DatiFileC1Model(records=lista_dati_model, nome_file=nome_file)
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
