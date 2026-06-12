"""
Utilitários de validação — TaskFlow System
Funções reutilizáveis para validação de entrada nas rotas da API.
"""

from src.models.task import Prioridade, Status


def validar_campos_obrigatorios(dados: dict, campos: list) -> list:
    """
    Verifica se todos os campos obrigatórios estão presentes e não vazios.

    Args:
        dados: Dicionário com os dados recebidos.
        campos: Lista de nomes de campos obrigatórios.

    Returns:
        Lista de campos ausentes ou vazios (vazia se tudo OK).
    """
    ausentes = []
    for campo in campos:
        valor = dados.get(campo)
        if valor is None or (isinstance(valor, str) and not valor.strip()):
            ausentes.append(campo)
    return ausentes


def validar_prioridade(valor: str) -> Prioridade | None:
    """
    Converte string para enum Prioridade.

    Returns:
        Enum Prioridade se válido, None se inválido.
    """
    try:
        return Prioridade(valor.lower())
    except (ValueError, AttributeError):
        return None


def validar_status(valor: str) -> Status | None:
    """
    Converte string para enum Status.

    Returns:
        Enum Status se válido, None se inválido.
    """
    try:
        return Status(valor.lower())
    except (ValueError, AttributeError):
        return None


def resposta_erro(mensagem: str, codigo: int) -> tuple:
    """Cria uma tupla de resposta de erro padronizada."""
    return {"erro": mensagem}, codigo


def resposta_sucesso(dados: dict | list, codigo: int = 200) -> tuple:
    """Cria uma tupla de resposta de sucesso padronizada."""
    return dados, codigo
