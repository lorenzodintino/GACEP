import streamlit as st
from applicazione import App



class OperazioneCaricaFileDiTesto(App):
    def __init__(self):
        super().__init__()



    def esegui(self):
        st.write('OPERAZIONE ESEGUITA')