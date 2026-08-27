from fastapi import FastAPI

app = FastAPI()

# Coleção de 5 produtos em memória (aula 02)
produtos = [
    {"id": 1, "nome": "Notebook", "preco": 3500},
    {"id": 2, "nome": "Mouse", "preco": 80},
    {"id": 3, "nome": "Teclado", "preco": 150},
    {"id": 4, "nome": "Monitor", "preco": 1200},
    {"id": 5, "nome": "Impressora", "preco": 300}
]


@app.get("/api/produtos/")
def listar_produtos():
    return produtos


# Rodar servidor:
# uvicorn aula2_api_basica_get_colecao:app --reload
# Acesse a documentação em http://localhost:8000/docs
