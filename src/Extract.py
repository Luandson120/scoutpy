import pandas as pd
from pathlib import Path
from datetime import datetime

RAIZ = Path(__file__).resolve().parent.parent
DADOS_RAW = RAIZ / "dados" / "raw"
DADOS_PROCESSED = RAIZ / "dados" / "processed"

# Mapeamento liga -> competition_id (confirmado em competitions.csv)
LIGAS = {
    "premier_league": "GB1",
    "la_liga": "ES1",
    "bundesliga": "L1",
    "serie_a": "IT1",
    "ligue_1": "FR1",
    "brasileirao": "BRA1",
}

IDADE_MAXIMA = 23


def calcular_idade(data_nascimento: pd.Timestamp, referencia: datetime) -> float:
    if pd.isna(data_nascimento):
        return None
    anos = referencia.year - data_nascimento.year
    # ajusta se ainda não fez aniversário este ano
    if (referencia.month, referencia.day) < (data_nascimento.month, data_nascimento.day):
        anos -= 1
    return anos


def carregar_players() -> pd.DataFrame:
    print("Carregando players.csv...")
    players = pd.read_csv(DADOS_RAW / "players.csv")
    players["date_of_birth"] = pd.to_datetime(players["date_of_birth"], errors="coerce")

    hoje = datetime.now()
    players["idade"] = players["date_of_birth"].apply(lambda d: calcular_idade(d, hoje))

    return players


def carregar_appearances_agregadas(competition_id: str) -> pd.DataFrame:
    """
    Lê appearances.csv filtrando só a liga alvo e agrega por jogador:
    partidas jogadas, minutos totais, gols totais, assistências totais.
    """
    print(f"  Lendo appearances.csv (filtrando competition_id == {competition_id})...")

    chunks_filtrados = []
    for chunk in pd.read_csv(DADOS_RAW / "appearances.csv", chunksize=200_000):
        filtrado = chunk[chunk["competition_id"] == competition_id]
        if not filtrado.empty:
            chunks_filtrados.append(filtrado)

    if not chunks_filtrados:
        return pd.DataFrame(columns=["player_id", "partidas_jogadas", "minutos_jogados", "gols", "assistencias"])

    appearances = pd.concat(chunks_filtrados, ignore_index=True)

    agregado = appearances.groupby("player_id").agg(
        partidas_jogadas=("appearance_id", "count"),
        minutos_jogados=("minutes_played", "sum"),
        gols=("goals", "sum"),
        assistencias=("assists", "sum"),
    ).reset_index()

    return agregado


def processar_liga(nome_liga: str, competition_id: str, players: pd.DataFrame) -> pd.DataFrame:
    print(f"\nProcessando {nome_liga} ({competition_id})...")

    jogadores_liga = players[
        (players["current_club_domestic_competition_id"] == competition_id)
        & (players["idade"] <= IDADE_MAXIMA)
        & (players["idade"].notna())
    ].copy()

    print(f"  Jogadores sub-{IDADE_MAXIMA} encontrados: {len(jogadores_liga)}")


    stats = carregar_appearances_agregadas(competition_id)


    resultado = jogadores_liga.merge(stats, on="player_id", how="left")


    for col in ["partidas_jogadas", "minutos_jogados", "gols", "assistencias"]:
        resultado[col] = resultado[col].fillna(0).astype(int)

    colunas_finais = [
        "player_id", "name", "date_of_birth", "idade",
        "position", "sub_position", "foot", "height_in_cm",
        "country_of_citizenship", "current_club_name",
        "market_value_in_eur", "highest_market_value_in_eur",
        "partidas_jogadas", "minutos_jogados", "gols", "assistencias",
    ]
    resultado = resultado[colunas_finais]

    return resultado


def main():
    DADOS_PROCESSED.mkdir(parents=True, exist_ok=True)
    players = carregar_players()

    for nome_liga, competition_id in LIGAS.items():
        resultado = processar_liga(nome_liga, competition_id, players)
        caminho_saida = DADOS_PROCESSED / f"{nome_liga}.csv"
        resultado.to_csv(caminho_saida, index=False)
        print(f"  Salvo em {caminho_saida} ({len(resultado)} jogadores)")

    print("\nExtração concluída!")


if __name__ == "__main__":
    main()