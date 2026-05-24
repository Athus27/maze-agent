from pathlib import Path

class Interface:
    def __init__(self):
        self.running = True

    def iniciar(self):
        """Inicia o loop principal da interface"""
        while self.running:
            self.menu_principal()

    def menu_principal(self):
        print("\n" + "="*50)
        print("MENU PRINCIPAL - ALGORITMOS DE BUSCA")
        print("="*50)
        print("1 - Busca Cega (DFS, BFS)")
        print("2 - Busca Informada (A*, Greedy)")
        print("3 - Busca Local (Hill Climbing, Simulated Annealing, GA)")
        print("4 - Busca Online (LRTA*, RTA*)")
        print("5 - Sair")
        print("-"*50)
        
        opcao = input("Digite a opção desejada: ").strip()
        
        switcher = {
            "1": self.menu_busca_cega,
            "2": self.menu_busca_informada,
            "3": self.menu_busca_local,
            "4": self.menu_busca_online,
            "5": self.sair
        }
        
        funcao = switcher.get(opcao, self.opcao_invalida)
        funcao()

    def menu_busca_cega(self):
        print("\n" + "="*50)
        print("BUSCA CEGA")
        print("="*50)
        print("1 - DFS (Depth-First Search)")
        print("2 - BFS (Breadth-First Search)")
        print("0 - Voltar")
        print("-"*50)
        
        opcao = input("Escolha um algoritmo: ").strip()
        if opcao == "1":
            self.executar_algoritmo("DFS")
        elif opcao == "2":
            self.executar_algoritmo("BFS")
        elif opcao == "0":
            return
        else:
            self.opcao_invalida()

    def menu_busca_informada(self):
        print("\n" + "="*50)
        print("BUSCA INFORMADA")
        print("="*50)
        print("1 - A* (A-Star)")
        print("2 - Greedy Best-First Search")
        print("0 - Voltar")
        print("-"*50)
        
        opcao = input("Escolha um algoritmo: ").strip()
        if opcao == "1":
            self.executar_algoritmo("A*")
        elif opcao == "2":
            self.executar_algoritmo("Greedy")
        elif opcao == "0":
            return
        else:
            self.opcao_invalida()

    def menu_busca_local(self):
        print("\n" + "="*50)
        print("BUSCA LOCAL")
        print("="*50)
        print("1 - Hill Climbing")
        print("2 - Simulated Annealing")
        print("3 - Genetic Algorithm")
        print("0 - Voltar")
        print("-"*50)
        
        opcao = input("Escolha um algoritmo: ").strip()
        if opcao == "1":
            self.executar_algoritmo("Hill Climbing")
        elif opcao == "2":
            self.executar_algoritmo("Simulated Annealing")
        elif opcao == "3":
            self.executar_algoritmo("Genetic Algorithm")
        elif opcao == "0":
            return
        else:
            self.opcao_invalida()

    def menu_busca_online(self):
        print("\n" + "="*50)
        print("BUSCA ONLINE")
        print("="*50)
        print("1 - LRTA* (Learning RTA*)")
        print("2 - RTA* (Real-Time A*)")
        print("0 - Voltar")
        print("-"*50)
        
        opcao = input("Escolha um algoritmo: ").strip()
        if opcao == "1":
            self.executar_algoritmo("LRTA*")
        elif opcao == "2":
            self.executar_algoritmo("RTA*")
        elif opcao == "0":
            return
        else:
            self.opcao_invalida()

    def hook_selecionar_labirinto(self):
        """Interrompe o fluxo para o usuário escolher o mapa antes de rodar o algoritmo"""
        print("\n" + "="*50)
        print("SELEÇÃO DE LABIRINTO")
        print("="*50)
        print("1 - Listar labirintos padrão")
        print("2 - Digitar caminho personalizado")
        print("0 - Cancelar")
        print("-"*50)
        
        opcao = input("Escolha a origem do mapa: ").strip()
        
        if opcao == "1":
            pasta_padrao = Path(__file__).resolve().parents[2] / "data" / "labyrinths"
            
            if not pasta_padrao.exists():
                print(f"\nPasta padrão não encontrada em: {pasta_padrao}")
                return None
                
            arquivos = list(pasta_padrao.glob("*.txt"))
            if not arquivos:
                print("\nNenhum labirinto encontrado na pasta padrão.")
                return None
                
            print("\nMapas disponíveis:")
            for i, arq in enumerate(arquivos):
                print(f"{i + 1} - {arq.name}")
                
            escolha = input("\nDigite o número do mapa: ").strip()
            try:
                indice = int(escolha) - 1
                if 0 <= indice < len(arquivos):
                    return str(arquivos[indice])
                else:
                    print("\nNúmero fora da lista.")
                    return None
            except ValueError:
                print("\nEntrada inválida.")
                return None
                
        elif opcao == "2":
            caminho = input("\nDigite o caminho completo do arquivo .txt: ").strip()
            if Path(caminho).is_file():
                return caminho
            else:
                print("\nArquivo não encontrado neste caminho.")
                return None
                
        return None

    def executar_algoritmo(self, nome_algoritmo):
        """Método unificado que gerencia a seleção do mapa e chama o solucionador"""
        print(f"\n>>> Preparando execução do algoritmo: {nome_algoritmo}")
        
        caminho_mapa = self.hook_selecionar_labirinto()
        
        if not caminho_mapa:
            print("\nExecução cancelada: Nenhum mapa selecionado.")
            input("Pressione ENTER para voltar...")
            return
            
        print(f"\nCarregando mapa: {caminho_mapa}")
        
        try:
            from app.services.solucionador_service import gerenciar_solucao
            
            lab_resolvido = gerenciar_solucao(nome_algoritmo, caminho_mapa)
            
            print("\n--- Resultado da Busca ---")
            lab_resolvido.print()
            print(f"Estados Explorados: {lab_resolvido.num_explored}")
            
        except Exception as e:
            print(f"\nErro durante a execução: {e}")
            
        input("\nPressione ENTER para continuar...")

    def opcao_invalida(self):
        print("\n Opção inválida! Tente novamente.")
        input("Pressione ENTER para continuar...")

    def sair(self):
        print("\n Encerrando o programa...")
        self.running = False
