"""
Testes de Integração — Rotas de Tarefas
Testa os endpoints CRUD de tarefas e filtros por status/prioridade.
"""

import pytest
from src.models.task import Tarefa, Status, Prioridade


class TestCriarTarefa:
    """Testa POST /tasks."""

    def test_criar_tarefa_valida(self, sessao_autenticada):
        """Deve criar tarefa e retornar 201."""
        resp = sessao_autenticada.post("/tasks", json={"titulo": "Nova tarefa"})
        assert resp.status_code == 201
        dados = resp.get_json()
        assert dados["titulo"] == "Nova tarefa"
        assert dados["status"] == "a_fazer"
        assert dados["prioridade"] == "media"

    def test_criar_tarefa_com_prioridade(self, sessao_autenticada):
        """Deve criar tarefa com prioridade especificada."""
        resp = sessao_autenticada.post("/tasks", json={
            "titulo": "Urgente!",
            "prioridade": "critica",
        })
        assert resp.status_code == 201
        assert resp.get_json()["prioridade"] == "critica"

    def test_criar_tarefa_com_descricao(self, sessao_autenticada):
        """Deve criar tarefa com descrição."""
        resp = sessao_autenticada.post("/tasks", json={
            "titulo": "Tarefa detalhada",
            "descricao": "Descrição aqui",
        })
        assert resp.status_code == 201
        assert resp.get_json()["descricao"] == "Descrição aqui"

    def test_criar_sem_titulo_retorna_400(self, sessao_autenticada):
        """Deve retornar 400 se título ausente."""
        resp = sessao_autenticada.post("/tasks", json={"descricao": "Sem título"})
        assert resp.status_code == 400

    def test_criar_prioridade_invalida_retorna_400(self, sessao_autenticada):
        """Deve retornar 400 para prioridade inválida."""
        resp = sessao_autenticada.post("/tasks", json={
            "titulo": "Teste",
            "prioridade": "URGENTISSIMA",
        })
        assert resp.status_code == 400

    def test_criar_sem_autenticacao_retorna_401(self, client):
        """Deve retornar 401 sem sessão ativa."""
        resp = client.post("/tasks", json={"titulo": "Tarefa"})
        assert resp.status_code == 401


class TestListarTarefas:
    """Testa GET /tasks."""

    def test_listar_todas_as_tarefas(self, sessao_autenticada, usuario_padrao):
        """Deve retornar lista com todas as tarefas."""
        Tarefa(titulo="Tarefa 1", usuario_id=usuario_padrao.id).salvar()
        Tarefa(titulo="Tarefa 2", usuario_id=usuario_padrao.id).salvar()
        resp = sessao_autenticada.get("/tasks")
        assert resp.status_code == 200
        assert len(resp.get_json()) == 2

    def test_listar_por_status(self, sessao_autenticada, usuario_padrao):
        """Deve filtrar tarefas por status."""
        t = Tarefa(titulo="Em progresso", usuario_id=usuario_padrao.id).salvar()
        t.mudar_status(Status.EM_PROGRESSO)
        Tarefa(titulo="A fazer", usuario_id=usuario_padrao.id).salvar()

        resp = sessao_autenticada.get("/tasks?status=em_progresso")
        assert resp.status_code == 200
        resultados = resp.get_json()
        assert len(resultados) == 1
        assert resultados[0]["status"] == "em_progresso"

    def test_listar_status_invalido_retorna_400(self, sessao_autenticada):
        """Status inválido deve retornar 400."""
        resp = sessao_autenticada.get("/tasks?status=invalido")
        assert resp.status_code == 400

    def test_listar_sem_autenticacao_retorna_401(self, client):
        """Deve retornar 401 sem sessão."""
        resp = client.get("/tasks")
        assert resp.status_code == 401


class TestBuscarTarefa:
    """Testa GET /tasks/<id>."""

    def test_buscar_tarefa_existente(self, sessao_autenticada, usuario_padrao):
        """Deve retornar a tarefa pelo ID."""
        tarefa = Tarefa(titulo="Buscar", usuario_id=usuario_padrao.id).salvar()
        resp = sessao_autenticada.get(f"/tasks/{tarefa.id}")
        assert resp.status_code == 200
        assert resp.get_json()["titulo"] == "Buscar"

    def test_buscar_tarefa_inexistente_retorna_404(self, sessao_autenticada):
        """ID não existente deve retornar 404."""
        resp = sessao_autenticada.get("/tasks/9999")
        assert resp.status_code == 404


class TestAtualizarTarefa:
    """Testa PUT /tasks/<id>."""

    def test_atualizar_titulo(self, sessao_autenticada, usuario_padrao):
        """Deve atualizar o título da tarefa."""
        tarefa = Tarefa(titulo="Antigo", usuario_id=usuario_padrao.id).salvar()
        resp = sessao_autenticada.put(f"/tasks/{tarefa.id}", json={"titulo": "Novo"})
        assert resp.status_code == 200
        assert resp.get_json()["titulo"] == "Novo"

    def test_atualizar_prioridade(self, sessao_autenticada, usuario_padrao):
        """Deve atualizar a prioridade da tarefa."""
        tarefa = Tarefa(titulo="Tarefa", usuario_id=usuario_padrao.id).salvar()
        resp = sessao_autenticada.put(f"/tasks/{tarefa.id}", json={"prioridade": "alta"})
        assert resp.status_code == 200
        assert resp.get_json()["prioridade"] == "alta"

    def test_atualizar_inexistente_retorna_404(self, sessao_autenticada):
        """ID inexistente deve retornar 404."""
        resp = sessao_autenticada.put("/tasks/9999", json={"titulo": "X"})
        assert resp.status_code == 404


class TestMudarStatus:
    """Testa PATCH /tasks/<id>/status."""

    def test_mudar_status_valido(self, sessao_autenticada, usuario_padrao):
        """Deve mudar status para EM_PROGRESSO."""
        tarefa = Tarefa(titulo="Tarefa", usuario_id=usuario_padrao.id).salvar()
        resp = sessao_autenticada.patch(
            f"/tasks/{tarefa.id}/status",
            json={"status": "em_progresso"}
        )
        assert resp.status_code == 200
        assert resp.get_json()["status"] == "em_progresso"

    def test_transicao_invalida_retorna_400(self, sessao_autenticada, usuario_padrao):
        """Transição inválida (A_FAZER → CONCLUIDO) deve retornar 400."""
        tarefa = Tarefa(titulo="Tarefa", usuario_id=usuario_padrao.id).salvar()
        resp = sessao_autenticada.patch(
            f"/tasks/{tarefa.id}/status",
            json={"status": "concluido"}
        )
        assert resp.status_code == 400

    def test_status_invalido_retorna_400(self, sessao_autenticada, usuario_padrao):
        """Status inválido deve retornar 400."""
        tarefa = Tarefa(titulo="Tarefa", usuario_id=usuario_padrao.id).salvar()
        resp = sessao_autenticada.patch(
            f"/tasks/{tarefa.id}/status",
            json={"status": "voando"}
        )
        assert resp.status_code == 400


class TestExcluirTarefa:
    """Testa DELETE /tasks/<id>."""

    def test_excluir_tarefa_existente(self, sessao_autenticada, usuario_padrao):
        """Deve excluir a tarefa e retornar 200."""
        tarefa = Tarefa(titulo="Para excluir", usuario_id=usuario_padrao.id).salvar()
        resp = sessao_autenticada.delete(f"/tasks/{tarefa.id}")
        assert resp.status_code == 200
        assert Tarefa.buscar_por_id(tarefa.id) is None

    def test_excluir_inexistente_retorna_404(self, sessao_autenticada):
        """ID inexistente deve retornar 404."""
        resp = sessao_autenticada.delete("/tasks/9999")
        assert resp.status_code == 404


class TestFiltrarPorPrioridade:
    """
    Testa GET /tasks/priority/<nivel>
    Endpoint adicionado na mudança de escopo (Sprint 2).
    """

    def test_filtrar_por_prioridade_critica(self, sessao_autenticada, usuario_padrao):
        """Deve retornar apenas tarefas críticas."""
        Tarefa(titulo="Normal", usuario_id=usuario_padrao.id, prioridade=Prioridade.MEDIA).salvar()
        Tarefa(titulo="Urgente", usuario_id=usuario_padrao.id, prioridade=Prioridade.CRITICA).salvar()

        resp = sessao_autenticada.get("/tasks/priority/critica")
        assert resp.status_code == 200
        resultados = resp.get_json()
        assert len(resultados) == 1
        assert resultados[0]["prioridade"] == "critica"

    def test_filtrar_prioridade_invalida_retorna_400(self, sessao_autenticada):
        """Prioridade inválida deve retornar 400."""
        resp = sessao_autenticada.get("/tasks/priority/superurgente")
        assert resp.status_code == 400

    def test_filtrar_sem_autenticacao_retorna_401(self, client):
        """Deve retornar 401 sem sessão."""
        resp = client.get("/tasks/priority/alta")
        assert resp.status_code == 401
