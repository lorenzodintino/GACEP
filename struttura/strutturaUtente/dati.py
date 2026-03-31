from typing import Optional, List
from enum import Enum
from pydantic import BaseModel, Field, EmailStr
import uuid
from datetime import date, datetime



class Sesso(str, Enum):
    M = "Maschio"
    F = "Femmina"
    X = "Non specificato"


class Ruolo(str, Enum):
    SUPERADMIN = "SUPERADMIN"
    ADMIN = "ADMIN"
    UTENTE = "UTENTE"
    GUEST = "GUEST"


class Servizio(str, Enum):
    GACEP = 'Gacep'




class DatiUtenteModel(BaseModel):
    uuid: str = Field(default_factory= lambda: str(uuid.uuid4()), max_length=100)
    username: str = Field(..., min_length=3, max_length=30)
    codice_fiscale: Optional[str] = Field(default=None, min_length=16, max_length=16)
    email: EmailStr = Field(..., max_length=100)
    password: str = Field(...,)
    nome: Optional[str] = Field(default=None)
    cognome: Optional[str] = Field(default=None)
    via: Optional[str] = Field(default=None)
    civico: Optional[str] = Field(default=None)
    cap: Optional[str] = Field(default=None)
    citta: Optional[str] = Field(default=None)
    provincia: Optional[str] = Field(default=None)
    nazione: Optional[str] = Field(default=None)
    data_nascita: Optional[date] = Field(default=None)
    telefono: Optional[str] = Field(default=None, max_length=100)
    sesso: Sesso = Field(default=Sesso.X)
    ruolo: Ruolo = Field(default=Ruolo.GUEST)
    data_registrazione: datetime = Field(default_factory=datetime.now)
    ultimo_accesso: Optional[datetime] = Field(default=None)
    data_ultima_modifica: Optional[datetime] = Field(default=None)
    stato_attivo: bool = Field(default=True)
    servizio: List[Servizio] = Field(default_factory=list)
    primo_accesso: bool = Field(default=True)
    note: Optional[str] = Field(default=None)




    class Config:



        pass