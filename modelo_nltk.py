import numpy as np
import nltk

from nltk.stem.porter import PorterStemmer
stemmer = PorterStemmer()

def tokenize(sentenca):
    """
    divide a sentença em uma array de palavras/tokens
    um token pode ser uma palavra, caractere de pontuação ou número
    """
    return nltk.word_tokenize(sentenca)

def stem(palavra):
    """
    stemming = encontrar a forma raiz da palavra
    exemplos:
    palavras = ["organizar", "organiza", "organizando"]
    palavras = [stem(p) for p in palavras]
    -> ["organ", "organ", "organ"]
    """
    return stemmer.stem(palavra.lower())

def bolsa_de_palavras(sentenca_tokenizada, palavras):
    """
    retorna um array de bolsa de palavras:
    1 para cada palavra conhecida que existe na sentença, 0 caso contrário
    exemplo:
    sentenca = ["olá", "como", "vai", "você"]
    palavras = ["oi", "olá", "eu", "você", "tchau", "obrigado", "legal"]
    bolsa = [  0 ,    1 ,    0 ,   1 ,    0 ,    0 ,      0]
    """
    
    palavras_sentenca = [stem(palavra) for palavra in sentenca_tokenizada]
    
    bolsa = np.zeros(len(palavras), dtype=np.float32)
    for idx, p in enumerate(palavras):
        if p in palavras_sentenca: 
            bolsa[idx] = 1

    return bolsa