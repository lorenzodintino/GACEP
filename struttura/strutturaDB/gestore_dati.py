import json
from mysql.connector import Error
from pydantic import BaseModel
from enum import Enum
from typing import Any
from datetime import datetime, date

from struttura.strutturaResult import Result, display_errore
from struttura.strutturaLogger import crea_log
from struttura.strutturaDB import get_connection

logger = crea_log()


def _prepara_dati_per_sql(dati_modello: BaseModel) -> dict:
    dati_dict = dati_modello.model_dump()

    for key, value in dati_dict.items():
        if isinstance(value, list) or isinstance(value, dict):
            dati_dict[key] = json.dumps(value)
        elif isinstance(value, Enum):
            dati_dict[key] = value.value

    return dati_dict


def inserisci_dati(dati_modello: BaseModel, table_name: str) -> Result:
    dati_per_sql = _prepara_dati_per_sql(dati_modello)
    colonne = ', '.join([f"`{k}`" for k in dati_per_sql.keys()])
    segnaposto = ', '.join(["%s"] * len(dati_per_sql))
    valori = list(dati_per_sql.values())

    query = f"INSERT INTO `{table_name}` ({colonne}) VALUES ({segnaposto})"

    conn_result = get_connection()

    connection = conn_result.risultato

    try:
        cursor = connection.cursor()
        cursor.execute(query, valori)
        connection.commit()

        logger.info(f"Dati inseriti con successo in '{table_name}'")

        return Result.success(f"Dati inseriti con successo in '{table_name}'")
    except Error as e:
        if connection.is_connected():
            connection.rollback()
        risultato = Result.failure(f"Errore durante l'inserimento in '{table_name}'", info=e)

        display_errore(risultato)

        logger.error(risultato.errore)
        logger.critical(risultato.info)
        raise

    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()


def aggiorna_dati(table_name: str, uuid: str, dati_modello: BaseModel) -> Result:
    dati_per_sql = _prepara_dati_per_sql(dati_modello)
    set_clause = ', '.join([f"`{k}` = %s" for k in dati_per_sql.keys()])
    valori = list(dati_per_sql.values()) + [uuid]

    query = f"UPDATE `{table_name}` SET {set_clause} WHERE `uuid` = %s"

    conn_result = get_connection()

    connection = conn_result.risultato

    try:
        cursor = connection.cursor()
        cursor.execute(query, valori)
        connection.commit()

        logger.info(f"Dati per UUID {uuid} aggiornati con successo in '{table_name}'")

        return Result.success(f"Dati per UUID {uuid} aggiornati con successo in '{table_name}'")
    except Error as e:
        if connection.is_connected():
            connection.rollback()

        risultato = Result.failure(f"Errore SQL durante l'aggiornameto in '{table_name}'", info=e)
        display_errore(risultato)

        logger.error(risultato.errore)
        logger.critical(risultato.info)
        raise
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()


def seleziona_dati_con_filtri_or(table_name: str, filtri: dict) -> Result:
    where_conditions = " OR ".join([f"`{k}` = %s" for k in filtri.keys()])
    valori = list(filtri.values())
    query = f"SELECT * FROM `{table_name}` WHERE {where_conditions} LIMIT 1"

    conn_result = get_connection()

    connection = conn_result.risultato
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, valori)
        riga = cursor.fetchone()

        if riga:
            return Result.success(riga)
        else:
            risultato = Result.failure("Nessun dato trovato con i filtri specificati", info='Nesssun avviso')

            display_errore(risultato)

            logger.error(risultato.errore)
            logger.critical(risultato.info)

            raise

    except Error as e:
        risultato = Result.failure(f"Errore SQL durante la selezione in '{table_name}'", info=e)

        display_errore(risultato)
        logger.error(risultato.errore)
        logger.critical(risultato.info)
        raise
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()


def seleziona_dati_per_campo(table_name: str, field_name: str, field_value: Any)->Result:

    query = f"SELECT * FROM `{table_name}` WHERE `{field_name}` = %s LIMIT 1"

    conn_result = get_connection()

    connection = conn_result.risultato
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, (field_value))
        riga = cursor.fetchone()

        if riga:
            return Result.success(riga)
        else:
            risultato = Result.failure(f"Nessun dato trovato per {field_name} = {field_value}", info='Nesssun avviso')

            display_errore(risultato)

            logger.error(risultato.errore)
            logger.critical(risultato.info)

            raise

    except Error as e:
        risultato = Result.failure(f"Errore SQL durante la selezione in '{table_name}'", info=e)

        display_errore(risultato)
        logger.error(risultato.errore)
        logger.critical(risultato.info)
        raise
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
