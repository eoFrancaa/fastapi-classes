from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class ProdutoInput(BaseModel):
    nome: str
    preco: float


# Coleção de 5 produtos em memória (aula 05)
produtos = [
    {"id": 1, "nome": "Notebook", "preco": 3500},
    {"id": 2, "nome": "Mouse", "preco": 80},
    {"id": 3, "nome": "Teclado", "preco": 150},
    {"id": 4, "nome": "Monitor", "preco": 1200},
    {"id": 5, "nome": "Impressora", "preco": 300},
]


@app.get("/api/produtos/")
def listar_produtos():
    return produtos


@app.get("/api/produtos/{id}/")
def buscar_produto_por_id(id: int):
    for produto in produtos:
        if produto["id"] == id:
            return produto
    raise HTTPException(status_code=404, detail="Produto não encontrado.")


@app.post("/api/produtos/", status_code=201)
def criar_produto(produto: ProdutoInput):
    novo_id = max(item["id"] for item in produtos) + 1
    novo_produto = {"id": novo_id, "nome": produto.nome, "preco": produto.preco}
    produtos.append(novo_produto)
    return novo_produto


@app.put("/api/produtos/{id}/")
def atualizar_produto(id: int, produto: ProdutoInput):
    for index, item in enumerate(produtos):
        if item["id"] == id:
            produtos[index] = {"id": id, "nome": produto.nome, "preco": produto.preco}
            return produtos[index]
    raise HTTPException(status_code=404, detail="Produto não encontrado.")


# Rodar servidor:
# uvicorn aula5_put:app --reload
# Acesse a documentação em http://localhost:8000/docs