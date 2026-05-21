class Interface:
    def __init__(self):
        self.loop = True

    def menu(self):
        self.opcoes()
        opcao = input("Digite a opção desejada: ")
        switcher = {
			"1": self.opcoes_algoritmos,
			"2": self.voltar_menu
		}
        funcao = switcher.get(opcao, lambda: print("Opção inválida."))
        funcao();

    def opcoes(self):
        print("Opções:")
        print("1 - Executar algoritmo")
        print("2 - Voltar ao menu")

    def opcoes_algoritmos(self):
        print("Busca Cega")
        print("Busca Informada")
        print("Busca Local")
        print("Busca Online")

    def opcoes_busca_classica(self):
        print("DFS")
        print("BFS")

    def opcoes_busca_informada(self):
        print("A*")
        print("Greedy Best-First Search")

    def opcoes_busca_local(self):
        print("Hill Climbing")
        print("Simulated Annealing")
        print("Genetic Algorithm")

    def opcoes_busca_online(self):
        print("LRTA*")
        print("RTA*")

