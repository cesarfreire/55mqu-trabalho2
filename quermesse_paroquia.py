import csv
import os
import random
import time

from cronometro import tempo_execucao


class QuermesseDaParoquia:
    def __init__(self, caminho_instancia):
        self.pessoas = None
        self.m = None
        self.dependencias = None
        self.D = None
        self.custos = None
        self.C = None
        self.n = None
        self.caminho_instancia = caminho_instancia
        self.ler_instancia()

    def ler_instancia(self):
        """ Lê os dados de uma instância de problema de Quermesse da Paróquia """
        with open(self.caminho_instancia, 'r') as file:
            # Leitura dos valores de n (sabores) e C (orçamento)
            self.n, self.C = map(float, file.readline().strip().split())

            # Leitura dos custos dos sabores
            self.custos = list(map(int, file.readline().strip().split()))

            # Leitura das dependências
            self.D = int(file.readline().strip())
            self.dependencias = {}
            for _ in range(self.D):
                i, j = map(int, file.readline().strip().split())
                if j not in self.dependencias:
                    self.dependencias[j] = []
                self.dependencias[j].append(i)

            # Leitura do número de pessoas m
            self.m = int(file.readline().strip())

            # Leitura das importâncias das pessoas e suas preferências
            self.pessoas = []
            for _ in range(self.m):
                data = list(map(int, file.readline().strip().split()))
                importancia = data[0]
                num_flavors = data[1]
                flavors = data[2:]
                self.pessoas.append((importancia, flavors))

    def eh_valido(self, sabores_escolhidos):
        """ Verifica se uma seleção de sabores é válida respeitando as dependências """

        # para cada sabor escolhido
        for j in sabores_escolhidos:
            # verifica se ele tem dependências
            if j in self.dependencias:
                # verifica se todas as dependências foram escolhidas
                for i in self.dependencias[j]:
                    # se não, a seleção é inválida
                    if i not in sabores_escolhidos:
                        return False
        return True

    def calcular_custo(self, sabores_escolhidos):
        """ Calcula o custo total dos sabores selecionados """
        return sum(self.custos[i - 1] for i in sabores_escolhidos)

    def calcular_importancia(self, sabores_escolhidos):
        """ Calcula a importância total das pessoas atendidas """
        # inicializa a importância total
        importancia_total = 0

        # para cada pessoa
        for importancia, sabores in self.pessoas:
            # verifica se todos os sabores da pessoa foram escolhidos
            if all(sabor in sabores_escolhidos for sabor in sabores):
                # se sim, adiciona a importância da pessoa à importância total
                importancia_total += importancia
        return importancia_total

    @tempo_execucao
    def cria_solucao_gulosa_inicial(self):
        """ Cria uma solução inicial de forma gulosa """

        # lista que armazena os sabores selecionados
        sabores_selecionados = []

        # custo atual da solução
        custo_atual = 0

        # ordena as pessoas por importância e sabores
        for importancia, sabores in sorted(self.pessoas, key=lambda x: -x[0]):

            # verifica se todos os sabores da pessoa já foram selecionados
            if all(sabor in sabores_selecionados for sabor in sabores):
                # se sim, passa para a próxima pessoa
                continue

            # calcula o custo adicional de adicionar os sabores da pessoa
            custo_adicional = sum(self.custos[sabor - 1] for sabor in sabores if sabor not in sabores_selecionados)

            # verifica se o custo atual mais o custo adicional é menor ou igual ao orçamento
            if custo_atual + custo_adicional <= self.C and self.eh_valido(sabores_selecionados + sabores):
                # adiciona os sabores da pessoa à lista de sabores selecionados
                sabores_selecionados.extend(sabor for sabor in sabores if sabor not in sabores_selecionados)

                # atualiza o custo atual
                custo_atual += custo_adicional

        # retorna a lista de sabores selecionados
        return sabores_selecionados

    @tempo_execucao
    def iterated_greedy(self, max_iteracoes=199, taxa_destruicao=0.745):
        """ Implementa o algoritmo guloso iterado """
        solucao_atual = self.cria_solucao_gulosa_inicial()
        melhor_solucao = solucao_atual[:]
        melhor_importancia = self.calcular_importancia(solucao_atual)

        for iteracao in range(max_iteracoes):
            # Destruição
            # verifica quantos sabores serão removidos
            qtdade_remocao = max(1, int(taxa_destruicao * len(solucao_atual)))
            # seleciona aleatoriamente os sabores a serem removidos
            sabores_removidos = random.sample(solucao_atual, qtdade_remocao)
            # remove os sabores selecionados
            for flavor in sabores_removidos:
                solucao_atual.remove(flavor)

            # Reconstrução
            # recalcula o custo atual
            custo_atual = self.calcular_custo(solucao_atual)
            # ordena as pessoas por importância e sabores
            for importancia, sabores in sorted(self.pessoas, key=lambda x: -x[0]):
                # verifica se todos os sabores da pessoa já foram selecionados
                if all(sabor in solucao_atual for sabor in sabores):
                    continue

                # calcula o custo adicional de adicionar os sabores da pessoa
                custo_adicional = sum(self.custos[sabor - 1] for sabor in sabores if sabor not in solucao_atual)

                # verifica se o custo atual mais o custo adicional é menor ou igual ao orçamento
                if ((custo_atual + custo_adicional) <= self.C) and self.eh_valido(solucao_atual + sabores):
                    # adiciona os sabores da pessoa na lista de sabores selecionados
                    solucao_atual.extend(sabor for sabor in sabores if sabor not in solucao_atual)
                    # atualiza o custo atual
                    custo_atual += custo_adicional

            importancia_atual = self.calcular_importancia(solucao_atual)
            if importancia_atual > melhor_importancia:
                melhor_solucao = solucao_atual[:]
                melhor_importancia = importancia_atual

        custo_final = self.calcular_custo(melhor_solucao)
        return melhor_solucao, melhor_importancia, custo_final


def run():
    instances_path = 'instances'
    results = []
    header = ['Instância', 'Execução', 'Tempo de Execução (s)', 'Importância Total', 'Custo Final']
    with open("resultados_irace_3.csv", mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        for instance_file in os.listdir(instances_path):
            if instance_file.endswith('.txt'):
                for execucao in range(1, 11):  # Executa cada instância 10 vezes
                    tempo_inicio = time.time()
                    file_path = os.path.join(instances_path, instance_file)
                    qp = QuermesseDaParoquia(file_path)
                    solucao, importancia, custo_final = qp.iterated_greedy()
                    tempo_fim = time.time()
                    tempo_execucao = tempo_fim - tempo_inicio
                    results.append((instance_file, solucao, importancia, custo_final))
                    writer.writerow([instance_file, execucao, tempo_execucao, importancia, custo_final])

    # Exibir resultados
    for instance_file, solucao, importancia, custo_final in results:
        print(f'Instância: {instance_file}')
        print(f'Melhor solução encontrada: {solucao}')
        print(f'Importância total: {importancia}')
        print(f'Custo final: {custo_final}')
        print('--------------------------------------')


if __name__ == '__main__':
    run()
