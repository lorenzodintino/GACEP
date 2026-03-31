from struttura import Builder,generate_setters_for
from struttura.strutturaC3 import DatiRecordC3Model



@generate_setters_for(DatiRecordC3Model)
class RecordC3Builder(Builder[DatiRecordC3Model]):
    def __init__(self):
        super().__init__(DatiRecordC3Model)