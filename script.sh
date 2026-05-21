#!/usr/bin/env bash
# dump_project.sh — gera um .txt com árvore + conteúdo do projeto pra colar no ChatGPT
# Uso: ./dump_project.sh [pasta_raiz] [arquivo_saida]
# Ex:  ./dump_project.sh . meu_projeto.txt
#      ./dump_project.sh ~/projetos/app contexto.txt

ROOT="${1:-.}"
OUTPUT="${2:-projeto_dump.txt}"

# ── Extensões de texto/código permitidas ──────────────────────────────────────
ALLOWED_EXT="js|ts|jsx|tsx|mjs|cjs|vue|svelte|astro|\
py|pyi|ipynb|\
c|h|cpp|hpp|cc|\
java|kt|scala|\
go|rs|rb|php|cs|\
html|htm|css|scss|sass|less|\
json|jsonc|yaml|yml|toml|ini|env|env\.example|\
sh|bash|zsh|fish|ps1|\
md|mdx|txt|rst|\
sql|graphql|gql|\
dockerfile|makefile|cmake"

# ── Diretórios e arquivos a ignorar ──────────────────────────────────────────
EXCLUDE_DIRS="node_modules|\.git|\.svn|dist|build|out|\.next|\.nuxt|\
__pycache__|\.venv|venv|env|\.env|\.mypy_cache|\.pytest_cache|\
target|\.cargo|vendor|\.gradle|\.idea|\.vscode|coverage|\.nyc_output|\
\.turbo|\.parcel-cache|storybook-static|\.storybook/public"

EXCLUDE_FILES="package-lock\.json|yarn\.lock|pnpm-lock\.yaml|\
composer\.lock|Cargo\.lock|Gemfile\.lock|poetry\.lock|\
\.DS_Store|thumbs\.db|\.gitignore|\.gitattributes"

MAX_FILE_BYTES=100000  # ignora arquivos > 100KB (gerados, minificados etc.)

# ─────────────────────────────────────────────────────────────────────────────

ROOT="$(realpath "$ROOT")"

if [ ! -d "$ROOT" ]; then
  echo "Erro: '$ROOT' não é uma pasta válida." >&2
  exit 1
fi

echo "📂 Gerando dump de: $ROOT"
echo "📄 Saída: $OUTPUT"

{
  # ── Cabeçalho ──
  echo "========================================================"
  echo " PROJETO: $(basename "$ROOT")"
  echo " Gerado em: $(date '+%Y-%m-%d %H:%M:%S')"
  echo "========================================================"
  echo ""

  # ── Árvore de arquivos ────────────────────────────────────────────────────
  echo "## ESTRUTURA DO PROJETO"
  echo ""

  if command -v tree &>/dev/null; then
    # tree instalado: usa ele com exclusões
    TREE_IGNORE=$(echo "$EXCLUDE_DIRS" | tr '|' '\n' | sed 's/\\//g' | tr '\n' '|' | sed 's/|$//')
    tree "$ROOT" -a --noreport -I "$TREE_IGNORE" 2>/dev/null
  else
    # fallback: simula árvore com find + indentação
    echo "(instale 'tree' para melhor visualização: sudo apt install tree)"
    echo ""
    find "$ROOT" -not \( \
      $(echo "$EXCLUDE_DIRS" | tr '|' '\n' | while read d; do echo "-path '*/$d' -prune -o"; done) \
      -false \
    \) -type f | sort | while read -r file; do
      rel="${file#$ROOT/}"
      depth=$(echo "$rel" | tr -cd '/' | wc -c)
      indent=$(printf '%0.s  ' $(seq 1 $depth))
      echo "${indent}└── $(basename "$rel")"
    done
  fi

  echo ""
  echo "========================================================"
  echo ""

  # ── Conteúdo dos arquivos ─────────────────────────────────────────────────
  echo "## CONTEÚDO DOS ARQUIVOS"
  echo ""

  TOTAL=0
  SKIPPED=0

  while IFS= read -r -d '' file; do
    rel="${file#$ROOT/}"

    # Pula por diretório
    if echo "$rel" | grep -qE "(^|/)($EXCLUDE_DIRS)/"; then
      continue
    fi

    # Pula por nome de arquivo
    basename_file="$(basename "$file")"
    if echo "$basename_file" | grep -qiE "^($EXCLUDE_FILES)$"; then
      ((SKIPPED++))
      continue
    fi

    # Pula por extensão (só permite as listadas, case-insensitive)
    ext="${basename_file##*.}"
    # Trata arquivos sem extensão (Dockerfile, Makefile)
    if ! echo "$basename_file" | grep -qiE "^(dockerfile|makefile|rakefile|procfile|gemfile|brewfile)$"; then
      if ! echo "$ext" | grep -qiE "^($ALLOWED_EXT)$"; then
        ((SKIPPED++))
        continue
      fi
    fi

    # Pula arquivos grandes
    filesize=$(wc -c < "$file" 2>/dev/null || echo 0)
    if [ "$filesize" -gt "$MAX_FILE_BYTES" ]; then
      echo "### $rel"
      echo "[IGNORADO: arquivo muito grande ($(( filesize / 1024 ))KB > 100KB)]"
      echo ""
      ((SKIPPED++))
      continue
    fi

    # Pula binários (verifica se tem bytes nulos)
    if file "$file" 2>/dev/null | grep -qE "binary|executable|ELF|image|audio|video"; then
      ((SKIPPED++))
      continue
    fi

    # Imprime conteúdo
    echo "### $rel"
    echo '```'
    cat "$file"
    echo '```'
    echo ""
    ((TOTAL++))

  done < <(find "$ROOT" -type f -print0 | sort -z)

  echo "========================================================"
  echo " RESUMO: $TOTAL arquivo(s) incluído(s), $SKIPPED ignorado(s)"
  echo "========================================================"

} > "$OUTPUT"

# ── Stats finais ──────────────────────────────────────────────────────────────
SIZE=$(du -sh "$OUTPUT" 2>/dev/null | cut -f1)
LINES=$(wc -l < "$OUTPUT")

echo "✅ Pronto!"
echo "   Tamanho: $SIZE | Linhas: $LINES"
echo ""

if [ "$SIZE" != "${SIZE%[0-9]M}" ] || [ "${SIZE%.*}" -gt 2 ] 2>/dev/null; then
  echo "⚠️  Arquivo grande. Se o ChatGPT reclamar de contexto, rode com uma subpasta:"
  echo "   ./dump_project.sh ./src output.txt"
fi