"""
Factory da Aplicação Flask — TaskFlow System
Inicializa e configura a aplicação com todas as rotas registradas.
"""

from flask import Flask, jsonify
from src.routes.auth import auth_bp
from src.routes.tasks import tasks_bp


def criar_app(config: dict = None) -> Flask:
    """
    Factory pattern para criação da aplicação Flask.

    Args:
        config: Dicionário de configurações opcionais (usado nos testes).

    Returns:
        Instância configurada do Flask.
    """
    app = Flask(__name__)

    # Configurações padrão
    app.config["SECRET_KEY"] = "taskflow-secret-key-unifecaf-2025"
    app.config["TESTING"] = False

    # Sobrescreve configurações se fornecidas (para testes)
    if config:
        app.config.update(config)

    # Registra os blueprints (rotas)
    app.register_blueprint(auth_bp)
    app.register_blueprint(tasks_bp)

    # Rota raiz — healthcheck
    @app.route("/")
    def index():
        return jsonify({
            "sistema": "TaskFlow System",
            "versao": "1.0.0",
            "status": "online",
            "empresa": "TechFlow Solutions",
            "descricao": "API de gerenciamento de tarefas ágil"
        }), 200

    # Tratamento de erros globais
    @app.errorhandler(404)
    def nao_encontrado(e):
        return jsonify({"erro": "Rota não encontrada."}), 404

    @app.errorhandler(405)
    def metodo_nao_permitido(e):
        return jsonify({"erro": "Método HTTP não permitido para esta rota."}), 405

    @app.errorhandler(500)
    def erro_interno(e):
        return jsonify({"erro": "Erro interno do servidor."}), 500

    return app


if __name__ == "__main__":
    app = criar_app()
    print("=" * 50)
    print("  TaskFlow System — TechFlow Solutions")
    print("  Servidor iniciado em http://localhost:5000")
    print("=" * 50)
    app.run(debug=True, host="0.0.0.0", port=5000)
