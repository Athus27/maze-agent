from fastapi import FastAPI  # Importa classe FastAPI do módulo fastapi para criar API

app = FastAPI()

agentes_do_labirinto = {
    1: {"nome": "Agente Busca em Largura", "posicao_atual": [0,0]},
    2: {"nome": "Agente Busca Profundidade", "posicao_atual": [1,1]},
}
@app.get("/")  # Decorador que define uma rota HTTP GET no caminho raiz ("/") do servidor.
def read_root():
    return {"Hello": "World"}
    # Retorna Dicionario Python, FastAPI converte automaticamente para JSON


@app.get("/items/{item_id}")  # Define rota HTTP GET que aceita um param dinamico item_id na URL
def read_item(item_id: int, q: str | None = None):
    # 1. item_id: Capturado da URL e convertido obrigatoriamente para número inteiro (int).
    # 2. q: Um parâmetro opcional de busca na URL (?q=valor), que pode ser texto (str) ou nulo (None).
    return {"item_id": item_id, "q": q}
    # Retorna os dados processados e tipados em formato JSON.


@app.put("/items/{item_id}")  # Define rota HTTP PUT para atualizar um item específico identificado por item_id
def update_item(item_id: int, item: dict):
    return {"item_id": item_id, "item": item}
