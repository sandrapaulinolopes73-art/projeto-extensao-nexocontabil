from pathlib import Path
import json
import pandas as pd

BASE = Path(__file__).resolve().parents[1]

ARQUIVO_ENTRADA = BASE / "dados" / "cobrancas_originais.xlsx"
ARQUIVO_SAIDA = BASE / "dados" / "cobrancas_tratadas_powerbi.csv"
ARQUIVO_METRICAS = BASE / "RESUMO_METRICAS_POWERBI.json"

BAIRROS_ZONAS = {
    "Bangu": "Zona Oeste",
    "Campo Grande": "Zona Oeste",
    "Realengo": "Zona Oeste",
    "Santa Cruz": "Zona Oeste",
    "Barra da Tijuca": "Zona Sudoeste",
    "Recreio": "Zona Sudoeste",
    "Jacarepaguá": "Zona Sudoeste",
    "Vila Valqueire": "Zona Sudoeste",
    "Bento Ribeiro": "Zona Norte 1",
    "Campinho": "Zona Norte 1",
    "Marechal Hermes": "Zona Norte 1",
    "Osvaldo Cruz": "Zona Norte 1",
    "Grajaú": "Zona Norte 2",
    "Maracanã": "Zona Norte 2",
    "Tijuca": "Zona Norte 2",
    "Vila Isabel": "Zona Norte 2",
}


def converter_valor(valor):
    if pd.isna(valor):
        return float("nan")

    valor = str(valor).strip()

    if "," in valor:
        valor = valor.replace(".", "").replace(",", ".")

    return pd.to_numeric(valor, errors="coerce")


def tratar_cobrancas():
    df = pd.read_excel(ARQUIVO_ENTRADA)

    df.columns = df.columns.str.strip()

    df["Bairro"] = df["Bairro"].astype("string").str.strip()
    df["zona"] = df["Bairro"].map(BAIRROS_ZONAS)

    if df["zona"].isna().any():
        bairros = df.loc[df["zona"].isna(), "Bairro"].unique()
        raise ValueError(f"Bairros sem zona cadastrada: {bairros}")

    df["valor_cobrado"] = df["valor_cobrado"].apply(converter_valor)

    df["data_vencimento"] = pd.to_datetime(
        df["data_vencimento"], errors="coerce", dayfirst=True
    )

    df["data_pagamento"] = pd.to_datetime(
        df["data_pagamento"], errors="coerce", dayfirst=True
    )

    df["competencia_data"] = pd.to_datetime(
        df["competencia"].astype(str) + "-01", errors="coerce"
    )

    df["status"] = df["status"].fillna("Não informado").astype(str).str.strip()

    if df["id_cobranca"].isna().any():
        raise ValueError("Existem cobranças sem identificador.")

    if df["id_cobranca"].duplicated().any():
        raise ValueError("Existem identificadores duplicados.")

    if df["valor_cobrado"].isna().any():
        raise ValueError("Existem valores inválidos ou vazios.")

    df.to_csv(ARQUIVO_SAIDA, index=False, encoding="utf-8-sig", date_format="%Y-%m-%d")

    total = len(df)
    vencidas = df[df["status"] == "Vencido"]
    pagas = df[df["status"] == "Pago"]
    pendentes = df[df["status"] == "Pendente"]
    nao_informadas = df[df["status"] == "Não informado"]

    total_classificado = len(pagas) + len(vencidas) + len(pendentes)

    metricas = {
        "total_cobrancas": total,
        "cobrancas_pagas": len(pagas),
        "cobrancas_vencidas": len(vencidas),
        "cobrancas_pendentes": len(pendentes),
        "cobrancas_sem_status": len(nao_informadas),
        "taxa_vencidas_sobre_total_pct": (
            round(len(vencidas) / total * 100, 2) if total else 0
        ),
        "taxa_vencidas_sobre_classificadas_pct": (
            round(len(vencidas) / total_classificado * 100, 2)
            if total_classificado
            else 0
        ),
        "valor_total_vencido": round(vencidas["valor_cobrado"].sum(), 2),
        "valor_total_pendente": round(pendentes["valor_cobrado"].sum(), 2),
        "valor_total_pago": round(pagas["valor_cobrado"].sum(), 2),
    }

    with open(ARQUIVO_METRICAS, "w", encoding="utf-8") as arquivo:
        json.dump(metricas, arquivo, ensure_ascii=False, indent=4)

    print("TRATAMENTO CONCLUÍDO!")
    print(f"Registros tratados: {total}")
    print(f"Arquivo CSV: {ARQUIVO_SAIDA}")
    print(f"Arquivo de indicadores: {ARQUIVO_METRICAS}")
    print("\nINDICADORES:")

    for nome, valor in metricas.items():
        print(f"{nome}: {valor}")


if __name__ == "__main__":
    tratar_cobrancas()
