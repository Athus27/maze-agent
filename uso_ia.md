# Uso de IA

## Ferramenta utilizada

- ChatGPT/Codex, usado como apoio para explicacao de codigo, revisao de logica e criacao deste arquivo.

## Principais prompts utilizados

1. Expliquei que a lista de cidades nao aparecia no HTML usando `index.html` e `api-ibge.js`.
2. Perguntei como corrigir a linha Python que somava dois `glob()`:
   `sorted(MAPAS_DIR.glob("*.txt")+MAPAS_DIR_CUSTOM.glob("*.txt"))`.
3. Pedi explicacao, sem codar, de como carregar cidades em `Register.jsx` usando `city&State.js`.
4. Depois pedi ajuda para entender e implementar a logica de carregar cidades no React.
5. Pedi explicacao da formula:
   `desempenho_J = -(alpha * custo_caminho) - (beta * nos_expandidos) - (gamma * t_total)`.
6. Perguntei, com base nos requisitos do trabalho, o que ainda faltava fazer.
7. Pedi a criacao deste `uso_ia.md` curto e direto.

## Solucoes sugeridas/aplicadas

- Corrigir a funcao de cidades no JavaScript puro:
  - receber o id do estado;
  - usar `document.createElement("option")`;
  - preencher o select `cidades`, nao o select `estados`.

- Corrigir a soma de `glob()` em Python usando lista:
  - transformar os iteradores em lista antes de somar;
  - alternativa sugerida: usar unpacking com `[*glob1, *glob2]`.

- No React, ligar o select de estados ao carregamento de cidades:
  - criar um handler em `Register.jsx`;
  - pegar `event.currentTarget.value`;
  - chamar `carregarCidades(estadoId)`;
  - passar o handler para `RegisterPage.jsx`;
  - usar esse handler no `onChange` do select de estados.

- Explicar a metrica `desempenho_J`:
  - `custo_caminho` vem de `resultado.custo_caminho`;
  - `nos_expandidos` vem de `resultado.nos_expandidos`;
  - `t_total` e calculado com `perf_counter()`;
  - `alpha`, `beta` e `gamma` sao pesos definidos no servico;
  - a metrica penaliza custo, expansoes e tempo.

- Revisar os requisitos do TP:
  - Semana 1 esta quase pronta;
  - ainda faltam analise escrita, visualizacao melhor, busca local, busca online, relatorio e auditoria de IA.

## Trechos de codigo sugeridos por IA

- Uso de lista para juntar mapas:

```python
for mapa in sorted([*MAPAS_DIR.glob("*.txt"), *MAPAS_DIR_CUSTOM.glob("*.txt")]):
```

- Handler de mudanca de estado no React:

```jsx
const handleEstadoChange = (event) => {
  const estadoId = event.currentTarget.value;

  if (!estadoId) {
    return;
  }

  carregarCidades(estadoId);
};
```

- Formula de desempenho analisada:

```python
desempenho_J = -(alpha * custo_caminho) - (beta * nos_expandidos) - (gamma * t_total)
```

## Sugestoes rejeitadas

- Nao foram adotadas solucoes prontas de bibliotecas externas para os algoritmos de busca.
- A IA foi usada para explicacao e revisao, nao para substituir o entendimento do codigo.

## Erros ou limitacoes da IA

- Em alguns momentos, a IA procurou arquivos no diretorio errado antes de localizar o projeto correto.
- Algumas validacoes automaticas nao puderam ser feitas diretamente quando o arquivo era `.jsx`.

## Como a solucao foi validada

- Conferencia manual dos arquivos indicados.
- Verificacao da logica de chamadas entre funcoes.
- Uso de comandos como `node --check` quando aplicavel.
- Comparacao do codigo existente com os requisitos do enunciado do TP.

## Modificacoes feitas por mim

- O grupo manteve o controle das decisoes finais.
- As sugestoes da IA foram adaptadas ao codigo existente.
- A implementacao final deve ser revisada e explicada pelo grupo na entrega.
