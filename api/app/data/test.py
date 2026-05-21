# api/app/data/test.py
from pathlib import Path
import sys

# Configuração do caminho para o Python encontrar a pasta 'app'
BASE_DIR = Path(__file__).resolve().parents[2]
SEARCH_DIR = BASE_DIR / "app" / "algorithms" / "search"

for path in (BASE_DIR, SEARCH_DIR):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

# Importa a Interface unificada
from app.services.test.Interface import Interface

def main():
    # Instancia e inicia o loop da interface
    programa = Interface()
    programa.iniciar()

if __name__ == "__main__":
    main()