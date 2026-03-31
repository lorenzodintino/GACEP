import uuid
from typing import List

from pydantic import BaseModel, Field

class DatiRecordC3Model(BaseModel):
    uuid: str = Field(default_factory=lambda: str(uuid.uuid4()))
    regione_addebitante: str = Field(..., max_length=3)
    az_osp_inviante: str = Field(..., max_length=3)
    codice_struttura_erogatrice: str = Field(..., max_length=6)
    numero_ricetta: str = Field(..., max_length=16)
    progressivo_riga_per_ricetta: str = Field(..., max_length=2)
    id:str = Field(...,max_length=20)
    codice_prestazione: str = Field(..., max_length=7)
    codice_prestazione_cur: str = Field(..., max_length=8)
    branca_specialistica:str = Field(..., max_length=2)




class DatiFileC3Model(BaseModel):
    records: List[DatiRecordC3Model] = Field(default_factory=list)
    nome_file: str = Field(default="")