<div align="center">
  <img src="logo.png" alt="logo" width="200"/>
</div>

# HordaMaster API

![GitHub repo size](https://img.shields.io/github/repo-size/maisepmaya/back-end-puc-rio-project?style=for-the-badge)
![GitHub language count](https://img.shields.io/github/languages/count/maisepmaya/back-end-puc-rio-project?style=for-the-badge)

A **HordaMaster API** foi desenvolvida em **Flask** para gerenciar fichas e cartões de inimigos em jogos de RPG.  
Ela permite **criar, visualizar, atualizar e excluir** fichas de monstros, organizando grandes grupos de adversários de forma prática.

🔗 Para a interface visual e gerenciamento no **frontend**, confira o repositório do [HordaMaster Frontend](https://github.com/maisepmaya/front-end-puc-rio-project.git).

## 🚀 Tecnologias utilizada

- Python 
- SQLite
- Flask

## 📥 Instalação e Execução

```bash
# Clone o repositório
git clone https://github.com/maisepmaya/back-end-puc-rio-project.git
cd back-end-puc-rio-project

# Crie e ative o ambiente virtual
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows

# Instale as dependências
pip install -r requirements.txt

# Execute em modo desenvolvimento
flask run --host 0.0.0.0 --port 5000 --reload

# Ou em modo de produção
flask run --host 0.0.0.0 --port 5000
```

## 🐳 Executando com Docker

```bash
# Construa a imagem
docker build -t hordamaster-api .

# Execute o container
docker run -d -p 5000:5000 hordamaster-api
```

## ⚔️ Funcionalidades

#### Gerenciamento de Fichas

- **Criar uma nova ficha** → POST /sheet/create
- **Remover uma ficha** → DELETE /sheet/delete
- **Listar todas as fichas** → GET /sheet/getAll

#### Gerenciamento de Cartões
- **Criar um novo cartão** → POST /card/create
- **Remover um cartão** → DELETE /card/delete
- **Remover todos os cartões** → DELETE /card/deleteAll
- **Atualizar um cartão** → PUT /card/update
- **Listar todos os cartões** → GET /card/getAll

## 📂 Estrutura do Projeto

``` bash
/
├── app.py            # Arquivo principal da aplicação
├── model/            # Modelos do banco de dados
├── schemas/          # Definição dos esquemas de entrada/saída
├── requirements.txt  # Lista de dependências do projeto
├── Dockerfile        # Arquivo do Docker
└── README.md         # Documentação do projeto
```

---

# Documentação da API HordaMaster

A documentação completa e interativa da API está disponível via Swagger UI. Com o servidor em execução, acesse:
[http://localhost:5000/](http://localhost:5000/)

Abaixo está um resumo dos endpoints, parâmetros e respostas esperadas.


## Fichas (`/sheet`)

### Criar uma nova ficha

Cria uma nova ficha de inimigo.

```http
POST /sheet/create
```

**Corpo da Requisição (`application/json`):**
```json
{
  "name": "Goblin Lançador",
  "level": 1,
  "life": 7,
  "ac": 15,
  "icon": "path/to/icon.png",
  "info": "Ataque: +4, Dardo: 1d4+2"
}
```

**Respostas:**
- **`200 OK`**: Retorna a ficha criada (`SheetViewSchema`).
- **`409 Conflict`**: Uma ficha com o mesmo nome já existe.
- **`400 Bad Request`**: Erro de validação ou erro inesperado.

### Remover uma ficha

Remove uma ficha e todos os seus cartões associados.

```http
DELETE /sheet/delete?id={sheet_id}
```

**Parâmetros da Query:**
| Parâmetro | Tipo     | Descrição                  |
|-----------|----------|------------------------------|
| `id`      | `string` | **Obrigatório.** ID da ficha a ser removida. |

**Respostas:**
- **`200 OK`**: Confirma a remoção.
- **`404 Not Found`**: Ficha não encontrada.

### Listar todas as fichas

Retorna as fichas, com um filtro opcional por tipo.

```http
GET /sheet/getAll?type={sheet_type}
```

**Parâmetros da Query:**
| Parâmetro | Tipo     | Descrição                               |
|-----------|----------|-------------------------------------------|
| `type`    | `string` | Opcional. Filtra por tipo: `independent` ou `dependent`. |

**Respostas:**
- **`200 OK`**: Retorna um objeto contendo as fichas (`ObjectSheetsSchema`).
- **`400 Bad Request`**: Erro inesperado.

## Cartões (`/card`)

### Criar um novo cartão

Cria um novo cartão de combate. O cartão pode ser criado a partir de uma ficha existente (passando o `id` da ficha) ou criando uma nova ficha "dependente" (passando um objeto de ficha completo).

```http
POST /card/create
```

**Corpo da Requisição (`application/json`):**

*Exemplo 1: A partir de uma ficha existente*
```json
{
  "index": 1,
  "sheet": "id-da-ficha-existente"
}
```

*Exemplo 2: Criando uma ficha dependente*
```json
{
  "index": 2,
  "sheet": {
    "name": "Orc Chefe",
    "level": 3,
    "life": 30,
    "ac": 16,
    "icon": "path/to/orc-chefe.png",
    "info": "Grito de Guerra: Aliados ganham +1 de ataque."
  }
}
```

**Respostas:**
- **`200 OK`**: Retorna o cartão criado (`CardViewSchema`).
- **`404 Not Found`**: A ficha (com o `id` informado) não foi encontrada.
- **`400 Bad Request`**: Erro de validação ou erro inesperado.

### Remover um cartão

Remove um cartão específico. Se o cartão estiver associado a uma ficha do tipo `dependent`, a ficha também será removida.

```http
DELETE /card/delete?id={card_id}
```

**Parâmetros da Query:**
| Parâmetro | Tipo     | Descrição                  |
|-----------|----------|------------------------------|
| `id`      | `string` | **Obrigatório.** ID do cartão a ser removido. |

**Respostas:**
- **`200 OK`**: Confirma a remoção.
- **`404 Not Found`**: Cartão não encontrado.
- **`400 Bad Request`**: Erro inesperado.


### Remover todos os cartões

Remove todos os cartões e todas as fichas do tipo `dependent`.

```http
DELETE /card/deleteAll
```

**Respostas:**
- **`200 OK`**: Confirma a remoção em massa.
- **`400 Bad Request`**: Erro inesperado.

### Atualizar um cartão

Atualiza os dados de um cartão, como seu índice, vida atual ou informações.

```http
PUT /card/update
```

**Corpo da Requisição (`application/json`):**
```json
{
  "id": "id-do-cartao-existente",
  "index": 5,
  "currLife": 12,
  "info": "Envenenado (2 turnos)"
}
```

**Respostas:**
- **`200 OK`**: Retorna o cartão atualizado (`CardViewSchema`).
- **`404 Not Found`**: Cartão não encontrado.
- **`400 Bad Request`**: Erro de validação ou erro inesperado.

### Listar todos os cartões

Retorna todos os cartões de combate ativos.

```http
GET /card/getAll
```

**Respostas:**
- **`200 OK`**: Retorna um objeto contendo os cartões (`ObjectCardSchema`).
- **`400 Bad Request`**: Erro inesperado.


#

📜 Projeto da **Pós-Graduação em Desenvolvimento Full-Stack** - **PUC-Rio**.
