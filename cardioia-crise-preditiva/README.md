# CardioIA – Crise Preditiva (FIAP)

Projeto acadêmico da FIAP com duas partes:
1. **Modelo supervisionado de classificação** para prever `pico_risco`.
2. **Sistema multiagente** com 3 agentes mínimos (Analista de Risco, Especialista em Protocolos e Orquestrador).

Nesta versão, a IA conversacional roda localmente via **Ollama** com **gemma4:e2b** (equivalente ao requisito de orquestração multiagente com tools e handoffs).

## Arquitetura da Parte 2 (resumo)

- **Agente Analista de Risco**
  - Tool: `predict_risk_tool`
  - Função: aplicar o modelo treinado e retornar probabilidade + classe de risco.
- **Agente Especialista em Protocolos**
  - Tool: `get_protocols_tool`
  - Função: mapear a classe de risco para condutas simuladas em JSON.
- **Agente Orquestrador**
  - Entrada única do sistema.
  - Executa handoffs para os dois agentes.
  - Mantém histórico de mensagens/eventos.
  - Faz validação de saída final.

## Pré-requisitos

- Python 3.10+
- Ollama instalado e ativo
- Modelo local já baixado (`gemma4:e2b`)

## Setup rápido

1. Criar ambiente virtual:
```bash
python -m venv .venv
```

2. Ativar ambiente virtual (Windows PowerShell):
```bash
.venv\Scripts\Activate.ps1
```

3. Instalar dependências:
```bash
pip install -r requirements.txt
```

4. Configurar variáveis:
```bash
copy .env.example .env
```

5. Garantir Ollama rodando:
```bash
ollama serve
```

## Treinar modelo (Parte 1 integrada)

```bash
python -m src.train_model
```

Saída esperada:
- Geração/carregamento da base sintética em `data/raw/`
- Cópia processada em `data/processed/`
- Modelo salvo em `models/modelo_pico_risco.joblib`

## Executar demo multiagente (Parte 2)

Com paciente padrão:
```bash
python -m src.cli_demo
```

Com paciente customizado:
```bash
python -m src.cli_demo --patient-json "{\"idade\":67,\"pressao_sistolica\":168,\"frequencia_cardiaca\":112,\"colesterol_total\":265,\"saturacao_o2\":93,\"historico_familiar\":1,\"tabagista\":1}"
```

Gerando evidência JSON para PDF da Parte 2:
```bash
python -m src.cli_demo --save-output docs\exemplo_execucao.json
```

## Estrutura principal

```text
data/                  # base sintética e protocolos simulados
models/                # artefato do modelo treinado
src/                   # treino, predição, tools e agentes
notebooks/             # notebook da Parte 1 (Colab)
docs/                  # relatório, arquitetura e evidências
video/                 # roteiro da gravação
```

## Como mapear para os requisitos FIAP

- **Handoffs entre agentes:** implementado no `OrchestratorAgent` via eventos `handoff`.
- **Uso de tools:** implementado em `src/agents/tools.py`.
- **Histórico de mensagens/eventos:** campo `historico` no output final.
- **Validação de saída:** checagem de campos obrigatórios no `OrchestratorAgent`.

