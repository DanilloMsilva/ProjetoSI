import torch.nn as nn


class RedeNeural(nn.Module):
    def __init__(self, tamanho_entrada, tamanho_oculto, num_classes):
        super(RedeNeural, self).__init__()
        self.camada1 = nn.Linear(tamanho_entrada, tamanho_oculto) 
        self.camada2 = nn.Linear(tamanho_oculto, tamanho_oculto) 
        self.camada3 = nn.Linear(tamanho_oculto, num_classes)
        self.relu = nn.ReLU()
    
    def forward(self, x):
        saida = self.camada1(x)
        saida = self.relu(saida)
        saida = self.camada2(saida)
        saida = self.relu(saida)
        saida = self.camada3(saida)
        return saida