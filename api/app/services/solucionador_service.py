"""
1 - Entrada: O endpoint da sua API recebe do React o nome do algoritmo desejado (ex: "DFS") e o identificador do mapa.  
2 - Fábrica: O seu arquivo em services/ intercepta essa string e decide qual módulo de algoritmo invocar.
3 - Execução: O algoritmo selecionado roda sobre a estrutura do labirinto. 
4 - Saída: O serviço padroniza o resultado em um formato único de resposta que a API converte em JSON para o React consumir.
"""
from app.algorithms.search.dfs import busca_dfs
from app.algorithms.search.bfs import busca_bfs

# O dicionário : (Factory)
ALGORITMOS_BUSCA = {
    "DFS": busca_dfs,
    "BFS": busca_bfs,
    # "UCS": busca_ucs,
    # "A*": busca_astar,
}

#Fábrica escolhe a Estratégia certa dinamicamente baseado no comando do usuário.2
def gerenciar_solucao(nome_algoritmo: str, labirinto):
    algoritmo_funcao = ALGORITMOS_BUSCA.get(nome_algoritmo)
    
    if not algoritmo_funcao:
        raise ValueError(f"Algoritmo '{nome_algoritmo}' não é válido ou não foi implementado.")
    algoritmo_funcao(labirinto)
    return labirinto

