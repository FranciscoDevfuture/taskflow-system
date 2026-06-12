"""
Testes Unitários — Modelo de Usuário
Valida criação, autenticação e regras de negócio do modelo Usuario.
"""

import pytest
from src.models.user import Usuario, Admin, Papel


class TestCriacaoDeUsuario:
    """Testa a criação de usuários com dados válidos e inválidos."""

    def test_criar_usuario_valido(self):
        """Deve criar usuário com todos os campos válidos."""
        usuario = Usuario(nome="João Silva", email="joao@email.com", senha="senha123")
        assert usuario.nome == "João Silva"
        assert usuario.email == "joao@email.com"
        assert usuario.papel == Papel.USUARIO
        assert usuario.ativo is True

    def test_senha_nao_armazenada_em_texto_puro(self):
        """A senha nunca deve ser armazenada em texto puro."""
        usuario = Usuario(nome="Ana", email="ana@email.com", senha="minha_senha")
        assert usuario.senha_hash != "minha_senha"
        assert len(usuario.senha_hash) > 20  # hash é longo

    def test_email_normalizado_para_minusculo(self):
        """Email deve ser convertido para minúsculas."""
        usuario = Usuario(nome="Maria", email="MARIA@EMAIL.COM", senha="senha123")
        assert usuario.email == "maria@email.com"

    def test_nome_vazio_lanca_excecao(self):
        """Nome vazio deve lançar ValueError."""
        with pytest.raises(ValueError, match="Nome é obrigatório"):
            Usuario(nome="", email="a@b.com", senha="senha123")

    def test_nome_muito_curto_lanca_excecao(self):
        """Nome com menos de 2 caracteres deve lançar ValueError."""
        with pytest.raises(ValueError, match="2 caracteres"):
            Usuario(nome="A", email="a@b.com", senha="senha123")

    def test_email_invalido_lanca_excecao(self):
        """Email sem @ deve lançar ValueError."""
        with pytest.raises(ValueError, match="Email inválido"):
            Usuario(nome="Teste", email="emailsemarroba.com", senha="senha123")

    def test_email_vazio_lanca_excecao(self):
        """Email vazio deve lançar ValueError."""
        with pytest.raises(ValueError, match="Email é obrigatório"):
            Usuario(nome="Teste", email="", senha="senha123")

    def test_senha_curta_lanca_excecao(self):
        """Senha com menos de 6 caracteres deve lançar ValueError."""
        with pytest.raises(ValueError, match="6 caracteres"):
            Usuario(nome="Teste", email="a@b.com", senha="12345")

    def test_senha_vazia_lanca_excecao(self):
        """Senha vazia deve lançar ValueError."""
        with pytest.raises(ValueError, match="Senha é obrigatória"):
            Usuario(nome="Teste", email="a@b.com", senha="")


class TestAutenticacao:
    """Testa verificação de senha e autenticação."""

    def test_verificar_senha_correta(self):
        """Deve retornar True para a senha correta."""
        usuario = Usuario(nome="Carlos", email="carlos@email.com", senha="senha_certa")
        assert usuario.verificar_senha("senha_certa") is True

    def test_verificar_senha_incorreta(self):
        """Deve retornar False para senha incorreta."""
        usuario = Usuario(nome="Carlos", email="carlos@email.com", senha="senha_certa")
        assert usuario.verificar_senha("senha_errada") is False

    def test_alterar_senha_com_sucesso(self):
        """Deve alterar senha quando a senha atual está correta."""
        usuario = Usuario(nome="Pedro", email="pedro@email.com", senha="senha_velha")
        resultado = usuario.alterar_senha("senha_velha", "senha_nova123")
        assert resultado is True
        assert usuario.verificar_senha("senha_nova123") is True
        assert usuario.verificar_senha("senha_velha") is False

    def test_alterar_senha_incorreta_retorna_false(self):
        """Deve retornar False se a senha atual estiver errada."""
        usuario = Usuario(nome="Pedro", email="pedro@email.com", senha="senha_real")
        resultado = usuario.alterar_senha("senha_errada", "nova_senha123")
        assert resultado is False


class TestRepositorio:
    """Testa operações de persistência em memória."""

    def test_salvar_e_buscar_por_id(self):
        """Deve salvar e recuperar usuário pelo ID."""
        usuario = Usuario(nome="Lucas", email="lucas@email.com", senha="senha123").salvar()
        encontrado = Usuario.buscar_por_id(usuario.id)
        assert encontrado is not None
        assert encontrado.email == "lucas@email.com"

    def test_buscar_por_email(self):
        """Deve encontrar usuário pelo email."""
        Usuario(nome="Fernanda", email="fernanda@email.com", senha="senha123").salvar()
        encontrado = Usuario.buscar_por_email("fernanda@email.com")
        assert encontrado is not None
        assert encontrado.nome == "Fernanda"

    def test_buscar_email_inexistente_retorna_none(self):
        """Deve retornar None para email não cadastrado."""
        resultado = Usuario.buscar_por_email("naoexiste@email.com")
        assert resultado is None

    def test_email_duplicado_lanca_excecao(self):
        """Dois usuários com o mesmo email não são permitidos."""
        Usuario(nome="User 1", email="igual@email.com", senha="senha123").salvar()
        with pytest.raises(ValueError, match="já está em uso"):
            Usuario(nome="User 2", email="igual@email.com", senha="senha456").salvar()

    def test_to_dict_nao_expoe_senha(self):
        """O método to_dict não deve expor a senha ou o hash."""
        usuario = Usuario(nome="Seguro", email="seguro@email.com", senha="secreta").salvar()
        dicionario = usuario.to_dict()
        assert "senha" not in dicionario
        assert "senha_hash" not in dicionario
        assert "id" in dicionario
        assert "email" in dicionario


class TestAdmin:
    """Testa funcionalidades específicas do Admin."""

    def test_criar_admin_com_papel_correto(self):
        """Admin deve ter papel ADMIN automaticamente."""
        admin = Admin(nome="Admin", email="admin@email.com", senha="admin123")
        assert admin.papel == Papel.ADMIN

    def test_admin_pode_desativar_usuario(self):
        """Admin deve conseguir desativar outro usuário."""
        admin = Admin(nome="Admin", email="admin@email.com", senha="admin123").salvar()
        usuario = Usuario(nome="Alvo", email="alvo@email.com", senha="senha123").salvar()
        resultado = admin.desativar_usuario(usuario.id)
        assert resultado is True
        assert usuario.ativo is False

    def test_admin_nao_pode_se_desativar(self):
        """Admin não deve conseguir desativar a si mesmo."""
        admin = Admin(nome="Admin", email="admin@email.com", senha="admin123").salvar()
        resultado = admin.desativar_usuario(admin.id)
        assert resultado is False
        assert admin.ativo is True
