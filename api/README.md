# TP01 - Semana 1: Agente e Busca Classica

Este projeto implementa a primeira etapa do trabalho: um agente que resolve labirintos
conhecidos usando algoritmos de busca classica e heuristica.

## Como executar

O jeito mais simples, a partir da raiz do projeto, e:

```bash
bash run.sh
```

Esse comando roda os experimentos da Semana 1 e gera a tabela de resultados.

Se quiser rodar manualmente, use:

```bash
PYTHONPATH=api python3 api/app/data/test.py
```

Instale as dependencias somente se o Python reclamar que falta alguma biblioteca:

```bash
pip install -r api/requirements.txt
```

O script executa BFS, DFS, UCS, Gulosa e A* em todos os mapas de
`api/app/data/labyrinths/`. Os resultados sao salvos em:

- `api/app/data/resultados/semana1_resultados.csv`
- `api/app/data/resultados/semana1_expandidos.svg`

## Modelagem PEAS

**Performance:** o agente deve encontrar uma solucao com baixo custo de caminho,
poucos nos expandidos, baixo tempo de execucao e fronteira controlada. A funcao usada
como medida auxiliar de desempenho e:

```text
J = -1.0 * custo - 0.5 * nos_expandidos - 100.0 * tempo_execucao
```

**Environment:** labirinto discreto em grade, com celulas livres, paredes, uma posicao
inicial `A` e um objetivo final `B`.

**Actuators:** movimentos ortogonais: cima, baixo, esquerda e direita.

**Sensors:** na Semana 1 o mapa e conhecido por completo antes da busca. Portanto, o
agente acessa a matriz completa do labirinto para planejar.

## Classificacao do agente

O agente e baseado em objetivos com modelo interno. Ele possui uma representacao do
ambiente, conhece o estado inicial, testa o objetivo e escolhe acoes que levam de `A`
ate `B`. Como o projeto tambem registra custo, tempo e nos expandidos, a avaliacao do
resultado pode ser tratada como uma medida simples de utilidade.

## Formulacao formal

O problema de busca classica foi modelado como:

```text
<S, A, T, s0, G, c>
```

- `S`: conjunto de posicoes livres do labirinto.
- `A`: conjunto de acoes `{up, down, left, right}`.
- `T`: funcao de transicao que move o agente para uma celula vizinha livre.
- `s0`: posicao inicial marcada com `A`.
- `G`: teste de objetivo, verdadeiro quando o estado atual e a posicao `B`.
- `c`: custo de movimento. Na Semana 1, cada movimento valido tem custo `1`.

## Algoritmos implementados

- BFS: `app/algorithms/search/cega/busca_largura.py`
- DFS: `app/algorithms/search/cega/busca_profundidade.py`
- UCS: `app/algorithms/search/informada/busca_custo_uniforme.py`
- Gulosa: `app/algorithms/search/informada/busca_gulosa.py`
- A*: `app/algorithms/search/informada/busca_weighted_astar.py` com peso `1.0`

A heuristica usada pelos algoritmos informados e a distancia de Manhattan:

```text
h(n) = |x_n - x_B| + |y_n - y_B|
```

Para movimentos ortogonais com custo unitario, essa heuristica e admissivel, pois nunca
superestima o menor numero de passos ate o objetivo em um mapa sem diagonais.

## Metricas registradas

Para cada execucao sao registradas as metricas exigidas na Semana 1:

- sucesso ou falha;
- custo do caminho;
- numero de passos;
- numero de nos explorados;
- numero de nos expandidos;
- tempo de execucao;
- tamanho maximo da fronteira.

## Observacoes

Os arquivos em `app/algorithms/search/legacy/` foram mantidos como versoes antigas de
apoio. A implementacao usada nos experimentos fica nos modulos `cega`, `informada`,
`common.py` e `services/solucionador_service.py`.
