from ..common import LabirintoBuscaBase, No, ResultadoBusca

class LabirintoBusca(LabirintoBuscaBase):
    def busca_weighted_astar(self, peso: float = 2.0) -> ResultadoBusca:
        if peso <= 0:
            raise ValueError('O peso da Weighted A* deve ser positivo.')
        nome = 'A*' if peso == 1.0 else f'Weighted A* (w={peso})'
        return self.busca_prioridade(
            nome,
            lambda no: no.g + peso * self.h(no.estado)
        )
