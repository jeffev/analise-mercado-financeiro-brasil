# Projeto de Previsão de Ações

Este projeto tem como objetivo extrair indicadores financeiros das ações do mercado brasileiro através de webscraping no site StatusInvest, processar esses dados, realizar uma análise exploratória, e finalmente, treinar um modelo de machine learning para prever se o preço de uma ação vai subir ou cair.

## Estrutura do Projeto

A estrutura do projeto é dividida nas seguintes partes:

- `data/`: Contém os dados brutos (`raw/`), processados (`processed/`) e modelos gerados (`models/`).
- `notebooks/`: Jupyter notebooks são usados para exploração e criação dos modelos (`exploration_modeling/`) e processamento (`processing/`).
- `src/`: Código-fonte para scripts de webscraping (`scraping/`) e processamento de dados (`data_processing/`).
- `requirements.txt`: Lista todas as dependências necessárias para executar o projeto.

## Como Executar

Para executar este projeto, siga os passos abaixo:

1. Clone este repositório para a sua máquina local.
2. Crie um ambiente virtual Python e ative-o:
   ```
   python -m venv venv
   source venv/bin/activate  # No Windows use `venv\Scripts\activate`
   ```
3. Instale as dependências do projeto:
   ```
   pip install -r requirements.txt
   ```
4. Execute os scripts de webscraping para coletar os dados:
   ```
   python src/scraping/scraper.py
   ```
5. Execute os scripts de processamento para processar os dados:
   ```
   python src/data_processing/processor.py
   ```
6. Explore a análise inicial e processamento e criação do modelo de dados nos Jupyter notebooks em `notebooks/exploration_modeling/previsoes_acoes.ipynb`.
7. Para rodar a aplicação do Streamlit basta rodar o camando abaixo:
   ```
   streamlit run .\src\app.py 
   ```

## Contribuindo
Sua contribuição é bem-vinda! Por favor, sinta-se à vontade para forkar o repositório, fazer suas alterações e criar um pull request.

## Autor
Jefferson Valandro - [Site Pessoal](https://jeffev.github.io/jeffersonvalandro/)

## Licença
Este projeto está licenciado sob a [Licença MIT](https://opensource.org/licenses/MIT).
