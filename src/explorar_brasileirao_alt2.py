import pandas as pd
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
df = pd.read_csv(RAIZ / "dados" / "raw" / "brasileirao_alt2" / "brasileirao_serie_a_2018_2023_v3.csv", nrows=10)

print(f"Colunas ({len(df.columns)}):")
print(list(df.columns))
print("\nPrimeiras linhas:")
print(df.head(10).to_string())