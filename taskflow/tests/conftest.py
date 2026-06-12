"""
Fixtures compartilhadas para os testes — TaskFlow System
Configura o cliente de teste e reseta o estado entre cada teste.
"""

import pytest
from src.app import criar_app
from src.models.user import Usuario
from src.models.task import Tarefa


@pytest.fixture
def app():
    """Cria instância da aplicação configurada para testes."""
    app = criar_app({
        "TESTING": True,
        "SECRET_KEY": "test-secret-key",
    })
    yield app


@pytest.fixture
def client(app):
    """Retorna o cliente de teste Flask."""
    return app.test_client()


@pytest.fixture(autouse=True)
def limpar_repositorios():
    """
    Limpa os repositórios em memória antes de cada teste.
    Garante isolamento total entre os testes.
    """
    Usuario.limpar_repositorio()
    Tarefa.limpar_repositorio()
    yield
    Usuario.limpar_repositorio()
    Tarefa.limpar_repositorio()


@pytest.fixture
def usuario_padrao():
    """Cria e retorna um usuário padrão para os testes."""
    return Usuario(
        nome="Fulano de Tal",
        email="fulano@taskflow.com",
        senha="senha123",
    ).salvar()


@pytest.fixture
def admin_padrao():
    """Cria e retorna um usuário admin para os testes."""
    from src.models.user import Admin
    return Admin(
        nome="Admin Sistema",
        email="admin@taskflow.com",
        senha="admin123",
    ).salvar()


@pytest.fixture
def sessao_autenticada(client, usuario_padrao):
    """Realiza login e retorna o client com sessão ativa."""
    client.post("/auth/login", json={
        "email": "fulano@taskflow.com",
        "senha": "senha123",
    })
    return client
