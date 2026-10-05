from pathlib import Path

import pandas as pd

# Raiz do projeto (pasta acima de src/)
RAIZ = Path(__file__).resolve().parent.parent
DIR_DADOS = RAIZ / "data"

ATIVOS = DIR_DADOS / "ativos.csv"
VULN = DIR_DADOS / "vulnerabilidades.csv"


def carregar_dados():
    """Lê as bases de ativos e vulnerabilidades (CSV separado por ';')."""
    ativos = pd.read_csv(ATIVOS, sep=";")
    vuln = pd.read_csv(VULN, sep=";")
    return ativos, vuln
