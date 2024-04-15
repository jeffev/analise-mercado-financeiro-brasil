import streamlit as st
import pandas as pd
import streamlit_highcharts as hg

from joblib import load
from streamlit_option_menu import option_menu
from utils.utils import colors
from utils.data_loader import get_sentimento_composto, load_data
from utils.model import prever_classificacao_acao

st.set_page_config(page_title="Investlink")

sentimento_composto = get_sentimento_composto()
df = load_data()
gb_model = load('data/models/gradient_boosting_model.joblib')

def pagina_previsao_acoes():
    st.title('Previsão de Ações')
    ticker = st.text_input('Digite o ticker da ação:', key='ticker_input')
    
    if st.button('Analisar'):
        resultado_string = prever_classificacao_acao(ticker, df)
        if resultado_string is None:
            st.write(f'O ticker {ticker.upper()} é inválido. Exemplo: VALE3')
        else:
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
