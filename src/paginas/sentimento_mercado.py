import streamlit as st
import streamlit_highcharts as hg
from utils.data_loader import get_sentimento_composto

def pagina_sentimento_mercado():
    st.title('Sentimento do Mercado')
    sentimento_composto = get_sentimento_composto()
    
    chartDef={ 'chart': { 'height': '70%',
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

    chartDef['series'][0]['data'][0]['y'] = sentimento_composto[2]  # Positivo
    chartDef['series'][1]['data'][0]['y'] = sentimento_composto[0]  # Negativo
    chartDef['series'][2]['data'][0]['y'] = sentimento_composto[1]  # Neutro

    hg.streamlit_highcharts(chartDef,450)