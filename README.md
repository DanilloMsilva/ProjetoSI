# Projeto de ChatBot em Python usando Tkinter e PyTorch

Este é um projeto de ChatBot desenvolvido em Python como parte do meu curso na faculdade. O ChatBot utiliza a biblioteca Tkinter para a interface gráfica e PyTorch para o processamento da linguagem natural. Ele é capaz de responder a diferentes intenções do usuário, como recomendações de lugares, hotéis, restaurantes, informações sobre aeroportos, entre outros.

## Conteúdo

- [Pré-requisitos](#pré-requisitos)
- [Instalação](#instalação)
- [Como Usar](#como-usar)
- [Notas Adicionais](#notas-adicionais)

## Pré-requisitos

Certifique-se de ter as seguintes bibliotecas Python instaladas:

* `tkinter`: Biblioteca gráfica para a interface do usuário.
* `pandas`: Para manipulação de dados tabulares.
* `torch`: PyTorch, uma biblioteca de aprendizado de máquina.
* `nltk`: Toolkit de processamento de linguagem natural.

```bash
pip install tk pandas torch nltk
```

## Instalação

1. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/seu-projeto.git
```

## Como usar

1. Baixe o código-fonte do ChatBot.
2. Certifique-se de ter o conjunto de dados adequado para lugares turísticos, hotéis, restaurantes, aeroportos, etc. Você pode utilizar os dados que estão dentro da pasta CSV
3. Execute o arquivo app.py para iniciar o ChatBot.
4. A interface gráfica será exibida. Digite uma mensagem na caixa de entrada e pressione "Enter" ou clique em "Enviar". O ChatBot responderá com base nas intenções definidas no arquivo intencoes.json.

## Funcionalidades

O ChatBot oferece recomendações e informações sobre:

* Lugares turísticos na Itália.
* Hotéis italianos com base na cidade.
* Restaurantes italianos com base na localização.
* Aeroportos italianos em uma cidade específica.
* Rotas entre cidades italianas.

## Notas adicionais

* O treinamento do modelo de processamento de linguagem natural é baseado em um conjunto de dados simples.
* O ChatBot possui uma interface gráfica simples usando Tkinter.

Este projeto foi desenvolvido como parte dos meus estudos na faculdade. 