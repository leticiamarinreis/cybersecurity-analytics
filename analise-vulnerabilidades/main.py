from src.carregamento import carregar_dados
from src.padronizacao import padronizar_dados
from src.tratamento_datas import tratar_datas
from src.cruzamento import cruzar_dados
from src.priorizacao import calcular_score
from src.classificacao import classificar
from src.kpis import gerar_kpis
from src.validacao import validar_dados
from src.analise_ativos import analisar_ativos


def main():
    # 1. Carregamento
    ativos, vulnerabilidades = carregar_dados()

    # 2. Padronização
    ativos, vulnerabilidades = padronizar_dados(ativos, vulnerabilidades)

    # 3. Tratamento das datas
    vulnerabilidades = tratar_datas(vulnerabilidades)

    # 4. Cruzamento
    base = cruzar_dados(ativos, vulnerabilidades)

    # 5. Priorização
    base = calcular_score(base)

    # 6. Classificação
    base = classificar(base)

    # 7. KPIs
    gerar_kpis(base)

    # 8. Validação
    validar_dados(base)

    # 9. Análise dos ativos (também exporta os CSVs em outputs/)
    analisar_ativos(base)


if __name__ == "__main__":
    main()
