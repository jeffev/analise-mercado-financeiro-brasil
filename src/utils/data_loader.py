import numpy as np
import pandas as pd
from joblib import load
from utils.utils import indicators_mapping, safe_sqrt

model_dir = 'data/models'
gb_model = load(f'{model_dir}/gradient_boosting_model.joblib')

def get_sentimento_composto():
    sentimento_composto = np.load("data/processed/sentimento_composto.npy")
    sentimento_composto = [round(valor * 100, 2) for valor in sentimento_composto]
    return sentimento_composto

def load_data():
    df = pd.read_csv("data/raw/statusinvest-busca-avancada.csv", sep=';')
    df.columns = df.columns.str.strip()

    for col in df.columns[1:]:
        df[col] = df[col].str.replace('.', '').str.replace(',', '.')
        try:
            df[col] = pd.to_numeric(df[col])
        except ValueError as e:
            print(f"Erro ao converter valores para números na coluna {col}: {e}")
            df[col] = pd.to_numeric(df[col], errors='coerce')

    df.fillna(0, inplace=True)

    df['Graam_formula'] = df.apply(lambda row: safe_sqrt(22.5 * row['LPA'] * row['VPA']), axis=1)
    df['Graam_formula'] = pd.to_numeric(df['Graam_formula'], errors='coerce')

    df['Desconto_Graam_PRECO'] = (df['PRECO'] - df['Graam_formula']) / df['Graam_formula'] * 100

    df.set_index('TICKER', inplace=True)

    return df

def get_indicators(df, ticker):
    if ticker.strip().upper() in df.index.str.strip().str.upper():
        indicators_row = df.loc[ticker.strip().upper()]

        indicators = {}
        for indicator_name, column_name in indicators_mapping.items():
            value_str = str(indicators_row[column_name]).replace(',', '.')
            indicators[indicator_name] = float(value_str)

        return indicators
    else:
        return None
