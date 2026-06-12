# 📚 Documentação da API — TaskFlow System

Base URL: `http://localhost:5000`

---

## Autenticação

### POST /auth/login
```json
// Body
{ "email": "usuario@email.com", "senha": "senha123" }

// Resposta 200
{ "mensagem": "Login realizado com sucesso.", "usuario": { "id": 1, "nome": "...", "email": "...", "papel": "usuario" } }
```

### POST /auth/logout
```json
// Resposta 200
{ "mensagem": "Logout realizado com sucesso." }
```

---

## Tarefas

### POST /tasks — Criar tarefa
```json
// Body
{ "titulo": "Revisar relatório", "descricao": "...", "prioridade": "alta" }

// Resposta 201
{ "id": 1, "titulo": "...", "status": "a_fazer", "prioridade": "alta", ... }
```

### GET /tasks — Listar tarefas
- Query param opcional: `?status=a_fazer|em_progresso|concluido`

### GET /tasks/<id> — Buscar por ID

### PUT /tasks/<id> — Atualizar tarefa
```json
{ "titulo": "Novo título", "prioridade": "critica" }
```

### PATCH /tasks/<id>/status — Mudar status
```json
{ "status": "em_progresso" }
```
Transições válidas: `a_fazer → em_progresso → concluido`

### DELETE /tasks/<id> — Excluir tarefa

### GET /tasks/priority/<nivel> — Filtrar por prioridade
- Valores: `baixa | media | alta | critica`
