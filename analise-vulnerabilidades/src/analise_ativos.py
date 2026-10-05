from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DIR_SAIDA = RAIZ / "outputs"


def analisar_ativos(base):
    """Ranking de ativos com vulnerabilidades expostas e exportação dos CSVs."""
    DIR_SAIDA.mkdir(exist_ok=True)

    top = (
        base[base["status_exposto"] & base["asset_join_ok"]]
        .groupby(["ativo_id", "sistema", "crit_norm", "amb_norm", "status_ativo"])
        .agg(
            vulnerabilidades=("vuln_id", "count"),
            criticas=("sev_norm", lambda x: (x == "Crítica").sum()),
            altas=("sev_norm", lambda x: (x == "Alta").sum()),
            score=("priority_score", "sum"),
        )
        .sort_values(["criticas", "score", "vulnerabilidades"], ascending=False)
    )

    print("\n=== Top 15 ativos expostos ===")
    print(top.head(15).to_string())

    # Saídas
    ordem = ["P1", "P2", "P3", "Sem classificação"]
    priorizadas = base.drop(columns=["_merge"]).copy()
    priorizadas["_ordem"] = priorizadas["prioridade"].map({p: i for i, p in enumerate(ordem)})
    priorizadas = priorizadas.sort_values(
        ["_ordem", "priority_score"], ascending=[True, False]
    ).drop(columns="_ordem")

    priorizadas.to_csv(
        DIR_SAIDA / "vulnerabilidades_priorizadas.csv",
        sep=";", index=False, encoding="utf-8-sig",
    )
    top.reset_index().to_csv(
        DIR_SAIDA / "ativos_expostos.csv",
        sep=";", index=False, encoding="utf-8-sig",
    )
    print(f"\nArquivos gerados em: {DIR_SAIDA}")

    return top
