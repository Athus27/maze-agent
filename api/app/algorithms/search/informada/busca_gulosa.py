from ..common import LabirintoBuscaBase, No, ResultadoBusca

class LabirintoBusca(LabirintoBuscaBase):
    def busca_gulosa(self) -> ResultadoBusca:
        return self.busca_prioridade(
            'Greedy Best-First Search',
            lambda no: self.h(no.estado)
        )
