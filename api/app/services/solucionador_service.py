"""
1 - Entrada: O endpoint da API recebe do React o nome do algoritmo desejado (ex: "DFS") e o identificador do mapa.  
2 - Fábrica: esse arquivo intercepta essa string e decide qual módulo de algoritmo invocar.
3 - Execução: O algoritmo selecionado roda sobre a estrutura do labirinto. 
4 - Saída: O serviço padroniza o resultado em um formato único de resposta que a API converte em JSON para o React consumir.
"""
import time

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
    t_inicio = time.time()
    
    algoritmo_funcao(labirinto)
    
    t_fim = time.time()
    t_total = t_fim - t_inicio
    
    custo_caminho = len(labirinto.solucao[0]) if labirinto.solucao else 0
    nos_expandidos = labirinto.num_explored
    
    # 5. Aplica a sua função de Desempenho (J)
    # Definindo pesos hipotéticos (você pode ajustar depois)
    alpha = 1.0
    beta = 0.5
    gamma = 100.0 # Peso maior para o tempo
    
    # ainda n tem 'inválidos' e 'revisitadas' ainda, ignoramos nesta fórmula inicial
    desempenho_J = -(alpha * custo_caminho) - (beta * nos_expandidos) - (gamma * t_total)
    
    # Salva os resultados no labirinto para a Interface conseguir imprimir
    labirinto.metricas = {
        "custo": custo_caminho,
        "expandidos": nos_expandidos,
        "tempo_segundos": t_total,
        "desempenho_J": desempenho_J
    }
    
    
    return labirinto

