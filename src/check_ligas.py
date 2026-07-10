import pandas as pd
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
competitions = pd.read_csv(RAIZ / "dados" / "raw" / "competitions.csv")

domesticas = competitions[competitions["type"] == "domestic_league"]

# Procurando pelas ligas de interesse pelo nome/país
ligas_alvo = ["England", "Spain", "Germany", "Italy", "France", "Brazil"]
filtro = domesticas[domesticas["country_name"].isin(ligas_alvo)]

print(filtro[["competition_id", "name", "country_name", "domestic_league_code", "confederation"]].to_string())