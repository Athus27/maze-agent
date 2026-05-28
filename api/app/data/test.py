import csv
from html import escape
from pathlib import Path

from app.services.solucionador_service import ALGORITMOS_SEMANA1, gerenciar_solucao


BASE_DIR = Path(__file__).resolve().parents[1]
MAPAS_DIR = BASE_DIR / "data" / "labyrinths"
MAPAS_DIR_CUSTOM = MAPAS_DIR /"custom"
RESULTADOS_DIR = BASE_DIR / "data" / "resultados"
CAMPOS = [
    "mapa",
    "algoritmo",
    "sucesso",
    "custo",
    "passos",
    "explorados",
    "expandidos",
    "tempo_segundos",
    "fronteira_max",
    "desempenho_J",
]


def executar_experimentos():
    registros = []

    for mapa in sorted([*MAPAS_DIR.glob("*.txt"), *MAPAS_DIR_CUSTOM.glob("*.txt")]):
        for algoritmo in ALGORITMOS_SEMANA1:
            labirinto = gerenciar_solucao(algoritmo, str(mapa))
            metricas = labirinto.metricas

            registros.append({
                "mapa": mapa.name,
                "algoritmo": algoritmo,
                "sucesso": metricas["sucesso"],
                "custo": metricas["custo"],
                "passos": metricas["passos"],
                "explorados": metricas["explorados"],
                "expandidos": metricas["expandidos"],
                "tempo_segundos": f'{metricas["tempo_segundos"]:.8f}',
                "fronteira_max": metricas["fronteira_max"],
                "desempenho_J": (
                    f'{metricas["desempenho_J"]:.8f}'
                    if metricas["desempenho_J"] is not None
                    else ""
                ),
            })

    if not registros:
        raise FileNotFoundError(f"Nenhum mapa .txt encontrado em: {MAPAS_DIR}")

    return registros


def salvar_csv(registros, destino: Path):
    with destino.open("w", newline="", encoding="utf-8") as arquivo:
        writer = csv.DictWriter(arquivo, fieldnames=CAMPOS)
        writer.writeheader()
        writer.writerows(registros)


def imprimir_tabela(registros):
    campos_visiveis = CAMPOS[:-1]
    larguras = {
        campo: max(len(campo), *(len(str(registro[campo])) for registro in registros))
        for campo in campos_visiveis
    }

    cabecalho = " | ".join(campo.ljust(larguras[campo]) for campo in campos_visiveis)
    divisor = "-+-".join("-" * larguras[campo] for campo in campos_visiveis)
    print(cabecalho)
    print(divisor)

    for registro in registros:
        print(" | ".join(str(registro[campo]).ljust(larguras[campo]) for campo in campos_visiveis))


def salvar_grafico_expandidos(registros, destino: Path):
    somas = {algoritmo: 0 for algoritmo in ALGORITMOS_SEMANA1}
    contagens = {algoritmo: 0 for algoritmo in ALGORITMOS_SEMANA1}

    for registro in registros:
        algoritmo = registro["algoritmo"]
        somas[algoritmo] += int(registro["expandidos"])
        contagens[algoritmo] += 1

    medias = {
        algoritmo: somas[algoritmo] / contagens[algoritmo]
        for algoritmo in ALGORITMOS_SEMANA1
        if contagens[algoritmo] > 0
    }

    largura = 760
    altura = 420
    margem_x = 70
    margem_y = 60
    area_largura = largura - 2 * margem_x
    area_altura = altura - 2 * margem_y
    maior_valor = max(medias.values()) if medias else 1
    passo = area_largura / max(len(medias), 1)
    barra_largura = passo * 0.58

    elementos = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{largura}" height="{altura}" viewBox="0 0 {largura} {altura}">',
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        '<text x="380" y="30" text-anchor="middle" font-family="Arial" font-size="18">Media de nos expandidos por algoritmo</text>',
        f'<line x1="{margem_x}" y1="{altura - margem_y}" x2="{largura - margem_x}" y2="{altura - margem_y}" stroke="#222"/>',
        f'<line x1="{margem_x}" y1="{margem_y}" x2="{margem_x}" y2="{altura - margem_y}" stroke="#222"/>',
    ]

    for indice, (algoritmo, media) in enumerate(medias.items()):
        x = margem_x + indice * passo + (passo - barra_largura) / 2
        barra_altura = 0 if maior_valor == 0 else (media / maior_valor) * area_altura
        y = altura - margem_y - barra_altura
        label_x = x + barra_largura / 2
        elementos.extend([
            f'<rect x="{x:.2f}" y="{y:.2f}" width="{barra_largura:.2f}" height="{barra_altura:.2f}" fill="#4f7cac"/>',
            f'<text x="{label_x:.2f}" y="{y - 8:.2f}" text-anchor="middle" font-family="Arial" font-size="12">{media:.1f}</text>',
            f'<text x="{label_x:.2f}" y="{altura - margem_y + 24}" text-anchor="middle" font-family="Arial" font-size="12">{escape(algoritmo)}</text>',
        ])

    elementos.append("</svg>")
    destino.write_text("\n".join(elementos), encoding="utf-8")


def main():
    RESULTADOS_DIR.mkdir(parents=True, exist_ok=True)

    registros = executar_experimentos()
    csv_path = RESULTADOS_DIR / "semana1_resultados.csv"
    grafico_path = RESULTADOS_DIR / "semana1_expandidos.svg"

    salvar_csv(registros, csv_path)
    salvar_grafico_expandidos(registros, grafico_path)
    imprimir_tabela(registros)

    print(f"\nCSV salvo em: {csv_path}")
    print(f"Grafico salvo em: {grafico_path}")


if __name__ == "__main__":
    main()
