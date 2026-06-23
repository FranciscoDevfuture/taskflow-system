# 🚀 TaskFlow System

![Python](https://img.shields.io/badge/python-3.14-blue.svg)
![Flask](https://img.shields.io/badge/flask-2.3.3-green.svg)
![Status](https://img.shields.io/badge/status-em%20desenvolvimento-yellow)

> Uma API RESTful para gerenciamento ágil de tarefas, desenvolvida com Flask e boas práticas de Engenharia de Software.

## 📋 Sobre o Projeto

O **TaskFlow System** é uma API de gerenciamento de tarefas que permite autenticação de usuários, CRUD completo de tarefas, filtros por status e prioridade, além de contar com testes automatizados e integração contínua. Foi desenvolvido como parte do curso de Engenharia de Software na Unifecaf.

### 🎯 Principais Funcionalidades

- ✅ **Autenticação segura**: Login e logout com sessão Flask
- ✅ **CRUD completo de tarefas**: Criar, listar, atualizar e deletar tarefas
- ✅ **Filtros avançados**: Por status (`a_fazer`, `em_progresso`, `concluido`) e prioridade (`baixa`, `media`, `alta`, `critica`)
- ✅ **Validações robustas**: Campos obrigatórios, transições de status válidas e regras de negócio
- ✅ **Testes automatizados**: 85 testes com Pytest
- ✅ **CI/CD**: Pipeline automatizado com GitHub Actions

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Finalidade |
|------------|------------|
| **Python 3.14** | Linguagem de programação |
| **Flask** | Framework web |
| **SQLite** | Banco de dados (em memória para testes) |
| **Pytest** | Testes automatizados |
| **GitHub Actions** | Integração contínua |
| **Postman** | Testes manuais da API |

## 📁 Estrutura do Projeto
taskflow-system/
├── src/
│ ├── models/ # Modelos de dados (Usuário, Tarefa)
│ ├── routes/ # Rotas da API (auth, tasks)
│ ├── utils/ # Utilitários e validadores
│ └── app.py # Fábrica da aplicação Flask
├── tests/ # Testes automatizados (85 testes)
├── requirements.txt # Dependências do projeto
└── README.md # Documentação




## 🚀 Como Executar o Projeto

### Pré-requisitos

- Python 3.14+
- Pip

### Passo a Passo

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/seu-usuario/taskflow-system.git
   cd taskflow-system/taskflow
Instale as dependências:
   pip install -r requirements.txt
Inicie o servidor:
   python -m src.app



   Acesse a API:

A API estará disponível em: http://localhost:5000

Health check: GET /


Credenciais para Teste
Login:


{
  "email": "admin@taskflow.com",
  "senha": "admin123"
}

Registro (via script):

python init_usuario.py



 Endpoints da API
Método	Endpoint	Descrição
POST	/auth/login	Login de usuário
POST	/auth/logout	Logout
GET	/auth/me	Dados do usuário logado
GET	/tasks	Listar tarefas
GET	/tasks?status={status}	Filtrar por status
GET	/tasks?prioridade={prioridade}	Filtrar por prioridade
POST	/tasks	Criar tarefa
GET	/tasks/{id}	Buscar tarefa específica
PUT	/tasks/{id}	Atualizar tarefa
PATCH	/tasks/{id}/status	Mudar status da tarefa
DELETE	/tasks/{id}	Deletar tarefa


Exemplo de Criar Tarefa

POST /tasks
Content-Type: application/json

{
  "titulo": "Finalizar relatório",
  "descricao": "Completar o relatório mensal",
  "prioridade": "alta"
}

🧪 Testes Automatizados
O projeto conta com 85 testes que garantem a confiabilidade do sistema.

Executar os testes:
python -m pytest tests/ -v


Cobertura de Testes
✅ Modelos de dados (Usuário, Tarefa)
✅ Rotas de autenticação (login, logout, sessão)
✅ Rotas de tarefas (CRUD, filtros, status)
✅ Validações e regras de negócio
✅ Transições de status


Ler 11 páginas da web
Claro! Aqui está um modelo de README.md para o seu projeto TaskFlow, baseado em tudo que vimos até agora e pronto para ser usado no GitHub e no seu vídeo. 📝

markdown
# 🚀 TaskFlow System

![Python](https://img.shields.io/badge/python-3.14-blue.svg)
![Flask](https://img.shields.io/badge/flask-2.3.3-green.svg)
![Status](https://img.shields.io/badge/status-em%20desenvolvimento-yellow)

> Uma API RESTful para gerenciamento ágil de tarefas, desenvolvida com Flask e boas práticas de Engenharia de Software.

## 📋 Sobre o Projeto

O **TaskFlow System** é uma API de gerenciamento de tarefas que permite autenticação de usuários, CRUD completo de tarefas, filtros por status e prioridade, além de contar com testes automatizados e integração contínua. Foi desenvolvido como parte do curso de Engenharia de Software na Unifecaf.

### 🎯 Principais Funcionalidades

- ✅ **Autenticação segura**: Login e logout com sessão Flask
- ✅ **CRUD completo de tarefas**: Criar, listar, atualizar e deletar tarefas
- ✅ **Filtros avançados**: Por status (`a_fazer`, `em_progresso`, `concluido`) e prioridade (`baixa`, `media`, `alta`, `critica`)
- ✅ **Validações robustas**: Campos obrigatórios, transições de status válidas e regras de negócio
- ✅ **Testes automatizados**: 85 testes com Pytest
- ✅ **CI/CD**: Pipeline automatizado com GitHub Actions

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Finalidade |
|------------|------------|
| **Python 3.14** | Linguagem de programação |
| **Flask** | Framework web |
| **SQLite** | Banco de dados (em memória para testes) |
| **Pytest** | Testes automatizados |
| **GitHub Actions** | Integração contínua |
| **Postman** | Testes manuais da API |

## 📁 Estrutura do Projeto
taskflow-system/
├── src/
│ ├── models/ # Modelos de dados (Usuário, Tarefa)
│ ├── routes/ # Rotas da API (auth, tasks)
│ ├── utils/ # Utilitários e validadores
│ └── app.py # Fábrica da aplicação Flask
├── tests/ # Testes automatizados (85 testes)
├── requirements.txt # Dependências do projeto
└── README.md # Documentação

text

## 🚀 Como Executar o Projeto

### Pré-requisitos

- Python 3.14+
- Pip

### Passo a Passo

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/seu-usuario/taskflow-system.git
   cd taskflow-system/taskflow
Instale as dependências:

bash
pip install -r requirements.txt
Inicie o servidor:

bash
python -m src.app
Acesse a API:

A API estará disponível em: http://localhost:5000

Health check: GET /

🔑 Credenciais para Teste
Login:

json
{
  "email": "admin@taskflow.com",
  "senha": "admin123"
}
Registro (via script):

bash
python init_usuario.py
📚 Endpoints da API
Método	Endpoint	Descrição
POST	/auth/login	Login de usuário
POST	/auth/logout	Logout
GET	/auth/me	Dados do usuário logado
GET	/tasks	Listar tarefas
GET	/tasks?status={status}	Filtrar por status
GET	/tasks?prioridade={prioridade}	Filtrar por prioridade
POST	/tasks	Criar tarefa
GET	/tasks/{id}	Buscar tarefa específica
PUT	/tasks/{id}	Atualizar tarefa
PATCH	/tasks/{id}/status	Mudar status da tarefa
DELETE	/tasks/{id}	Deletar tarefa
Exemplo de Criar Tarefa
bash
POST /tasks
Content-Type: application/json

{
  "titulo": "Finalizar relatório",
  "descricao": "Completar o relatório mensal",
  "prioridade": "alta"
}
🧪 Testes Automatizados
O projeto conta com 85 testes que garantem a confiabilidade do sistema.

Executar os testes:

bash
python -m pytest tests/ -v
Cobertura de Testes
✅ Modelos de dados (Usuário, Tarefa)

✅ Rotas de autenticação (login, logout, sessão)

✅ Rotas de tarefas (CRUD, filtros, status)

✅ Validações e regras de negócio

✅ Transições de status

🔄 Integração Contínua (CI)
O projeto utiliza GitHub Actions para CI/CD. A cada push ou pull request para a branch main, o pipeline automaticamente:

🔍 Executa linting

✅ Roda todos os testes automatizados

📊 Gera relatório de cobertura

https://img.shields.io/github/actions/workflow/status/seu-usuario/taskflow-system/tests.yml

📊 Kanban e Metodologia Ágil
O desenvolvimento foi organizado utilizando a metodologia ágil Kanban, com as seguintes colunas:

📋 Backlog: Histórias planejadas

🔨 Em Desenvolvimento: Tarefas em andamento

✅ Concluído: Entregues

Essa organização garantiu visibilidade total do progresso e priorização eficiente das entregas.


Mudança de Escopo
Durante o desenvolvimento, uma mudança de escopo significativa foi realizada: a autenticação migrou de JWT (JSON Web Token) para sessão Flask. Essa decisão foi tomada para:

Simplificar a demonstração do sistema

Facilitar os testes manuais com Postman

Reduzir a complexidade de configuração

A mudança foi gerenciada através de atualização do backlog, ajuste das tarefas e nova documentação, demonstrando a flexibilidade da metodologia ágil.

🔧 Melhorias Futuras
Migrar para banco de dados persistente (PostgreSQL)

Implementar autenticação com JWT

Adicionar refresh token

Implementar cache com Redis

Criar um frontend com Vue.js ou React

🤝 Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.

👨‍💻 Autor
Francisco Santos - Desenvolvedor do TaskFlow System

📜 Licença
Este projeto está sob a licença MIT - veja o arquivo LICENSE para mais detalhes.

🙏 Agradecimentos
Professores e colegas do curso de Engenharia de Software - Unifecaf

Comunidade open-source.




