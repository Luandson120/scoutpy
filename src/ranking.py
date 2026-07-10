import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.preprocessing import MinMaxScaler

RAIZ = Path(__file__).resolve().parent.parent
DADOS_PROCESSED = RAIZ / "dados" / "processed"

LIGAS = ["premier_league", "la_liga", "bundesliga", "serie_a", "ligue_1", "brasileirao"]

# Pesos por posição do projeto. Cada métrica é normalizada (0-1) antes de aplicar o peso.
# Métricas indisponíveis (Serie A/Brasileirão sem FBRef) entram como 0 - o jogador não
# é penalizado abaixo de 0, só não ganha pontos extras que os outros ganham.
PESOS_POR_POSICAO = {
    "Centroavante": {"gols_90": 4.0, "finalizacoes_alvo_90": 2.0, "assistencias_90": 1.0},
    "Ponta": {"gols_90": 3.0, "assistencias_90": 3.0, "cruzamentos_90": 1.0},
    "Meia": {"assistencias_90": 3.0, "gols_90": 2.0, "cruzamentos_90": 1.0},
    "Volante": {"interceptacoes_90": 2.0, "desarmes_90": 2.0, "assistencias_90": 0.5, "gols_90": 0.5},
    "Lateral": {"cruzamentos_90": 2.0, "assistencias_90": 2.0, "desarmes_90": 1.0},
    "Zagueiro": {"desarmes_90": 2.5, "interceptacoes_90": 2.5},
    "Goleiro": {"partidas_jogadas": 1.0},  # ainda sem métricas de goleiro (keeper) - ver limitação no README
}

TODAS_METRICAS = [
    "gols_90", "assistencias_90", "finalizacoes_alvo_90",
    "cruzamentos_90", "desarmes_90", "interceptacoes_90", "partidas_jogadas",
]


def calcular_taxas_por_90(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Taxas baseadas em minutos do Transfermarkt (gols/assistências acumulados)
    minutos = df["minutos_jogados"].replace(0, np.nan)
    df["gols_90"] = (df["gols"] / minutos * 90).fillna(0)
    df["assistencias_90"] = (df["assistencias"] / minutos * 90).fillna(0)

    # Taxas baseadas em minutos do FBRef (só temporada atual) - quando disponível
    if "Playing Time_90s" in df.columns:
        noventas_fbref = df["Playing Time_90s"].replace(0, np.nan)
        df["finalizacoes_alvo_90"] = (df["Standard_SoT"] / noventas_fbref).fillna(0)
        df["cruzamentos_90"] = (df["Performance_Crs"] / noventas_fbref).fillna(0)
        df["desarmes_90"] = (df["Performance_TklW"] / noventas_fbref).fillna(0)
        df["interceptacoes_90"] = (df["Performance_Int"] / noventas_fbref).fillna(0)
    else:
        # Serie A / Brasileirão - sem dados FBRef, todas essas métricas ficam 0
        for col in ["finalizacoes_alvo_90", "cruzamentos_90", "desarmes_90", "interceptacoes_90"]:
            df[col] = 0.0

    return df


def calcular_score(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Normaliza cada métrica pra escala 0-1, usando TODOS os jogadores (todas as ligas)
    # como referência - assim o score é comparável entre ligas diferentes
    scaler = MinMaxScaler()
    df[TODAS_METRICAS] = scaler.fit_transform(df[TODAS_METRICAS])

    df["score"] = 0.0
    for posicao, pesos in PESOS_POR_POSICAO.items():
        mascara = df["posicao_projeto"] == posicao
        for metrica, peso in pesos.items():
            df.loc[mascara, "score"] += df.loc[mascara, metrica] * peso

    return df


def main():
    print("Carregando as 6 ligas...")
    dfs = []
    for liga in LIGAS:
        caminho = DADOS_PROCESSED / f"{liga}.csv"
        df = pd.read_csv(caminho)
        df["liga"] = liga
        dfs.append(df)

    todos = pd.concat(dfs, ignore_index=True)
    print(f"Total de jogadores (todas as ligas): {len(todos)}")

    print("Calculando taxas por 90 minutos...")
    todos = calcular_taxas_por_90(todos)

    print("Normalizando métricas e calculando score...")
    todos = calcular_score(todos)

    # Salva o ranking geral (todas as ligas juntas, útil pro "melhor XI mundial" depois)
    colunas_saida = [
        "liga", "name", "posicao_projeto", "idade", "current_club_name",
        "partidas_jogadas", "minutos_jogados", "gols", "assistencias",
        "gols_90", "assistencias_90", "finalizacoes_alvo_90",
        "cruzamentos_90", "desarmes_90", "interceptacoes_90",
        "market_value_in_eur", "score",
    ]
    ranking_geral = todos[colunas_saida].sort_values("score", ascending=False)
    caminho_ranking = DADOS_PROCESSED / "ranking_geral.csv"
    ranking_geral.to_csv(caminho_ranking, index=False)
    print(f"\nRanking geral salvo em {caminho_ranking}")

    # Mostra o top 5 por posição, só pra conferência visual rápida
    print("\n--- Top 5 por posição (todas as ligas) ---")
    for posicao in PESOS_POR_POSICAO:
        top5 = ranking_geral[ranking_geral["posicao_projeto"] == posicao].head(5)
        print(f"\n{posicao}:")
        print(top5[["name", "liga", "score"]].to_string(index=False))


if __name__ == "__main__":
    main()
