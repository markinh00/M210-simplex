from Simplex import Simplex
import numpy as np
import pandas as pd


def verificar_input(texto: str, inputs_validos: list) -> str:
    while True:
        input_usuario = input(texto)

        if input_usuario not in inputs_validos:
            print("Por favor digite uma das opções válidas")
        else:
            break

    return input_usuario


def verificar_input_num(texto: str, return_type: str) -> [int, float]:
    while True:
        input_usuario = input(texto)

        try:
            if return_type == "float":
                input_usuario = float(input_usuario)
            elif return_type == "int":
                input_usuario = int(input_usuario)
            return input_usuario
        except Exception as e:
            print(f"Por favor, digite um número inteiro.\n{e}")


class UserInterface:
    def __init__(self):
        self.tabela: list[list] = []
        self.legenda_eixo_x: list[str] = []
        self.legenda_eixo_y: list[str] = ["Z"]
        self.min_max: str = ""

        self.run()

    def mostrar_tabela(self, tabela: list[list]) -> None:
        nova_tabela = np.append("", self.legenda_eixo_x)
        legendas_eixo_y = np.array(self.legenda_eixo_y)
        for linha in tabela:
            linha = np.append("", linha)
            nova_tabela = np.vstack([nova_tabela, linha])

        print(pd.DataFrame(data=nova_tabela[1:, 1:],
                           index=legendas_eixo_y[0:],
                           columns=nova_tabela[0, 1:]))
        print("")

    def zerar_tabela(self):
        self.tabela = []
        self.legenda_eixo_x = []
        self.legenda_eixo_y = ["Z"]
        self.min_max = ""

    def run(self) -> None:
        while True:
            # preenchendo legendas_eixo_x e legendas_eixo_y
            self.min_max = verificar_input("Qual é o tipo da função? (min ou max): ", ["min", "max"])
            quant_variaveis = verificar_input_num("Quantas variáveis tem a função objetiva?: ", "int")

            for i in range(0, quant_variaveis):
                nome_variavel = input(f"Qual o nome da {i + 1}° variável?: ")
                self.legenda_eixo_x.append(nome_variavel)

            quant_restricoes = verificar_input_num("Quantas restrições?: ", "int")
            for i in range(1, quant_restricoes + 1):
                nome_variavel_folga = input(f"Qual o nome da variável de folga da {i}° restrição?: ")
                self.legenda_eixo_x.append(f"{nome_variavel_folga}")
                self.legenda_eixo_y.append(f"{nome_variavel_folga}")
            self.legenda_eixo_x.append("LD")

            # preenchendo a linha Z
            linha = [0 for _ in range(0, len(self.legenda_eixo_x))]
            for i in range(0, quant_variaveis):
                valor_variavel = verificar_input_num(f"Valor de {self.legenda_eixo_x[i]} na função objetiva: ", "float")

                # caso seja uma minimização é necessário inverter os valores da linha z
                if self.min_max == "max":
                    valor_variavel = (-1) * valor_variavel

                linha[i] = valor_variavel

            self.tabela.append(linha)

            # preenchendo as restrições
            for i in range(1, quant_restricoes + 1):
                linha = [0 for _ in range(0, len(self.legenda_eixo_x))]
                for j in range(0, quant_variaveis):
                    texto = f"Valor de {self.legenda_eixo_x[j]} em {self.legenda_eixo_y[i]}: "

                    valor_variavel = verificar_input_num(texto, "float")
                    linha[j] = valor_variavel

                lado_direito = verificar_input_num(f"Valor do lado direito em {self.legenda_eixo_y[i]}: ", "float")
                linha[len(linha) - 1] = lado_direito

                self.tabela.append(linha)

            # preenchendo a matriz das restrições
            j = quant_variaveis
            for i in range(1, quant_restricoes + 1):
                self.tabela[i][j] = 1
                j = j + 1

            self.mostrar_tabela(self.tabela)
            tabela_correta = verificar_input("A tabela está correta? (s | n): ", ["s", 'n'])

            if tabela_correta == 's':
                simplex = Simplex(self.tabela, self.legenda_eixo_x, self.legenda_eixo_y)
                simplex.mostrar_tabelas()
                break
            if tabela_correta == 'n':
                self.zerar_tabela()
                print("refazendo a tabela...")
