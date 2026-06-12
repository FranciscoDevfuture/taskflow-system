
#teste2

"""
Testes de Integração — Rotas de Autenticação
Testa os endpoints /auth/login, /auth/logout e /auth/me via cliente HTTP.
"""

import pytest
from src.models.user import Usuario


class TestLogin:
    """Testa o endpoint POST /auth/login."""

    def test_login_bem_sucedido(self, client, usuario_padrao):
        """Login com credenciais válidas deve retornar 200."""
        resp = client.post("/auth/login", json={
            "email": "fulano@taskflow.com",
            "senha": "senha123",
        })
        assert resp.status_code == 200
        dados = resp.get_json()
        assert "usuario" in dados
        assert dados["usuario"]["email"] == "fulano@taskflow.com"

    def test_login_retorna_dados_sem_senha(self, client, usuario_padrao):
        """A resposta de login não deve conter campos de senha."""
        resp = client.post("/auth/login", json={
            "email": "fulano@taskflow.com",
            "senha": "senha123",
        })
        dados = resp.get_json()
        assert "senha" not in dados["usuario"]
        assert "senha_hash" not in dados["usuario"]

    def test_login_senha_incorreta_retorna_401(self, client, usuario_padrao):
        """Login com senha errada deve retornar 401."""
        resp = client.post("/auth/login", json={
            "email": "fulano@taskflow.com",
            "senha": "senha_errada",
        })
        assert resp.status_code == 401
        assert "erro" in resp.get_json()

    def test_login_email_inexistente_retorna_401(self, client):
        """Login com email não cadastrado deve retornar 401."""
        resp = client.post("/auth/login", json={
            "email": "naoexiste@taskflow.com",
            "senha": "qualquer",
        })
        assert resp.status_code == 401

    def test_login_sem_email_retorna_400(self, client):
        """Requisição sem campo email deve retornar 400."""
        resp = client.post("/auth/login", json={"senha": "senha123"})
        assert resp.status_code in (400, 415)
        assert "email" in resp.get_json()["erro"]

    def test_login_sem_senha_retorna_400(self, client):
        """Requisição sem campo senha deve retornar 400."""
        resp = client.post("/auth/login", json={"email": "a@b.com"})
        assert resp.status_code in (400, 415)

    def test_login_sem_body_retorna_4xx(self, client):
        """Requisição sem body deve retornar 400."""
        resp = client.post("/auth/login")
        assert resp.status_code in (400, 415)

    def test_login_usuario_inativo_retorna_401(self, client, usuario_padrao):
        """Usuário desativado não deve conseguir fazer login."""
        usuario_padrao.ativo = False
        resp = client.post("/auth/login", json={
            "email": "fulano@taskflow.com",
            "senha": "senha123",
        })
        assert resp.status_code == 401


class TestLogout:
    """Testa o endpoint POST /auth/logout."""

    def test_logout_com_sessao_ativa_retorna_200(self, sessao_autenticada):
        """Logout com sessão ativa deve retornar 200."""
        resp = sessao_autenticada.post("/auth/logout")
        assert resp.status_code == 200
        assert "mensagem" in resp.get_json()

    def test_logout_sem_sessao_retorna_401(self, client):
        """Logout sem sessão ativa deve retornar 401."""
        resp = client.post("/auth/logout")
        assert resp.status_code == 401

    def test_apos_logout_sessao_invalida(self, sessao_autenticada):
        """Após logout, requisições autenticadas devem retornar 401."""
        sessao_autenticada.post("/auth/logout")
        resp = sessao_autenticada.get("/auth/me")
        assert resp.status_code == 401


class TestMe:
    """Testa o endpoint GET /auth/me."""

    def test_me_autenticado_retorna_dados(self, sessao_autenticada):
        """Usuário autenticado deve receber seus dados."""
        resp = sessao_autenticada.get("/auth/me")
        assert resp.status_code == 200
        dados = resp.get_json()
        assert dados["email"] == "fulano@taskflow.com"

    def test_me_nao_autenticado_retorna_401(self, client):
        """Sem sessão, /auth/me deve retornar 401."""
        resp = client.get("/auth/me")
        assert resp.status_code == 401
