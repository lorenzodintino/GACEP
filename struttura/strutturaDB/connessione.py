import streamlit as st
import mysql.connector
from mysql.connector import Error
from struttura.strutturaResult import Result, display_errore
from struttura.strutturaLogger import crea_log


logger = crea_log()



def get_connection():
    try:
        db_config = st.secrets['mysql']
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            # logger.info('Connessione al database effettuata')
            return Result.success(connection)
    except Error as e:
        risultato = Result.failure("Errore durante la connessione al database")
        logger.error(risultato.errore)
        logger.critical(e)


        display_errore(risultato)
        raise