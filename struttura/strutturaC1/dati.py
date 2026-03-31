import uuid
from typing import List

from pydantic import BaseModel, Field


class DatiRecordC1Model(BaseModel):
    uuid: str = Field(default_factory=lambda: str(uuid.uuid4()))
    regione_addebitante: str = Field(..., max_length=3)
    az_osp_inviante: str = Field(..., max_length=3)
    codice_struttura_erogatrice: str = Field(..., max_length=6)
    medico_prescrittore: str = Field(..., max_length=16)
    cognome_dell_utente: str = Field(..., max_length=30)
    nome_dell_utente: str = Field(..., max_length=20)
    campo_vuoto: str = Field(..., max_length=16)
    codice_fiscale_dell_utente: str = Field(..., max_length=16)
    sesso_dell_utente: str = Field(..., max_length=1)
    data_di_nascita_dell_utente: str = Field(..., max_length=8)
    provincia_e_comune_di_residenza: str = Field(..., max_length=6)
    usl_di_residenza: str = Field(..., max_length=3)
    progressivo_riga_per_ricetta: str = Field(..., max_length=2)
    id: str = Field(..., max_length=20)


class DatiFileC1Model(BaseModel):
    records: List[DatiRecordC1Model] = Field(default_factory=list)
    nome_file: str = Field(...)
