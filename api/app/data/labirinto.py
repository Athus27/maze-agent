# api/app/data/labirinto.py


class Labirinto:
    def __init__(self, filename):
        with open(filename) as f:
            contents = f.read()

        if contents.count("A") != 1:
            raise Exception("labirinto deve ter exatamente um ponto de partida")
        if contents.count("B") != 1:
            raise Exception("labirinto deve ter exatamente uma chegada")

        contents = contents.splitlines()
        self.altura = len(contents)
        self.largura = max(len(line) for line in contents)

        self.paredes = []
        for i in range(self.altura):
            row = []
            for j in range(self.largura):
                try:
                    if contents[i][j] == "A":
                        self.inicio = (i, j)
                        row.append(False)
                    elif contents[i][j] == "B":
                        self.objetivo = (i, j)
                        row.append(False)
                    elif contents[i][j] == " ":
                        row.append(False)
                    else:
                        row.append(True)
                except IndexError:
                    row.append(False)
            self.paredes.append(row)

        self.solucao = None
        self.num_explored = 0
        self.explored = set()

    def print(self):
        solucao = self.solucao[1] if self.solucao is not None else None
        print()
        for i, row in enumerate(self.paredes):
            for j, col in enumerate(row):
                if col:
                    print("█", end="")
                elif (i, j) == self.inicio:
                    print("A", end="")
                elif (i, j) == self.objetivo:
                    print("B", end="")
                elif solucao is not None and (i, j) in solucao:
                    print("*", end="")
                else:
                    print(" ", end="")
            print()
        print()

    def vizinhos(self, estado):
        linha, coluna = estado
        candidatos = [
            ("up", (linha - 1, coluna)),
            ("down", (linha + 1, coluna)),
            ("left", (linha, coluna - 1)),
            ("right", (linha, coluna + 1)),
        ]

        resultado = []
        for acao, (l, c) in candidatos:
            if (
                0 <= l < self.altura
                and 0 <= c < self.largura
                and not self.paredes[l][c]
            ):
                resultado.append((acao, (l, c)))
        return resultado

    def output_image(self, filename, show_solution=True, show_explored=False):
        from PIL import Image, ImageDraw

        cell_size = 50
        cell_border = 2

        img = Image.new(
            "RGBA", (self.largura * cell_size, self.altura * cell_size), "black"
        )
        draw = ImageDraw.Draw(img)

        solucao = self.solucao[1] if self.solucao is not None else None
        for i, row in enumerate(self.paredes):
            for j, col in enumerate(row):
                if col:
                    fill = (40, 40, 40)
                elif (i, j) == self.inicio:
                    fill = (255, 0, 0)
                elif (i, j) == self.objetivo:
                    fill = (0, 171, 28)
                elif solucao is not None and show_solution and (i, j) in solucao:
                    fill = (220, 235, 113)
                elif solucao is not None and show_explored and (i, j) in self.explored:
                    fill = (212, 97, 85)
                else:
                    fill = (237, 240, 252)

                draw.rectangle(
                    (
                        [
                            (j * cell_size + cell_border, i * cell_size + cell_border),
                            (
                                (j + 1) * cell_size - cell_border,
                                (i + 1) * cell_size - cell_border,
                            ),
                        ]
                    ),
                    fill=fill,
                )

        img.save(filename)
