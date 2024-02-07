# Projeto de Análise do Mercado Financeiro Brasileiro

## Descrição do Projeto
Este projeto é um pipeline completo de Ciência de Dados que visa analisar o mercado financeiro brasileiro, especificamente o mercado de ações da B3 (Bolsa de Valores brasileira). O pipeline abrange desde a coleta de dados por web scraping até a implementação de um modelo de machine learning para prever se o preço das ações está caro ou barato.

## Estrutura do Projeto
O projeto está estruturado da seguinte forma:

- **data/**: Este diretório armazena os dados coletados por web scraping e quaisquer outros conjuntos de dados utilizados no projeto.

- **notebooks/**: Aqui estão localizados os notebooks Jupyter utilizados para explorar e analisar os dados, bem como para treinar e avaliar o modelo de machine learning.

- **src/**: Contém o código-fonte do projeto, incluindo scripts para web scraping, pré-processamento de dados, treinamento de modelos e implementação da aplicação final.

- **docs/**: Este diretório contém a documentação do projeto, incluindo este arquivo README.md e quaisquer outros documentos relevantes.

## Passos do Pipeline
O pipeline completo do projeto inclui os seguintes passos:

1. **Web Scraping**: Coleta de dados financeiros relevantes da web, incluindo indicadores de empresas listadas na B3.

2. **Armazenamento de Dados**: Os dados coletados são armazenados localmente em arquivos CSV para fácil acesso e manipulação.

3. **Pré-processamento de Dados**: Limpeza e transformação dos dados para garantir que estejam prontos para análise e modelagem.

4. **Análise de Dados**: Exploração e visualização dos dados para entender melhor os indicadores financeiros e identificar padrões.

5. **Treinamento de Modelo**: Utilização de algoritmos de machine learning para treinar um modelo capaz de prever se o preço das ações está caro ou barato.

6. **Implantação do Modelo**: Desenvolvimento de uma aplicação que recebe indicadores financeiros como entrada e utiliza o modelo treinado para fazer previsões em tempo real.

## Como Executar o Projeto
Para executar o projeto localmente, siga estas etapas:

1. Clone o repositório para o seu ambiente local:
   ```
   git clone https://github.com/jeffev/projeto-ciencia-dados-bolsa-valores.git
   ```

2. Navegue até o diretório do projeto:
   ```
   cd projeto-ciencia-dados-bolsa-valores
   ```

3. Siga as instruções específicas encontradas nos arquivos README.md dentro de cada diretório para executar os diferentes componentes do pipeline.

## Autor
Jefferson Valandro - [Site Pessoal](https://jeffev.github.io/jeffersonvalandro/)

## Licença
Este projeto está licenciado sob a [Licença MIT](https://opensource.org/licenses/MIT).
