from struttura import Builder,generate_setters_for
from struttura.strutturaC2 import DatiRecordC2Model



@generate_setters_for(DatiRecordC2Model)
class RecordC2Builder(Builder[DatiRecordC2Model]):
    def __init__(self):
        super().__init__(DatiRecordC2Model)