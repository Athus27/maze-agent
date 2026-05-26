"""
1 - Entrada: o serviço recebe o nome do algoritmo e o caminho do mapa.
2 - Fábrica: este arquivo escolhe o módulo certo dentro de `app/algorithms/search`.
3 - Execução: o algoritmo roda sem alterar sua lógica original.
4 - Saída: o resultado é convertido para o objeto `Labirinto` que a interface já sabe imprimir.
"""
from time import perf_counter

from app.data.labirinto import Labirinto
from app.algorithms.search.cega.busca_largura import LabirintoBusca as BuscaLargura
from app.algorithms.search.cega.busca_profundidade import LabirintoBusca as BuscaProfundidade
from app.algorithms.search.informada.busca_custo_uniforme import LabirintoBusca as BuscaCustoUniforme
from app.algorithms.search.informada.busca_gulosa import LabirintoBusca as BuscaGulosa
from app.algorithms.search.informada.busca_weighted_astar import LabirintoBusca as BuscaWeightedAStar
from app.algorithms.search.informada.busca_idastar import LabirintoBusca as BuscaIDAStar


ALGORITMOS_BUSCA = {
    "BFS": lambda caminho: BuscaLargura(caminho).busca_largura(),
    "DFS": lambda caminho: BuscaProfundidade(caminho).busca_profundidade(),
    "UCS": lambda caminho: BuscaCustoUniforme(caminho).busca_custo_uniforme(),
    "Greedy": lambda caminho: BuscaGulosa(caminho).busca_gulosa(),
    "A*": lambda caminho: BuscaWeightedAStar(caminho).busca_weighted_astar(peso=1.0),
    "Weighted A*": lambda caminho: BuscaWeightedAStar(caminho).busca_weighted_astar(peso=2.0),
    "IDA*": lambda caminho: BuscaIDAStar(caminho).busca_idastar(),
}

ALGORITMOS_SEMANA1 = ("BFS", "DFS", "UCS", "Greedy", "A*")


def gerenciar_solucao(nome_algoritmo: str, caminho_mapa: str):
    algoritmo_funcao = ALGORITMOS_BUSCA.get(nome_algoritmo)

    if not algoritmo_funcao:
        raise ValueError(f"Algoritmo '{nome_algoritmo}' não é válido ou não foi implementado.")

    labirinto = Labirinto(caminho_mapa)
    t_inicio = perf_counter()
    resultado = algoritmo_funcao(caminho_mapa)
    t_total = perf_counter() - t_inicio

    labirinto.solucao = (resultado.acoes, resultado.caminho) if resultado.encontrado else None
    labirinto.num_explored = resultado.nos_explorados
    labirinto.explored = set(resultado.estados_explorados)

    custo_caminho = resultado.custo_caminho
    passos = resultado.tamanho_caminho
    nos_expandidos = resultado.nos_expandidos

    alpha = 1.0
    beta = 0.5
    gamma = 100.0
    desempenho_J = None
    if resultado.encontrado and custo_caminho is not None:
        desempenho_J = -(alpha * custo_caminho) - (beta * nos_expandidos) - (gamma * t_total)

    labirinto.metricas = {
        "algoritmo": resultado.algoritmo,
        "sucesso": resultado.encontrado,
        "custo": custo_caminho,
        "passos": passos,
        "explorados": resultado.nos_explorados,
        "expandidos": nos_expandidos,
        "tempo_segundos": t_total,
        "fronteira_max": resultado.tamanho_max_fronteira,
        "desempenho_J": desempenho_J,
    }

    return labirinto
