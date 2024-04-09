from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import os
import time

def fechar_pop_ups(driver):
    popups = driver.find_elements(By.CSS_SELECTOR, ".popup-fixed .btn-close")
    for popup in popups:
        try:
            WebDriverWait(driver, 3).until(EC.element_to_be_clickable(popup)).click()
            print("Popup fechado com sucesso.")
            
            time.sleep(1)
        except Exception as e:
            print("Erro ao fechar popup:", str(e))


def coletar_indicadores(ticker):
    driver = webdriver.Chrome()

    url = f"https://statusinvest.com.br/acoes/{ticker}"
    driver.get(url)

    time.sleep(1)

    try:
        fechar_pop_ups(driver)

        historico_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@title="Histórico do ativo"]'))
        )
        historico_button.click()
        
        time.sleep(1)

        fechar_pop_ups(driver)

        max_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'li[title="Máximo disponível"] a'))
        )
        driver.execute_script("arguments[0].click();", max_button)

        time.sleep(1)

        fechar_pop_ups(driver)

        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'table-history'))
        )

        os.makedirs('data/raw', exist_ok=True)
        
        filepath = os.path.join('data', 'raw', f'indicadores_{ticker}.csv')
        with open(filepath, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            
            table = driver.find_element(By.CSS_SELECTOR, ".table-history")

            # Extrai e escreve os cabeçalhos das colunas
            headers = table.find_element(By.CSS_SELECTOR, ".tr").find_elements(By.CSS_SELECTOR, ".th")
            header_row = ['Tipo do Indicador', 'Nome do Indicador'] + [header.text for header in headers]
            writer.writerow(header_row)

            # Identifica todos os grupos de indicadores
            groups = driver.find_elements(By.CSS_SELECTOR, ".indicator-historical-container .indicators")
            for group in groups:
                # Encontra e escreve o nome do grupo de indicadores
                indicador_nome_grupo = group.find_element(By.CSS_SELECTOR, ".indicador-name strong").text

                # Encontra a tabela dentro do grupo
                table = group.find_element(By.CSS_SELECTOR, ".table-history")
                
                # Extrai os nomes dos indicadores dentro do grupo
                nomes_indicadores = [nome.text for nome in group.find_elements(By.CSS_SELECTOR, "h3.title")]

                # Extrai e escreve os dados das linhas da tabela
                data_rows = table.find_elements(By.CSS_SELECTOR, ".tr")[1:]  # Ignora a linha de cabeçalho
                for i, row in enumerate(data_rows):
                    data_cells = row.find_elements(By.CSS_SELECTOR, ".td")  # Ajuste o seletor se necessário
                    row_data = [indicador_nome_grupo, nomes_indicadores[i]] + [cell.text for cell in data_cells]
                    writer.writerow(row_data)

    finally:
        driver.quit()



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

# Iterar sobre a lista de tickers e chamar a função para cada um
for ticker in tickers:
    coletar_indicadores(ticker)
    print(f"Indicadores coletados para {ticker}")