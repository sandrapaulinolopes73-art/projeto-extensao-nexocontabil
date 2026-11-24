from pathlib import Path
import pandas as pd
import numpy as np

BASE = Path(__file__).resolve().parents[1]

arquivo_original = BASE / "dados" / "lancamentos_condominiais_simulados.csv"
arquivo_saida = BASE / "dados" / "lancamentos_2026_simulados.csv"

# Lê os dados originais de 2025
df_2025 = pd.read_csv(arquivo_original)

# Gerador de dados reproduzíveis
np.random.seed(42)

# Mesmos condomínios e tipos existentes
condominios = df_2025[["condominio", "tipo_condominio"]].drop_duplicates()

# Cria 250 registros para 2026
novos_dados = []

for i in range(250):
    condominio = condominios.iloc[i % len(condominios)]

    mes = np.random.randint(1, 13)
    valor = round(np.random.uniform(300, 1800), 2)

    status = np.random.choice(["Pago", "Pendente", "Atrasado"], p=[0.68, 0.18, 0.14])

    dias_atraso = np.random.randint(1, 61) if status == "Atrasado" else 0

    novos_dados.append(
        {
            "id_lancamento": 251 + i,
            "mes_referencia": f"2026-{mes:02d}",
            "condominio": condominio["condominio"],
            "tipo_condominio": condominio["tipo_condominio"],
            "valor_boleto_reais": valor,
            "status_pagamento": status,
            "dias_atraso": dias_atraso,
        }
    )

df_2026 = pd.DataFrame(novos_dados)

# Salva os novos dados separadamente
df_2026.to_csv(arquivo_saida, index=False, encoding="utf-8-sig")

print("Dados simulados de 2026 gerados!")
print(f"Total de registros: {len(df_2026)}")
print(df_2026.head())

# Junta os dados originais de 2025 com os novos dados de 2026
df_completo = pd.concat([df_2025, df_2026], ignore_index=True)

# Salva a base atualizada em um novo arquivo
arquivo_completo = BASE / "dados" / "lancamentos_condominiais_simulados_atualizado.csv"

df_completo.to_csv(arquivo_completo, index=False, encoding="utf-8-sig")

print("Base atualizada com sucesso!")
print(f"Total de registros: {len(df_completo)}")
