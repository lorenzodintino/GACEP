from typing import Union, List

from struttura import generate_getters_for
from struttura.strutturaC3 import DatiRecordC3Model, RecordC3Builder, DatiFileC3Model
from struttura.strutturaResult import Result, display_errore


@generate_getters_for(model=DatiRecordC3Model, data_attribute_name='dati')
class RecordC3:

    def __init__(self, dati: DatiRecordC3Model):
        if not isinstance(dati, DatiRecordC3Model):
            risultato = Result.failure("'dati' deve essere una istanza di DatiRecordC3Model")

            display_errore(risultato)
            raise

        self._dati = dati

    @classmethod
    def crea(cls, dati_input: Union[DatiRecordC3Model, RecordC3Builder]):
        if isinstance(dati_input, RecordC3Builder):
            build_result = dati_input.costruisci()

            if build_result.is_failure():
                return build_result

            dati_classe = build_result.risultato
        elif isinstance(dati_input, DatiRecordC3Model):
            dati_classe = dati_input
        else:
            risultato = Result.failure(f"'dati_input' deve essere una istanza di RecordC3Builder o DatiRecordC3Model")
            display_errore(risultato)
            raise

        nuova_classe = cls(dati_classe)
        return nuova_classe

    @property
    def dati(self) -> DatiRecordC3Model:
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
    def get_id(self):
        return self.dati.id

    @property
    def get_codice_prestazione(self):
        return self.dati.codice_prestazione

    @property
    def get_codice_prestazione_cur(self):
        return self.dati.codice_prestazione_cur

    @property
    def get_branca_specialistica(self):
        return self.dati.branca_specialistica




class FileC3:

    def __init__(self, dati: DatiRecordC3Model):
        self._dati = dati

        self._records_objects = [RecordC3(d) for d in self._dati.records]

    @classmethod
    def crea(cls, lista_record: List[RecordC3], nome_file: str = ''):
        lista_dati_model = [rec.dati for rec in lista_record]
        dati_file_model = DatiFileC3Model(records=lista_dati_model, nome_file=nome_file)
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
