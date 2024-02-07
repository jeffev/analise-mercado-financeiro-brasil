from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv

driver = webdriver.Chrome()

# Abre a página
driver.get("https://statusinvest.com.br/acoes/petr4")

try:
    # Aguarda até que o botão Histórico esteja presente e clica nele
    historico_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//button[@title="Histórico do ativo"]'))
    )
    historico_button.click()
    
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'table-history'))
    )
    
    # Prepara o arquivo CSV para escrita
    with open('dados_tabela.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        # Identifica todos os grupos de indicadores
        groups = driver.find_elements(By.CSS_SELECTOR, ".indicator-historical-container .indicators")
        for group in groups:
            # Encontra e escreve o nome do grupo de indicadores
            indicador_nome_grupo = group.find_element(By.CSS_SELECTOR, ".indicador-name strong").text

            # Encontra a tabela dentro do grupo
            table = group.find_element(By.CSS_SELECTOR, ".table-history")
            
            # Extrai os nomes dos indicadores dentro do grupo
            nomes_indicadores = [nome.text for nome in group.find_elements(By.CSS_SELECTOR, "h3.title")]

            # Extrai e escreve os cabeçalhos das colunas
            headers = table.find_element(By.CSS_SELECTOR, ".tr").find_elements(By.CSS_SELECTOR, ".th")
            header_row = ['Tipo do Indicador', 'Nome do Indicador'] + [header.text for header in headers]
            writer.writerow(header_row)
            
            # Extrai e escreve os dados das linhas da tabela
            data_rows = table.find_elements(By.CSS_SELECTOR, ".tr")[1:]  # Ignora a linha de cabeçalho
            for i, row in enumerate(data_rows):
                data_cells = row.find_elements(By.CSS_SELECTOR, ".td")  # Ajuste o seletor se necessário
                row_data = [indicador_nome_grupo, nomes_indicadores[i]] + [cell.text for cell in data_cells]
                writer.writerow(row_data)

            # Escreve uma linha vazia para separar os grupos de indicadores
            writer.writerow([])

finally:
    driver.quit()
