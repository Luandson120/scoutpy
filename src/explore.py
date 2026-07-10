import pandas as pd
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent  # sobe de src/ pra raiz do projeto

arquivos = [
    "players",
    "appearances",
    "competitions",
    "games",
    "player_valuations",
    "clubs",
]

for nome in arquivos:
    caminho = RAIZ / "dados" / "raw" / f"{nome}.csv"
    df = pd.read_csv(caminho, nrows=5)
    print(f"\n{'='*60}")
    print(f"ARQUIVO: {nome}.csv")
    print(f"{'='*60}")
    print(f"Colunas ({len(df.columns)}):")
    print(list(df.columns))
    print("\nPrimeiras linhas:")
    print(df.head(3).to_string())