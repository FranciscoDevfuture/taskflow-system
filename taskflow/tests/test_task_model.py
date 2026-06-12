"""
Testes Unitários — Modelo de Tarefa
Valida criação, transições de status, prioridade e regras de negócio.
"""

import pytest
from src.models.task import Tarefa, Status, Prioridade, TRANSICOES_VALIDAS


class TestCriacaoDeTarefa:
    """Testa a criação de tarefas com dados válidos e inválidos."""

    def test_criar_tarefa_valida(self):
        """Deve criar tarefa com título e usuário válidos."""
        tarefa = Tarefa(titulo="Revisar relatório", usuario_id=1)
        assert tarefa.titulo == "Revisar relatório"
        assert tarefa.status == Status.A_FAZER
        assert tarefa.prioridade == Prioridade.MEDIA  # prioridade padrão

    def test_status_inicial_e_a_fazer(self):
        """Toda tarefa deve iniciar com status A_FAZER."""
        tarefa = Tarefa(titulo="Nova tarefa", usuario_id=1)
        assert tarefa.status == Status.A_FAZER

    def test_prioridade_padrao_e_media(self):
        """A prioridade padrão deve ser MEDIA quando não especificada."""
        tarefa = Tarefa(titulo="Tarefa sem prioridade", usuario_id=1)
        assert tarefa.prioridade == Prioridade.MEDIA

    def test_criar_tarefa_com_prioridade_critica(self):
        """Deve aceitar prioridade CRITICA."""
        tarefa = Tarefa(titulo="Servidor caiu!", usuario_id=1, prioridade=Prioridade.CRITICA)
        assert tarefa.prioridade == Prioridade.CRITICA

    def test_criar_tarefa_com_descricao(self):
        """Deve armazenar a descrição corretamente."""
        tarefa = Tarefa(titulo="Tarefa", usuario_id=1, descricao="Detalhamento aqui")
        assert tarefa.descricao == "Detalhamento aqui"

    def test_titulo_vazio_lanca_excecao(self):
        """Título vazio deve lançar ValueError."""
        with pytest.raises(ValueError, match="obrigatorio"):
            Tarefa(titulo="", usuario_id=1)

    def test_titulo_muito_curto_lanca_excecao(self):
        """Título com menos de 3 caracteres deve lançar ValueError."""
        with pytest.raises(ValueError, match="3 caracteres"):
            Tarefa(titulo="AB", usuario_id=1)

    def test_titulo_muito_longo_lanca_excecao(self):
        """Título com mais de 100 caracteres deve lançar ValueError."""
        with pytest.raises(ValueError, match="100 caracteres"):
            Tarefa(titulo="T" * 101, usuario_id=1)

    def test_usuario_id_invalido_lanca_excecao(self):
        """usuario_id não inteiro deve lançar ValueError."""
        with pytest.raises(ValueError, match="inteiro positivo"):
            Tarefa(titulo="Válida", usuario_id="abc")

    def test_usuario_id_negativo_lanca_excecao(self):
        """usuario_id negativo deve lançar ValueError."""
        with pytest.raises(ValueError, match="inteiro positivo"):
            Tarefa(titulo="Válida", usuario_id=-1)


class TestValidacaoDePrioridade:
    """
    Testa validação do campo prioridade (adicionado na mudança de escopo).
    """

    def test_prioridade_baixa_aceita(self):
        """Deve aceitar prioridade BAIXA."""
        tarefa = Tarefa(titulo="Tarefa baixa", usuario_id=1, prioridade=Prioridade.BAIXA)
        assert tarefa.prioridade == Prioridade.BAIXA

    def test_prioridade_alta_aceita(self):
        """Deve aceitar prioridade ALTA."""
        tarefa = Tarefa(titulo="Tarefa alta", usuario_id=1, prioridade=Prioridade.ALTA)
        assert tarefa.prioridade == Prioridade.ALTA

    def test_prioridade_string_invalida_lanca_excecao(self):
        """String inválida como prioridade deve lançar ValueError."""
        with pytest.raises(ValueError, match="Prioridade invalida"):
            Tarefa(titulo="Teste", usuario_id=1, prioridade="URGENTISSIMA")

    def test_prioridade_none_lanca_excecao(self):
        """None como prioridade deve lançar ValueError."""
        with pytest.raises(ValueError, match="Prioridade invalida"):
            Tarefa(titulo="Teste", usuario_id=1, prioridade=None)

    def test_prioridade_inteiro_lanca_excecao(self):
        """Inteiro como prioridade deve lançar ValueError."""
        with pytest.raises(ValueError, match="Prioridade invalida"):
            Tarefa(titulo="Teste", usuario_id=1, prioridade=1)

    def test_todos_valores_de_prioridade_sao_aceitos(self):
        """Todos os quatro valores do enum devem ser aceitos."""
        for prioridade in Prioridade:
            tarefa = Tarefa(titulo=f"Tarefa {prioridade.value}", usuario_id=1, prioridade=prioridade)
            assert tarefa.prioridade == prioridade


class TestTransicoesDeStatus:
    """Testa o fluxo de transições de status (Kanban)."""

    def test_transicao_valida_a_fazer_para_em_progresso(self):
        """Deve permitir A_FAZER → EM_PROGRESSO."""
        tarefa = Tarefa(titulo="Tarefa", usuario_id=1)
        resultado = tarefa.mudar_status(Status.EM_PROGRESSO)
        assert resultado is True
        assert tarefa.status == Status.EM_PROGRESSO

    def test_transicao_valida_em_progresso_para_concluido(self):
        """Deve permitir EM_PROGRESSO → CONCLUIDO."""
        tarefa = Tarefa(titulo="Tarefa", usuario_id=1)
        tarefa.mudar_status(Status.EM_PROGRESSO)
        resultado = tarefa.mudar_status(Status.CONCLUIDO)
        assert resultado is True
        assert tarefa.status == Status.CONCLUIDO

    def test_transicao_valida_em_progresso_para_a_fazer(self):
        """Deve permitir retorno EM_PROGRESSO → A_FAZER."""
        tarefa = Tarefa(titulo="Tarefa", usuario_id=1)
        tarefa.mudar_status(Status.EM_PROGRESSO)
        resultado = tarefa.mudar_status(Status.A_FAZER)
        assert resultado is True
        assert tarefa.status == Status.A_FAZER

    def test_transicao_invalida_a_fazer_para_concluido(self):
        """Não deve permitir saltar de A_FAZER direto para CONCLUIDO."""
        tarefa = Tarefa(titulo="Tarefa", usuario_id=1)
        resultado = tarefa.mudar_status(Status.CONCLUIDO)
        assert resultado is False
        assert tarefa.status == Status.A_FAZER  # Status não muda

    def test_transicao_invalida_concluido_para_qualquer(self):
        """CONCLUIDO é estado final — nenhuma transição deve ser permitida."""
        tarefa = Tarefa(titulo="Tarefa", usuario_id=1)
        tarefa.mudar_status(Status.EM_PROGRESSO)
        tarefa.mudar_status(Status.CONCLUIDO)

        for status in Status:
            resultado = tarefa.mudar_status(status)
            assert resultado is False

    def test_atualizado_em_muda_apos_transicao(self):
        """O campo atualizado_em deve ser atualizado após transição."""
        tarefa = Tarefa(titulo="Tarefa", usuario_id=1).salvar()
        criado_em = tarefa.atualizado_em
        tarefa.mudar_status(Status.EM_PROGRESSO)
        assert tarefa.atualizado_em >= criado_em


class TestRepositorioDeTarefas:
    """Testa persistência e consultas no repositório."""

    def test_salvar_e_buscar_por_id(self):
        """Deve salvar e recuperar tarefa pelo ID."""
        tarefa = Tarefa(titulo="Tarefa salva", usuario_id=1).salvar()
        encontrada = Tarefa.buscar_por_id(tarefa.id)
        assert encontrada is not None
        assert encontrada.titulo == "Tarefa salva"

    def test_excluir_tarefa(self):
        """Deve remover a tarefa do repositório."""
        tarefa = Tarefa(titulo="Para excluir", usuario_id=1).salvar()
        resultado = Tarefa.excluir(tarefa.id)
        assert resultado is True
        assert Tarefa.buscar_por_id(tarefa.id) is None

    def test_excluir_id_inexistente_retorna_false(self):
        """Excluir ID inexistente deve retornar False."""
        assert Tarefa.excluir(9999) is False

    def test_listar_por_status(self):
        """Deve filtrar tarefas por status corretamente."""
        Tarefa(titulo="Tarefa 1", usuario_id=1).salvar()
        t2 = Tarefa(titulo="Tarefa 2", usuario_id=1).salvar()
        t2.mudar_status(Status.EM_PROGRESSO)

        a_fazer = Tarefa.listar_por_status(Status.A_FAZER)
        em_progresso = Tarefa.listar_por_status(Status.EM_PROGRESSO)

        assert len(a_fazer) == 1
        assert len(em_progresso) == 1

    def test_listar_por_prioridade(self):
        """Deve filtrar tarefas por prioridade corretamente."""
        Tarefa(titulo="Baixa", usuario_id=1, prioridade=Prioridade.BAIXA).salvar()
        Tarefa(titulo="Crítica", usuario_id=1, prioridade=Prioridade.CRITICA).salvar()

        criticas = Tarefa.listar_por_prioridade(Prioridade.CRITICA)
        assert len(criticas) == 1
        assert criticas[0].titulo == "Crítica"

    def test_to_dict_contem_campos_esperados(self):
        """to_dict deve conter todos os campos necessários."""
        tarefa = Tarefa(titulo="Tarefa", usuario_id=1, prioridade=Prioridade.ALTA).salvar()
        d = tarefa.to_dict()
        campos = ["id", "titulo", "descricao", "status", "prioridade", "usuario_id",
                  "criado_em", "atualizado_em"]
        for campo in campos:
            assert campo in d, f"Campo '{campo}' ausente no to_dict()"
