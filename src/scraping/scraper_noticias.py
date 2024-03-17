import csv
import requests
from bs4 import BeautifulSoup
import os

urls = [
    'https://br.investing.com/news/economic-indicators',
    'https://br.investing.com/news/economic-indicators/2',
    'https://br.investing.com/news/economic-indicators/3',
    'https://br.investing.com/news/stock-market-news',
    'https://br.investing.com/news/stock-market-news/2',
    'https://br.investing.com/news/stock-market-news/3'
]

output_folder = 'data/raw'

os.makedirs(output_folder, exist_ok=True)

output_file = os.path.join(output_folder, 'noticias.csv')

with open(output_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Título'])

    for url in urls:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        news_list = soup.find_all('a', class_='title')

        for news in news_list:
            title = news.text.strip()
            writer.writerow([title])

print(f'Dados gravados com sucesso no arquivo {output_file}')
