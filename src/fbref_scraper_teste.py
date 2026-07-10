
"""
fbref_scraper_teste.py — Confirma os nomes exatos de colunas das 5 tabelas
disponíveis no soccerdata/FBRef antes de escrever o extract_fbref.py.
"""

import soccerdata as sd

TEMPORADA = "2025-2026"

fbref = sd.FBref(leagues="ENG-Premier League", seasons=TEMPORADA)

for stat_type in ["standard", "shooting", "misc", "playing_time", "keeper"]:
    print(f"\n{'=' * 60}")
    print(f"STAT_TYPE: {stat_type}")
    print(f"{'=' * 60}")
    df = fbref.read_player_season_stats(stat_type=stat_type)
    print(f"Formato: {df.shape}")
    print(f"Colunas: {list(df.columns)}")
