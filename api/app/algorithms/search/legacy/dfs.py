from .estrutura import No, PilhaFronteira


def busca_dfs(labirinto):
    """Encontra uma solução para o labirinto usando Busca em Profundidade (DFS)."""
    labirinto.num_explored = 0
    inicio = No(estado=labirinto.inicio, pai=None, acao=None)
    fronteira = PilhaFronteira()
    fronteira.add(inicio)
    labirinto.explored = set()

    while True:
        if fronteira.empty():
            raise Exception("sem solução")

        no = fronteira.remove()
        labirinto.num_explored += 1

        if no.estado == labirinto.objetivo:
            acoes = []
            celulas = []
            while no.pai is not None:
                acoes.append(no.acao)
                celulas.append(no.estado)
                no = no.pai
            acoes.reverse()
            celulas.reverse()
            labirinto.solucao = (acoes, celulas)
            return

        labirinto.explored.add(no.estado)

        for acao, estado in labirinto.vizinhos(no.estado):
            if not fronteira.contem_estado(estado) and estado not in labirinto.explored:
                filho = No(estado=estado, pai=no, acao=acao)
                fronteira.add(filho)
