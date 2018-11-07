import random
import math
from Individuo import Individuo
from Item import Item

#peso de cada item = 1~50
#valor de cada item = 100~1000
taxa_mutacao = 1
geracoes = 50
tamanho_individuo = 20
tamanho_populacao = 50

def Gera_itens():
    Coleção_de_itens = []

    for i in range(0,tamanho_individuo): # quantidade de itens
        auxiliar_random = random.randrange(1, 51)
        item = Item(i,
                    auxiliar_random, #peso do item
                    (int(random.randrange(6,8) * (auxiliar_random*0.8)))  #valor do item
                    )
        Coleção_de_itens.append(item)
    return Coleção_de_itens

def calcula_individuo(individuo,Coleção_de_itens):
    itens_selecionados = []
    peso_do_pre_individuo = 0
    valor_do_pre_individuo = 0
    for idx, item in enumerate(individuo):
        if item == 1:
            itens_selecionados.append(idx)
    for i in itens_selecionados:
        peso_do_pre_individuo += Coleção_de_itens[i].peso
        valor_do_pre_individuo += Coleção_de_itens[i].valor
    return peso_do_pre_individuo,valor_do_pre_individuo

def Gera_individuo(capacidade_mochila,Coleção_de_itens):
    while True:
        pre_individuo = []
        for i in range(0,tamanho_individuo):
            pre_individuo.append(random.randrange(0,2))
        peso_do_pre_individuo,valor_do_pre_individuo = calcula_individuo(pre_individuo,Coleção_de_itens)

        if (peso_do_pre_individuo <= capacidade_mochila):
            break
    individuo = Individuo(pre_individuo,peso_do_pre_individuo,valor_do_pre_individuo)
    return individuo

def Gera_populacao(Coleção_de_itens,capacidade_mochila):
    Coleção_de_individuos = []
    for i in range(0,tamanho_populacao):
        individuo = Gera_individuo(capacidade_mochila,Coleção_de_itens)
        Coleção_de_individuos.append(individuo)
    return Coleção_de_individuos

def Torneio(Coleção_de_individuos):
    individuos_selecionados = []
    for i in range(0,5):
        individuos_selecionados.append(Coleção_de_individuos[random.randrange(0,tamanho_populacao)])
        individuos_selecionados_ordenado = sorted(individuos_selecionados, key = Individuo.Key_valor, reverse = True)
    return individuos_selecionados_ordenado[0].id

def Crossover (progenitor1, progenitor2,Coleção_de_itens, capacidade_mochila):
    continuar = 15
    while True:
        corte1 = random.randrange(0,tamanho_individuo/2)
        corte2 = random.randrange(tamanho_individuo/2,tamanho_individuo)
        novo_individuo = progenitor1[0:corte1]
        for cromossomo in progenitor2[corte1:corte2]:
            novo_individuo.append(cromossomo)
        for cromossomo in progenitor1[corte2:tamanho_individuo]:
            novo_individuo.append(cromossomo)

        peso_do_individuo,valor = calcula_individuo(novo_individuo,Coleção_de_itens)
        continuar -= 1

        if continuar == 0:
            novo_individuo = progenitor1
            break
        if peso_do_individuo < capacidade_mochila:
            break
    return novo_individuo

def Mutacao(individuo,capacidade_mochila, Coleção_de_itens):
    continuar = 15
    while True:
        cromossomo = random.randrange(0,tamanho_individuo)
        if individuo[cromossomo] == 1:
            individuo[cromossomo] = 0
        else:
            individuo[cromossomo] = 1
        peso_do_individuo,valor = calcula_individuo(individuo,Coleção_de_itens)
        if continuar == 0:
            break
        if peso_do_individuo < capacidade_mochila:
            break
    return individuo

def Elitismo(antiga_geracao,proxima_geracao):
    geracao_selecionada = []
    antiga_geracao_ordenado = sorted(antiga_geracao, key = Individuo.Key_valor, reverse=True)
    proxima_geracao_ordenado = sorted(proxima_geracao, key = Individuo.Key_valor)

    taken = [0 for _ in range(0, int(tamanho_populacao * 0.3))]
    for i in range(tamanho_populacao):
        geracao_selecionada.append(proxima_geracao_ordenado[i])
    for i in range(0, int(tamanho_populacao * 0.3)):
        for j in range(0, int(tamanho_populacao * 0.3)):
            if geracao_selecionada[i].valor < antiga_geracao_ordenado[j].valor and taken[j] == 0:
                geracao_selecionada[i] = antiga_geracao_ordenado[j]
                taken[j] = 1
    geracao_selecionada = sorted(geracao_selecionada,key=Individuo.Key_valor, reverse=True)
    return geracao_selecionada




# ===================> Main <===================
def main():
    Coleção_de_itens = Gera_itens()
    somatoria_peso_itens = sum(i.peso for i in Coleção_de_itens)
    capacidade_mochila = int(somatoria_peso_itens * 0.6)
    Coleção_de_individuos = Gera_populacao(Coleção_de_itens,capacidade_mochila)
    proxima_geracao = []
    antiga_geracao = []
    primeira_geracao = [indiv for indiv in Coleção_de_individuos]
    primeira_geracao = sorted(primeira_geracao, key= Individuo.Key_valor, reverse=True)

    for i in range(0, geracoes):
        for j in range(0, tamanho_populacao):
            progenitor1 = Torneio(Coleção_de_individuos)
            progenitor2 = Torneio(Coleção_de_individuos)

            novo_individuo = Crossover(progenitor1,progenitor2,Coleção_de_itens,capacidade_mochila)

            selecionado = random.randrange(0, 10)
            if selecionado < taxa_mutacao:
                novo_individuo = Mutacao(novo_individuo, capacidade_mochila, Coleção_de_itens)

            peso_do_novo_individuo,valor_do_novo_individuo = calcula_individuo(novo_individuo,Coleção_de_itens)
            individuo = Individuo(novo_individuo,peso_do_novo_individuo,valor_do_novo_individuo)
            proxima_geracao.append(individuo)

        del antiga_geracao[:]
        antiga_geracao = [indiv for indiv in Coleção_de_individuos]

        proxima_geracao = Elitismo(antiga_geracao,proxima_geracao)

        del Coleção_de_individuos[:]
        Coleção_de_individuos = [indiv for indiv in proxima_geracao]
        del proxima_geracao[:]

    print(" ")
    print('\033[32m' + 'capacidade da mochila = ' + str(capacidade_mochila) + '\033[0;0m')
    print(" ")
    # Print dos itens gerados
    print('\033[31m'+'Inicio - Coleção de itens gerados'+'\033[0;0m')
    for item in Coleção_de_itens:
        print("id: " + str(item.id) +" peso: " + str(item.peso) +" valor: " +  str(item.valor))
    print('\033[31m' + 'Fim - Coleção de itens gerados' + '\033[0;0m')
    print(" ")
    # Print da primeira geração
    print('\033[31m' + 'Inicio - Primeira geração' + '\033[0;0m')
    for item in primeira_geracao:
        print("id: " + str(item.id) + " peso: " + str(item.peso) + " valor: " + str(item.valor))
    print('\033[31m' + 'Fim - Primeira geração' + '\033[0;0m')
    print(" ")
    print('\033[31m' + 'Inicio - Ultima geração' + '\033[0;0m')
    for item in Coleção_de_individuos:
        print("id: " + str(item.id) + " peso: " + str(item.peso) + " valor: " + str(item.valor))
    print('\033[31m' + 'Fim - Ultima geração' + '\033[0;0m')


if __name__ == '__main__':
    main()
