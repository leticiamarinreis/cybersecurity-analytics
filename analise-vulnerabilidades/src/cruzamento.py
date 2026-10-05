COLUNAS_ATIVOS = [
    "ativo_id",
    "sistema",
    "crit_norm",
    "dominio",
    "amb_norm",
    "localidade",
    "status_ativo",
]


def cruzar_dados(ativos, vuln):
    """Left join das vulnerabilidades com os ativos pelo ativo_id."""
    base = vuln.merge(
        ativos[COLUNAS_ATIVOS],
        on="ativo_id",
        how="left",
        indicator=True,
    )

    # Expostas = ainda não corrigidas.
    base["status_exposto"] = base["status"].isin(["Aberta", "Em tratamento"])

    # Indica se a vulnerabilidade encontrou um ativo correspondente.
    base["asset_join_ok"] = base["_merge"] == "both"

    return base
