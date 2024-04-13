import torch
import numpy as np

from transformers import AutoModelForSequenceClassification, AutoTokenizer

# Carrega o modelo e tokenizer pré-treinado para sentimento Sebrae
model = AutoModelForSequenceClassification.from_pretrained("ggrazzioli/cls_sentimento_sebrae")
tokenizer = AutoTokenizer.from_pretrained("ggrazzioli/cls_sentimento_sebrae")

# Função para converter logits em sentimento
def get_sentimento(logits):
    probs = torch.nn.functional.softmax(logits, dim=-1)
    sentimentos = ["Negativo", "Neutro", "Positivo"]
    sentimento = sentimentos[torch.argmax(probs)]
    return sentimento

caminho_arquivo = "data/raw/noticias.csv"

with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
    frases = arquivo.readlines()

logits_list = []

for frase in frases:
    inputs = tokenizer(frase, return_tensors="pt")

    outputs = model(**inputs)


    probabilities = torch.softmax(logits, dim=1)

    print("##########")
    print(frase)
    
    print(probabilities.detach().numpy()[0])
    print(get_sentimento(logits))

    logits_list.append(probabilities.detach().numpy()[0])

logits_array = np.array(logits_list)

sentimento_composto = np.median(logits_array, axis=0)

print("Sentimento composto:", sentimento_composto)

# Grava o sentimento composto em um arquivo para utilizar no deploy
np.save("data/processed/sentimento_composto.npy", sentimento_composto)