import pandas as pd


def gerar_dados_obras() -> pd.DataFrame:
    """Gera dados fictícios de 8 obras de pavimentação urbana com rotas e escopos."""
    dados = [
        {
            "id_obra": "OBR-001",
            "nome_obra": "Pavimentação Av. das Nações",
            "rota": "Trecho A ao B - Centro / Zona Sul",
            "orcamento_previsto": 450000.00,
            "custo_realizado": 395000.00,
            "area_m2": 12000,
        },
        {
            "id_obra": "OBR-002",
            "nome_obra": "Recapeamento Rua das Flores",
            "rota": "Rua das Flores - Km 0 ao 3.5",
            "orcamento_previsto": 180000.00,
            "custo_realizado": 215000.00,
            "area_m2": 5500,
        },
        {
            "id_obra": "OBR-003",
            "nome_obra": "Pavimentação Rota Industrial",
            "rota": "Distrito Industrial - Via Acesso Norte",
            "orcamento_previsto": 820000.00,
            "custo_realizado": 740000.00,
            "area_m2": 22000,
        },
        {
            "id_obra": "OBR-004",
            "nome_obra": "Asfaltamento Bairro Primavera",
            "rota": "Anel Viário Leste - Trecho Urbano",
            "orcamento_previsto": 310000.00,
            "custo_realizado": 368000.00,
            "area_m2": 8900,
        },
        {
            "id_obra": "OBR-005",
            "nome_obra": "Pavimentação Av. Beira-Mar",
            "rota": "Av. Beira-Mar - Orla Sul ao Centro",
            "orcamento_previsto": 950000.00,
            "custo_realizado": 880000.00,
            "area_m2": 26000,
        },
        {
            "id_obra": "OBR-006",
            "nome_obra": "Recapeamento Alameda dos Pinheiros",
            "rota": "Al. dos Pinheiros - Bloco 1 ao 4",
            "orcamento_previsto": 140000.00,
            "custo_realizado": 162000.00,
            "area_m2": 4100,
        },
        {
            "id_obra": "OBR-007",
            "nome_obra": "Pavimentação Rota Logística Oeste",
            "rota": "Marginal R-12 - Acesso à Rodovia",
            "orcamento_previsto": 600000.00,
            "custo_realizado": 510000.00,
            "area_m2": 17500,
        },
        {
            "id_obra": "OBR-008",
            "nome_obra": "Asfaltamento Conjunto Habitacional",
            "rota": "Ruas Internas CH-02 - Setor Norte",
            "orcamento_previsto": 270000.00,
            "custo_realizado": 298000.00,
            "area_m2": 7200,
        },
    ]
    return pd.DataFrame(dados)


def processar_resultados(df: pd.DataFrame) -> pd.DataFrame:
    """Calcula margens financeiras, status e indicadores de custo por m²."""
    df["resultado_financeiro"] = df["orcamento_previsto"] - df["custo_realizado"]
    df["margem_lucro_%"] = (
        df["resultado_financeiro"] / df["orcamento_previsto"]
    ) * 100
    df["status"] = df["resultado_financeiro"].apply(
        lambda x: "LUCRO" if x >= 0 else "PREJUÍZO"
    )
    df["custo_por_m2"] = df["custo_realizado"] / df["area_m2"]
    return df


def exibir_resumo(df: pd.DataFrame) -> None:
    """Exibe um painel executivo simplificado no terminal."""
    total_orcado = df["orcamento_previsto"].sum()
    total_gasto = df["custo_realizado"].sum()
    resultado = total_orcado - total_gasto

    print("=" * 65)
    print("       RELATÓRIO COMPARATIVO DE OBRAS - PAVIMENTAÇÃO URBANA")
    print("=" * 65)
    print(
        f"Obras Analisadas: {len(df)} | Lucro: {(df['status'] == 'LUCRO').sum()} | Prejuízo: {(df['status'] == 'PREJUÍZO').sum()}"
    )
    print(f"Orçamento Total:   R$ {total_orcado:,.2f}")
    print(f"Custo Realizado:   R$ {total_gasto:,.2f}")
    print(f"Resultado Geral:   R$ {resultado:,.2f}")
    print("=" * 65 + "\n")


def formatar_tabela(df: pd.DataFrame) -> pd.DataFrame:
    """Formata os valores numéricos em moeda para exibição limpa."""
    df_exibicao = df.copy()
    df_exibicao["Orçamento"] = df_exibicao["orcamento_previsto"].apply(
        lambda x: f"R$ {x:,.2f}"
    )
    df_exibicao["Custo Real"] = df_exibicao["custo_realizado"].apply(
        lambda x: f"R$ {x:,.2f}"
    )
    df_exibicao["Resultado"] = df_exibicao["resultado_financeiro"].apply(
        lambda x: f"R$ {x:,.2f}"
    )
    df_exibicao["Margem"] = df_exibicao["margem_lucro_%"].apply(
        lambda x: f"{x:.2f}%"
    )

    colunas = [
        "id_obra",
        "nome_obra",
        "rota",
        "Orçamento",
        "Custo Real",
        "Resultado",
        "Margem",
        "status",
    ]
    return df_exibicao[colunas]


def main():
    df_raw = gerar_dados_obras()
    df_processado = processar_resultados(df_raw)

    # Exibição do resumo executivo e da tabela detalhada
    exibir_resumo(df_processado)
    tabela = formatar_tabela(df_processado)
    print(tabela.to_string(index=False))

    # Exporta para CSV
    df_processado.to_csv("resultado_obras.csv", index=False)
    print("\n[✓] Relatório exportado: resultado_obras.csv")


if __name__ == "__main__":
    main()
