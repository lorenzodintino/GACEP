from struttura.strutturaResult import Result, display_errore
from struttura.strutturaUtente import DatiUtenteModel, UtenteBuilder, Utente
from struttura.strutturaDB import gestore_dati
import bcrypt
import json
from pydantic import ValidationError
from struttura.strutturaLogger import crea_log

logger = crea_log()


class UtenteRepository:

    def __init__(self, table_name:str = 'streamlit_utenti'):
        self.table_name = table_name


    def _dati_db_a_utente(self, dati_raw:dict)->Result:
        if not dati_raw:
            risultato = Result.failure('Dati grezzi non forniti', info='Nessun avviso')
            display_errore(risultato)
            logger.error(risultato.errore)
            logger.critical(risultato.info)
            raise

        if 'servizio'in dati_raw and isinstance(dati_raw.get('servizio'), str):
            try:
                dati_raw['servizio'] = json.loads(dati_raw['servizio'])
            except json.JSONDecodeError:
                dati_raw['servizio'] = []


        try:
            dati_utente_model = DatiUtenteModel(**dati_raw)
            utente = Utente(dati_utente_model)
            return Result.success(utente)
        except ValidationError as e:
            risultato = Result.failure(f"Errore di validazione nel ricostruire l'utente dal db", info=e)

            display_errore(risultato)
            logger.error(risultato.errore)
            logger.critical(risultato.info)
            raise


    def registra_utente(self, builder:UtenteBuilder)->Result:

        result_build = builder.costruisci()

        dati_nuovo_utente = result_build.risultato

        return gestore_dati.inserisci_dati(dati_modello=dati_nuovo_utente, table_name=self.table_name)


    def aggiorna(self,utente:Utente)-> Result:
        return gestore_dati.aggiorna_dati(table_name=self.table_name, uuid=utente.uuid, dati_modello=utente.dati)


    def trova_per_uuid(self,uuid:str)->Result:
        result_db = gestore_dati.seleziona_dati_per_campo(
            table_name=self.table_name,
            field_name='uuid',
            field_value=uuid
        )

        return self._dati_db_a_utente(result_db.risultato)

    def trova_per_email(self,email:str)->Result:
        result_db = gestore_dati.seleziona_dati_per_campo(
            table_name=self.table_name,
            field_name='email',
            field_value=email
        )

        return self._dati_db_a_utente(result_db.risultato)


    def autentica_utente(self, identificativo:str, password_fornita:str)->Result:
        result_db = gestore_dati.seleziona_dati_con_filtri_or(
            table_name=self.table_name,
            filtri={'username':identificativo, 'email':identificativo}
        )


        result_utente = self._dati_db_a_utente(result_db.risultato)

        utente = result_utente.risultato

        password_hash_db = utente.password.encode('utf-8')
        password_fornita_bytes = password_fornita.encode('utf-8')

        if bcrypt.checkpw(password_fornita_bytes, password_hash_db):
            return Result.success(utente)
        else:
            risultato = Result.failure(f"Credenziali non valide", info='Nessun avviso')
            display_errore(risultato)
            logger.error(risultato.errore)
            logger.critical(risultato.info)
            raise