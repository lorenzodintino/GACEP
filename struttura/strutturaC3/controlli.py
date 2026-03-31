from typing import Optional

from struttura.strutturaC3 import FileC3, RecordC3
from struttura.strutturaResult import Result, display_errore

valori_per_posizione_dell_utente_nei_confronti_del_ticket = {
    '01': {
        'messaggio': 'esente totale'
    },
    '02': {
        'messaggio': 'non esente'
    }
}


class ControlloFileC3:
    def __init__(self, file: FileC3):

        self.record: Optional[RecordC3] = None
        self.fine_ricetta: bool = False
        self.lista_errori = []
        self.file: FileC3 = file
        self.riga = 0
        self.limite_massimo_errori = 100
        self.limite_raggiunto: bool = False

    def _controllo_limite_errori(self):
        if len(self.lista_errori) >= self.limite_massimo_errori:
            self.limite_raggiunto = True
        return

    def _controllo_se_fine_ricetta(self):
        if self.record.get_progressivo_riga_per_ricetta == '99':
            return True
        return False




    def controllo(self):

        for record in self.file:
            self._controllo_limite_errori()
            if self.limite_raggiunto:
                break
            self.record = record
            self.riga += 1
            self.fine_ricetta = self._controllo_se_fine_ricetta()



        if self.limite_raggiunto:
            risultato = Result.failure(
                f"Il File non può essere accettato poichè ha raggiunto la soglia massima di {self.limite_massimo_errori} errori",
                info=[f"Sono state controllate {self.riga} righe su un totale di {len(self.file.records)}",
                self.lista_errori]
            )
            # display_errore(risultato)
            return risultato

        if len(self.lista_errori) > 0:
            return Result.failure(
                self.lista_errori,
                info='LISTA_DI_ERRORI'
            )
        return Result.success(f"File valido")
