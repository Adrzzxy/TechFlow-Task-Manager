# 📋 TechFlow Solutions — Sistema de Gerenciamento de Tarefas

![CI Status](https://github.com/seu-usuario/techflow-tasks/actions/workflows/ci.yml/badge.svg)

## 🎯 Objetivo do Projeto

Desenvolver um sistema web de **gerenciamento de tarefas** para uma startup de logística, permitindo acompanhar o fluxo de trabalho em tempo real, priorizar tarefas críticas e monitorar o desempenho da equipe.

O projeto é desenvolvido pela **TechFlow Solutions** aplicando princípios de **Engenharia de Software** e **metodologias ágeis**.

---

## 📌 Escopo Inicial

- API REST para gerenciamento de tarefas com operações CRUD (Criar, Ler, Atualizar, Deletar)
- Suporte a prioridades (baixa, média, alta) e status (A Fazer, Em Progresso, Concluído)
- Testes automatizados com Pytest
- Pipeline de integração contínua com GitHub Actions

---

## 🔄 Metodologia Adotada

O projeto utiliza **Kanban** como metodologia ágil principal, com quadro no GitHub Projects organizado em três colunas:

| Coluna | Descrição |
|---|---|
| **A Fazer (To Do)** | Tarefas planejadas e não iniciadas |
| **Em Progresso (In Progress)** | Tarefas em desenvolvimento ativo |
| **Concluído (Done)** | Tarefas finalizadas e validadas |

---

## 🏗️ Estrutura do Repositório

```
techflow-tasks/
├── src/
│   └── app.py            # Aplicação Flask principal (CRUD de tarefas)
├── tests/
│   └── test_app.py       # Testes automatizados com Pytest
├── docs/
│   └── documentacao.pdf  # Documentação técnica completa
├── .github/
│   └── workflows/
│       └── ci.yml        # Pipeline de CI com GitHub Actions
├── requirements.txt      # Dependências do projeto
└── README.md             # Este arquivo
```

---

## 🚀 Como Executar

### Pré-requisitos
- Python 3.11+
- pip

### Instalação

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/techflow-tasks.git
cd techflow-tasks

# Instale as dependências
pip install -r requirements.txt

# Inicie o servidor
python src/app.py
```

A API estará disponível em `http://localhost:5000`.

### Executar os Testes

```bash
pytest tests/ -v
```

---

## 📡 Endpoints da API

| Método | Endpoint | Descrição |
|---|---|---|
| `POST` | `/tarefas` | Criar nova tarefa |
| `GET` | `/tarefas` | Listar todas as tarefas |
| `GET` | `/tarefas/<id>` | Buscar tarefa por ID |
| `PUT` | `/tarefas/<id>` | Atualizar tarefa |
| `DELETE` | `/tarefas/<id>` | Deletar tarefa |
| `GET` | `/health` | Verificar status da API |

### Exemplo de uso

```bash
# Criar tarefa
curl -X POST http://localhost:5000/tarefas \
  -H "Content-Type: application/json" \
  -d '{"titulo": "Implementar autenticação", "prioridade": "alta"}'

# Listar tarefas em progresso
curl http://localhost:5000/tarefas?status=em_progresso
```

---

## 🔀 Mudança de Escopo

**Data:** Sprint 2  
**Justificativa:** Após feedback do cliente (startup de logística), identificou-se a necessidade de adicionar um **filtro de tarefas por status** na listagem, permitindo que gestores visualizem apenas tarefas de uma etapa específica do fluxo.

**Impacto:** A funcionalidade foi adicionada ao endpoint `GET /tarefas` como parâmetro de query (`?status=`), sem quebrar a interface existente. Um novo card foi criado no Kanban e o commit correspondente documenta a mudança.

---

## 👥 Equipe

- **Desenvolvedor/Gestor de Projetos:** TechFlow Solutions  
- **Cliente:** Startup de Logística (fictícia)

---

## 📚 Referências

- [Documentação Flask](https://flask.palletsprojects.com/)
- [Documentação Pytest](https://docs.pytest.org/)
- [GitHub Actions Docs](https://docs.github.com/en/actions)
- Pressman, R. — *Engenharia de Software: Uma Abordagem Profissional*
