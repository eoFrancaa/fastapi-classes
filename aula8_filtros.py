from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class ProdutoInput(BaseModel):
    nome: str | None = None
    preco: float | None = None


def validar_produto(nome, preco):
    erros = {}

    if nome is None:
        erros["nome"] = "O campo é obrigatório."
    elif not isinstance(nome, str):
        erros["nome"] = "O campo deve ser uma string."
    else:
        nome_limpo = nome.strip()
        if nome_limpo == "":
            erros["nome"] = "O campo não pode ser vazio."
        elif len(nome_limpo) < 2 or len(nome_limpo) > 100:
            erros["nome"] = "O nome deve possuir entre 2 e 100 caracteres."

    if preco is None:
        erros["preco"] = "O campo é obrigatório."
    elif not isinstance(preco, (int, float)) or isinstance(preco, bool):
        erros["preco"] = "O campo deve ser numérico."
    elif preco <= 0:
        erros["preco"] = "O preço deve ser maior que zero."
    elif round(preco, 2) != preco:
        erros["preco"] = "O campo deve ter no máximo 2 casas decimais."

    return erros


# Coleção de 5 produtos em memória (aula 8)
produtos = [
    {"id": 1, "nome": "Notebook", "preco": 3500},
    {"id": 2, "nome": "Mouse", "preco": 80},
    {"id": 3, "nome": "Teclado", "preco": 150},
    {"id": 4, "nome": "Monitor", "preco": 1200},
    {"id": 5, "nome": "Impressora", "preco": 300},
]


@app.get("/api/produtos/")
def listar_produtos(preco_minimo: str | None = None, preco_maximo: str | None = None):
    erros = {}

    if preco_minimo is not None:
        try:
            preco_minimo = float(preco_minimo)
        except ValueError:
            erros["preco_minimo"] = "O valor deve ser numérico."

    if preco_maximo is not None:
        try:
            preco_maximo = float(preco_maximo)
        except ValueError:
            erros["preco_maximo"] = "O valor deve ser numérico."

    if erros:
        raise HTTPException(status_code=400, detail=erros)

    resultado = produtos

    if preco_minimo is not None:
        resultado = [p for p in resultado if p["preco"] >= preco_minimo]
    if preco_maximo is not None:
        resultado = [p for p in resultado if p["preco"] <= preco_maximo]

    return resultado


@app.get("/api/produtos/{id}/")
def buscar_produto_por_id(id: int):
    for produto in produtos:
        if produto["id"] == id:
            return produto
    raise HTTPException(status_code=404, detail="Produto não encontrado.")


@app.post("/api/produtos/", status_code=201)
def criar_produto(produto: ProdutoInput):
    nome_limpo = produto.nome.strip() if produto.nome is not None else None
    erros = validar_produto(nome_limpo, produto.preco)
    if erros:
        raise HTTPException(status_code=400, detail=erros)

    novo_id = max(item["id"] for item in produtos) + 1
    novo_produto = {"id": novo_id, "nome": nome_limpo, "preco": produto.preco}
    produtos.append(novo_produto)
    return novo_produto


@app.put("/api/produtos/{id}/")
def atualizar_produto(id: int, produto: ProdutoInput):
    for index, item in enumerate(produtos):
        if item["id"] == id:
            nome_limpo = produto.nome.strip() if produto.nome is not None else None
            erros = validar_produto(nome_limpo, produto.preco)
            if erros:
                raise HTTPException(status_code=400, detail=erros)
            produtos[index] = {"id": id, "nome": nome_limpo, "preco": produto.preco}
            return produtos[index]
    raise HTTPException(status_code=404, detail="Produto não encontrado.")


@app.delete("/api/produtos/{id}/", status_code=204)
def remover_produto(id: int):
    for index, item in enumerate(produtos):
        if item["id"] == id:
            produtos.pop(index)
            return
    raise HTTPException(status_code=404, detail="Produto não encontrado.")


# Rodar servidor:
# uvicorn aula8_filtros:app --reload
# Acesse a documentação em http://localhost:8000/docs