from joblib import load
import pandas as pd
from utils.utils import class_names
from utils.data_loader import get_indicators

gb_model = load('data/models/gradient_boosting_model.joblib')

def prever_classificacao_acao(ticker, df):
    indicators = get_indicators(df, ticker)
    if indicators is None:
        return None
    df_indicators = pd.DataFrame(indicators, index=[0])
    prediction = gb_model.predict(df_indicators)
    resultado_string = class_names[prediction[0]]
    return resultado_string
