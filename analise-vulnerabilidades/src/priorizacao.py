# Quanto maior o número, maior a prioridade.
PRIORITY = {"Baixa": 1, "Média": 2, "Alta": 3, "Crítica": 4}


def calcular_score(base):
    """Score = criticidade do ativo x severidade da vulnerabilidade (máx. 16)."""
    base = base.copy()
    base["priority_score"] = (
        base["crit_norm"].map(PRIORITY).fillna(0)
        * base["sev_norm"].map(PRIORITY).fillna(0)
    ).astype(int)
    return base
