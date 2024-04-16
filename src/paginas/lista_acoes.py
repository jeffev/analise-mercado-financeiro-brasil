import streamlit as st
from utils.data_loader import load_data

def pagina_lista_acoes():
    st.title('Lista de Ações')
    df = load_data()
    st.write(df)