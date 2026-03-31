from struttura import Builder,generate_setters_for
from struttura.strutturaC1 import DatiRecordC1Model



@generate_setters_for(DatiRecordC1Model)
class RecordC1Builder(Builder[DatiRecordC1Model]):
    def __init__(self):
        super().__init__(DatiRecordC1Model)