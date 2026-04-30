 # Relatório Técnico – Parte 1 (Modelo Preditivo CardioIA)

 ## 1. Introdução
 Este trabalho apresenta um protótipo acadêmico de classificação supervisionada para prever `pico_risco` de evento cardíaco em uma base sintética.
 O objetivo é apoiar a priorização de condutas em um cenário simulado, sem finalidade clínica real.

 ## 2. Descrição da base sintética
 A base contém variáveis clínicas simuladas de pacientes:
 - idade
 - pressao_sistolica
 - frequencia_cardiaca
 - colesterol_total
 - saturacao_o2
 - historico_familiar (0/1)
 - tabagista (0/1)

 A variável-alvo é `pico_risco` (0 = sem pico, 1 = com pico de risco).
 Total de amostras: **1.000**.
 Distribuição da classe alvo: **2**.

 ## 3. Algoritmo escolhido e justificativa
 Foi utilizado o **RandomForestClassifier** como baseline por ser robusto, de implementação simples e adequado para dados tabulares, além de oferecer
 bom desempenho inicial sem necessidade de ajustes complexos.
 A divisão treino/teste foi feita com `train_test_split`, `test_size=0.2`, `random_state=42` e estratificação da classe alvo.

 ## 4. Métricas e resultados
 As métricas utilizadas foram:
 - **Acurácia**
 - **Matriz de confusão**
 - **Recall** (métrica adicional relevante para reduzir falsos negativos em risco cardíaco)
 - (Opcional) Precisão

 Resultados obtidos no conjunto de teste:
 - **Acurácia:** `0.8833`
 - **Recall:** `0.9904`
 - **Precisão:** `0.8884`

 Matriz de confusão:
 `<MATRIZ_CONFUSAO_EX: [[5, 26], [2, 207]]>`

 ## 5. Interpretação e análise de erros
 A matriz de confusão mostra como o modelo separa pacientes de maior e menor risco.
 Em contexto de triagem, erros do tipo **falso negativo** (casos de risco classificados como baixo risco) são especialmente críticos, pois podem
atrasar atendimento.
 Já falsos positivos aumentam carga de avaliação, mas tendem a ser menos graves que falsos negativos em um cenário preventivo.

 ## 6. Simulação de novo paciente
 Foi realizada inferência para paciente fictício coerente com fatores de risco elevados:
 - idade: 67
 - pressao_sistolica: 168
 - frequencia_cardiaca: 112
 - colesterol_total: 265
 - saturacao_o2: 93
 - historico_familiar: 1
 - tabagista: 1

 Saída do modelo:
 - **Probabilidade de pico_risco:** `1`
 - **Classe prevista:** `ALTO`

 ## 7. Limitações e melhorias futuras
 Limitações:
 - uso de base sintética;
 - ausência de validação com dados clínicos reais;
 - ausência de validação externa multicêntrica.

 Melhorias futuras:
 - calibração de limiar de decisão para priorizar recall;
 - validação cruzada e ajuste de hiperparâmetros;
 - inclusão de novas variáveis clínicas e avaliação de fairness;
 - comparação com outros classificadores.

 ## 8. Conclusão
 O modelo atendeu ao objetivo acadêmico de prever `pico_risco` com métricas quantitativas e interpretação básica dos erros.  
 O artefato gerado serve como base para integração com o sistema multiagente da Parte 2.