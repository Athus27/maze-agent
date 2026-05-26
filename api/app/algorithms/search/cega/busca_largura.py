from collections import deque
from typing import List, Set

from ..common import LabirintoBuscaBase, No, ResultadoBusca, Estado

class LabirintoBusca(LabirintoBuscaBase):
    def busca_largura(self) -> ResultadoBusca:
        inicio = No(self.inicio)
        fronteira = deque([inicio])
        em_fronteira = {self.inicio}
        explorados: Set[Estado] = set()
        ordem_explorados: List[Estado] = []
        nos_explorados = 0
        nos_expandidos = 0
        tamanho_max_fronteira = len(fronteira)

        while fronteira:
            no = fronteira.popleft()
            em_fronteira.remove(no.estado)
            nos_explorados += 1
            ordem_explorados.append(no.estado)

            if no.estado == self.objetivo:
                caminho, acoes = self.reconstruir(no)
                return ResultadoBusca(
                    'Busca em Largura (BFS)',
                    True,
                    caminho,
                    acoes,
                    no.g,
                    nos_explorados,
                    nos_expandidos,
                    ordem_explorados,
                    tamanho_max_fronteira,
                )

            explorados.add(no.estado)
            nos_expandidos += 1

            for acao, estado, custo in self.vizinhos(no.estado):
                if estado not in explorados and estado not in em_fronteira:
                    filho = No(estado=estado, pai=no, acao=acao, g=no.g + custo)
                    fronteira.append(filho)
                    em_fronteira.add(estado)
                    tamanho_max_fronteira = max(tamanho_max_fronteira, len(fronteira))

        return ResultadoBusca(
            'Busca em Largura (BFS)',
            False,
            [],
            [],
            None,
            nos_explorados,
            nos_expandidos,
            ordem_explorados,
            tamanho_max_fronteira,
        )
