"""
Testes automatizados para o Sistema de Gerenciamento de Tarefas.
Utiliza Pytest para validar todas as operações CRUD da API.
"""

import pytest
import sys
import os

# Adiciona o diretório src ao path para importar o app
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from app import app, tarefas, criar_tarefa


@pytest.fixture(autouse=True)
def limpar_tarefas():
    """Limpa o banco de dados antes de cada teste."""
    tarefas.clear()
    # Reseta o ID
    import app as app_module
    app_module.proximo_id = 1
    yield
    tarefas.clear()


@pytest.fixture
def cliente():
    """Cria um cliente de teste Flask."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


# ─── Testes unitários da função criar_tarefa ──────────────────────────────────

class TestCriarTarefa:
    def test_criar_tarefa_valida(self):
        tarefa = criar_tarefa("Implementar login", "Criar tela de autenticação")
        assert tarefa["titulo"] == "Implementar login"
        assert tarefa["status"] == "a_fazer"
        assert tarefa["prioridade"] == "media"
        assert "id" in tarefa

    def test_titulo_vazio_levanta_erro(self):
        with pytest.raises(ValueError, match="título"):
            criar_tarefa("", "Descrição qualquer")

    def test_titulo_apenas_espacos_levanta_erro(self):
        with pytest.raises(ValueError):
            criar_tarefa("   ", "Descrição qualquer")

    def test_prioridade_invalida_levanta_erro(self):
        with pytest.raises(ValueError, match="Prioridade"):
            criar_tarefa("Tarefa", "Desc", prioridade="urgente")

    def test_status_invalido_levanta_erro(self):
        with pytest.raises(ValueError, match="Status"):
            criar_tarefa("Tarefa", "Desc", status="pausado")

    def test_ids_sao_incrementais(self):
        t1 = criar_tarefa("Tarefa 1", "")
        t2 = criar_tarefa("Tarefa 2", "")
        assert t2["id"] == t1["id"] + 1


# ─── Testes de integração da API ──────────────────────────────────────────────

class TestApiCriar:
    def test_criar_tarefa_sucesso(self, cliente):
        resposta = cliente.post("/tarefas", json={
            "titulo": "Nova tarefa",
            "descricao": "Descrição da tarefa",
            "prioridade": "alta"
        })
        assert resposta.status_code == 201
        dados = resposta.get_json()
        assert dados["titulo"] == "Nova tarefa"
        assert dados["prioridade"] == "alta"

    def test_criar_sem_titulo_retorna_400(self, cliente):
        resposta = cliente.post("/tarefas", json={"descricao": "Sem título"})
        assert resposta.status_code == 400

    def test_criar_sem_corpo_retorna_erro(self, cliente):
        # Flask retorna 415 (Unsupported Media Type) para content-type incorreto
        resposta = cliente.post("/tarefas", data="texto inválido",
                                content_type="text/plain")
        assert resposta.status_code in (400, 415)


class TestApiListar:
    def test_listar_vazio(self, cliente):
        resposta = cliente.get("/tarefas")
        assert resposta.status_code == 200
        assert resposta.get_json() == []

    def test_listar_com_tarefas(self, cliente):
        cliente.post("/tarefas", json={"titulo": "T1", "descricao": ""})
        cliente.post("/tarefas", json={"titulo": "T2", "descricao": ""})
        resposta = cliente.get("/tarefas")
        assert len(resposta.get_json()) == 2

    def test_filtrar_por_status(self, cliente):
        cliente.post("/tarefas", json={"titulo": "T1", "descricao": "", "status": "a_fazer"})
        cliente.post("/tarefas", json={"titulo": "T2", "descricao": "", "status": "concluido"})
        resposta = cliente.get("/tarefas?status=concluido")
        dados = resposta.get_json()
        assert len(dados) == 1
        assert dados[0]["titulo"] == "T2"


class TestApiBuscar:
    def test_buscar_tarefa_existente(self, cliente):
        cliente.post("/tarefas", json={"titulo": "Minha tarefa", "descricao": ""})
        resposta = cliente.get("/tarefas/1")
        assert resposta.status_code == 200
        assert resposta.get_json()["titulo"] == "Minha tarefa"

    def test_buscar_tarefa_inexistente(self, cliente):
        resposta = cliente.get("/tarefas/999")
        assert resposta.status_code == 404


class TestApiAtualizar:
    def test_atualizar_status(self, cliente):
        cliente.post("/tarefas", json={"titulo": "Tarefa", "descricao": ""})
        resposta = cliente.put("/tarefas/1", json={"status": "em_progresso"})
        assert resposta.status_code == 200
        assert resposta.get_json()["status"] == "em_progresso"

    def test_atualizar_inexistente(self, cliente):
        resposta = cliente.put("/tarefas/999", json={"titulo": "X"})
        assert resposta.status_code == 404


class TestApiDeletar:
    def test_deletar_tarefa(self, cliente):
        cliente.post("/tarefas", json={"titulo": "Para deletar", "descricao": ""})
        resposta = cliente.delete("/tarefas/1")
        assert resposta.status_code == 200
        assert cliente.get("/tarefas/1").status_code == 404

    def test_deletar_inexistente(self, cliente):
        resposta = cliente.delete("/tarefas/999")
        assert resposta.status_code == 404


class TestHealthCheck:
    def test_health_ok(self, cliente):
        resposta = cliente.get("/health")
        assert resposta.status_code == 200
        assert resposta.get_json()["status"] == "ok"
