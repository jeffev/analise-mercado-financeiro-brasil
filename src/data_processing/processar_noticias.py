import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from tqdm import tqdm
import os

nltk.download('punkt')
nltk.download('stopwords')

stop_words = set(stopwords.words('portuguese'))
ps = PorterStemmer()

# Função para pré-processamento de texto
def preprocess_text(text):
    tokens = word_tokenize(text.lower())
    tokens = [token for token in tokens if token.isalnum()]
    tokens = [token for token in tokens if token not in stop_words]
    tokens = [ps.stem(token) for token in tokens]
    return ' '.join(tokens)

# Ler o arquivo CSV
input_file = 'data/raw/noticias.csv'
output_folder = 'data/processed'
os.makedirs(output_folder, exist_ok=True)
output_file = os.path.join(output_folder, 'noticias.parquet')

df_processed = pd.DataFrame(columns=['Título Processado'])

with open(input_file, mode='r', encoding='utf-8') as file:
    for line in tqdm(file.readlines()):
        title = line.strip()
        processed_title = preprocess_text(title)
        df_processed.loc[len(df_processed)] = [processed_title]

# Salvar o DataFrame processado em formato Parquet
df_processed.to_parquet(output_file, index=False)

print(f'Dados processados e gravados com sucesso em {output_file}')
