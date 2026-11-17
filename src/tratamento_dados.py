from pathlib import Path
import pandas as pd

BASE = Path(__file__).resolve().parents[1]
ARQUIVO_ENTRADA = BASE / "dados" / "lancamentos_condominiais_simulados.csv"
ARQUIVO_SAIDA = BASE / "dados" / "lancamentos_tratados.csv"

def tratar_dados(caminho=ARQUIVO_ENTRADA):
    df = pd.read_csv(caminho)
    # Padronização de texto e categorias
    df["condominio"] = df["condominio"].astype(str).str.strip()
    df["status_pagamento"] = df["status_pagamento"].astype(str).str.strip().str.capitalize()
    # Conversão segura de campos numéricos
    df["valor_boleto_reais"] = pd.to_numeric(df["valor_boleto_reais"], errors="coerce")
    df["dias_atraso"] = pd.to_numeric(df["dias_atraso"], errors="coerce").fillna(0).astype(int)
    # Remove registros sem identificador e elimina duplicidade pelo ID
    df = df.dropna(subset=["id_lancamento"])
    df = df.drop_duplicates(subset=["id_lancamento"])
    # Preenche valor ausente com mediana, preservando a rastreabilidade da regra
    df["valor_boleto_reais"] = df["valor_boleto_reais"].fillna(df["valor_boleto_reais"].median()).round(2)
    # Mantém apenas categorias esperadas
    df = df[df["status_pagamento"].isin(["Pago", "Pendente", "Atrasado"])]
    df.to_csv(ARQUIVO_SAIDA, index=False, encoding="utf-8-sig")
    return df

if __name__ == "__main__":
    tratado = tratar_dados()
    print(f"Tratamento concluído: {len(tratado)} registros.")
    print(tratado.head())
