# 🛡️ Análise Executiva de Vulnerabilidades & Exposição a Riscos de CyberSecurity

Este projeto processa, limpa e cruza bases brontas de ativos e vulnerabilidades de TI para avaliar o nível de exposição ao risco cibernético, diagnosticar problemas de qualidade de dados e gerar insumos para priorização estratégica e tomada de decisão executiva.

---

## 📌 Visão Geral do Pipeline

O pipeline foi projetado de forma modular em Python, realizando desde a leitura dos arquivos com delimitador `;` até a consolidação de relatórios priorizados para dashboards e apresentações executivas.

---

## 🌐 Como Acessar o Dashboard Executivo

O dashboard foi disponibilizado em formato HTML estático e pode ser visualizado diretamente no seu navegador de preferência, sem a necessidade de servidores web ou dependências complexas de backend.

### 📍 Método 1: Acesso via Arquivo Local (Navegador)

1. Faça o download do arquivo `Cyber Exposure _ Dashboard executivo.html` (ou utilize o arquivo salvo na sua máquina).
2. Dê um **duplo clique** sobre o arquivo **ou** abra o seu navegador (Chrome, Edge, Firefox, Safari) e pressione `Ctrl + O` (Windows) ou `Cmd + O` (Mac).
3. Selecione o arquivo no diretório:
   ```text
   file:///Users/leticiamarinreis/Downloads/Cyber%20Exposure%20_%20Dashboard%20executivo.html

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
│   └── Cyber Exposure _ Dashboard executivo.html
│
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```
---

## 🔄 Arquitetura das Etapas de Dados

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

---

## ⚙️ Como Executar

### Pré-requisitos
* Python 3.8+
* Biblioteca `pandas`
