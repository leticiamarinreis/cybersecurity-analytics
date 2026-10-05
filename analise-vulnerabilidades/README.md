# Análise de Vulnerabilidades

Pipeline em Python/pandas que cruza a base de vulnerabilidades com a base de ativos,
calcula um score de risco, classifica em P1/P2/P3 e gera indicadores.

## Como executar

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

## Dados de entrada (`data/`, separador `;`)

- `ativos.csv`: ativo_id, sistema, criticidade, dominio, ambiente, localidade, status_ativo
- `vulnerabilidades.csv`: vuln_id, ativo_id, severidade, origem, status, data_abertura, data_correcao

Os arquivos incluídos são **dados de exemplo** (com inconsistências propositais de escrita).
Substitua pelos seus arquivos reais mantendo os mesmos nomes de colunas.

## Etapas do pipeline

| Módulo | Função |
|---|---|
| `carregamento` | Lê os CSVs |
| `padronizacao` | Normaliza criticidade, severidade, origem e ambiente |
| `tratamento_datas` | Converte datas (DD/MM/AAAA) |
| `cruzamento` | Left join por `ativo_id`; marca exposição e falhas de join |
| `priorizacao` | Score = criticidade x severidade (1 a 16) |
| `classificacao` | P1 / P2 / P3 / Sem classificação |
| `kpis` | Total, expostas, aceitas, corrigidas, P1 expostas |
| `validacao` | Vulnerabilidades sem ativo, valores não padronizados, datas inválidas |
| `analise_ativos` | Ranking de ativos expostos e exportação dos CSVs |

## Saídas (`outputs/`)

- `vulnerabilidades_priorizadas.csv`: base completa ordenada por prioridade e score
- `ativos_expostos.csv`: ranking de ativos com vulnerabilidades expostas

## Regras de classificação

- **P1**: severidade Crítica em ativo Crítico ou Alto
- **P2**: Crítica/Alta em ativo Médio; Alta em ativo Crítico; Crítica em ativo Baixo
- **P3**: demais casos
- **Sem classificação**: severidade ou criticidade ausente
