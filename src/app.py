import streamlit as st
import pandas as pd
from joblib import load
import numpy as np

# Mapeamento dos números para os nomes das classes
class_names = {
    1: "Cara",
    2: "Barata",
    3: "Neutra"
}

# Criar um dicionário para mapear os indicadores financeiros desejados
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
    "CAGR LUCROS 5 ANOS": "CAGR LUCROS 5 ANOS"
}

# Função personalizada para calcular a raiz quadrada apenas para valores válidos
def safe_sqrt(x):
    if x >= 0:
        return np.sqrt(x)
    else:
        return -1

# Carregar o modelo treinado
model_dir = 'data/models'
gb_model = load(f'{model_dir}/gradient_boosting_model.joblib')

# Ler o arquivo CSV
df = pd.read_csv('data/raw/statusinvest-busca-avancada.csv', sep=';')
df.columns = df.columns.str.strip()


def get_indicators(ticker):
    # Verificar se o ticker está presente no arquivo CSV
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


# Função para prever se a ação está cara, barata ou neutra
def predict_price_status(ticker):
    indicators = get_indicators(ticker)

    # Transformar os indicadores em um DataFrame
    df = pd.DataFrame(indicators, index=[0])

    # Substituir valores nulos por zero
    df.fillna(0, inplace=True)

    df = df.copy()
    df['Graam'] = df.apply(lambda row: safe_sqrt(22.5 * row['LPA'] * row['VPA']), axis=1)

    # Realizar a previsão
    prediction = gb_model.predict(df)

    return prediction

# Interface do Streamlit
st.title('Análise de Ações')
ticker = st.text_input('Digite o ticker da ação:')
if st.button('Analisar'):
    indicators = get_indicators(ticker)
    if indicators is None:
        st.write(f'O ticker {ticker.upper()} é inválido.')
    else:
        df = pd.DataFrame(indicators, index=[0])
        df.fillna(0, inplace=True)
        df['Graam'] = df.apply(lambda row: safe_sqrt(22.5 * row['LPA'] * row['VPA']), axis=1)
        prediction = gb_model.predict(df)
        resultado_string = class_names[prediction[0]]
        st.write(f'A ação {ticker.upper()} está classificada como: {resultado_string}')

