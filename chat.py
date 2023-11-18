import re
import random
import json
import pandas as pd
import torch
from modelo import RedeNeural
 
from modelo_nltk import bolsa_de_palavras, tokenize
 
 
with open('intencoes.json', 'r', encoding='utf-8') as json_data:
    intencoes = json.load(json_data)
 
nome_bot = "Luma"
 
def lugares_italianos(caminho_arquivo=None, cidade=None, num_lugares=1):
    caminho_arquivo = "pontosturisticos.csv" if caminho_arquivo is None else caminho_arquivo
    dados_lugares = pd.read_csv(caminho_arquivo)
 
    if cidade:
        lugares_italia = dados_lugares[dados_lugares['lugar'].str.lower() == cidade.lower()]
    else:
        lugares_italia = dados_lugares
 
    if not lugares_italia.empty:
        lugares_italia_aleatorios = lugares_italia.sample(num_lugares)
        recomendacoes = [
            {
                "Nome": lugar['pontos turisticos'],
                "Descrição": lugar['descrição']
            }
            for index, lugar in lugares_italia_aleatorios.iterrows()
        ]
        return recomendacoes
    else:
        return []
 
def recomendar_hoteis_italianos(caminho_arquivo=None, cidade=None, num_hoteis=1):
    caminho_arquivo = "hoteisitalianos.csv" if caminho_arquivo is None else caminho_arquivo
    dados_hoteis = pd.read_csv(caminho_arquivo)
 
    if cidade:
        hoteis_italianos = dados_hoteis[dados_hoteis['lugar'].str.lower() == cidade.lower()]
    else:
        hoteis_italianos = dados_hoteis
 
    if not hoteis_italianos.empty:
        hoteis_italianos_aleatorios = hoteis_italianos.sample(num_hoteis)
        recomendacoes = [
            {
                "Nome": hotel['nome'],
                "Local": hotel['lugar'],
                "Preço": hotel['preco']
            }
            for index, hotel in hoteis_italianos_aleatorios.iterrows()
        ]
        return recomendacoes
    else:
        return []
 
def recomendar_hotel_por_preco(caminho_arquivo=None, preco_limite=None):
    caminho_arquivo = "./csv/hoteisitalianos.csv" if caminho_arquivo is None else caminho_arquivo
    dados_hoteis = pd.read_csv(caminho_arquivo)
 
 
    dados_hoteis['preco'] = dados_hoteis['preco'].replace('[^0-9.]', '', regex=True).astype(float)
 
    if preco_limite is not None:
        hoteis_filtrados = dados_hoteis[dados_hoteis['preco'] < preco_limite]
    else:
        hoteis_filtrados = dados_hoteis
 
    if not hoteis_filtrados.empty:
        hotel_recomendado = hoteis_filtrados.sample(1).iloc[0]
        recomendacao = {
            "Nome": hotel_recomendado['nome'],
            "Local": hotel_recomendado['lugar'],
            "Preço": hotel_recomendado['preco']
        }
        return recomendacao
    else:
        return None
 
def recomendar_restaurantes_italianos(caminho_arquivo=None, localizacao=None, num_restaurantes=1):
    caminho_arquivo = "restaurantesitalianos.csv" if caminho_arquivo is None else caminho_arquivo
    dados_restaurantes = pd.read_csv(caminho_arquivo)
 
    if localizacao:
        restaurantes_italianos = dados_restaurantes[dados_restaurantes['lugar'].str.lower() == localizacao.lower()]
    else:
        restaurantes_italianos = dados_restaurantes
 
    if not restaurantes_italianos.empty:
        restaurantes_italianos_aleatorios = restaurantes_italianos.sample(num_restaurantes)
        recomendacoes = [
            {
                "Nome": restaurantes['nome'],
                "Local": restaurantes['lugar'],
                "Preço": restaurantes['preco'],
                "Rua":restaurantes['rua'],
                "Vegetariano/Vegano":restaurantes['vegetariano/vegano']
            }
            for index, restaurantes in restaurantes_italianos_aleatorios.iterrows()
        ]
        return recomendacoes
    else:
        return []
 
 
def recomendar_lugares_italianos(caminho_arquivo=None, num_lugares=5):
    caminho_arquivo = "pontosturisticos.csv" if caminho_arquivo is None else caminho_arquivo
    dados_lugares = pd.read_csv(caminho_arquivo)
 
    lugares_italianos = dados_lugares[dados_lugares['pais'] == 'Italia']
 
    if not lugares_italianos.empty:
        lugares_italianos_aleatorios = lugares_italianos.sample(num_lugares)
        recomendacoes = [
            {
                "Nome": lugar['pontos turisticos'],
                "Pais": lugar['pais'],
                "Local": lugar['lugar'],
                "Descrição": lugar['descrição']
            }
            for index, lugar in lugares_italianos_aleatorios.iterrows()
        ]
        return recomendacoes
    else:
        return []
 
def aeroportos_italianos(caminho_arquivo=None, cidade=None, num_aeroporto=1):
    caminho_arquivo = "aeroportositalianos.csv" if caminho_arquivo is None else caminho_arquivo
    dados_aeroporto = pd.read_csv(caminho_arquivo)
 
    if cidade:
        aeroportos_italiano = dados_aeroporto[dados_aeroporto['cidade'].str.lower() == cidade.lower()]
    else:
        aeroportos_italiano = dados_aeroporto
 
    if not aeroportos_italiano.empty:
        aeroportos_italiano_aleatorios = aeroportos_italiano.sample(num_aeroporto)
        recomendacoes = [
            {
                "Cidade": aeroporto['cidade'],
                "Nome": aeroporto['aeroporto internacional']
            }
            for index, aeroporto in aeroportos_italiano_aleatorios.iterrows()
        ]
        return recomendacoes
    else:
        return []
 
def aeroportos_cidades(caminho_arquivo=None, num_cidades=3):
    caminho_arquivo = "aeroportositalianos.csv" if caminho_arquivo is None else caminho_arquivo
    dados_aeroporto = pd.read_csv(caminho_arquivo)
 
    aeroportos_cidades_aleatorios = dados_aeroporto.sample(num_cidades)
    recomendacoes = [
        {
            "Cidade": aeroporto['cidade']
        }
        for index, aeroporto in aeroportos_cidades_aleatorios.iterrows()
    ]
    return recomendacoes
 
def encontrar_rotas(cidade_partida, cidade_destino, caminho_arquivo=None):
    caminho_arquivo = "destinositalia.csv" if caminho_arquivo is None else caminho_arquivo
    dados = pd.read_csv(caminho_arquivo)
 
 
    rotas = dados[(dados['cidade de entrada'] == cidade_partida) & (dados['cidade de termino'] == cidade_destino)]
 
    return rotas
 
def obter_resposta(msg):
    msg = msg.lower()
 
    for intencao in intencoes['intencoes']:
        for padrao in intencao['padroes']:
            if msg in intencao["padroes"]:
                if intencao["tag"] == "recomendacaolugar":
                    resposta = random.choice(intencao['respostas'])
                    lugares_recomendados = recomendar_lugares_italianos('./csv/pontosturisticos.csv')
                    if lugares_recomendados:
                        resposta += "\n\nEssas são minhas recomendações:"
                        for lugar in lugares_recomendados:
                            resposta += (
                                f"\n\nNome: {lugar['Nome']}"
                                f"\nPais: {lugar['Pais']}"
                                f"\nLugar: {lugar['Local']}"
                                f"\nDescrição: {lugar['Descrição']}"
                            )
                        resposta += "\n\nSe desejar mais recomendações é só pedir :)"
                    else:
                        resposta += "\nNão há lugares italianos na base de dados."
                    return resposta
 
            if padrao.lower() in msg:    
                if intencao["tag"] == "pontosturisticos":
                    resposta = random.choice(intencao['respostas'])
 
                    cidade = None
                    for padrao in intencao['padroes']:
                        if padrao.lower() in msg:
                            indice_cidade = msg.find(padrao.lower()) + len(padrao)
                            cidade = msg[indice_cidade:].strip()
                            break
                    lugares_recomendados = lugares_italianos('./csv/pontosturisticos.csv', cidade)
                    if lugares_recomendados:
                        resposta += "\n\nEssa é a minha recomendação de um lugar turistico em {}:".format(cidade)
                        for lugares in lugares_recomendados:
                            resposta += (
                                f"\n\nNome: {lugares['Nome']}"
                                f"\nDescição: {lugares['Descrição']}"
                            )
                        resposta += "\nSe desejar mais recomendações de lugares turisticos em {} é só pedir :)".format(cidade)
                    else:
                        resposta += f"\nNão há lugares turisticos em {cidade} na base de dados."
                    return resposta
 
            if padrao.lower() in msg:    
                if intencao["tag"] == "recomendacaohotel":
                    resposta = random.choice(intencao['respostas'])
 
                    cidade = None
                    for padrao in intencao['padroes']:
                        if padrao.lower() in msg:
                            indice_cidade = msg.find(padrao.lower()) + len(padrao)
                            cidade = msg[indice_cidade:].strip()
                            break
                    hoteis_recomendados = recomendar_hoteis_italianos('./csv/hoteisitalianos.csv', cidade)
                    if hoteis_recomendados:
                        resposta += "\n\nEssas são minhas recomendações de hotéis em {}:".format(cidade)
                        for hotel in hoteis_recomendados:
                            resposta += (
                                f"\n\nNome: {hotel['Nome']}"
                                f"\nPreço: {hotel['Preço']}"
                            )
                        resposta += "\nSe desejar mais recomendações de hotéis em {} é só pedir :)".format(cidade)
                    else:
                        resposta += f"\nNão há hotéis em {cidade} na base de dados."
                    return resposta
 
            if padrao.lower() in msg:
                if intencao["tag"] == "hotelpreco":
                    resposta = random.choice(intencao['respostas'])
 
                    preco_limite = None
                    for padrao in intencao['padroes']:
                        if padrao.lower() in msg:
                            indice_preco = msg.find(padrao.lower()) + len(padrao)
                            preco_limite = float(msg[indice_preco:].strip().replace("reais", "").replace("real", "").replace("R$", ""))
                            break
 
                    hotel_recomendado = recomendar_hotel_por_preco(preco_limite=preco_limite)
 
                    if hotel_recomendado:
                        resposta += "\n\nEu recomendo o seguinte hotel:"
                        resposta += (
                            f"\n\nNome: {hotel_recomendado['Nome']}"
                            f"\nLocal: {hotel_recomendado['Local']}"
                            f"\nPreço: R${hotel_recomendado['Preço']}"
                        )
                        resposta += "\n\nEspero que goste da recomendação!"
                    else:
                        resposta += "\n\nNão há hotéis disponíveis dentro do limite de preço especificado."
                    return resposta
 
 
            if padrao.lower() in msg:
                if intencao["tag"] == "recomendarrestaurantes":
                    resposta = random.choice(intencao['respostas'])
 
                    localizacao = None
                    for padrao in intencao['padroes']:
                        if padrao.lower() in msg:
                            indice_localizacao = msg.find(padrao.lower()) + len(padrao)
                            localizacao = msg[indice_localizacao:].strip()
                            break
                    restaurantes_recomendados = recomendar_restaurantes_italianos('./csv/restaurantesitalianos.csv', localizacao)
                    if restaurantes_recomendados:
                        resposta += "\n\nEssas são minhas recomendações de restaurantes em {}:".format(localizacao)
                        for restaurante in restaurantes_recomendados:
                            resposta += (
                                f"\n\nNome: {restaurante['Nome']}"
                                f"\nPreço: {restaurante['Preço']}"
                                f"\nRua: {restaurante['Rua']}"
                                f"\nO lugar oferece opções vegetarianas e veganas: {restaurante['Vegetariano/Vegano']}"
                            )
                        resposta += "\nSe desejar mais recomendações de restaurante em {} é só pedir :)".format(localizacao)
                    else:
                        resposta += f"\nNão há restaurantes em {localizacao} na base de dados."
                    return resposta
 
            if padrao.lower() in msg:    
                if intencao["tag"] == "aeroportocidade":
                    resposta = random.choice(intencao['respostas'])
 
                    cidade = None
                    for padrao in intencao['padroes']:
                        if padrao.lower() in msg:
                            indice_cidade = msg.find(padrao.lower()) + len(padrao)
                            cidade = msg[indice_cidade:].strip()
                            break
                    aeroportos = aeroportos_italianos('./csv/aeroportositalianos.csv', cidade)
                    if aeroportos:
                        resposta += "\n\nEsse é o aeroporto localizado em meu banco de dados em {}:".format(cidade)
                        for aeroporto in aeroportos:
                            resposta += (
                                f"\n\nNome: {aeroporto['Nome']}\n"
                            )
                        resposta += "\nEspero ter conseguido te ajudar a achar um aeroporto em {} :)".format(cidade)
                    else:
                        resposta += f"\nNão há hotéis em {cidade} na base de dados."
                    return resposta
 
            if padrao.lower() in msg:
                if intencao["tag"] == "nomecidadeaeroporto":
                    resposta = random.choice(intencao['respostas'])
                    cidade_aeroportos = aeroportos_cidades('./csv/aeroportositalianos.csv')
                    if cidade_aeroportos:
                        resposta += "\n\nEssas são algumas das cidades italianas que possui um aeroporto internacional:"
                        for aeroporto in cidade_aeroportos:
                            resposta += (
                                f"\nCidade: {aeroporto['Cidade']}"
                            )
                        resposta += "\nSe desejar mais cidades é só pedir :)"
                    else:
                        resposta += "\nNão há aeroportos italianos internacionais na base de dados."
                    return resposta
 
            if padrao.lower() in msg:
                if intencao["tag"] == "recomendarrotas":
                    resposta = random.choice(intencao['respostas'])
 
                    cidades = re.findall(r'\b\w+\b', msg)
                    if len(cidades) >= 6:
                        cidade_partida = cidades[3]
                        cidade_destino = cidades[-1]
                        rotas_encontradas = encontrar_rotas(cidade_partida, cidade_destino, './csv/destinositalia.csv')  # Substitua pelo caminho correto do seu arquivo CSV de rotas
                        if not rotas_encontradas.empty:
                            resposta += "\n\nO melhor trajeto que consegui encontrar foi:"
                            for indice, linha in rotas_encontradas.iterrows():
                                resposta += f"\nCidade 1: {linha['rota 1']}\n"
                                resposta += f"\nCidade 2: {linha['rota 2']}\n"
                                resposta += f"\nCidade 3: {linha['rota 3']}\n"
                                resposta += f"\nCidade 4: {linha['rota 4']}\n"
                                resposta += f"\nCidade 5: {linha['rota 5']}\n"
                                resposta += f"\n\n{linha['descrição']}\n"
                        else:
                            resposta += f"\nNão foram encontradas rotas de {cidade_partida} para {cidade_destino}."
                    else:
                        resposta += "Por favor, forneça as cidades de partida e destino na seguinte estrutura: 'como chegar de [cidade de partida] há [cidade de destino]'."
                    return resposta
 
            if padrao.lower() in msg:
                if intencao["tag"] == "saudacao":
                    resposta = random.choice(intencao['respostas'])
                    return resposta
 
            if padrao.lower() in msg:
                if intencao["tag"] == "duvidapassagem":
                    resposta = random.choice(intencao['respostas'])
                    return resposta
 
            if padrao.lower() in msg:
                if intencao["tag"] == "aeroportodestino":
                    resposta = random.choice(intencao['respostas'])
                    return resposta
 
    tokens = tokenize(msg)
    bag = bolsa_de_palavras(tokens, todas_palavras)
    bag = torch.tensor(bag, dtype=torch.float32).view(1, -1)
 
 
    modelo.eval()
 
 
    output = modelo(bag)
    _, predicted = torch.max(output, dim=1)
 
 
    tag = tags[predicted.item()]
 
 
    for intent in intencoes['intencoes']:
        if intent['tag'] == tag:
            resposta = random.choice(intent['respostas'])
            return resposta
 
    return "Eu não entendi"  
 
 
if __name__ == "__main__":
    dispositivo = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
 
    ARQUIVO = "dados.pth"
    dados = torch.load(ARQUIVO)
 
    tamanho_entrada = dados["tamanho_entrada"]
    tamanho_oculto = dados["tamanho_oculto"]
    tamanho_saida = dados["tamanho_saida"]
    todas_palavras = dados['todas_palavras']
    tags = dados['tags']
    estado_modelo = dados["estado_do_modelo"]
 
    modelo = RedeNeural(tamanho_entrada, tamanho_oculto, tamanho_saida).to(dispositivo)
    modelo.load_state_dict(estado_modelo)
    modelo.eval()
 
    print("Vamos conversar! (digite 'quit' para sair)")
    while True:
        sentenca = input("Você: ")
        if sentenca == "quit":
            break
 
        resp = obter_resposta(sentenca)
        print(resp)