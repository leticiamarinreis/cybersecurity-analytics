def validar_dados(base):
    """Checagens básicas de qualidade da base cruzada."""
    print("\n=== Validação ===")
    print(
        "Vulnerabilidades sem ativo correspondente:",
        int((~base["asset_join_ok"]).sum()),
    )
    print("Severidade não padronizada:", int(base["sev_norm"].isna().sum()))
    print("Criticidade não padronizada:", int(base["crit_norm"].isna().sum()))
    print("Datas de abertura inválidas:", int(base["abertura_dt"].isna().sum()))
