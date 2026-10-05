# Dicionário para padronizar a criticidade dos ativos.
CRIT_MAP = {
    "Baixa": "Baixa",
    "BaixA": "Baixa",
    "baixa": "Baixa",
    "Média": "Média",
    "Media": "Média",
    "media": "Média",
    "Alta": "Alta",
    "Crítica": "Crítica",
    "Critica": "Crítica",
    "critica": "Crítica",
    "": "Indefinida",
}

# Dicionário para padronizar a severidade das vulnerabilidades.
SEV_MAP = {
    "Baixa": "Baixa",
    "baixa": "Baixa",
    "BaixA": "Baixa",
    "Média": "Média",
    "Media": "Média",
    "media": "Média",
    "Alta": "Alta",
    "ALTA": "Alta",
    "Alto": "Alta",
    "Crítica": "Crítica",
    "Critica": "Crítica",
    "critica": "Crítica",
}

# Dicionário para padronizar a origem da vulnerabilidade.
ORIGIN_MAP = {
    "Cloud Security": "Cloud Security",
    "CloudSecurity": "Cloud Security",
    "Cloud-Security": "Cloud Security",
}


def padronizar_dados(ativos, vuln):
    """Cria colunas normalizadas (crit_norm, amb_norm, sev_norm, orig_norm)."""
    ativos = ativos.copy()
    vuln = vuln.copy()

    # Remove espaços nas pontas (um valor " " vira "" e cai em "Indefinida").
    # Valores realmente nulos continuam NaN.
    crit = ativos["criticidade"].astype("object").str.strip()
    ativos["crit_norm"] = crit.map(CRIT_MAP)

    ativos["amb_norm"] = ativos["ambiente"].fillna("Indefinido")

    sev = vuln["severidade"].astype("object").str.strip()
    vuln["sev_norm"] = sev.map(SEV_MAP)

    # Se a origem não estiver no dicionário, mantém o valor original.
    vuln["orig_norm"] = vuln["origem"].map(ORIGIN_MAP).fillna(vuln["origem"])

    return ativos, vuln
