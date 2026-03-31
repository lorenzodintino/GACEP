from struttura.strutturaDB import get_connection
from mysql.connector import Error
from mysql.connector import MySQLConnection
from struttura.strutturaResult import Result, display_errore


class OperazioneDB:
    def __init__(self):
        self.connessione: MySQLConnection = get_connection().risultato

        try:
            self.cursor = self.connessione.cursor()
        except Error as e:
            if self.connessione.is_connected():
                self.connessione.rollback()
            risultato = Result.failure(f"Errore cursor DB: {e}")
            display_errore(risultato)
            return




    def query_select_all(self, query, params=None):
        try:
            self.cursor.execute(query, params)
            results = self.cursor.fetchall()
            risultato = Result.success(results)
            return risultato

        except Error as e:
            risultato = Result.failure(f"Errore durante esecuzione query: {query}; ERRORE: {e}")
            display_errore(risultato)
            return


    def svuota_tabella(self, tabella:str):
        query = f"""TRUNCATE TABLE {tabella}"""
        try:
            self.cursor.execute(query)
            self.connessione.commit()
            print(f"tabella {tabella} svuotata con successo")
            return
        except Error as e:
            self.connessione.rollback()
            risultato = Result.failure(f"Errore DB durante svuotamento tabella {tabella}: {e}")
            display_errore(risultato)
            return



