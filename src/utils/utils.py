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

def safe_sqrt(x):
    """
    Calcula a raiz quadrada de um número não negativo.

    Parâmetros:
    x (float ou int): O número do qual se deseja calcular a raiz quadrada.

    Retorna:
    float: A raiz quadrada de x, se x for não negativo. Retorna -1 se x for negativo.
    """
    if x >= 0:
        return np.sqrt(x)
    else:
        return -1
