# Projeto de Previsão de Ações

Este projeto visa prever se a ação esta cara, barata ou netra utilizando indicadores financeiros extraídos do mercado brasileiro por meio de webscraping no site StatusInvest. Além disso, inclui análise exploratória dos dados e treinamento de modelos de machine learning.

## Bônus

### Lista de Ações com Fórmula de Graham

Para visualizar ações em potencial, foi implementada a fórmula de Graham para avaliação. A fórmula de Graham considera o preço da ação, o lucro por ação (LPA) e o preço sobre o lucro (P/L) para determinar se uma ação está subvalorizada, sobrevalorizada ou com preço justo. A fórmula é dada por:

### Análise de Sentimento do Mercado

Foi realizada uma análise de sentimento do mercado utilizando as últimas notícias do site br.investing.com. As notícias foram analisadas para determinar se o sentimento geral do mercado é positivo, neutro ou negativo. Isso pode fornecer insights adicionais para a tomada de decisão em relação às previsões das ações.

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
