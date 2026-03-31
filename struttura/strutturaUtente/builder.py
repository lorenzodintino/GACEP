import bcrypt
from datetime import date
from struttura import Builder
from struttura.strutturaUtente import DatiUtenteModel, Sesso, Servizio, Ruolo



class UtenteBuilder(Builder[DatiUtenteModel]):
    
    def __init__(self):
        
        super().__init__(DatiUtenteModel)

    def set_username(self, username: str):
        return self._set("username", username)

    def set_email(self, email: str):
        return self._set("email", email)

    def set_password(self, password: str):
        password_bytes = password.encode("utf-8")
        salt = bcrypt.gensalt()
        hash_password = bcrypt.hashpw(password_bytes, salt)
        return self._set("password", hash_password.decode("utf-8"))

    def set_nome(self, nome: str):
        return self._set("nome", nome)

    def set_cognome(self, cognome: str):
        return self._set("cognome", cognome)

    def set_nome_completo(self, nome: str, cognome: str):
        self.set_nome(nome)
        self.set_cognome(cognome)
        return self

    def set_codice_fiscale(self, codice_fiscale: str):
        return self._set("codice_fiscale", codice_fiscale.upper())

    def set_via(self, via: str):
        return self._set("via", via)

    def set_civico(self, civico: str):
        return self._set("civico", civico)

    def set_cap(self, cap: str):
        return self._set("cap", cap)

    def set_citta(self, citta: str):
        return self._set("citta", citta)

    def set_provincia(self, provincia: str):
        return self._set("provincia", provincia)

    def set_nazione(self, nazione: str):
        return self._set("nazione", nazione)

    def set_data_nascita(self, data_nascita: date):
        return self._set("data_nascita", data_nascita)

    def set_telefono(self, telefono: str):
        return self._set("telefono", telefono)

    def set_sesso(self, sesso: Sesso):
        return self._set("sesso", sesso)

    def set_ruolo(self, ruolo: Ruolo):
        return self._set("ruolo", ruolo)

    def add_servizio(self, servizio_to_add: Servizio):
        if "servizio" not in self.dati_builder:
            self.dati_builder["servizio"] = []
        if servizio_to_add not in self.dati_builder["servizio"]:
            self.dati_builder["servizio"].append(servizio_to_add)
        return self

    def remove_servizio(self, servizio_to_remove: Servizio):
        if "servizio" in self.dati_builder and servizio_to_remove in self.dati_builder["servizio"]:
            self.dati_builder["servizio"].remove(servizio_to_remove)
        return self