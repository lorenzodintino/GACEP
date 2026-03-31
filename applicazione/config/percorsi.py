import streamlit as st
from pathlib import Path
from pydantic import BaseModel, Field
import sys
import os


def get_base_path():
    if hasattr(sys, '_MEIPASS'):
        # Se eseguito da un bundle PyInstaller, la base è la cartella temporanea
        return sys._MEIPASS
    else:
        # Se eseguito come script .py, la base è la cartella principale del progetto.
        # Questo calcola il percorso della directory root del progetto (due livelli sopra a config)
        return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))




def get_storage():
    return 'applicazione\\storage\\'

def get_storage_new():
    """
    Restituisce il percorso completo e affidabile della cartella di storage.
    """
    base_path = get_base_path()
    # Unisce il percorso base con il percorso relativo della cartella storage
    # print(os.path.join(base_path, 'applicazione', 'storage'))
    return os.path.join(base_path, 'applicazione', 'storage') + '\\'


def get_pages():
    return 'applicazione\\views\\pages\\'




#
# if __name__ == '__main__':
#     get_storage()