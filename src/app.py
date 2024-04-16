import streamlit as st
from streamlit_option_menu import option_menu
from paginas.previsao_acoes import pagina_previsao_acoes
from paginas.lista_acoes import pagina_lista_acoes
from paginas.sentimento_mercado import pagina_sentimento_mercado

st.set_page_config(page_title="Investlink")

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
