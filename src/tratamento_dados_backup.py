from pathlib import Path
import pandas as pd
import numpy as np
import json

BASE = Path(__file__).resolve().parents[1]
ARQUIVO_ENTRADA = BASE / "dados" / "lancamentos_condominiais_simulados_atualizado.csv"
ARQUIVO_SAIDA = BASE / "dados" / "lancamentos_tratados.csv"


def tratar_dados(caminho=ARQUIVO_ENTRADA):
    df = pd.read_csv(caminho)
    # Padronização de texto e categorias
    df["condominio"] = df["condominio"].astype(str).str.strip()
    df["status_pagamento"] = (
        df["status_pagamento"].astype(str).str.strip().str.capitalize()
    )
    # Conversão segura de campos numéricos
    df["valor_boleto_reais"] = pd.to_numeric(df["valor_boleto_reais"], errors="coerce")
    df["dias_atraso"] = (
        pd.to_numeric(df["dias_atraso"], errors="coerce").fillna(0).astype(int)
    )
    # Remove registros sem identificador e elimina duplicidade pelo ID
    df = df.dropna(subset=["id_lancamento"])
    df = df.drop_duplicates(subset=["id_lancamento"])
    # Preenche valor ausente com mediana, preservando a rastreabilidade da regra
    df["valor_boleto_reais"] = (
        df["valor_boleto_reais"].fillna(df["valor_boleto_reais"].median()).round(2)
    )
    # Mantém apenas categorias esperadas
    df = df[df["status_pagamento"].isin(["Pago", "Pendente", "Atrasado"])]
    df.to_csv(ARQUIVO_SAIDA, index=False, encoding="utf-8-sig")
    return df


def gerar_projecao(df):
    # Considera somente os lançamentos atrasados
    atrasados = df[df["status_pagamento"] == "Atrasado"].copy()

    # Converte a referência para data
    atrasados["mes_referencia"] = pd.to_datetime(
        atrasados["mes_referencia"], format="%Y-%m"
    )

    # Soma os valores atrasados por mês
    historico = atrasados.groupby("mes_referencia")["valor_boleto_reais"].sum()

    # Completa os meses sem atrasos com valor zero
    meses = pd.date_range(historico.index.min(), historico.index.max(), freq="MS")

    historico = historico.reindex(meses, fill_value=0)

    # Calcula a tendência linear
    x = np.arange(len(historico))
    y = historico.values

    coeficientes = np.polyfit(x, y, 1)

    # Projeta os próximos seis meses
    x_futuro = np.arange(len(historico), len(historico) + 6)
    valores_futuros = np.polyval(coeficientes, x_futuro)

    # Evita valores negativos na projeção
    valores_futuros = np.maximum(valores_futuros, 0)

    meses_futuros = pd.date_range(
        historico.index.max() + pd.offsets.MonthBegin(1), periods=6, freq="MS"
    )

    projecao = pd.DataFrame(
        {
            "mes_referencia": meses_futuros.strftime("%Y-%m"),
            "valor_projetado_reais": valores_futuros.round(2),
        }
    )
    projecao["tipo"] = "Projeção"
    # GERAR DADOS DO GRÁFICO MENSAL
    grafico_mensal = (
        df.groupby("mes_referencia")["valor_boleto_reais"].sum().reset_index()
    )

    grafico_mensal = grafico_mensal.sort_values("mes_referencia")

    arquivo_grafico = BASE / "dashboard" / "grafico_mensal.js"

    dados_mensais_js = json.dumps(
        grafico_mensal.to_dict(orient="records"), ensure_ascii=False
    )

    arquivo_grafico.write_text(
        f"window.dadosMensais = {dados_mensais_js};", encoding="utf-8"
    )
    historico_df = pd.DataFrame(
        {
            "mes_referencia": historico.index.strftime("%Y-%m"),
            "valor_projetado_reais": historico.values.round(2),
            "tipo": "Histórico",
        }
    )

    dados_grafico = pd.concat([historico_df, projecao], ignore_index=True)

    arquivo = BASE / "dados" / "projecao_inadimplencia.csv"

    dados_grafico.to_csv(arquivo, index=False, encoding="utf-8-sig")

    arquivo_js = BASE / "dashboard" / "projecao_dados.js"

    dados_js = json.dumps(dados_grafico.to_dict(orient="records"), ensure_ascii=False)

    arquivo_js.write_text(f"window.dadosProjecao = {dados_js};", encoding="utf-8")

    print("Projeção dos próximos seis meses gerada!")
    print(projecao)


if __name__ == "__main__":
    tratado = tratar_dados()
    gerar_projecao(tratado)
    print(f"Tratamento concluído: {len(tratado)} registros.")
    print(tratado.head())


import pandas as pd

# Caminho da planilha original
arquivo = "dados/cobrancas_originais.xlsx"

# Ler a planilha
df = pd.read_excel(arquivo)

# Mostrar informações da base
print("\nCONFERÊNCIA DA PLANILHA")
print("Quantidade de registros:", len(df))
print("Quantidade de colunas:", len(df.columns))

print("\nNomes das colunas:")
print(df.columns.tolist())

print("\nPrimeiras cinco linhas:")
print(df.head())
