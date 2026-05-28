"""
TechFlow Solutions - Sistema de Gerenciamento de Tarefas
Aplicação Flask com operações CRUD completas para tarefas.
"""

from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# Banco de dados em memória (simula persistência)
tarefas = {}
proximo_id = 1


def criar_tarefa(titulo, descricao, prioridade="media", status="a_fazer"):
    """Cria uma nova tarefa e retorna o objeto criado."""
    global proximo_id

    if not titulo or not titulo.strip():
        raise ValueError("O título da tarefa não pode ser vazio.")

    prioridades_validas = ["baixa", "media", "alta"]
    if prioridade not in prioridades_validas:
        raise ValueError(f"Prioridade inválida. Use: {prioridades_validas}")

    status_validos = ["a_fazer", "em_progresso", "concluido"]
    if status not in status_validos:
        raise ValueError(f"Status inválido. Use: {status_validos}")

    tarefa = {
        "id": proximo_id,
        "titulo": titulo.strip(),
        "descricao": descricao.strip() if descricao else "",
        "prioridade": prioridade,
        "status": status,
        "criado_em": datetime.now().isoformat(),
        "atualizado_em": datetime.now().isoformat(),
    }

    tarefas[proximo_id] = tarefa
    proximo_id += 1
    return tarefa


# ─── CREATE ───────────────────────────────────────────────────────────────────

@app.route("/tarefas", methods=["POST"])
def criar():
    """Cria uma nova tarefa."""
    dados = request.get_json()
    if not dados:
        return jsonify({"erro": "Corpo da requisição inválido."}), 400

    try:
        tarefa = criar_tarefa(
            titulo=dados.get("titulo", ""),
            descricao=dados.get("descricao", ""),
            prioridade=dados.get("prioridade", "media"),
            status=dados.get("status", "a_fazer"),
        )
        return jsonify(tarefa), 201
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400


# ─── READ ─────────────────────────────────────────────────────────────────────

@app.route("/tarefas", methods=["GET"])
def listar():
    """Lista todas as tarefas, com filtro opcional por status."""
    status_filtro = request.args.get("status")
    resultado = list(tarefas.values())

    if status_filtro:
        resultado = [t for t in resultado if t["status"] == status_filtro]

    return jsonify(resultado), 200


@app.route("/tarefas/<int:tarefa_id>", methods=["GET"])
def buscar(tarefa_id):
    """Busca uma tarefa específica pelo ID."""
    tarefa = tarefas.get(tarefa_id)
    if not tarefa:
        return jsonify({"erro": "Tarefa não encontrada."}), 404
    return jsonify(tarefa), 200


# ─── UPDATE ───────────────────────────────────────────────────────────────────

@app.route("/tarefas/<int:tarefa_id>", methods=["PUT"])
def atualizar(tarefa_id):
    """Atualiza uma tarefa existente."""
    tarefa = tarefas.get(tarefa_id)
    if not tarefa:
        return jsonify({"erro": "Tarefa não encontrada."}), 404

    dados = request.get_json()
    if not dados:
        return jsonify({"erro": "Corpo da requisição inválido."}), 400

    campos_permitidos = ["titulo", "descricao", "prioridade", "status"]
    for campo in campos_permitidos:
        if campo in dados:
            tarefa[campo] = dados[campo]

    tarefa["atualizado_em"] = datetime.now().isoformat()
    return jsonify(tarefa), 200


# ─── DELETE ───────────────────────────────────────────────────────────────────

@app.route("/tarefas/<int:tarefa_id>", methods=["DELETE"])
def deletar(tarefa_id):
    """Remove uma tarefa pelo ID."""
    tarefa = tarefas.pop(tarefa_id, None)
    if not tarefa:
        return jsonify({"erro": "Tarefa não encontrada."}), 404
    return jsonify({"mensagem": "Tarefa removida com sucesso."}), 200


# ─── HEALTH CHECK ─────────────────────────────────────────────────────────────

@app.route("/health", methods=["GET"])
def health():
    """Verifica se a API está funcionando."""
    return jsonify({"status": "ok", "total_tarefas": len(tarefas)}), 200


if __name__ == "__main__":
    app.run(debug=True, port=5000)
