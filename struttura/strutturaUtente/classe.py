from struttura.strutturaUtente import DatiUtenteModel, UtenteBuilder
from struttura.strutturaResult import Result, display_errore
from pydantic import ValidationError
from typing import Union, Any
from datetime import datetime


class Utente:
    def __init__(self, dati: DatiUtenteModel):
        if not isinstance(dati, DatiUtenteModel):
            risultato = Result.failure("'dati' deve essere una istanza di DatiUtenteModel", info='Nessun avviso')

            display_errore(risultato)
            raise

        self._dati = dati

    @classmethod
    def crea(cls, dati_input: Union[DatiUtenteModel, UtenteBuilder]) -> Result:
        if isinstance(dati_input, UtenteBuilder):
            build_result = dati_input.costruisci()

            dati_classe = build_result.risultato
        elif isinstance(dati_input, DatiUtenteModel):
            dati_classe = dati_input
        else:
            risultato = Result.failure(f"'dati_input' deve essere una istanza di UtenteBuilder o DatiUtenteModel",
                                       info='Nessun avviso')

            display_errore(risultato)
            raise

        nuova_classe = cls(dati_classe)
        return Result.success(nuova_classe)

    def aggiorna(self, **aggiornamenti) -> Result:

        if not aggiornamenti:
            return Result.success(self, info='Nessun dato da aggiornare')

        try:

            dati_da_validare = self._dati.model_dump()
            dati_da_validare.update(aggiornamenti)

            modello_aggiornato = DatiUtenteModel(**dati_da_validare)

            self._dati = modello_aggiornato
            self._dati.data_ultima_modifica = datetime.now()

            return Result.success(self, info='Dati aggiornati correttamente')

        except ValidationError as e:
            risultato = Result.failure(f"Errore durante l aggiornamento della classe", info=e)

            display_errore(risultato)
            raise

    def __getattr__(self, attr: str) -> Any:

        if hasattr(self._dati, attr):
            return getattr(self._dati, attr)

        raise AttributeError(f"'Utente' object non ha l'attributo '{attr}'")

    @property
    def dati(self) -> DatiUtenteModel:
        """Restituisce il modello dati Pydantic sottostante."""
        return self._dati

    @property
    def dati_json(self) -> str:
        """Restituisce una rappresentazione JSON dei dati dell'utente."""
        return self._dati.model_dump_json(indent=2)

    @property
    def nome_completo(self) -> str:
        """Restituisce una stringa con nome e cognome."""
        return f"{self._dati.nome or ''} {self._dati.cognome or ''}".strip()

    #     --- METODI GET ---
    @property
    def get_uuid(self):
        return self.dati.uuid

    @property
    def get_username(self):
        return self.dati.username

    @property
    def get_codice_fiscale(self):
        return self.dati.codice_fiscale

    @property
    def get_email(self):
        return self.dati.email

    # @property
    # def get_password(self):
    #     return self.dati.password

    @property
    def get_nome(self):
        return self.dati.nome

    @property
    def get_cognome(self):
        return self.dati.cognome

    @property
    def get_via(self):
        return self.dati.via

    @property
    def get_civico(self):
        return self.dati.civico

    @property
    def get_cap(self):
        return self.dati.cap

    @property
    def get_citta(self):
        return self.dati.citta

    @property
    def get_provincia(self):
        return self.dati.provincia

    @property
    def get_nazione(self):
        return self.dati.nazione

    @property
    def get_data_nascita(self):
        return self.dati.data_nascita

    @property
    def get_telefono(self):
        return self.dati.telefono

    @property
    def get_sesso(self):
        return self.dati.sesso

    @property
    def get_ruolo(self):
        return self.dati.ruolo

    @property
    def get_data_registrazione(self):
        return self.dati.data_registrazione

    @property
    def get_ultimo_accesso(self):
        return self.dati.ultimo_accesso

    @property
    def get_data_ultima_modifica(self):
        return self.dati.data_ultima_modifica

    @property
    def get_stato_attivo(self):
        return self.dati.stato_attivo

    @property
    def get_servizio(self):
        return self.dati.servizio

    @property
    def get_primo_accesso(self):
        return self.dati.primo_accesso

    @property
    def get_note(self):
        return self.dati.note
