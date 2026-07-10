

import pandas as pd
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DADOS_PROCESSED = RAIZ / "dados" / "processed"

LIGAS = ["premier_league", "la_liga", "bundesliga", "serie_a", "ligue_1", "brasileirao"]

PARTIDAS_MINIMAS = 3
MINUTOS_MINIMOS = 180

MAPA_POSICOES = {
    "Goalkeeper": "Goleiro",
    "Centre-Back": "Zagueiro",
    "Left-Back": "Lateral",
    "Right-Back": "Lateral",
    "Defensive Midfield": "Volante",
    "Central Midfield": "Meia",
    "Attacking Midfield": "Meia",
    "Left Midfield": "Meia",
    "Right Midfield": "Meia",
    "Left Winger": "Ponta",
    "Right Winger": "Ponta",
    "Centre-Forward": "Centroavante",
    "Second Striker": "Centroavante",
}


def transformar_liga(nome_liga: str) -> None:
    caminho = DADOS_PROCESSED / f"{nome_liga}.csv"
    df = pd.read_csv(caminho)
    total_antes = len(df)

    df = df[
        (df["partidas_jogadas"] >= PARTIDAS_MINIMAS)
        & (df["minutos_jogados"] >= MINUTOS_MINIMOS)
    ].copy()
    apos_filtro_volume = len(df)

    df["posicao_projeto"] = df["sub_position"].map(MAPA_POSICOES)

    sem_posicao = df["posicao_projeto"].isna().sum()
    df = df[df["posicao_projeto"].notna()].copy()

    df.to_csv(caminho, index=False)

    print(
        f"{nome_liga}: {total_antes} -> {apos_filtro_volume} (filtro volume) "
        f"-> {len(df)} (com posição definida). "
        f"Descartados sem sub_position mapeável: {sem_posicao}"
    )


def main():
    print(f"Filtro: partidas >= {PARTIDAS_MINIMAS}, minutos >= {MINUTOS_MINIMOS}\n")
    for liga in LIGAS:
        transformar_liga(liga)
    print("\nTransformação concluída!")


if __name__ == "__main__":
    main()