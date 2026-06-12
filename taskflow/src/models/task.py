"""
Modelo de Tarefa - TaskFlow System
Gerencia o ciclo de vida das tarefas, status e prioridades.
"""

from enum import Enum
from datetime import datetime, timezone


class Status(Enum):
    """Ciclo de vida de uma tarefa no sistema Kanban."""
    A_FAZER = "a_fazer"
    EM_PROGRESSO = "em_progresso"
    CONCLUIDO = "concluido"


class Prioridade(Enum):
    """
    Nivel de urgencia de uma tarefa.
    Adicionado na mudanca de escopo (Sprint 2) a pedido do cliente.
    """
    BAIXA = "baixa"
    MEDIA = "media"
    ALTA = "alta"
    CRITICA = "critica"


# Transicoes de status permitidas (fluxo Kanban)
TRANSICOES_VALIDAS = {
    Status.A_FAZER: [Status.EM_PROGRESSO],
    Status.EM_PROGRESSO: [Status.CONCLUIDO, Status.A_FAZER],
    Status.CONCLUIDO: [],
}


class Tarefa:
    """
    Representa uma tarefa no sistema TaskFlow.

    Atributos:
        id (int): Identificador unico da tarefa.
        titulo (str): Titulo curto e descritivo da tarefa.
        descricao (str): Detalhamento da tarefa (opcional).
        status (Status): Estado atual no fluxo Kanban.
        prioridade (Prioridade): Nivel de urgencia da tarefa.
        usuario_id (int): ID do usuario responsavel.
        criado_em (datetime): Timestamp de criacao.
        atualizado_em (datetime): Timestamp da ultima atualizacao.
    """

    _repositorio: dict = {}
    _proximo_id: int = 1

    def __init__(
        self,
        titulo: str,
        usuario_id: int,
        descricao: str = "",
        prioridade: Prioridade = Prioridade.MEDIA,
    ):
        self._validar_titulo(titulo)
        self._validar_usuario_id(usuario_id)
        self._validar_prioridade(prioridade)

        self.id = None
        self.titulo = titulo.strip()
        self.descricao = descricao.strip() if descricao else ""
        self.status = Status.A_FAZER
        self.prioridade = prioridade
        self.usuario_id = usuario_id
        self.criado_em = datetime.now(timezone.utc)
        self.atualizado_em = datetime.now(timezone.utc)

    @staticmethod
    def _validar_titulo(titulo: str):
        if not titulo or not titulo.strip():
            raise ValueError("Titulo da tarefa e obrigatorio.")
        if len(titulo.strip()) < 3:
            raise ValueError("Titulo deve ter ao menos 3 caracteres.")
        if len(titulo.strip()) > 100:
            raise ValueError("Titulo nao pode ultrapassar 100 caracteres.")

    @staticmethod
    def _validar_usuario_id(usuario_id):
        if not isinstance(usuario_id, int) or usuario_id <= 0:
            raise ValueError("usuario_id deve ser um inteiro positivo.")

    @staticmethod
    def _validar_prioridade(prioridade):
        if not isinstance(prioridade, Prioridade):
            valores = [p.value for p in Prioridade]
            raise ValueError(f"Prioridade invalida. Valores aceitos: {valores}")

    def mudar_status(self, novo_status: Status) -> bool:
        """Altera o status respeitando o fluxo Kanban."""
        if novo_status not in TRANSICOES_VALIDAS.get(self.status, []):
            return False
        self.status = novo_status
        self.atualizado_em = datetime.now(timezone.utc)
        return True

    def atualizar(self, titulo: str = None, descricao: str = None,
                  prioridade: Prioridade = None):
        """Atualiza os campos editaveis da tarefa."""
        if titulo is not None:
            self._validar_titulo(titulo)
            self.titulo = titulo.strip()
        if descricao is not None:
            self.descricao = descricao.strip()
        if prioridade is not None:
            self._validar_prioridade(prioridade)
            self.prioridade = prioridade
        self.atualizado_em = datetime.now(timezone.utc)

    def salvar(self):
        """Salva a tarefa no repositorio e retorna self."""
        if self.id is None:
            self.id = Tarefa._proximo_id
            Tarefa._proximo_id += 1
        Tarefa._repositorio[self.id] = self
        return self

    @classmethod
    def buscar_por_id(cls, tarefa_id: int):
        """Busca tarefa pelo ID."""
        return cls._repositorio.get(tarefa_id)

    @classmethod
    def listar_todas(cls) -> list:
        """Retorna todas as tarefas ordenadas por prioridade."""
        ordem = [Prioridade.CRITICA, Prioridade.ALTA, Prioridade.MEDIA, Prioridade.BAIXA]
        return sorted(
            cls._repositorio.values(),
            key=lambda t: ordem.index(t.prioridade)
        )

    @classmethod
    def listar_por_status(cls, status: Status) -> list:
        """Retorna tarefas filtradas por status."""
        return [t for t in cls._repositorio.values() if t.status == status]

    @classmethod
    def listar_por_prioridade(cls, prioridade: Prioridade) -> list:
        """Retorna tarefas filtradas por prioridade."""
        return [t for t in cls._repositorio.values() if t.prioridade == prioridade]

    @classmethod
    def listar_por_usuario(cls, usuario_id: int) -> list:
        """Retorna tarefas de um usuario especifico."""
        return [t for t in cls._repositorio.values() if t.usuario_id == usuario_id]

    @classmethod
    def excluir(cls, tarefa_id: int) -> bool:
        """Remove a tarefa do repositorio."""
        if tarefa_id in cls._repositorio:
            del cls._repositorio[tarefa_id]
            return True
        return False

    @classmethod
    def limpar_repositorio(cls):
        """Limpa todos os dados (usado nos testes)."""
        cls._repositorio.clear()
        cls._proximo_id = 1

    def to_dict(self) -> dict:
        """Converte a tarefa para dicionario serializavel em JSON."""
        return {
            "id": self.id,
            "titulo": self.titulo,
            "descricao": self.descricao,
            "status": self.status.value,
            "prioridade": self.prioridade.value,
            "usuario_id": self.usuario_id,
            "criado_em": self.criado_em.isoformat(),
            "atualizado_em": self.atualizado_em.isoformat(),
        }

    def __repr__(self):
        return (
            f"<Tarefa id={self.id} titulo='{self.titulo}' "
            f"status={self.status.value} prioridade={self.prioridade.value}>"
        )
