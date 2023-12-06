import pandas as pd
import numpy as np


class Simplex:
    def __init__(self, tabela_inicial: list[list], legenda_eixo_x: list[str], legenda_eixo_y: list[str]):
        self.legendas_eixo_x = [legenda_eixo_x]
        self.legendas_eixo_y = [legenda_eixo_y]

        self.n_linhas = len(tabela_inicial)
        self.n_colunas = len(tabela_inicial[0])

        self.tabela_atual = tabela_inicial
        self.tabelas = [tabela_inicial]

        self.run()

    def mostrar_tabelas(self) -> None:
        for i in range(0, len(self.tabelas)):
            nova_tabela = np.append("", self.legendas_eixo_x[i])
            legendas_eixo_y = np.array(self.legendas_eixo_y[i])
            for linha in self.tabelas[i]:
                linha = np.append("", linha)
                nova_tabela = np.vstack([nova_tabela, linha])

            print(pd.DataFrame(data=nova_tabela[1:, 1:],
                               index=legendas_eixo_y[0:],
                               columns=nova_tabela[0, 1:]))
            print("")

    def pegar_index_elemento_pivo(self) -> list:
        # procurando o menor valor em z
        menor_valor_linha_z = min(self.tabela_atual[0])
        index_coluna_pivo = self.tabela_atual[0].index(menor_valor_linha_z)

        index_linha_pivo = 999999999
        menor_valor_linha = 999999999
        for i in range(1, len(self.tabela_atual)):
            dividendo = self.tabela_atual[i][len(self.tabela_atual[0]) - 1]
            divisor = self.tabela_atual[i][index_coluna_pivo]

            if divisor == 0:
                valor = 99999999
            else:
                valor = dividendo / divisor

            if menor_valor_linha > valor > 0:
                menor_valor_linha = valor
                index_linha_pivo = i

        return [index_linha_pivo, index_coluna_pivo]

    def tem_negativo(self) -> bool:
        for item in self.tabela_atual[0]:
            if item < 0:
                return True

        return False

    def run(self):
        # enquanto existir um número negativo na linha Z o processo continua
        while self.tem_negativo():
            # prcurando o elemento pivo
            x, y = self.pegar_index_elemento_pivo()
            elemento_pivo = self.tabela_atual[x][y]

            # criando as novas legendas
            # procurando as legendas mais atuais
            nova_legenda_exio_x = self.legendas_eixo_x[len(self.legendas_eixo_x) - 1].copy()
            nova_legenda_exio_y = self.legendas_eixo_y[len(self.legendas_eixo_y) - 1].copy()

            # trocando as legendas
            aux_legenda = nova_legenda_exio_x[y]
            nova_legenda_exio_x[y] = nova_legenda_exio_y[x]
            nova_legenda_exio_y[x] = aux_legenda

            self.legendas_eixo_x.append(nova_legenda_exio_x)
            self.legendas_eixo_y.append(nova_legenda_exio_y)

            # criando uma tabela nova
            nova_tabela = [[0.0 for _ in range(0, self.n_colunas)] for _ in range(0, self.n_linhas)]

            # preenchendo a linha de referência da tabela nova
            for i in range(0, len(self.tabela_atual[x][:])):
                nova_tabela[x][i] = float("{:.2f}".format(self.tabela_atual[x][i] / elemento_pivo))

            # preenchendo as outras linhas da tabela nova
            for i in range(0, len(self.tabela_atual)):
                if i != x:
                    for j in range(0, len(self.tabela_atual[0])):
                        nova_tabela[i][j] = nova_tabela[x][j] * -1 * self.tabela_atual[i][y] + self.tabela_atual[i][j]
                        nova_tabela[i][j] = float("{:.2f}".format(nova_tabela[i][j]))

            # adicionando a tabela nova a lista de tabelas
            self.tabelas.append(nova_tabela)

            # atualizando a tabela mais atual
            self.tabela_atual = self.tabelas[len(self.tabelas) - 1]
