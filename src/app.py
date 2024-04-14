import streamlit as st
import pandas as pd
import numpy as np
import streamlit_highcharts as hg

from joblib import load
from streamlit_option_menu import option_menu

st.set_page_config(page_title="Investlink")

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

@st.cache_data (ttl=36000)
def load_sentimento_composto():
    return np.load("data/processed/sentimento_composto.npy")

sentimento_composto = load_sentimento_composto()
sentimento_composto = [round(valor * 100, 2) for valor in sentimento_composto]

@st.cache_data (ttl=36000)
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
            st.write(f'O ticker {ticker.upper()} é inválido. Exemplo: VALE3')
        else:
            df = pd.DataFrame(indicators, index=[0])
            
            prediction = gb_model.predict(df)
            resultado_string = class_names[prediction[0]]
            st.markdown(f'<p style="color: {colors[resultado_string]};">A ação {ticker.upper()} está classificada como: {resultado_string}</p>', unsafe_allow_html=True)

def pagina_lista_acoes():
    st.title('Lista de Ações')
    st.write(df)

def pagina_sentimento_mercado():
    chartDef={ 'chart': { 'height': '90%',
                'type': 'solidgauge'},
    'pane': { 'background': [ { 'borderWidth': 0,
                                'innerRadius': '88%',
                                'radius': '112%'},
                                { 'borderWidth': 0,
                                'innerRadius': '63%',
                                'radius': '87%'},
                                { 'borderWidth': 0,
                                'innerRadius': '38%',
                                'radius': '62%'}],
                'endAngle': 360,
                'startAngle': 0},
    'plotOptions': { 'solidgauge': { 'dataLabels': { 'enabled': False},
                                    'linecap': 'round',
                                    'rounded': True,
                                    'stickyTracking': False}},
    'series': [ { 'data': [ { 'color': 'lightgreen',
                                'innerRadius': '88%',
                                'radius': '112%',
                                'y': 80}],
                    'name': 'Positivo'},
                { 'data': [ { 'color': 'red',
                                'innerRadius': '63%',
                                'radius': '87%',
                                'y': 65}],
                    'name': 'Negativo'},
                { 'data': [ { 'color': 'blue',
                                'innerRadius': '38%',
                                'radius': '62%',
                                'y': 50}],
                    'name': 'Neutro'}],
    'title': { 'style': { 'fontSize': '24px'},
                'text': 'Sentimento do mercado'},
    'tooltip': { 'backgroundColor': 'none',
                'borderWidth': 0,
                'pointFormat': '{series.name}<br><span '
                                'style="font-size:2em; '
                                'color: '
                                '{point.color}; '
                                'font-weight: '
                                'bold">{point.y}</span>',
                'positioner': { 'x': '50px',
                                'y': 100},
                'shadow': False,
                'style': { 'fontSize': '16px'},
                'valueSuffix': '%'},
    'yAxis': { 'lineWidth': 0,
                'max': 100,
                'min': 0,
                'tickPositions': []}}

    # Atualizar os valores de y nas séries
    chartDef['series'][0]['data'][0]['y'] = sentimento_composto[2]  # Positivo
    chartDef['series'][1]['data'][0]['y'] = sentimento_composto[0]  # Negativo
    chartDef['series'][2]['data'][0]['y'] = sentimento_composto[1]  # Neutro

    hg.streamlit_highcharts(chartDef,640)

with st.sidebar:
    pagina_selecionada = option_menu("Investlink", ["Previsão de Ações", 'Lista de Ações', 'Sentimento do mercado'], 
        icons=['file-earmark-bar-graph', 'list-task', 'emoji-heart-eyes'], menu_icon="cast", default_index=0)

if pagina_selecionada == 'Previsão de Ações':
    pagina_previsao_acoes()
elif pagina_selecionada == 'Lista de Ações':
    pagina_lista_acoes()
elif pagina_selecionada == 'Sentimento do mercado':
    pagina_sentimento_mercado()

st.write("Para saber mais sobre o projeto e acessar o código-fonte, visite o [GitHub](https://github.com/jeffev/analise-mercado-financeiro-brasil).")
