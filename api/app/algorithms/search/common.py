from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple, List, Dict, Set, Callable
import heapq
import itertools
import math

Estado = Tuple[int, int]


@dataclass
class No:
    estado: Estado
    pai: Optional["No"] = None
    acao: Optional[str] = None
    g: float = 0.0


@dataclass
class ResultadoBusca:
    algoritmo: str
    encontrado: bool
    caminho: List[Estado]
    acoes: List[str]
    custo_caminho: Optional[float]
    nos_explorados: int
    nos_expandidos: int
    estados_explorados: List[Estado]
    tamanho_max_fronteira: int

    @property
    def tamanho_caminho(self) -> Optional[int]:
        return len(self.acoes) if self.encontrado else None


class LabirintoBuscaBase:
    def __init__(self, filename: str):
        with open(filename, encoding="utf-8") as f:
            contents = f.read()

        if contents.count("A") != 1:
            raise ValueError("O labirinto deve ter exatamente um ponto inicial A.")
        if contents.count("B") != 1:
            raise ValueError("O labirinto deve ter exatamente um objetivo B.")

        linhas = contents.splitlines()
        self.altura = len(linhas)
        self.largura = max(len(linha) for linha in linhas)
        self.paredes: list[list[bool]] = []

        for i in range(self.altura):
            row: list[bool] = []
            for j in range(self.largura):
                char = linhas[i][j] if j < len(linhas[i]) else " "
                if char == "A":
                    self.inicio = (i, j)
                    row.append(False)
                elif char == "B":
                    self.objetivo = (i, j)
                    row.append(False)
                elif char == " ":
                    row.append(False)
                else:
                    row.append(True)
            self.paredes.append(row)

    def vizinhos(self, estado: Estado):
        linha, coluna = estado
        candidatos = [
            ("up", (linha - 1, coluna)),
            ("down", (linha + 1, coluna)),
            ("left", (linha, coluna - 1)),
            ("right", (linha, coluna + 1)),
        ]
        resultado = []
        for acao, (l, c) in candidatos:
            if 0 <= l < self.altura and 0 <= c < self.largura and not self.paredes[l][c]:
                resultado.append((acao, (l, c), 1.0))
        return resultado

    def h(self, estado: Estado) -> float:
        """Heurística de Manhattan para movimentos ortogonais com custo unitário."""
        return abs(estado[0] - self.objetivo[0]) + abs(estado[1] - self.objetivo[1])

    @staticmethod
    def reconstruir(no: No):
        estados = []
        acoes = []
        atual = no
        while atual.pai is not None:
            estados.append(atual.estado)
            acoes.append(atual.acao)
            atual = atual.pai
        estados.reverse()
        acoes.reverse()
        return estados, acoes

    def busca_prioridade(self, nome: str, funcao_prioridade: Callable[[No], float]) -> ResultadoBusca:
        contador = itertools.count()
        inicio = No(self.inicio, g=0.0)
        fronteira = []
        heapq.heappush(fronteira, (funcao_prioridade(inicio), next(contador), inicio))
        melhor_g: Dict[Estado, float] = {self.inicio: 0.0}
        fechados: Set[Estado] = set()
        ordem_explorados: List[Estado] = []
        nos_explorados = 0
        nos_expandidos = 0
        tamanho_max_fronteira = len(fronteira)

        while fronteira:
            _, _, no = heapq.heappop(fronteira)

            if no.estado in fechados:
                continue

            nos_explorados += 1
            ordem_explorados.append(no.estado)

            if no.estado == self.objetivo:
                caminho, acoes = self.reconstruir(no)
                return ResultadoBusca(
                    nome,
                    True,
                    caminho,
                    acoes,
                    no.g,
                    nos_explorados,
                    nos_expandidos,
                    ordem_explorados,
                    tamanho_max_fronteira,
                )

            fechados.add(no.estado)
            nos_expandidos += 1

            for acao, estado, custo in self.vizinhos(no.estado):
                novo_g = no.g + custo
                if estado in fechados:
                    continue
                if novo_g < melhor_g.get(estado, math.inf):
                    filho = No(estado=estado, pai=no, acao=acao, g=novo_g)
                    melhor_g[estado] = novo_g
                    heapq.heappush(fronteira, (funcao_prioridade(filho), next(contador), filho))
                    tamanho_max_fronteira = max(tamanho_max_fronteira, len(fronteira))

        return ResultadoBusca(
            nome,
            False,
            [],
            [],
            None,
            nos_explorados,
            nos_expandidos,
            ordem_explorados,
            tamanho_max_fronteira,
        )
