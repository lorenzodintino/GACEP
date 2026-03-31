from typing import Any, List, Optional, get_origin, get_args, Union
from pydantic import BaseModel, Field, EmailStr
from pydantic.fields import FieldInfo
from mysql.connector import Error, MySQLConnection
from mysql.connector.cursor import MySQLCursor
from enum import Enum
from datetime import datetime, date
from types import UnionType
import inspect


from struttura.strutturaResult import Result, display_errore
from struttura.strutturaDB import get_connection
from struttura.strutturaLogger import crea_log

logger = crea_log()




def _mappa_tipo_pydantic_a_mysql(field_type: Any, field_info: FieldInfo) -> str:
    origin = get_origin(field_type)

    if origin in (Union, UnionType):
        args = [arg for arg in get_args(field_type) if arg is not type(None)]
        if len(args) == 1:
            field_type = args[0]
            origin = get_origin(field_type)
        else:

            # return 'JSON'
            return 'TEXT'

    if origin in (List, list) or (inspect.isclass(field_type) and issubclass(field_type, BaseModel)):
        # return 'JSON'
        return 'TEXT'
    elif not inspect.isclass(field_type):
        return 'TEXT'
    elif issubclass(field_type, Enum):
        enum_values = ', '.join(f"'{e.value}'" for e in field_type)
        return f"ENUM({enum_values})"
    elif issubclass(field_type, bool):
        return "TINYINT(1)"
    elif issubclass(field_type, int):
        return "INT"
    elif issubclass(field_type, float):
        return "DOUBLE"
    elif issubclass(field_type, datetime):
        return "DATETIME"
    elif issubclass(field_type, date):
        return "DATE"
    elif field_type is EmailStr or issubclass(field_type, str):
        max_length = getattr(field_info, 'max_length', None)
        return f"VARCHAR({max_length or 191})"
    else:
         return "TEXT"
def _get_colonne_esistenti(cursor: MySQLCursor, table_name: str) -> Result:
    try:
        query = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = %s"
        cursor.execute(query, (table_name,))
        colonne = [row[0] for row in cursor.fetchall()]
        return Result.success(colonne)
    except Error as e:
        risultato = Result.failure(
            errore=f"Impossibile leggere lo schema delle tabelle",
            info=e
        )

        logger.error(risultato.errore)
        logger.critical(risultato.info)
        display_errore(risultato)
        raise


def _genera_definizione_colonna(name: str, field:FieldInfo, unique_fields: List[str]) -> str:
    sql_type = _mappa_tipo_pydantic_a_mysql(field.annotation, field)

    is_nullable = get_origin(field.annotation) in (Union, UnionType) and type(None) in get_args(field.annotation)

    null_constraint = "" if is_nullable else " NOT NULL"

    unique_constraint = " UNIQUE" if name in unique_fields else ""

    return f"`{name}` {sql_type}{null_constraint}{unique_constraint}"



def _crea_nuova_tabella(cursor: MySQLCursor, model: type[BaseModel], table_name: str, unique_fields: List[str]) -> None:
    defs = []
    for name, field in model.model_fields.items():
        defs.append(_genera_definizione_colonna(name, field, unique_fields))

    defs.append("PRIMARY KEY (`uuid`)")

    query = f"CREATE TABLE `{table_name}` ({', '.join(defs)})"

    logger.info(f"Query generata per la tabella '{table_name}'")
    logger.info(query)

    cursor.execute(query)

    logger.info('Query eseguita con successo')

def _aggiorna_tabella_esistente(cursor:MySQLCursor, model:type[BaseModel], table_name:str,unique_fields:List[str], colonne_db:set) -> Result:
    model_field_names = set(model.model_fields.keys())

    colonne_db_set = set(colonne_db)
    colonne_mancanti = model_field_names - colonne_db_set

    if not colonne_mancanti:
        logger.info(f"Nessuna colonna mancante trovata. La tabella '{table_name}' è già sincronizzata.")

        return Result.success(f"La tabella '{table_name}' è già sincronizzata.",info='nessuna_modifica')

    logger.info(f"Colonne mancanti trovate per la tabella '{table_name}': {sorted(list(colonne_mancanti))}")

    alter_statements = []
    for name in sorted(list(colonne_mancanti)):
        field = model.model_fields[name]
        col_def = _genera_definizione_colonna(name, field, unique_fields)
        alter_statements.append(f"ADD COLUMN {col_def}")

    query = f"ALTER TABLE `{table_name}` {', '.join(alter_statements)}"

    logger.info(f'Query generata: {query}')

    cursor.execute(query)

    logger.info('Query eseguita con successo')

    msg = f"Tabella '{table_name}' aggiornata. Aggiunte {len(colonne_mancanti)} colonne: {', '.join(sorted(list(colonne_mancanti)))}."
    return Result.success(msg)





def sincronizza_tabella(model: type[BaseModel], table_name: str, unique_fields:Optional[List[str]] = None) -> Result:


    logger.info(f"Inizio sincronizzazione per la tabella '{table_name}'")
    unique_fields = unique_fields or []


    logger.info("Tentativo di connessione al database")

    conn_result = get_connection()

    connection:MySQLConnection = conn_result.risultato

    try:
        logger.info(f"Lettura dello schema esistente per '{table_name}'...")
        cursor = connection.cursor()

        colonne_db_result = _get_colonne_esistenti(cursor, table_name)

        colonne_db = colonne_db_result.risultato
        tabella_esiste = bool(colonne_db)

        logger.info(f"Trovate {len(colonne_db)} colonne esistenti: {colonne_db if colonne_db else 'Nessuna.'}")

        if not tabella_esiste:
            logger.info(f"La tabella '{table_name}' non esiste. Si procedera con la creazione.")

            _crea_nuova_tabella(cursor, model, table_name, unique_fields)
            connection.commit()
            return Result.success(f"Tabella '{table_name}' creata con successo")
        else:
            logger.info(f"La tabella '{table_name}' esiste. Si verificherà la necessità di un aggiornamento.")

            update_result = _aggiorna_tabella_esistente(cursor, model, table_name, unique_fields, colonne_db)
            if update_result.info != 'nessuna_modifica':
                connection.commit()
            return update_result

    except Error as e:

        risultato = Result.failure(
            f"Errore SQL durante la sincronizzazione della tabella '{table_name}'",
            info=e
        )

        logger.error(risultato.errore)
        logger.critical(risultato.info)

        display_errore(risultato)
        raise
    finally:
        if connection and connection.is_connected():
            logger.info(f"Chiusura della connessione al database")
            cursor.close()
            connection.close()
