class No:
    def __init__(self, estado, pai, acao):
        self.estado = estado
        self.pai = pai
        self.acao = acao

""" Fronteira:
        É a estrutura de dados que armazena os nós (coordenadas) que já foram gerados/descobertos pelo algoritmo, mas que ainda não foram expandidos (avaliados). Ela controla quais vértices do grafo estão disponíveis para a próxima iteração do laço de busca.

            
        
"""
class PilhaFronteira:
    def __init__(self):
        self.fronteira = []

    def add(self, no):
        self.fronteira.append(no)

    def contem_estado(self, estado):
        return any(no.estado == estado for no in self.fronteira)

    def empty(self):
        return len(self.fronteira) == 0

    def remove(self):
        if self.empty():
            raise Exception("fronteira vazia")
        else:
            no = self.fronteira[-1]
            self.fronteira = self.fronteira[:-1]
            return no


class FilaFronteira(PilhaFronteira):
    def remove(self):
        if self.empty():
            raise Exception("fronteira vazia")
        else:
            no = self.fronteira[0]
            self.fronteira = self.fronteira[1:]
            return no