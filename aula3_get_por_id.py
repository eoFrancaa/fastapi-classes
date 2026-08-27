from fastapi import FastAPI, HTTPException

app = FastAPI()

# Coleção de 5 produtos em memória (aula 03)
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


# Rodar servidor:
# uvicorn aula3_get_por_id:app --reload
# Acesse a documentação em http://localhost:8000/docs
