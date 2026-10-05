import pandas as pd


def tier(row):
    """Classifica a vulnerabilidade em P1, P2, P3 ou Sem classificação."""
    s, c = row["sev_norm"], row["crit_norm"]

    if pd.isna(s) or pd.isna(c):
        return "Sem classificação"

    # P1: vulnerabilidade crítica em ativo crítico ou de alta criticidade.
    if s == "Crítica" and c in ["Crítica", "Alta"]:
        return "P1"

    # P2: alta relevância, abaixo do critério de P1.
    if (
        (s in ["Crítica", "Alta"] and c == "Média")
        or (s == "Alta" and c == "Crítica")
        or (s == "Crítica" and c == "Baixa")
    ):
        return "P2"

    return "P3"


def classificar(base):
    base = base.copy()
    base["prioridade"] = base.apply(tier, axis=1)
    return base
