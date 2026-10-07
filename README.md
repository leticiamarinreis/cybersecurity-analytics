# 🛡️ Análise Executiva de Vulnerabilidades & Exposição a Riscos de CyberSecurity

Este projeto processa, limpa e cruza bases de ativos e vulnerabilidades de TI para avaliar o nível de exposição ao risco cibernético, diagnosticar problemas de qualidade de dados e gerar insumos para priorização estratégica e tomada de decisão executiva.

---

## 📌 Visão Geral do Pipeline

O pipeline foi projetado de forma modular em Python, realizando desde a leitura dos arquivos com delimitador `;` até a consolidação de relatórios priorizados para dashboards e apresentações executivas.

---

## ⚙️ Linguagens e Bibliotecas Utilizadas

* Python 3.11
* Biblioteca `pandas`
* Biblioteca `matplotlib`

---

## 📁 Estrutura do Projeto

```text
analise-vulnerabilidades/
│
├── data/
│   ├── ativos.csv
│   └── vulnerabilidades.csv
│
├── src/
│   ├── __init__.py
│   ├── carregamento.py
│   ├── padronizacao.py
│   ├── tratamento_datas.py
│   ├── cruzamento.py
│   ├── dashboard_executivo_cyber.py
│   ├── priorizacao.py
│   ├── classificacao.py
│   ├── kpis.py
│   ├── validacao.py
│   └── analise_ativos.py
│
├── outputs/
│   ├── vulnerabilidades_priorizadas.csv
│   └── ativos_expostos.csv
│   └── CyberExposure_DashboardExecutivo.png
│
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```
---

## 🔄 Arquitetura das Etapas de Dados

Este projeto implementa a **Arquitetura Medalhão** (*Medallion Architecture*) para organizar e processar dados de ativos e vulnerabilidades em três camadas de maturidade: **Bronze**, **Silver** e **Gold**.

```text
+---------------------+      +---------------------+      +---------------------+
|      🥉 BRONZE      | ---> |      🥈 SILVER      | ---> |       🥇 GOLD       |
|     (Raw Data)      |      | (Cleaned/Enriched)  |      |  (Business Ready)   |
+---------------------+      +---------------------+      +---------------------+
| - ativos.csv        |      | - Limpeza e Join    |      | - Indicadores/KPIs  |
| - vulnerabil...csv  |      | - Regras de Negócio |      | - Visão Executiva   |
+---------------------+      +---------------------+      +---------------------+
```
---

### 🥉 Camada Bronze — Dados Brutos (Raw)

A camada **Bronze** é responsável por armazenar os dados no seu formato original de ingestão, garantindo rastreabilidade, auditabilidade e reprocessamento caso necessário.

* **Arquivos de Entrada:** `ativos.csv` e `vulnerabilidades.csv`
* **Tratamentos:**
  * Carregamento direto sem alterações de esquemas ou valores.
  * Preservação da fonte original para auditoria.

---

### 🥈 Camada Silver — Dados Tratados (Cleaned & Conformed)

A camada **Silver** realiza a limpeza, padronização, cruzamento de dados e enriquece a base com regras de negócio.

* **Integração:** Relacionamento e unificação pelo campo `ativo_id`.
* **Limpeza e Ajustes:**
  * Tratamento de valores inconsistentes nos campos de criticidade e severidade.
  * Correção de datas inválidas e gestão de ativos não mapeados.
* **Novos Atributos Criados:**
  * `cvss_band`: Faixa da pontuação CVSS.
  * `exposicao`: Classificação do nível de exposição do ativo.
  * `backlog`: Identificação de pendências de correção.
  * `idade_dias`: Tempo decorrido em dias desde a abertura.
  * `fora_sla`: Indicador booleano para itens fora do prazo.
  * `risk_score`: Pontuação final de risco do ativo/vulnerabilidade.

---

### 🥇 Camada Gold — Dados Analíticos (Business / Ready)

A camada **Gold** consolida as métricas, agregados e tabelas prontas para consumo final em dashboards executivos e relatórios de inteligência de segurança.

* **Métricas e Indicadores:**
  * Exposição total e backlog de vulnerabilidades.
  * Volume e acompanhamento de vulnerabilidades críticas.
  * **MTTR** (*Mean Time to Remediate*) e conformidade de **SLA**.
  * Ranking dos ativos mais críticos/vulneráveis.
* **Estruturas para Visualização:**
  * Matriz / *Heatmap* cruzando **CVSS × Criticidade do Ativo**.

---

## 🔄 Arquitetura do Fluxo de Dados do Scripts

O processamento e a transformação dos dados seguem um fluxo em esteira modular e sequencial:

```text
┌─────────────────┐
│   data/*.csv    │  (Dados brutos com inconsistências)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ carregamento.py │  Leitura dos arquivos CSV brutos com separador ';'
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ padronizacao.py │  Tratamento de strings, caixas e valores vazios
└────────┬────────┘
         │
         ▼
┌────────────────────┐
│tratamento_datas.py │  Conversão de formatos de data (DD/MM/AAAA)
└────────┬───────────┘
         │
         ▼
┌─────────────────┐
│  cruzamento.py  │  Left Join (vulnerabilidades + ativos pelo ativo_id)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ priorizacao.py  │  Cálculo do Score Matricial (Criticidade x Severidade)
└────────┬────────┘
         │
         ▼
┌──────────────────┐
│classificacao.py  │  Atribuição dos Níveis de Prioridade (P1, P2, P3)
└────────┬─────────┘
         │
         ▼
 ┌───────┴───────┐
 │               │
 ▼               ▼
┌──────────────┐ ┌───────────────────┐
│ validacao.py │ │ analise_ativos.py │
│   & kpis.py  │ │   & outputs/*.csv │
└──────────────┘ └───────────────────┘
 (Logs & KPIs)   (Bases consolidadas)
```
---

## 🧮 Regras de Negócio e Metodologia

### 1. Padronização de Dados (`padronizacao.py`)
Para contornar erros de digitação e registros inconsistentes das ferramentas de scanning:
* **Criticidade & Severidade:** Mapeados para valores padronizados (`Baixa`, `Média`, `Alta`, `Crítica`). Espaços vazios/brancos na criticidade são classificados como `Indefinida`.
* **Origem:** Normalização de strings duplicadas/formatadas incorretamente (ex: `CloudSecurity` e `Cloud-Security` unificados para `Cloud Security`).

### 2. Matriz de Score de Prioridade (`priorizacao.py`)
A prioridade técnica é dada por um score matricial:
$$\text{Priority Score} = \text{Criticidade do Ativo (1 a 4)} \times \text{Severidade da Vulnerabilidade (1 a 4)}$$

### 3. Matriz Executiva de SLA (`classificacao.py`)
* **P1 (Crítica/Emergencial):** Vulnerabilidades com severidade `Crítica` em ativos com criticidade `Crítica` ou `Alta`.
* **P2 (Alta Prioridade):** Vulnerabilidades de alta severidade em ativos médios, ou severidade crítica em ativos baixos/médios.
* **P3 (Atendimento Contínuo):** Demais combinações.
* **Sem classificação:** Vulnerabilidades com severidade ou criticidade nula/ausente.

---

## 📊 Principais Indicadores Calculados (KPIs)

* **Volume de Vulnerabilidades Expostas:** Total de itens com status `Aberta` ou `Em tratamento`.
* **Taxa de Integridade (Orfãs):** Vulnerabilidades sem ativo cadastrado correspondente (`~asset_join_ok`).
* **Top Ativos Críticos:** Ranking de ativos agrupados por quantidade de vulnerabilidades expostas e score acumulado.
* **Backlog P1 Exposto:** Total de falhas P1 pendentes de correção.

# Conclusão e Perspectivas Futuras

## 📌 Impacto do Projeto
O projeto demonstrou como transformar dados de vulnerabilidades e ativos em uma visão estruturada de risco cibernético e priorização de remediação. A **Arquitetura Medalhão** garantiu maior organização, rastreabilidade e qualidade dos dados, permitindo construir indicadores essenciais para apoiar a tomada de decisão:

* **Métricas Principais:** CVSS, Risk Score, SLA, Aging, MTTR, Backlog e Exposição.
* **Visualizações:** Rankings e Heatmaps estratégicos.

A análise evidenciou que a **qualidade dos dados é fundamental** para uma gestão eficiente de segurança.

---

## 🛠️ Tecnogias Utilizadas e Justificativa

A escolha de **Python**, **Pandas** e **Matplotlib** foi proporcional ao volume e à complexidade do case, permitindo:

* Tratamento, integração e validação de dados.
* Automação do pipeline e geração de visualizações reproduzíveis.
* Abordagem simples, eficiente e totalmente adequada ao problema.

---

## 🚀 Evolução e Escalabilidade

* **Próximos Passos (Enriquecimento):** O pipeline pode ser ampliado futuramente com integrações de fontes de dados adicionais como **CVE/CWE**, **EPSS**, **EDR** e **SIEM**.
* **Arquitetura em Escala:** Em cenários com grandes volumes, processamento distribuído e pipelines de alta recorrência, tecnologias como **Apache Spark / Databricks** e **Apache Airflow** seriam implementadas para substituir o processamento local, permitindo a evolução da solução conforme o crescimento do ambiente.
