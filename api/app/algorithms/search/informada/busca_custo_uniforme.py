from ..common import LabirintoBuscaBase, No, ResultadoBusca

class LabirintoBusca(LabirintoBuscaBase):
    def busca_custo_uniforme(self) -> ResultadoBusca:
        return self.busca_prioridade(
            'Busca de Custo Uniforme (UCS)',
            lambda no: no.g
        )
