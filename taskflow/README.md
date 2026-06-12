# 📋 TaskFlow System



> **TechFlow Solutions** — Sistema de Gerenciamento de Tarefas Ágil  
> Desenvolvido como projeto prático da disciplina de Engenharia de Software — UniFECAF

---
Projeto

## 🎯 Objetivo

O **TaskFlow System** é uma API RESTful de gerenciamento de tarefas desenvolvida para uma startup de logística. O sistema permite acompanhar o fluxo de trabalho em tempo real, priorizar tarefas críticas e monitorar o desempenho da equipe.

## 📦 Escopo do Projeto

### Escopo Inicial (Sprint 1)
- Autenticação de usuários (login/logout com sessão JWT)
- CRUD completo de tarefas (criar, listar, atualizar, excluir)
- Controle de status: `A_FAZER` → `EM_PROGRESSO` → `CONCLUIDO`
- Testes unitários com Pytest
- Pipeline de CI com GitHub Actions

## Mudança de Escopo Aprovada em 08/06/2026

### ⚠️ Mudança de Escopo (Sprint 2)
**Funcionalidade adicionada:** Campo `prioridade` nas tarefas.

**Justificativa:** Durante a revisão da Sprint 1, o cliente (startup de logística) identificou que diferentes tarefas possuem urgências distintas e que a equipe precisava de um mecanismo para identificar rapidamente o que deveria ser atacado primeiro. A adição do campo `prioridade` com os valores `BAIXA`, `MEDIA`, `ALTA` e `CRITICA` foi aprovada por estar alinhada ao objetivo central do produto e por não impactar o cronograma da Sprint 2.

**Impacto:** Novo campo no modelo `Tarefa`, novo endpoint de filtro por prioridade, novos testes automatizados para validação do campo.

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Versão | Finalidade |
|---|---|---|
| Python | 3.11+ | Linguagem principal |
| Flask | 3.0+ | Framework web |
| Flask-Login | 0.6+ | Gerenciamento de sessões |
| Werkzeug | 3.0+ | Hash de senhas |
| Pytest | 8.0+ | Testes automatizados |
| pytest-cov | 4.0+ | Cobertura de testes |
| flake8 | 7.0+ | Qualidade de código |
| GitHub Actions | — | Integração Contínua (CI) |

---

## 📁 Estrutura de Diretórios

```
taskflow/
├── src/
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py          # Modelo de Usuário e Admin
│   │   └── task.py          # Modelo de Tarefa (Status, Prioridade)
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py          # Rotas de autenticação
│   │   └── tasks.py         # Rotas CRUD de tarefas
│   ├── utils/
│   │   ├── __init__.py
│   │   └── validators.py    # Funções de validação
│   └── app.py               # Factory da aplicação Flask
├── tests/
│   ├── conftest.py          # Fixtures compartilhadas
│   ├── test_user_model.py   # Testes unitários - Usuário
│   ├── test_task_model.py   # Testes unitários - Tarefa
│   ├── test_auth_routes.py  # Testes de integração - Auth
│   └── test_task_routes.py  # Testes de integração - Tarefas
├── docs/
│   └── api.md               # Documentação da API
├── .github/
│   └── workflows/
│       └── ci.yml           # Pipeline GitHub Actions
├── requirements.txt
├── .flake8
└── README.md
```

---

## 🚀 Como Executar

### Pré-requisitos
- Python 3.11+
- pip

### Instalação

```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/taskflow-system.git
cd taskflow-system

# 2. Crie e ative o ambiente virtual
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Execute a aplicação
python src/app.py
```

A API estará disponível em `http://localhost:5000`

### Executar os Testes

```bash
# Todos os testes com relatório de cobertura
pytest tests/ -v --cov=src --cov-report=term-missing

# Apenas testes unitários
pytest tests/test_user_model.py tests/test_task_model.py -v

# Apenas testes de integração
pytest tests/test_auth_routes.py tests/test_task_routes.py -v
```

---

## 🔌 Endpoints da API

### Autenticação
| Método | Rota | Descrição |
|---|---|---|
| POST | `/auth/login` | Autenticar usuário |
| POST | `/auth/logout` | Encerrar sessão |

### Tarefas
| Método | Rota | Descrição |
|---|---|---|
| GET | `/tasks` | Listar todas as tarefas |
| POST | `/tasks` | Criar nova tarefa |
| GET | `/tasks/<id>` | Buscar tarefa por ID |
| PUT | `/tasks/<id>` | Atualizar tarefa |
| DELETE | `/tasks/<id>` | Excluir tarefa |
| PATCH | `/tasks/<id>/status` | Mudar status da tarefa |
| GET | `/tasks/priority/<nivel>` | Filtrar por prioridade *(adicionado na mudança de escopo)* |

---

## ⚙️ Pipeline CI — GitHub Actions

O pipeline é executado automaticamente a cada `push` ou `pull_request` para as branches `main` e `develop`:

1. ✅ Checkout do código
2. ✅ Setup Python 3.11
3. ✅ Instalação de dependências
4. ✅ Execução dos testes com Pytest + cobertura
5. ✅ Validação de qualidade com flake8

---

## 📊 Metodologia

Este projeto segue uma abordagem **híbrida Scrum + Kanban**:
- Sprints semanais com planejamento e revisão
- Quadro Kanban no GitHub Projects com colunas: **A Fazer | Em Progresso | Concluído**
- Commits semânticos seguindo o padrão [Conventional Commits](https://www.conventionalcommits.org/)
- Mínimo de 10 commits distribuídos ao longo do desenvolvimento

---

## 📄 Licença

Projeto acadêmico — UniFECAF · Engenharia de Software · 2025
