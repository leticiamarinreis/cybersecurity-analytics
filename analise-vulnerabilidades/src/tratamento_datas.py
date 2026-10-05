import pandas as pd


def tratar_datas(vuln):
    """Converte datas (formato DD/MM/AAAA); valores inválidos viram NaT."""
    vuln = vuln.copy()
    vuln["abertura_dt"] = pd.to_datetime(
        vuln["data_abertura"], errors="coerce", dayfirst=True
    )
    vuln["correcao_dt"] = pd.to_datetime(
        vuln["data_correcao"], errors="coerce", dayfirst=True
    )
    return vuln
