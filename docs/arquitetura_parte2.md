# Parte 2 – Arquitetura do Sistema Multiagente (base para PDF)

## 1. Visão de arquitetura

O sistema possui um ponto de entrada único (Agente Orquestrador), que coordena dois agentes especialistas:

1. **Agente Analista de Risco**
2. **Agente Especialista em Protocolos**

Além disso, há dois recursos de suporte:
- **Modelo preditivo treinado** (`models/modelo_pico_risco.joblib`)
- **Base de protocolos simulados** (`data/protocolos/protocolos_risco.json`)

Fluxo macro:

```text
Entrada do paciente -> Orquestrador
Orquestrador --handoff--> Analista de Risco --tool--> predict_risk_tool -> modelo ML
Orquestrador --handoff--> Especialista em Protocolos --tool--> get_protocols_tool -> JSON protocolos
Orquestrador -> resposta final consolidada + historico
```

## 2. Papéis dos agentes

### 2.1. Agente Analista de Risco
- Recebe dados clínicos do paciente.
- Executa `predict_risk_tool`.
- Retorna:
  - `probabilidade_pico_risco`
  - `classe_risco` (baixo/medio/alto)
  - `predicao_binaria`

### 2.2. Agente Especialista em Protocolos
- Recebe apenas `classe_risco`.
- Executa `get_protocols_tool`.
- Retorna:
  - `prioridade`
  - lista de `acoes` recomendadas.

### 2.3. Agente Orquestrador
- É o ponto de entrada da aplicação.
- Faz validação inicial da entrada.
- Registra e executa handoffs.
- Consolida o resultado técnico em mensagem final amigável com IA local.
- Valida schema de saída final.

## 3. Handoffs e tools

### 3.1. Handoff 1
- **Origem:** Orquestrador
- **Destino:** Analista de Risco
- **Payload:** dados do paciente (features obrigatórias)

### 3.2. Tool usada pelo Analista
- **Nome:** `predict_risk_tool`
- **Função:** carregar modelo, inferir risco e classificar.

### 3.3. Handoff 2
- **Origem:** Orquestrador
- **Destino:** Especialista em Protocolos
- **Payload:** `classe_risco`

### 3.4. Tool usada pelo Especialista
- **Nome:** `get_protocols_tool`
- **Função:** buscar protocolo simulado no JSON por classe de risco.

## 4. Histórico e validação

- O sistema mantém trilha de execução no campo `historico`, incluindo:
  - evento de entrada;
  - handoffs;
  - resultados dos agentes;
  - chamada e resposta da IA local.

- A validação final exige:
  - `probabilidade_pico_risco`
  - `classe_risco`
  - `protocolos`
  - `mensagem_final`
  - `protocolos.acoes` como lista não vazia

## 5. Exemplo de request/response

### 5.1. Request exemplo

```json
{
  "idade": 67,
  "pressao_sistolica": 168,
  "frequencia_cardiaca": 112,
  "colesterol_total": 265,
  "saturacao_o2": 93,
  "historico_familiar": 1,
  "tabagista": 1
}
```

### 5.2. Response exemplo (resumo)

```json
{
  "probabilidade_pico_risco": 0.81,
  "classe_risco": "alto",
  "protocolos": {
    "prioridade": "urgente",
    "acoes": [
      "Acionar protocolo de emergência institucional",
      "Solicitar avaliação médica imediata"
    ]
  },
  "mensagem_final": "..."
}
```


