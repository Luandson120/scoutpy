import pandas as pd
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DADOS_RAW = RAIZ / "dados" / "raw"

# 1. Confirma quantos jogadores do Brasileirão existem em players.csv
players = pd.read_csv(DADOS_RAW / "players.csv")
brasileirao_players = players[players["current_club_domestic_competition_id"] == "BRA1"]
print(f"Jogadores com current_club_domestic_competition_id == BRA1: {len(brasileirao_players)}")

ids_brasileirao = set(brasileirao_players["player_id"])

# 2. Procura por esses player_ids no appearances.csv, e vê quais competition_id aparecem
competition_ids_encontrados = {}
linhas_com_esses_jogadores = 0

for chunk in pd.read_csv(DADOS_RAW / "appearances.csv", chunksize=200_000):
    filtrado = chunk[chunk["player_id"].isin(ids_brasileirao)]
    linhas_com_esses_jogadores += len(filtrado)
    for comp_id, count in filtrado["competition_id"].value_counts().items():
        competition_ids_encontrados[comp_id] = competition_ids_encontrados.get(comp_id, 0) + count

print(f"\nTotal de appearances encontradas para jogadores do Brasileirão (qualquer competição): {linhas_com_esses_jogadores}")
print("\nCompetition_id mais frequentes nessas appearances:")
for comp_id, count in sorted(competition_ids_encontrados.items(), key=lambda x: -x[1])[:15]:
    print(f"  {comp_id}: {count}")