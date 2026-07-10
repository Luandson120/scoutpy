import pandas as pd
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
df = pd.read_csv(RAIZ / "dados" / "processed" / "premier_league.csv")

print(f"Formato: {df.shape}")
print(f"\nColunas ({len(df.columns)}):")
for col in df.columns:
    print(f"  {col}")

print("\nPrimeiras 3 linhas (colunas selecionadas):")
colunas_interesse = [c for c in df.columns if any(
    termo in c for termo in ["name", "posicao", "idade", "gols", "assist", "minut", "partid", "Tkl", "Int", "Crs", "SoT", "Sh"]
)]
print(df[colunas_interesse].head(3).to_string())