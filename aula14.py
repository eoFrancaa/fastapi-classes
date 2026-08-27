import json

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

ARQUIVO_JSON = "produtos_aula14.json"

# Aula 14 - Exercício 1 - Adicionar Marca no Produto

class ProdutoInput(BaseModel):
    nome: str | None = None
    preco: float | None = None


class RespostaPaginada(BaseModel):
    page: int
    page_size: int
    total_pages: int
    results: list[dict]


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


def carregar_produtos():
    try:
        with open(ARQUIVO_JSON, "r", encoding="utf-8") as arquivo:
            conteudo = arquivo.read()
    except FileNotFoundError:
        return []

    if conteudo.strip() == "":
        return []

    try:
        dados = json.loads(conteudo)
    except json.JSONDecodeError:
        return []

    if not isinstance(dados, list):
        return []

    return dados


def salvar_produtos(lista):
    with open(ARQUIVO_JSON, "w", encoding="utf-8") as arquivo:
        json.dump(lista, arquivo, indent=2, ensure_ascii=False)


produtos = carregar_produtos()


@app.get("/api/produtos/", response_model=RespostaPaginada)
def listar_produtos(
    preco_minimo: str | None = None,
    preco_maximo: str | None = None,
    search: str | None = None,
    ordering: str | None = None,
    page: str | None = None,
    page_size: str | None = None,
):
    erros = {}

    pagina = 1
    tamanho_pagina = 10

    if page is not None:
        if not page.isdigit() or int(page) < 1:
            erros["page"] = "O campo page deve ser um inteiro positivo."
        else:
            pagina = int(page)

    if page_size is not None:
        if not page_size.isdigit() or int(page_size) < 1:
            erros["page_size"] = "O campo page_size deve ser um inteiro positivo."
        else:
            tamanho_pagina = int(page_size)
            if tamanho_pagina > 100:
                erros["page_size"] = "O campo page_size não pode passar de 100."

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

    campos_ordenacao = ["nome", "preco"]
    campo_ordenacao = None
    ordem_desc = False
    if ordering is not None:
        if ordering.lstrip("-") in campos_ordenacao:
            campo_ordenacao = ordering.lstrip("-")
            ordem_desc = ordering.startswith("-")
        else:
            erros["ordering"] = "Campo de ordenação inválido."

    if erros:
        raise HTTPException(status_code=400, detail=erros)

    resultado = produtos

    if preco_minimo is not None:
        resultado = [p for p in resultado if p["preco"] >= preco_minimo]
    if preco_maximo is not None:
        resultado = [p for p in resultado if p["preco"] <= preco_maximo]

    if search is not None:
        termo = search.lower()
        resultado = [p for p in resultado if termo in p["nome"].lower()]

    if campo_ordenacao == "preco":
        resultado.sort(key=lambda p: p["preco"], reverse=ordem_desc)
    elif campo_ordenacao == "nome":
        resultado.sort(key=lambda p: p["nome"].lower(), reverse=ordem_desc)

    total = len(resultado)
    total_pages = (total + tamanho_pagina - 1) // tamanho_pagina
    inicio = (pagina - 1) * tamanho_pagina
    itens_da_pagina = resultado[inicio : inicio + tamanho_pagina]

    return RespostaPaginada(
        page=pagina,
        page_size=tamanho_pagina,
        total_pages=total_pages,
        results=itens_da_pagina,
    )


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

    novo_id = max([item["id"] for item in produtos], default=0) + 1
    novo_produto = {"id": novo_id, "nome": nome_limpo, "preco": produto.preco}
    produtos.append(novo_produto)
    salvar_produtos(produtos)
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
            salvar_produtos(produtos)
            return produtos[index]
    raise HTTPException(status_code=404, detail="Produto não encontrado.")


@app.delete("/api/produtos/{id}/", status_code=204)
def remover_produto(id: int):
    for index, item in enumerate(produtos):
        if item["id"] == id:
            produtos.pop(index)
            salvar_produtos(produtos)
            return
    raise HTTPException(status_code=404, detail="Produto não encontrado.")


# Rodar servidor:
# uvicorn aula14:app --reload
# Acesse a documentação em http://localhost:8000/docs