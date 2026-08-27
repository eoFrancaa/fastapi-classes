# Exemplos de FastAPI das aulas

## Visão geral

Este projeto reúne exemplos usados nas aulas para demonstrar a construção de APIs com FastAPI,
começando com rotas básicas e avançando de forma incremental por CRUD, validação, filtros, busca,
ordenação, persistência em JSON e paginação.

A sequência é acumulativa: cada aula mantém tudo o que existe na anterior e acrescenta um
novo conceito. A `aula12` é a última aula conceitual e a `aula13` é a consolidação final.

## Requisitos

- Python 3.10 ou superior
- pip

## Instalação

1. Clone o repositório:

   ```bash
   git clone https://github.com/marrcandre/fastapi-bsi4.git
   cd fastapi-bsi4
   ```

2. Crie e ative um ambiente virtual:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

   No Windows, use:

   ```bash
   .venv\Scripts\activate
   ```

3. Atualize o pip e instale as dependências:

   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

## Como executar

Cada arquivo representa um exemplo independente. Inicie o servidor com o Uvicorn informando o
módulo e a aplicação. Por padrão, a API roda na porta **8000**.

Exemplo com a aula 02:

```bash
uvicorn aula2_api_basica_get_colecao:app --reload
```

Para executar outro exemplo, substitua o nome do módulo:

```bash
uvicorn aula13_api_completa:app --reload
```

Após iniciar o servidor, acesse a documentação interativa:

- http://localhost:8000/docs
- http://localhost:8000/redoc

## Estrutura dos exemplos

Sequência conceitual incremental:

- aula2_api_basica_get_colecao.py  — GET da coleção (5 produtos em memória)
- aula3_get_por_id.py              — GET por ID (5 em memória)
- aula4_post.py                    — POST (criação; 5 em memória)
- aula5_put.py                     — PUT (atualização completa; 5 em memória)
- aula6_delete.py                  — DELETE (remoção; 5 em memória)
- aula7_validacao.py               — validação de nome e preço (5 em memória)
- aula8_filtros.py                 — filtros de preço (5 em memória)
- aula9_busca.py                   — busca por nome (5 em memória)
- aula10_ordenacao.py              — ordenação (5 em memória)
- aula11_persistencia_json.py      — persistência em arquivo JSON (60 produtos)
- aula12_paginacao.py              — paginação (60 produtos persistidos)
- aula13_api_completa.py           — API completa (consolidação final)

### Contrato HTTP

As rotas seguem o contrato consolidado das três tecnologias (Express, FastAPI e Django REST):

```text
GET    /api/produtos/          lista (array simples nas aulas 2–11; paginada a partir da aula 12)
GET    /api/produtos/{id}/     produto individual
POST   /api/produtos/          cria produto (201)
PUT    /api/produtos/{id}/     atualiza produto por completo (200)
DELETE /api/produtos/{id}/     remove produto (204 sem corpo)
```

Respostas:

- GET: `200`; POST: `201`; PUT: `200`; DELETE: `204` sem corpo.
- Recurso inexistente: `404` com `{"detail": "Produto não encontrado."}`.
- Erro de validação: `400` com `{"detail": {campo: "mensagem"}}`.

## Dados

- As aulas 2–10 usam os **5 produtos em memória** definidos no próprio código.
- A partir da **Aula 11**, a fonte de dados passa a ser o arquivo `produtos.json`, com os
  **60 produtos-base** (`{id, nome, preco}`, ids 1–60). Esse arquivo é compartilhado com o Express
  e com o Django REST Framework.
- A **Aula 12** introduz a paginação sobre a coleção persistida (`page`/`page_size`, resposta
  `{page, page_size, total_pages, results}`).
- A **Aula 13** consolida a API completa, sem introduzir conceito novo.

## Recursos do FastAPI utilizados

O FastAPI aproveita seus recursos naturais, mantendo a implementação didática e explícita:

- type hints nos parâmetros e nas rotas;
- modelos Pydantic (`BaseModel`) para entrada de dados;
- `HTTPException` para erros com `detail`;
- documentação automática em `/docs` e `/redoc`.

Não são utilizados banco de dados, ORM, SQLAlchemy ou bibliotecas externas de persistência,
filtros ou paginação.

## Testes HTTP didáticos com Bruno

As coleções de testes ficam em `http/fastapi/` (formato nativo do [Bruno](https://www.usebruno.com/),
versionáveis no repositório). Cada pasta corresponde a uma aula e reúne as requisições HTTP que
exercem os endpoints daquela aula, com asserções de status/campos/estrutura/erros.

- `Aula 02` — GET da coleção (5 em memória)
- `Aula 03` — GET por ID (inclui caso 404)
- `Aula 04` — POST (criação)
- `Aula 05` — PUT (atualização completa)
- `Aula 06` — DELETE (remoção)
- `Aula 07` — validação de `nome` e `preco` (erros 400)
- `Aula 08` — filtros de preço
- `Aula 09` — busca por nome
- `Aula 10` — ordenação
- `Aula 11` — persistência em `produtos.json` (60 produtos)
- `Aula 12` — paginação
- `Aula 13` — integração (API completa)

Como executar:

1. Instale o app [Bruno](https://usebruno.com/) (desktop) — a coleção abre como pasta (`http/fastapi/`).
2. Abra a coleção e **selecione o ambiente `Local`** no seletor de ambientes (escopo da coleção).
   - O ambiente `Local` define `baseUrl = http://localhost:8000`.
   - As requisições usam `{{baseUrl}}/api/produtos/`, então **não é preciso editar cada requisição**.
3. Inicie a aula correspondente:
   ```bash
   uvicorn aula2_api_basica_get_colecao:app --reload   # ou a aula desejada (2 a 13)
   ```
4. Execute as requisições daquela pasta (o "Collection Runner" executa a pasta inteira).

Observações:

- Cada aula é um servidor independente na porta 8000 — execute uma por vez, usando a pasta que
  corresponde ao arquivo iniciado.
- As aulas 2–10 usam dados em memória (5 produtos definidos no código). As aulas 11–13 leem/gravam
  `produtos.json` (60 produtos); os testes dessas aulas criam e removem o mesmo recurso temporário
  (id 61, seguinte ao dataset-base), de modo que `produtos.json` termina no estado-base (60 produtos,
  ids 1–60) ao final da execução.
- A coleção acompanha a progressão: Aulas 2–10 respondem com array simples; a partir da Aula 12 o GET
  passa a ser paginado (`{ page, page_size, total_pages, results }`), operando sobre os 60 produtos
  persistidos.
