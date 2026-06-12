"""
Rotas de Autenticação — TaskFlow System
Gerencia login e logout dos usuários via sessão Flask.
"""

from flask import Blueprint, request, jsonify, session
from src.models.user import Usuario
from src.utils.validators import validar_campos_obrigatorios

# Blueprint de autenticação
auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/login", methods=["POST"])
def login():
    """
    Autentica o usuário com email e senha.

    Body JSON:
        email (str): Email do usuário.
        senha (str): Senha em texto puro.

    Returns:
        200: Login bem-sucedido com dados do usuário.
        400: Campos obrigatórios ausentes.
        401: Credenciais inválidas.
    """
    dados = request.get_json()

    if not dados:
        return jsonify({"erro": "Corpo da requisição inválido ou ausente."}), 400

    # Valida campos obrigatórios
    ausentes = validar_campos_obrigatorios(dados, ["email", "senha"])
    if ausentes:
        return jsonify({
            "erro": f"Campos obrigatórios ausentes: {', '.join(ausentes)}"
        }), 400

    # Busca o usuário pelo email
    usuario = Usuario.buscar_por_email(dados["email"])

    # Verifica credenciais
    if not usuario or not usuario.verificar_senha(dados["senha"]):
        return jsonify({"erro": "Email ou senha inválidos."}), 401

    if not usuario.ativo:
        return jsonify({"erro": "Conta desativada. Contate o administrador."}), 401

    # Registra sessão
    session["usuario_id"] = usuario.id
    session["papel"] = usuario.papel.value

    return jsonify({
        "mensagem": "Login realizado com sucesso.",
        "usuario": usuario.to_dict()
    }), 200


@auth_bp.route("/logout", methods=["POST"])
def logout():
    """
    Encerra a sessão do usuário autenticado.

    Returns:
        200: Logout bem-sucedido.
        401: Nenhuma sessão ativa.
    """
    if "usuario_id" not in session:
        return jsonify({"erro": "Nenhuma sessão ativa."}), 401

    session.clear()
    return jsonify({"mensagem": "Logout realizado com sucesso."}), 200


@auth_bp.route("/me", methods=["GET"])
def me():
    """
    Retorna os dados do usuário autenticado na sessão.

    Returns:
        200: Dados do usuário logado.
        401: Não autenticado.
    """
    usuario_id = session.get("usuario_id")
    if not usuario_id:
        return jsonify({"erro": "Não autenticado."}), 401

    usuario = Usuario.buscar_por_id(usuario_id)
    if not usuario:
        session.clear()
        return jsonify({"erro": "Usuário não encontrado."}), 401

    return jsonify(usuario.to_dict()), 200
