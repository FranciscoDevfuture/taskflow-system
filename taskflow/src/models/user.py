"""
Modelo de Usuário — TaskFlow System
Gerencia autenticação, perfis e permissões dos usuários.
"""

from enum import Enum
from werkzeug.security import generate_password_hash, check_password_hash


class Papel(Enum):
    """Define o nível de acesso do usuário no sistema."""
    USUARIO = "usuario"
    ADMIN = "admin"


class Usuario:
    """
    Representa um usuário do sistema TaskFlow.

    Atributos:
        id (int): Identificador único do usuário.
        nome (str): Nome completo do usuário.
        email (str): Email único utilizado para login.
        senha_hash (str): Hash seguro da senha (nunca texto puro).
        papel (Papel): Nível de acesso (USUARIO ou ADMIN).
    """

    # Armazenamento em memória (simula banco de dados)
    _repositorio: dict = {}
    _proximo_id: int = 1

    def __init__(self, nome: str, email: str, senha: str, papel: Papel = Papel.USUARIO):
        """
        Cria um novo usuário com senha criptografada.

        Args:
            nome: Nome completo do usuário.
            email: Endereço de email (deve ser único).
            senha: Senha em texto puro (será convertida para hash).
            papel: Perfil de acesso (padrão: USUARIO).

        Raises:
            ValueError: Se nome, email ou senha forem inválidos.
        """
        self._validar_nome(nome)
        self._validar_email(email)
        self._validar_senha(senha)

        self.id = None  # Definido ao salvar
        self.nome = nome.strip()
        self.email = email.strip().lower()
        self.senha_hash = generate_password_hash(senha)
        self.papel = papel
        self.ativo = True

    # ─── Validações ───────────────────────────────────────────

    @staticmethod
    def _validar_nome(nome: str):
        if not nome or not nome.strip():
            raise ValueError("Nome é obrigatório.")
        if len(nome.strip()) < 2:
            raise ValueError("Nome deve ter ao menos 2 caracteres.")

    @staticmethod
    def _validar_email(email: str):
        if not email or not email.strip():
            raise ValueError("Email é obrigatório.")
        if "@" not in email or "." not in email:
            raise ValueError("Email inválido.")

    @staticmethod
    def _validar_senha(senha: str):
        if not senha:
            raise ValueError("Senha é obrigatória.")
        if len(senha) < 6:
            raise ValueError("Senha deve ter ao menos 6 caracteres.")

    # ─── Autenticação ─────────────────────────────────────────

    def verificar_senha(self, senha: str) -> bool:
        """Verifica se a senha fornecida corresponde ao hash armazenado."""
        return check_password_hash(self.senha_hash, senha)

    def alterar_senha(self, senha_atual: str, nova_senha: str) -> bool:
        """
        Altera a senha do usuário após verificar a senha atual.

        Returns:
            True se a senha foi alterada, False se a senha atual estiver errada.
        """
        if not self.verificar_senha(senha_atual):
            return False
        self._validar_senha(nova_senha)
        self.senha_hash = generate_password_hash(nova_senha)
        return True

    # ─── Persistência (repositório em memória) ───────────────

    def salvar(self) -> "Usuario":
        """Salva o usuário no repositório e retorna self."""
        # Verifica email duplicado
        for u in Usuario._repositorio.values():
            if u.email == self.email and u.id != self.id:
                raise ValueError(f"Email '{self.email}' já está em uso.")

        if self.id is None:
            self.id = Usuario._proximo_id
            Usuario._proximo_id += 1

        Usuario._repositorio[self.id] = self
        return self

    @classmethod
    def buscar_por_id(cls, usuario_id: int) -> "Usuario | None":
        """Busca usuário pelo ID."""
        return cls._repositorio.get(usuario_id)

    @classmethod
    def buscar_por_email(cls, email: str) -> "Usuario | None":
        """Busca usuário pelo email (case-insensitive)."""
        email = email.strip().lower()
        for u in cls._repositorio.values():
            if u.email == email:
                return u
        return None

    @classmethod
    def listar_todos(cls) -> list:
        """Retorna lista de todos os usuários ativos."""
        return [u for u in cls._repositorio.values() if u.ativo]

    @classmethod
    def limpar_repositorio(cls):
        """Limpa todos os dados (usado nos testes)."""
        cls._repositorio.clear()
        cls._proximo_id = 1

    # ─── Serialização ────────────────────────────────────────

    def to_dict(self) -> dict:
        """Converte o usuário para dicionário (sem a senha)."""
        return {
            "id": self.id,
            "nome": self.nome,
            "email": self.email,
            "papel": self.papel.value,
            "ativo": self.ativo,
        }

    def __repr__(self):
        return f"<Usuario id={self.id} email={self.email} papel={self.papel.value}>"


class Admin(Usuario):
    """
    Especialização de Usuario com permissões administrativas.
    Criado automaticamente com papel=Papel.ADMIN.
    """

    def __init__(self, nome: str, email: str, senha: str):
        super().__init__(nome, email, senha, papel=Papel.ADMIN)

    def listar_usuarios(self) -> list:
        """Lista todos os usuários do sistema."""
        return Usuario.listar_todos()

    def desativar_usuario(self, usuario_id: int) -> bool:
        """
        Desativa a conta de um usuário.

        Returns:
            True se desativado com sucesso, False se não encontrado.
        """
        usuario = Usuario.buscar_por_id(usuario_id)
        if usuario and usuario.id != self.id:
            usuario.ativo = False
            return True
        return False
