import numpy as np
import json

import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader

from modelo_nltk import bolsa_de_palavras, tokenize, stem
from modelo import RedeNeural

with open('intencoes.json', 'r', encoding='utf-8') as f:
    intents = json.load(f)

todas_palavras = []
tags = []
xy = []

for intent in intents['intencoes']:
    tag = intent['tag']
    
    tags.append(tag)
    for pattern in intent['padroes']:
        
        w = tokenize(pattern)
        
        todas_palavras.extend(w)
        
        xy.append((w, tag))


palavras_ignore = ['?', '.', '!']
todas_palavras = [stem(w) for w in todas_palavras if w not in palavras_ignore]

todas_palavras = sorted(set(todas_palavras))
tags = sorted(set(tags))

print(len(xy), "padrões")
print(len(tags), "tags:", tags)
print(len(todas_palavras), "palavras únicas stemizadas:", todas_palavras)


X_treino = []
y_treino = []
for (padrao_sentenca, tag) in xy:
    
    bolsa = bolsa_de_palavras(padrao_sentenca, todas_palavras)
    X_treino.append(bolsa)
    
    rotulo = tags.index(tag)
    y_treino.append(rotulo)

X_treino = np.array(X_treino)
y_treino = np.array(y_treino)


num_epochs = 1000
tamanho_lote = 8
taxa_aprendizado = 0.001
tamanho_entrada = len(X_treino[0])
tamanho_oculto = 8
tamanho_saida = len(tags)
print(tamanho_entrada, tamanho_saida)

class ConjuntoDeChat(Dataset):

    def __init__(self):
        self.n_amostras = len(X_treino)
        self.x_dados = X_treino
        self.y_dados = y_treino

    
    def __getitem__(self, indice):
        return self.x_dados[indice], self.y_dados[indice]

    
    def __len__(self):
        return self.n_amostras

conjunto_de_dados = ConjuntoDeChat()
treino_loader = DataLoader(dataset=conjunto_de_dados,
                          batch_size=tamanho_lote,
                          shuffle=True,
                          num_workers=0)

dispositivo = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

modelo = RedeNeural(tamanho_entrada, tamanho_oculto, tamanho_saida).to(dispositivo)


criterio = nn.CrossEntropyLoss()
otimizador = torch.optim.Adam(modelo.parameters(), lr=taxa_aprendizado)

# Treine o modelo
for epoca in range(num_epochs):
    for (palavras, rotulos) in treino_loader:
        palavras = palavras.to(dispositivo)
        rotulos = rotulos.to(dtype=torch.long).to(dispositivo)
        
       
        saidas = modelo(palavras)
       
        perda = criterio(saidas, rotulos)
        
        
        otimizador.zero_grad()
        perda.backward()
        otimizador.step()
        
    if (epoca+1) % 100 == 0:
        print (f'Época [{epoca+1}/{num_epochs}], Perda: {perda.item():.4f}')


print(f'perda final: {perda.item():.4f}')

dados = {
"estado_do_modelo": modelo.state_dict(),
"tamanho_entrada": tamanho_entrada,
"tamanho_oculto": tamanho_oculto,
"tamanho_saida": tamanho_saida,
"todas_palavras": todas_palavras,
"tags": tags
}

ARQUIVO = "dados.pth"
torch.save(dados, ARQUIVO)

print(f'treinamento completo. arquivo salvo em {ARQUIVO}')