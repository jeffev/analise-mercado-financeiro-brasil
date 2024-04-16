import streamlit as st
from utils.utils import colors
from utils.data_loader import load_data
from utils.model import prever_classificacao_acao

def pagina_previsao_acoes():
    st.title('Previsão de Ações')
    ticker = st.text_input('Digite o ticker da ação:', key='ticker_input')
    
    if st.button('Analisar'):
        df = load_data()
        resultado_string = prever_classificacao_acao(ticker, df)
        if resultado_string is None:
            st.write(f'O ticker {ticker.upper()} é inválido. Exemplo: VALE3')
        else:
            st.markdown(f'<p style="color: {colors[resultado_string]};">A ação {ticker.upper()} está classificada como: {resultado_string}</p>', unsafe_allow_html=True)
