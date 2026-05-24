from collections import deque

def busca_bfs(grafo, inicio, objetivo):
    fila = deque([inicio])
    visitados = set()
    pais = {}

    while fila:
        no = fila.popleft()

        if no == objetivo:
            break

        if no not in visitados:
            visitados.add(no)

            for vizinho in grafo[no]:
                if vizinho not in visitados:
                    fila.append(vizinho)
                    pais[vizinho] = no

    return pais