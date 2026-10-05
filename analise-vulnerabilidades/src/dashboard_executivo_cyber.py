# dashboard_executivo_cyber.py
# Dependencias: pandas, numpy, matplotlib e seaborn

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.gridspec import GridSpec
from matplotlib.patches import FancyBboxPatch

# ============================================================
# 1. CONFIGURACAO
# ============================================================

ARQUIVO_ATIVOS = "ativos.csv"
ARQUIVO_VULNERABILIDADES = "vulnerabilidades.csv"
ARQUIVO_SAIDA = "dashboard_executivo_cyber.png"
DATA_REFERENCIA = pd.Timestamp("2026-10-05")

# ============================================================
# 2. LEITURA DAS BASES
# ============================================================

ativos = pd.read_csv(ARQUIVO_ATIVOS, sep=";")
vulnerabilidades = pd.read_csv(ARQUIVO_VULNERABILIDADES, sep=";")

# ============================================================
# 3. LIMPEZA E PADRONIZACAO
# ============================================================

ativos["criticidade_norm"] = (
    ativos["criticidade"]
    .fillna("")
    .astype(str)
    .str.strip()
    .replace(
        {
            "media": "Média",
            "critica": "Crítica",
            "Critica": "Crítica",
            "BaixA": "Baixa",
            "": "N/A",
            "N/A": "N/A",
        }
    )
)

vulnerabilidades["sev_norm"] = (
    vulnerabilidades["severidade"]
    .fillna("")
    .astype(str)
    .str.strip()
    .replace(
        {
            "media": "Média",
            "Media": "Média",
            "critica": "Crítica",
            "Critica": "Crítica",
            "ALTA": "Alta",
            "Alto": "Alta",
            "BaixA": "Baixa",
            "": "N/A",
            "N/A": "N/A",
        }
    )
)

vulnerabilidades["origem_norm"] = (
    vulnerabilidades["origem"]
    .fillna("Não informada")
    .astype(str)
    .str.strip()
    .replace(
        {
            "CloudSecurity": "Cloud Security",
            "Cloud-Security": "Cloud Security",
        }
    )
)

# Datas invalidas sao convertidas para NaT.
vulnerabilidades["abertura"] = pd.to_datetime(
    vulnerabilidades["data_abertura"],
    dayfirst=True,
    errors="coerce",
)

vulnerabilidades["correcao"] = pd.to_datetime(
    vulnerabilidades["data_correcao"],
    dayfirst=True,
    errors="coerce",
)

# ============================================================
# 4. JUNCAO DAS BASES
# ============================================================

base = vulnerabilidades.merge(
    ativos[
        [
            "ativo_id",
            "sistema",
            "ambiente",
            "criticidade_norm",
            "status_ativo",
        ]
    ],
    on="ativo_id",
    how="left",
)

# ============================================================
# 5. REGRAS DE NEGOCIO
# ============================================================

STATUS_EXPOSICAO_ATIVA = ["Aberta", "Em tratamento"]

exposicao_ativa = base[
    base["status"].isin(STATUS_EXPOSICAO_ATIVA)
].copy()

# Para aging, usamos apenas datas validas e anteriores ou iguais
# a data de referencia.
exposicao_ativa_datas_validas = exposicao_ativa[
    exposicao_ativa["abertura"].notna()
    & (exposicao_ativa["abertura"] <= DATA_REFERENCIA)
].copy()

# Pesos propostos para o score. Sao uma regra analitica do case,
# nao um padrao oficial de mercado.
peso_severidade = {
    "Crítica": 10,
    "Alta": 7,
    "Média": 4,
    "Baixa": 1,
    "N/A": 0,
}

peso_criticidade_ativo = {
    "Crítica": 4,
    "Alta": 3,
    "Média": 2,
    "Baixa": 1,
    "N/A": 0,
}

# Risk score por vulnerabilidade:
# CVSS + severidade + criticidade do ativo + bonus de Producao.
exposicao_ativa["risk_score"] = (
    pd.to_numeric(
        exposicao_ativa["cvss_score"],
        errors="coerce",
    ).fillna(0)
    + exposicao_ativa["sev_norm"].map(peso_severidade).fillna(0)
    + exposicao_ativa["criticidade_norm"]
      .map(peso_criticidade_ativo)
      .fillna(0)
    + exposicao_ativa["ambiente"].eq("Produção").astype(int) * 3
)

# ============================================================
# 6. CALCULO DOS KPIs
# ============================================================

kpi_exposicao_ativa = len(exposicao_ativa)

kpi_criticas_ativas = int(
    (exposicao_ativa["sev_norm"] == "Crítica").sum()
)

# Exclui A9999 e outros IDs nao cadastrados do indicador de ativos.
kpi_ativos_impactados = exposicao_ativa.loc[
    exposicao_ativa["ativo_id"].isin(ativos["ativo_id"]),
    "ativo_id",
].nunique()

aging_dias = (
    DATA_REFERENCIA
    - exposicao_ativa_datas_validas["abertura"]
).dt.days

kpi_backlog_90 = (
    float((aging_dias > 90).mean() * 100)
    if len(aging_dias)
    else np.nan
)

corrigidas = base[
    (base["status"] == "Corrigida")
    & base["abertura"].notna()
    & base["correcao"].notna()
].copy()

corrigidas["mttr"] = (
    corrigidas["correcao"] - corrigidas["abertura"]
).dt.days

# Remove diferencas negativas, pois indicam inconsistencias temporais.
corrigidas = corrigidas[corrigidas["mttr"] >= 0].copy()

kpi_mttr = corrigidas["mttr"].mean()

# ============================================================
# 7. TEMA VISUAL
# ============================================================

sns.set_theme(style="whitegrid")

COR_FUNDO = "#F4F7FB"
COR_NAVY = "#12304A"
COR_AZUL = "#2673B8"
COR_TEAL = "#0796A3"
COR_VERMELHO = "#C63D4A"
COR_LARANJA = "#F39C3D"
COR_VERDE = "#2D8C6A"
COR_ROXO = "#7353BA"
COR_CINZA = "#617382"

figura = plt.figure(
    figsize=(24, 18),
    facecolor=COR_FUNDO,
)

grade = GridSpec(
    5,
    3,
    figure=figura,
    height_ratios=[0.55, 0.8, 2.35, 2.35, 2.35],
    hspace=0.60,
    wspace=0.32,
)

# ============================================================
# 8. FUNCOES VISUAIS AUXILIARES
# ============================================================

def estilizar_eixo(eixo, titulo):
    eixo.set_facecolor("white")
    eixo.set_title(
        titulo,
        loc="left",
        fontsize=15,
        fontweight="bold",
        color=COR_NAVY,
        pad=12,
    )
    eixo.spines[["top", "right", "left", "bottom"]].set_visible(False)
    eixo.grid(axis="y", alpha=0.22)
    eixo.grid(axis="x", alpha=0.12)


def adicionar_rotulos_barras(
    eixo,
    horizontal=False,
    formato="{:.0f}",
):
    for barra in eixo.patches:
        if horizontal:
            deslocamento = max(eixo.get_xlim()[1] * 0.01, 1)
            eixo.text(
                barra.get_width() + deslocamento,
                barra.get_y() + barra.get_height() / 2,
                formato.format(barra.get_width()),
                va="center",
                fontsize=9,
                color=COR_NAVY,
            )
        else:
            deslocamento = max(eixo.get_ylim()[1] * 0.015, 1)
            eixo.text(
                barra.get_x() + barra.get_width() / 2,
                barra.get_height() + deslocamento,
                formato.format(barra.get_height()),
                ha="center",
                fontsize=9,
                color=COR_NAVY,
            )

# ============================================================
# 9. CABECALHO
# ============================================================

ax_cabecalho = figura.add_subplot(grade[0, :])
ax_cabecalho.axis("off")

ax_cabecalho.text(
    0.01,
    0.72,
    "CYBER EXPOSURE | DASHBOARD EXECUTIVO",
    fontsize=28,
    fontweight="bold",
    color=COR_NAVY,
    va="center",
)

ax_cabecalho.text(
    0.01,
    0.20,
    "Visão consolidada de vulnerabilidades e priorização de ativos"
    "  •  Data de referência: 05/10/2026",
    fontsize=13,
    color=COR_CINZA,
)

# ============================================================
# 10. CARTOES DE KPI
# ============================================================

cartoes = [
    (
        "EXPOSIÇÃO ATIVA",
        f"{kpi_exposicao_ativa:,}".replace(",", "."),
        "Aberta + em tratamento",
        COR_VERMELHO,
    ),
    (
        "CRÍTICAS ATIVAS",
        f"{kpi_criticas_ativas:,}".replace(",", "."),
        "Severidade normalizada",
        COR_LARANJA,
    ),
    (
        "ATIVOS IMPACTADOS",
        f"{kpi_ativos_impactados:,}".replace(",", "."),
        "Ativos cadastrados",
        COR_AZUL,
    ),
    (
        "BACKLOG > 90 DIAS",
        f"{kpi_backlog_90:.1f}%".replace(".", ","),
        "Datas válidas",
        COR_ROXO,
    ),
    (
        "MTTR MÉDIO",
        f"{kpi_mttr:.1f} dias".replace(".", ","),
        "Registros corrigidos válidos",
        COR_VERDE,
    ),
]

subgrade_kpis = grade[1, :].subgridspec(
    1,
    5,
    wspace=0.15,
)

for indice, (titulo, valor, subtitulo, cor) in enumerate(cartoes):
    eixo = figura.add_subplot(subgrade_kpis[0, indice])
    eixo.axis("off")

    caixa = FancyBboxPatch(
        (0.01, 0.05),
        0.98,
        0.90,
        boxstyle="round,pad=0.02,rounding_size=0.04",
        fc="white",
        ec="#DCE4EC",
        lw=1.2,
    )
    eixo.add_patch(caixa)

    faixa = FancyBboxPatch(
        (0.01, 0.05),
        0.025,
        0.90,
        boxstyle="round,pad=0.00,rounding_size=0.02",
        fc=cor,
        ec=cor,
    )
    eixo.add_patch(faixa)

    eixo.text(
        0.08,
        0.75,
        titulo,
        fontsize=11,
        fontweight="bold",
        color=COR_CINZA,
        va="center",
    )
    eixo.text(
        0.08,
        0.43,
        valor,
        fontsize=24,
        fontweight="bold",
        color=COR_NAVY,
        va="center",
    )
    eixo.text(
        0.08,
        0.18,
        subtitulo,
        fontsize=9.5,
        color=COR_CINZA,
        va="center",
    )

# ============================================================
# 11. GRAFICO 1: VULNERABILIDADES POR STATUS
# ============================================================

ax_status = figura.add_subplot(grade[2, 0])
estilizar_eixo(ax_status, "1. Vulnerabilidades por status")

ordem_status = [
    "Aberta",
    "Em tratamento",
    "Aceita",
    "Corrigida",
]

quantidade_status = (
    base["status"]
    .value_counts()
    .reindex(ordem_status, fill_value=0)
)

ax_status.bar(
    quantidade_status.index,
    quantidade_status.values,
    color=[COR_VERMELHO, COR_LARANJA, COR_CINZA, COR_VERDE],
)
ax_status.tick_params(axis="x", rotation=25)
ax_status.set_ylabel("Registros")
adicionar_rotulos_barras(ax_status)

# ============================================================
# 12. GRAFICO 2: EXPOSICAO ATIVA POR SEVERIDADE
# ============================================================

ax_severidade = figura.add_subplot(grade[2, 1])
estilizar_eixo(
    ax_severidade,
    "2. Exposição ativa por severidade",
)

ordem_severidade = [
    "Crítica",
    "Alta",
    "Média",
    "Baixa",
    "N/A",
]

severidade_status = pd.crosstab(
    exposicao_ativa["sev_norm"],
    exposicao_ativa["status"],
).reindex(
    ordem_severidade,
    fill_value=0,
).reindex(
    columns=["Aberta", "Em tratamento"],
    fill_value=0,
)

base_empilhamento = np.zeros(len(severidade_status))

for status, cor in [
    ("Aberta", COR_VERMELHO),
    ("Em tratamento", COR_LARANJA),
]:
    ax_severidade.bar(
        severidade_status.index,
        severidade_status[status],
        bottom=base_empilhamento,
        label=status,
        color=cor,
    )
    base_empilhamento += severidade_status[status].to_numpy()

ax_severidade.legend(
    frameon=False,
    ncol=2,
    loc="upper right",
)
ax_severidade.tick_params(axis="x", rotation=25)
ax_severidade.set_ylabel("Registros")

# ============================================================
# 13. GRAFICO 3: EXPOSICAO ATIVA POR AMBIENTE
# ============================================================

ax_ambiente = figura.add_subplot(grade[2, 2])
estilizar_eixo(
    ax_ambiente,
    "3. Exposição ativa por ambiente",
)

quantidade_ambiente = (
    exposicao_ativa["ambiente"]
    .fillna("Não informado")
    .value_counts()
    .sort_values()
)

ax_ambiente.barh(
    quantidade_ambiente.index,
    quantidade_ambiente.values,
    color=COR_TEAL,
)
ax_ambiente.set_xlabel("Vulnerabilidades ativas")
adicionar_rotulos_barras(ax_ambiente, horizontal=True)

# ============================================================
# 14. GRAFICO 4: TOP 10 ATIVOS POR RISCO ATIVO
# ============================================================

ax_top_geral = figura.add_subplot(grade[3, 0])
estilizar_eixo(
    ax_top_geral,
    "4. Top 10 ativos por risco ativo",
)

top_10_geral = (
    exposicao_ativa
    .groupby("ativo_id")["risk_score"]
    .sum()
    .nlargest(10)
    .sort_values()
)

ax_top_geral.barh(
    top_10_geral.index,
    top_10_geral.values,
    color=COR_VERMELHO,
)
ax_top_geral.set_xlabel("Risk score acumulado")
adicionar_rotulos_barras(
    ax_top_geral,
    horizontal=True,
    formato="{:.1f}",
)

# ============================================================
# 15. GRAFICO 5: HEATMAP CRITICIDADE X CVSS
# ============================================================

ax_heatmap = figura.add_subplot(grade[3, 1])
estilizar_eixo(
    ax_heatmap,
    "5. Criticidade do ativo × faixa CVSS",
)

exposicao_ativa["cvss_faixa"] = pd.cut(
    pd.to_numeric(
        exposicao_ativa["cvss_score"],
        errors="coerce",
    ),
    bins=[-0.01, 3.9, 6.9, 8.9, 10],
    labels=["Baixo", "Médio", "Alto", "Crítico"],
)

matriz_risco = pd.crosstab(
    exposicao_ativa["criticidade_norm"],
    exposicao_ativa["cvss_faixa"],
).reindex(
    ["Crítica", "Alta", "Média", "Baixa", "N/A"],
    fill_value=0,
)

sns.heatmap(
    matriz_risco,
    annot=True,
    fmt="g",
    cmap="Reds",
    cbar=False,
    ax=ax_heatmap,
    linewidths=0.5,
    linecolor="white",
)
ax_heatmap.set_xlabel("CVSS")
ax_heatmap.set_ylabel("Criticidade do ativo")

# ============================================================
# 16. GRAFICO 6: AGING DA EXPOSICAO ATIVA
# ============================================================

ax_aging = figura.add_subplot(grade[3, 2])
estilizar_eixo(
    ax_aging,
    "6. Aging da exposição ativa",
)

faixa_aging = pd.cut(
    aging_dias,
    bins=[-1, 30, 60, 90, 10000],
    labels=["0–30", "31–60", "61–90", ">90"],
)

quantidade_aging = faixa_aging.value_counts().reindex(
    ["0–30", "31–60", "61–90", ">90"],
    fill_value=0,
)

ax_aging.bar(
    quantidade_aging.index,
    quantidade_aging.values,
    color=[COR_VERDE, COR_AZUL, COR_LARANJA, COR_VERMELHO],
)
ax_aging.set_ylabel("Vulnerabilidades")
adicionar_rotulos_barras(ax_aging)

# ============================================================
# 17. GRAFICO 7: MTTR MEDIO POR SEVERIDADE
# ============================================================

ax_mttr = figura.add_subplot(grade[4, 0])
estilizar_eixo(
    ax_mttr,
    "7. MTTR médio por severidade",
)

mttr_severidade = (
    corrigidas
    .groupby("sev_norm")["mttr"]
    .mean()
    .reindex(ordem_severidade)
    .dropna()
)

ax_mttr.bar(
    mttr_severidade.index,
    mttr_severidade.values,
    color=COR_ROXO,
)
ax_mttr.set_ylabel("Dias")
ax_mttr.tick_params(axis="x", rotation=25)
adicionar_rotulos_barras(
    ax_mttr,
    formato="{:.1f}",
)

# ============================================================
# 18. GRAFICO 8: NOVAS X CORRIGIDAS POR MES
# ============================================================

ax_tendencia = figura.add_subplot(grade[4, 1])
estilizar_eixo(
    ax_tendencia,
    "8. Novas × corrigidas por mês",
)

# Jan-set/2026 para evitar meses incompletos posteriores a referencia.
meses = pd.period_range(
    "2026-01",
    "2026-09",
    freq="M",
)

novas_por_mes = (
    base[
        base["abertura"].between(
            "2026-01-01",
            DATA_REFERENCIA,
        )
    ]
    .groupby(base["abertura"].dt.to_period("M"))
    .size()
    .reindex(meses, fill_value=0)
)

corrigidas_por_mes = (
    corrigidas[
        corrigidas["correcao"].between(
            "2026-01-01",
            DATA_REFERENCIA,
        )
    ]
    .groupby(corrigidas["correcao"].dt.to_period("M"))
    .size()
    .reindex(meses, fill_value=0)
)

posicoes_x = np.arange(len(meses))
rotulos_meses = [mes.strftime("%b") for mes in meses]

ax_tendencia.plot(
    posicoes_x,
    novas_por_mes.values,
    marker="o",
    linewidth=2.5,
    color=COR_AZUL,
    label="Novas",
)

ax_tendencia.plot(
    posicoes_x,
    corrigidas_por_mes.values,
    marker="o",
    linewidth=2.5,
    color=COR_VERDE,
    label="Corrigidas",
)

ax_tendencia.fill_between(
    posicoes_x,
    novas_por_mes.values,
    corrigidas_por_mes.values,
    where=novas_por_mes.values >= corrigidas_por_mes.values,
    color=COR_VERMELHO,
    alpha=0.08,
)

ax_tendencia.set_xticks(
    posicoes_x,
    rotulos_meses,
)
ax_tendencia.set_ylabel("Registros")
ax_tendencia.legend(
    frameon=False,
    ncol=2,
)

# ============================================================
# 19. GRAFICO 9: TOP 10 ATIVOS DE PRODUCAO
# ============================================================

ax_top_producao = figura.add_subplot(grade[4, 2])
estilizar_eixo(
    ax_top_producao,
    "9. Top 10 ativos de produção",
)

exposicao_producao = exposicao_ativa[
    exposicao_ativa["ambiente"] == "Produção"
].copy()

top_10_producao = (
    exposicao_producao
    .groupby("ativo_id")["risk_score"]
    .sum()
    .nlargest(10)
    .sort_values()
)

ax_top_producao.barh(
    top_10_producao.index,
    top_10_producao.values,
    color=COR_VERDE,
)
ax_top_producao.set_xlabel("Risk score acumulado")
adicionar_rotulos_barras(
    ax_top_producao,
    horizontal=True,
    formato="{:.1f}",
)

# ============================================================
# 20. RODAPE E EXPORTACAO
# ============================================================

figura.text(
    0.012,
    0.012,
    "Premissas: exposição ativa = Aberta + Em tratamento. "
    "Risk score = CVSS + peso da severidade + peso da "
    "criticidade do ativo + bônus de Produção. "
    "Datas inválidas são excluídas apenas de métricas temporais.",
    fontsize=10,
    color=COR_CINZA,
)

plt.savefig(
    ARQUIVO_SAIDA,
    dpi=180,
    bbox_inches="tight",
    facecolor=COR_FUNDO,
)

plt.show()
