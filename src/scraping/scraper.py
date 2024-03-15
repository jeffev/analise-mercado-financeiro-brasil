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
            # Tenta clicar no botão de fechar do popup
            WebDriverWait(driver, 3).until(EC.element_to_be_clickable(popup)).click()
            print("Popup fechado com sucesso.")
            # Espera um pouco para garantir que o popup seja fechado
            time.sleep(1)  # Reduz o tempo de espera se não for necessário tanto
        except Exception as e:
            # Captura qualquer exceção que possa ocorrer durante o fechamento do popup
            print("Erro ao fechar popup:", str(e))


def coletar_indicadores(ticker):
    driver = webdriver.Chrome()

    # Abre a página com o ticker fornecido
    url = f"https://statusinvest.com.br/acoes/{ticker}"
    driver.get(url)

    # Espera para a página carregar
    time.sleep(1)

    try:
        fechar_pop_ups(driver)

        # Aguarda até que o botão Histórico esteja presente e clica nele
        historico_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@title="Histórico do ativo"]'))
        )
        historico_button.click()
        
        # Após clicar no histórico, aguarda 2 segundos
        time.sleep(1)

        fechar_pop_ups(driver)

        # Utiliza JavaScript para clicar no botão "Máx."
        max_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'li[title="Máximo disponível"] a'))
        )
        driver.execute_script("arguments[0].click();", max_button)

        # Após clicar no MAX, aguarda 2 segundos
        time.sleep(1)

        fechar_pop_ups(driver)

        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'table-history'))
        )

        # Cria o diretório se ele não existir
        os.makedirs('data/raw', exist_ok=True)
        
        # Prepara o arquivo CSV para escrita
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


#tickers das 100 ações que compõem o Índice Brasil 100 (IBXX)
tickers = [
    "ABEV3", "ALPA4", "AMER3", "ASAI3", "AZUL4", "B3SA3", "BBAS3", "BBDC3",
    "BBDC4", "BBSE3", "BEEF3", "BIDI11", "BPAC11", "BRAP4", "BRFS3", "BRKM5",
    "BRML3", "CASH3", "CCRO3", "CIEL3", "CMIG4", "COGN3", "CPFE3", "CPLE6",
    "CRFB3", "CSAN3", "CSNA3", "CVCB3", "CYRE3", "DXCO3", "ECOR3", "EGIE3",
    "ELET3", "ELET6", "EMBR3", "ENBR3", "ENEV3", "ENGI11", "EQTL3", "EZTC3",
    "FLRY3", "GGBR4", "GOAU4", "GOLL4", "HAPV3", "HYPE3", "IGTI11", "IRBR3",
    "ITSA4", "ITUB4", "JBSS3", "JHSF3", "KLBN11", "LAME4", "LCAM3", "LREN3",
    "MGLU3", "MRFG3", "MRVE3", "MULT3", "NTCO3", "PCAR3", "PETR3", "PETR4",
    "PRIO3", "QUAL3", "RADL3", "RAIL3", "RENT3", "RRRP3", "SANB11", "SBSP3",
    "SOMA3", "STBP3", "SUZB3", "TAEE11", "TIMS3", "TOTS3", "UGPA3", "USIM5",
    "VALE3", "VBBR3", "VIIA3", "VIVT3", "WEGE3", "YDUQ3"
]

# Iterar sobre a lista de tickers e chamar a função para cada um
for ticker in tickers:
    coletar_indicadores(ticker)
    print(f"Indicadores coletados para {ticker}")