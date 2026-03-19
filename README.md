# Case Itaú: Mastermind Web App

Bem-vindo ao repositório do projeto **Mastermind**, um jogo de dedução desenvolvido com as tecnologias modernas de backend e frontend solicitadas!

## 🚀 Tecnologias Integradas

- **Backend**: *Python 3.10+* & *FastAPI*
- **Database**: *MariaDB*
- **ORM**: *SQLAlchemy*
- **Autenticação**: *JWT (JSON Web Tokens)*
- **Frontend**: *Angular 15+* com componentes vanilla CSS premium e dark mode (glassmorphism)
- **Gerenciadores de Pacote**: `pip` & `npm`

## 🏗 Arquitetura

O Backend baseia-se num design em camadas rigoroso focado na separação de responsabilidades e injeção de dependência (`Depends` do FastAPI):
- **Controller**: Entradas de roteamento HTTP e respostas com Pydantic Schemas. (ex: `game_controller.py`)
- **Service**: Concentra a regra de negócio crua (cálculos de palpite do mastermind). (ex: `game_service.py`)
- **Repository**: Isolamento do ORM. Concentração e reaproveitamento do CRUD com o modelo (`game_repository.py`)
- **Model**: Mapeamento representativo usando classes de tabela do SQLAlchemy (`Game.py`).

O Frontend está desenhado usando os pilares do Angular: serviços reutilizáveis injetáveis e *HttpInterceptors* que adicionam a autorização Bearer globalmente, além de capturar tratativas de erro (HTTP 401, 400).

---

## 💻 Instruções para Executar Localmente

Você tem duas opções para rodar a aplicação: **via Docker Compose (Recomendado e mais fácil)** ou **manualmente**.

### Opção 1: Rodando com Docker Compose 🐳 (Recomendado)

Se você possui o [Docker](https://docs.docker.com/get-docker/) instalado, basta inicializar todo o ecossistema (banco, backend e frontend) com um único comando!

1. Abra o terminal na pasta raiz do projeto (`CaseItau`).
2. Execute o comando:
   ```bash
   docker-compose up --build -d
   ```
3. Aguarde o download das imagens e a compilação paralela.
4. Acesse os serviços:
   - **Frontend (O Jogo):** [http://localhost:8080](http://localhost:8080)
   - **Backend API Docs:** [http://localhost:8000/docs](http://localhost:8000/docs)

> 💡 *Para parar e remover os containers:* `docker-compose down`

---

### Opção 2: Iniciando Manualmente (Sem Docker)

Siga o passo a passo para rodar o banco de dados, o backend e o frontend simultaneamente de forma local.

#### 1. Preparando o Banco de Dados MariaDB
Certifique-se de ter um MariaDB rodando. Crie um schema principal chamado `mastermind`:
```sql
CREATE DATABASE mastermind CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 2. Backend (Python/FastAPI)

1. Acesse o terminal na pasta raiz e vá para o diretório de backend:
   ```bash
   cd backend
   ```
2. Crie e ative o ambiente virtual:
   - **No Windows:** `python -m venv venv` e depois `.\venv\Scripts\activate`
   - **No Linux/Mac:** `python3 -m venv venv` e depois `source venv/bin/activate`
3. Instale as bibliotecas usando o `pip`:
   ```bash
   pip install -r requirements.txt
   ```
4. Crie seu `.env` contendo as variáveis demonstradas no `.env.example`:
   - Altere a porta, URL, e os tokens caso o seu banco de dados local não seja `root:secret` em `localhost:3306`.
5. Inicie a API FastAPI via Uvicorn:
   ```bash
   uvicorn app.main:app --reload
   ```
   > 👉 **Docs Automáticas**: Assim que iniciado, a especificação livre OpenAPI interativa do Swagger poderá ser testada em [http://localhost:8000/docs](http://localhost:8000/docs).

### 3. Frontend (Angular 15+)

1. Abra um segundo terminal e acesse a raiz `frontend`:
   ```bash
   cd frontend
   ```
2. Baixe os pacotes:
   ```bash
   npm install
   ```
3. Inicie o servidor em modo de observação local:
   ```bash
   npm start
   ```
  > 👉 Acesse [http://localhost:8080/](http://localhost:8080/) para ver a aplicação com os estilos prontos.

---

## 🧪 Testes Unitários

- **Para o Backend (Pytest):**
  Como o backend contém uma pesada regra de negócios (Mastermind logic), usei Pytest para forjar rotas sobrepostas a um banco SQLite dinâmico que destrói a sessão ao fim dos testes unitários.
  ```bash
  cd backend
  pytest tests/ -v
  ```