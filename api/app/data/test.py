from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parents[2]
SEARCH_DIR = BASE_DIR / "app" / "algorithms" / "search"

for path in (BASE_DIR, SEARCH_DIR):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from app.data.labirinto import Labirinto
from app.algorithms.search.dfs import busca_dfs


def main():
    lab = Labirinto(str(Path(__file__).parent / "labyrinths" / "lab1.txt"))
    busca_dfs(lab)
    lab.print()
    print(lab.num_explored)


if __name__ == "__main__":
    main()
