#!/usr/bin/env bash
set -euo pipefail

# Gera um dump simples do projeto em um único comando.
# Uso: ./script.sh

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUTPUT="$ROOT/projeto_dump.txt"
TMP_OUTPUT="$(mktemp /tmp/agente-labirinto-dump.XXXXXX)"

cleanup() {
  rm -f "$TMP_OUTPUT"
}
trap cleanup EXIT

ALLOWED_EXT='py|md|txt|json|yaml|yml|toml|ini|env|sh|js|ts|jsx|tsx|html|css|scss|sql|go|rs|java|kt|c|h|cpp|hpp|rb|php|cs'
EXCLUDE_DIRS='\.git|node_modules|dist|build|out|\.venv|venv|env|__pycache__|coverage|\.idea|\.vscode'
EXCLUDE_FILES='package-lock\.json|yarn\.lock|pnpm-lock\.yaml|projeto_dump\.txt'

include_file() {
  local file="$1"
  local rel="${file#$ROOT/}"
  local base
  base="$(basename "$file")"

  if echo "$rel" | grep -qE "(^|/)($EXCLUDE_DIRS)(/|$)"; then
    return 1
  fi

  if echo "$base" | grep -qiE "^($EXCLUDE_FILES)$"; then
    return 1
  fi

  local ext="${base##*.}"
  if ! echo "$base" | grep -qiE '^(dockerfile|makefile|procfile|gemfile)$'; then
    if ! echo "$ext" | grep -qiE "^($ALLOWED_EXT)$"; then
      return 1
    fi
  fi

  if file "$file" 2>/dev/null | grep -qiE 'binary|ELF|image|audio|video'; then
    return 1
  fi

  return 0
}

{
  echo "========================================================"
  echo " PROJETO: $(basename "$ROOT")"
  echo " Gerado em: $(date '+%Y-%m-%d %H:%M:%S')"
  echo "========================================================"
  echo ""

  echo "## ESTRUTURA DO PROJETO"
  echo ""
  while IFS= read -r -d '' file; do
    if include_file "$file"; then
      rel="${file#$ROOT/}"
      depth=$(printf '%s' "$rel" | tr -cd '/' | wc -c | tr -d ' ')
      indent=""
      for _ in $(seq 1 "$depth"); do
        indent="${indent}  "
      done
      echo "${indent}└── $rel"
    fi
  done < <(find "$ROOT" -type f -print0 | sort -z)

  echo ""
  echo "========================================================"
  echo ""
  echo "## CONTEÚDO DOS ARQUIVOS"
  echo ""

  while IFS= read -r -d '' file; do
    if ! include_file "$file"; then
      continue
    fi

    rel="${file#$ROOT/}"
    echo "### $rel"
    echo '```'
    cat "$file"
    echo '```'
    echo ""
  done < <(find "$ROOT" -type f -print0 | sort -z)
} > "$TMP_OUTPUT"

mv "$TMP_OUTPUT" "$OUTPUT"
trap - EXIT
echo "✅ Gerado: $OUTPUT"
