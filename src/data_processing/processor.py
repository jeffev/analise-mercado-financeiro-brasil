# Importar bibliotecas
import pandas as pd
import numpy as np
import yfinance as yf
from tqdm import tqdm

# Função para calcular a média do preço de fechamento para um determinado ano
def close_price_mean_for_year(df, year):
    df_year = df[df.index.year == year]
    return df_year['Close'].mean()

def set_alvo(preco_ano_atual, preco_ano_seguinte):
    """
    Define o valor do campo "Alvo" com base nos preços.

    Args:
        preco_ano_atual: Preço do ano atual.
        preco_ano_seguinte: Preço do ano seguinte.

    Returns:
        String com o valor do campo "Alvo" ("Barata", "Cara" ou "Neutra").
    """
    if np.isnan(preco_ano_atual) or np.isnan(preco_ano_seguinte):
        return None
    else:
        if preco_ano_seguinte > preco_ano_atual * 1.15:
            return "Barata"
        elif preco_ano_seguinte < preco_ano_atual * 0.85:
            return "Cara"
        else:
            return "Neutra"

def processar_dados(ticker, start_date, end_date):
    data = pd.read_csv(f"data/raw/indicadores_{ticker}.csv")

    precos = yf.download((ticker+'.SA'), start=start_date, end=end_date, interval="1wk")

    precos_df = pd.DataFrame(precos)

    if precos_df.empty:
        print(f"Não foi possível baixar os dados para o ticker {ticker}.")
        return None

    data = data.drop('Tipo do Indicador', axis=1)

    data = data.rename(columns={'ATUAL': '2024'})

    df = pd.DataFrame(data)

    for col in df.columns[1:]:
        df[col] = df[col].str.replace(",", ".").str.rstrip("%")

    df.iloc[:, 1:] = df.iloc[:, 1:].replace('-', np.nan)

    for col in df.columns[1:]:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    df_transposed = df.transpose()

    df_transposed = df_transposed.reset_index()

    df_transposed.columns = df_transposed.iloc[0]

    df_transposed = df_transposed[1:]

    df_transposed = df_transposed.reset_index(drop=True)

    df_transposed = df_transposed.rename(columns={'Nome do Indicador': 'Ano'})

    df_transposed['Ticker'] = ticker

    df_transposed['D.Y'] = df_transposed['D.Y'].astype(float).fillna(0)

    df_transposed['PrecoAnoSeguinte'] = df_transposed['Ano'].astype(int).apply(lambda x: close_price_mean_for_year(precos_df, x + 1))
    df_transposed['PrecoAnoAtual'] = df_transposed['Ano'].astype(int).apply(lambda x: close_price_mean_for_year(precos_df, x))

    df_transposed['Alvo'] = df_transposed.apply(lambda x: set_alvo(x['PrecoAnoAtual'], x['PrecoAnoSeguinte']), axis=1)
    
    return df_transposed
    

#tickers das ações que compõem o Índice IBXX
tickers = [
    "VALE3", "ITUB4", "PETR4", "ELET3", "BBAS3", "BBDC4",
    "B3SA3", "ITSA4", "ABEV3", "WEGE3", "RENT3", "BPAC11",
    "SUZB3", "PRIO3", "EQTL3", "RADL3", "UGPA3", "RDOR3",
    "BRFS3", "VBBR3", "RAIL3", "JBSS3", "SBSP3", "GGBR4",
    "VIVT3", "BBSE3", "EMBR3", "ENEV3", "ASAI3", "CSAN3",
    "HAPV3", "CPLE6", "KLBN11", "ENGI11", "CMIG4", "TOTS3",
    "LREN3", "NTCO3", "TIMS3", "CCRO3", "HYPE3", "ELET6",
    "ALOS3", "STBP3", "SANB11", "TRPL4", "CSNA3", "SMFT3",
    "TAEE11", "MULT3", "RRRP3", "CYRE3", "CRFB3", "GOAU4",
    "MGLU3", "CPFE3", "CMIN3", "YDUQ3", "RECV3", "CIEL3",
    "PSSA3", "BRKM5", "IGTI11", "USIM5", "COGN3", "BRAP4",
    "POMO4", "RAIZ4", "AZUL4", "VIVA3", "SMTO3", "GMAT3",
    "ARZZ3", "CSMG3", "SLCE3", "SOMA3", "AURE3", "VAMO3",
    "FLRY3", "MRFG3", "IRBR3", "MRVE3", "ECOR3", "MDIA3",
    "DIRR3", "DXCO3", "LWSA3", "BEEF3", "ALPA4", "CVCB3",
    "EZTC3", "PETZ3", "TEND3", "MOVI3", "BHIA3", "PCAR3",
]


# Lista para armazenar os DataFrames processados
dfs = []

#data inicial e final que irá buscar na API do yahoo os valores das ações
start_date = '2007-01-01'
end_date = '2024-12-31'

# Iterar sobre a lista de tickers e chamar a função para cada um
for ticker in tqdm(tickers, desc="Processando dados"):
    df = processar_dados(ticker, start_date, end_date)
    dfs.append(df)

df_final = pd.concat(dfs)

df_final.to_csv('data/processed/dados_processados.csv', index=False)