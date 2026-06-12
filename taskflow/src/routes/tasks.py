"""
Rotas de Tarefas — TaskFlow System
CRUD completo para gerenciamento de tarefas com controle de status e prioridade.
"""

from flask import Blueprint, request, jsonify, session
from src.models.task import Tarefa, Status, Prioridade
from src.utils.validators import (
    validar_campos_obrigatorios,
    validar_prioridade,
    validar_status,
)

# Blueprint de tarefas
tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")


def _usuario_logado():
    """Retorna o ID do usuário da sessão ou None se não autenticado."""
    return session.get("usuario_id")


def _requer_autenticacao():
    """Retorna resposta de erro 401 se não autenticado."""
    if not _usuario_logado():
        return jsonify({"erro": "Autenticação necessária."}), 401
    return None


# ─── CREATE ──────────────────────────────────────────────────────


@tasks_bp.route("", methods=["POST"])
def criar_tarefa():
    """
    Cria uma nova tarefa.

    Body JSON:
        titulo (str): Título da tarefa (obrigatório).
        descricao (str): Detalhamento (opcional).
        prioridade (str): baixa | media | alta | critica (padrão: media).

    Returns:
        201: Tarefa criada com sucesso.
        400: Dados inválidos.
        401: Não autenticado.
    """
    erro_auth = _requer_autenticacao()
    if erro_auth:
        return erro_auth

    dados = request.get_json()
    if not dados:
        return jsonify({"erro": "Corpo da requisição inválido."}), 400

    ausentes = validar_campos_obrigatorios(dados, ["titulo"])
    if ausentes:
        return jsonify({"erro": "Campo obrigatorio ausente: titulo"}), 400

    # Valida prioridade se fornecida
    prioridade = Prioridade.MEDIA
    if "prioridade" in dados:
        prioridade = validar_prioridade(dados["prioridade"])
        if prioridade is None:
            valores = [p.value for p in Prioridade]
            return jsonify({"erro": f"Prioridade inválida. Valores aceitos: {valores}"}), 400

    try:
        tarefa = Tarefa(
            titulo=dados["titulo"],
            descricao=dados.get("descricao", ""),
            prioridade=prioridade,
            usuario_id=_usuario_logado(),
        ).salvar()
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400

    return jsonify(tarefa.to_dict()), 201


# ─── READ ────────────────────────────────────────────────────────


@tasks_bp.route("", methods=["GET"])
def listar_tarefas():
    """
    Lista todas as tarefas, com filtro opcional por status.

    Query params:
        status (str): Filtrar por status (a_fazer | em_progresso | concluido).

    Returns:
        200: Lista de tarefas.
        400: Status inválido.
        401: Não autenticado.
    """
    erro_auth = _requer_autenticacao()
    if erro_auth:
        return erro_auth

    status_param = request.args.get("status")

    if status_param:
        status = validar_status(status_param)
        if status is None:
            valores = [s.value for s in Status]
            return jsonify({"erro": f"Status inválido. Valores aceitos: {valores}"}), 400
        tarefas = Tarefa.listar_por_status(status)
    else:
        tarefas = Tarefa.listar_todas()

    return jsonify([t.to_dict() for t in tarefas]), 200


@tasks_bp.route("/<int:tarefa_id>", methods=["GET"])
def buscar_tarefa(tarefa_id):
    """
    Busca uma tarefa pelo ID.

    Returns:
        200: Tarefa encontrada.
        401: Não autenticado.
        404: Tarefa não encontrada.
    """
    erro_auth = _requer_autenticacao()
    if erro_auth:
        return erro_auth

    tarefa = Tarefa.buscar_por_id(tarefa_id)
    if not tarefa:
        return jsonify({"erro": f"Tarefa {tarefa_id} não encontrada."}), 404

    return jsonify(tarefa.to_dict()), 200


# ─── UPDATE ──────────────────────────────────────────────────────


@tasks_bp.route("/<int:tarefa_id>", methods=["PUT"])
def atualizar_tarefa(tarefa_id):
    """
    Atualiza título, descrição e/ou prioridade de uma tarefa.

    Body JSON (todos opcionais):
        titulo (str): Novo título.
        descricao (str): Nova descrição.
        prioridade (str): Nova prioridade.

    Returns:
        200: Tarefa atualizada.
        400: Dados inválidos.
        401: Não autenticado.
        404: Tarefa não encontrada.
    """
    erro_auth = _requer_autenticacao()
    if erro_auth:
        return erro_auth

    tarefa = Tarefa.buscar_por_id(tarefa_id)
    if not tarefa:
        return jsonify({"erro": f"Tarefa {tarefa_id} não encontrada."}), 404

    dados = request.get_json() or {}

    # Valida prioridade se fornecida
    prioridade = None
    if "prioridade" in dados:
        prioridade = validar_prioridade(dados["prioridade"])
        if prioridade is None:
            valores = [p.value for p in Prioridade]
            return jsonify({"erro": f"Prioridade inválida. Valores aceitos: {valores}"}), 400

    try:
        tarefa.atualizar(
            titulo=dados.get("titulo"),
            descricao=dados.get("descricao"),
            prioridade=prioridade,
        )
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400

    return jsonify(tarefa.to_dict()), 200


@tasks_bp.route("/<int:tarefa_id>/status", methods=["PATCH"])
def mudar_status(tarefa_id):
    """
    Altera o status de uma tarefa respeitando o fluxo Kanban.

    Body JSON:
        status (str): Novo status (a_fazer | em_progresso | concluido).

    Returns:
        200: Status alterado.
        400: Transição inválida ou status inválido.
        401: Não autenticado.
        404: Tarefa não encontrada.
    """
    erro_auth = _requer_autenticacao()
    if erro_auth:
        return erro_auth

    tarefa = Tarefa.buscar_por_id(tarefa_id)
    if not tarefa:
        return jsonify({"erro": f"Tarefa {tarefa_id} não encontrada."}), 404

    dados = request.get_json() or {}
    if "status" not in dados:
        return jsonify({"erro": "Campo 'status' é obrigatório."}), 400

    novo_status = validar_status(dados["status"])
    if novo_status is None:
        valores = [s.value for s in Status]
        return jsonify({"erro": f"Status inválido. Valores aceitos: {valores}"}), 400

    if not tarefa.mudar_status(novo_status):
        return jsonify({
            "erro": f"Transição inválida: '{tarefa.status.value}' → '{novo_status.value}'."
        }), 400

    return jsonify(tarefa.to_dict()), 200


# ─── DELETE ──────────────────────────────────────────────────────


@tasks_bp.route("/<int:tarefa_id>", methods=["DELETE"])
def excluir_tarefa(tarefa_id):
    """
    Remove uma tarefa permanentemente.

    Returns:
        200: Tarefa excluída.
        401: Não autenticado.
        404: Tarefa não encontrada.
    """
    erro_auth = _requer_autenticacao()
    if erro_auth:
        return erro_auth

    if not Tarefa.excluir(tarefa_id):
        return jsonify({"erro": f"Tarefa {tarefa_id} não encontrada."}), 404

    return jsonify({"mensagem": f"Tarefa {tarefa_id} excluída com sucesso."}), 200


# ─── FILTRO POR PRIORIDADE (adicionado na mudança de escopo) ──────


@tasks_bp.route("/priority/<string:nivel>", methods=["GET"])
def listar_por_prioridade(nivel):
    """
    Lista tarefas filtradas por nível de prioridade.
    Endpoint adicionado na mudança de escopo da Sprint 2.

    Args:
        nivel: baixa | media | alta | critica

    Returns:
        200: Lista de tarefas com a prioridade informada.
        400: Nível de prioridade inválido.
        401: Não autenticado.
    """
    erro_auth = _requer_autenticacao()
    if erro_auth:
        return erro_auth

    prioridade = validar_prioridade(nivel)
    if prioridade is None:
        valores = [p.value for p in Prioridade]
        return jsonify({"erro": f"Prioridade inválida. Valores aceitos: {valores}"}), 400

    tarefas = Tarefa.listar_por_prioridade(prioridade)
    return jsonify([t.to_dict() for t in tarefas]), 200
