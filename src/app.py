import streamlit as st
import pandas as pd
from joblib import load
import numpy as np

class_names = {
    1: "Cara",
    2: "Barata",
    3: "Neutra"
}

colors = {
    'Barata': 'green',
    'Cara': 'red',
    'Neutra': 'blue'
}

indicators_mapping = {
    "D.Y": "DY",
    "P/L": "P/L",
    "PEG RATIO": "PEG Ratio",
    "P/VP": "P/VP",
    "EV/EBITDA": "EV/EBIT",
    "EV/EBIT": "EV/EBIT",
    "P/EBITDA": "P/EBIT",
    "P/EBIT": "P/EBIT",
    "VPA": "VPA",
    "P/ATIVO": "P/ATIVOS",
    "LPA": "LPA",
    "P/SR": "PSR",
    "P/CAP. GIRO": "P/CAP. GIRO",
    "P/ATIVO CIRC. LIQ.": "P. AT CIR. LIQ.",
    "DÍV. LÍQUIDA/PL": "DIV. LIQ. / PATRI.",
    "DÍV. LÍQUIDA/EBITDA": "DIVIDA LIQUIDA / EBIT",
    "DÍV. LÍQUIDA/EBIT": "DIVIDA LIQUIDA / EBIT",
    "PL/ATIVOS": "PATRIMONIO / ATIVOS",
    "PASSIVOS/ATIVOS": "PASSIVOS / ATIVOS",
    "LIQ. CORRENTE": "LIQ. CORRENTE",
    "M. BRUTA": "MARGEM BRUTA",
    "M. EBITDA": "MARGEM EBIT",
    "M. EBIT": "MARGEM EBIT",
    "M. LÍQUIDA": "MARG. LIQUIDA",
    "ROE": "ROE",
    "ROA": "ROA",
    "ROIC": "ROIC",
    "GIRO ATIVOS": "GIRO ATIVOS",
    "CAGR RECEITAS 5 ANOS": "CAGR RECEITAS 5 ANOS",
    "CAGR LUCROS 5 ANOS": "CAGR LUCROS 5 ANOS",
    "Graam": "Graam_formula"
}

# Função personalizada para calcular a raiz quadrada apenas para valores válidos
def safe_sqrt(x):
    if x >= 0:
        return np.sqrt(x)
    else:
        return -1

model_dir = 'data/models'
gb_model = load(f'{model_dir}/gradient_boosting_model.joblib')

@st.cache_data (ttl=3600)
def load_data(file_path):
    df = pd.read_csv(file_path, sep=';')
    df.columns = df.columns.str.strip()
    
    for col in df.columns[1:]:
        df[col] = df[col].str.replace('.', '').str.replace(',', '.')

    df = df.apply(pd.to_numeric, errors='ignore')

    df.fillna(0, inplace=True)

    df['Graam_formula'] = df.apply(lambda row: safe_sqrt(22.5 * row['LPA'] * row['VPA']), axis=1)
    df['Graam_formula'] = pd.to_numeric(df['Graam_formula'], errors='coerce')
    
    df['Desconto_Graam_PRECO'] = (df['PRECO'] - df['Graam_formula']) / df['Graam_formula'] * 100

    return df

df = load_data('data/raw/statusinvest-busca-avancada.csv')

def get_indicators(ticker):
    if ticker.upper() in df['TICKER'].values:
        # Selecionar a linha correspondente ao ticker
        indicators_row = df.loc[df['TICKER'] == ticker.upper()]
        
        # Extrair os indicadores da linha
        indicators = {}
        for indicator_name, column_name in indicators_mapping.items():
            value_str = str(indicators_row[column_name].values[0]).replace(',', '.')
            indicators[indicator_name] = float(value_str)

        return indicators
    else:
        print(f"Ticker {ticker.upper()} não encontrado no arquivo CSV.")
        return None

def pagina_previsao_acoes():
    st.title('Previsão de Ações')
    ticker = st.text_input('Digite o ticker da ação:', key='ticker_input')
    
    if st.button('Analisar'):
        indicators = get_indicators(ticker)
        if indicators is None:
            st.write(f'O ticker {ticker.upper()} é inválido.')
        else:
            df = pd.DataFrame(indicators, index=[0])
            
            prediction = gb_model.predict(df)
            resultado_string = class_names[prediction[0]]
            st.markdown(f'<p style="color: {colors[resultado_string]};">A ação {ticker.upper()} está classificada como: {resultado_string}</p>', unsafe_allow_html=True)

def pagina_lista_acoes():
    st.title('Lista de Ações')
    st.write(df)

pagina_selecionada = st.sidebar.selectbox(
    'Selecione a página:',
    ['Previsão de Ações', 'Lista de Ações']
)

if pagina_selecionada == 'Previsão de Ações':
    pagina_previsao_acoes()
elif pagina_selecionada == 'Lista de Ações':
    pagina_lista_acoes()

st.write("Para saber mais sobre o projeto e acessar o código-fonte, visite o [GitHub](https://github.com/jeffev/analise-mercado-financeiro-brasil).")
