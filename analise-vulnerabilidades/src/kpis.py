def gerar_kpis(base):
    """Imprime os principais indicadores da base."""
    print("\n=== KPIs ===")
    print("Total:", len(base))
    print("Expostas (Aberta + Em tratamento):", int(base["status_exposto"].sum()))
    print("Aceitas:", int((base["status"] == "Aceita").sum()))
    print("Corrigidas:", int((base["status"] == "Corrigida").sum()))
    print(
        "P1 expostas:",
        int(((base["prioridade"] == "P1") & base["status_exposto"]).sum()),
    )
