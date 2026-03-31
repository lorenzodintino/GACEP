
from struttura.strutturaDB import get_connection
import mysql.connector
from mysql.connector import MySQLConnection
from struttura.strutturaResult import Result, display_errore





def connection():
    conn = get_connection()


    return conn




def query_select(query):

    try:
        conn: MySQLConnection = connection().risultato

        cursor = conn.cursor()

        cursor.execute(query)

        risultato = cursor.fetchall()

        return Result.success(risultato)
    except Exception as e:

        risultato = Result.failure(f'Errore esecuzione query: {query}', info=e)
        display_errore(risultato)
        return

