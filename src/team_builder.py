
import pandas as pd
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DADOS_PROCESSED = RAIZ / "dados" / "processed"

LIGAS = ["premier_league", "la_liga", "bundesliga", "serie_a", "ligue_1", "brasileirao"]

FORMACAO = {
    "Goleiro": 1,
    "Zagueiro": 2,
    "Lateral": 2,
    "Volante": 1,
    "Meia": 2,
    "Ponta": 2,
    "Centroavante": 1,
}


def montar_xi(df: pd.DataFrame) -> pd.DataFrame:
    """Pega os N melhores (por score) de cada posição, conforme a FORMACAO."""
    selecionados = []
    for posicao, quantidade in FORMACAO.items():
        candidatos = df[df["posicao_projeto"] == posicao].sort_values("score", ascending=False)
        escolhidos = candidatos.head(quantidade)
        if len(escolhidos) < quantidade:
            print(f"    Aviso: só {len(escolhidos)}/{quantidade} jogador(es) disponível(is) para {posicao}")
        selecionados.append(escolhidos)
    return pd.concat(selecionados, ignore_index=True)


def imprimir_xi(xi: pd.DataFrame, titulo: str) -> None:
    print(f"\n{'='*60}")
    print(titulo)
    print(f"{'='*60}")
    for posicao in FORMACAO:
        jogadores = xi[xi["posicao_projeto"] == posicao]
        for _, jogador in jogadores.iterrows():
            liga_info = f" ({jogador['liga']})" if "liga" in jogador else ""
            print(f"  {posicao:15s}: {jogador['name']:25s} score={jogador['score']:.2f}{liga_info}")


def main():
    caminho_ranking = DADOS_PROCESSED / "ranking_geral.csv"
    ranking_geral = pd.read_csv(caminho_ranking)

    # Melhor XI de cada liga, separadamente
    todos_xis = {}
    for liga in LIGAS:
        df_liga = ranking_geral[ranking_geral["liga"] == liga]
        print(f"\nMontando XI de {liga}...")
        xi = montar_xi(df_liga)
        todos_xis[liga] = xi
        imprimir_xi(xi, f"MELHOR XI SUB-23 — {liga.upper()}")

    # Melhor XI mundial (todas as ligas competindo entre si)
    print("\nMontando XI mundial...")
    xi_mundial = montar_xi(ranking_geral)
    imprimir_xi(xi_mundial, "MELHOR XI SUB-23 MUNDIAL (5 ligas europeias + Brasileirão)")

    # Salva tudo em CSVs separados
    for liga, xi in todos_xis.items():
        caminho = DADOS_PROCESSED / f"xi_{liga}.csv"
        xi.to_csv(caminho, index=False)

    caminho_mundial = DADOS_PROCESSED / "xi_mundial.csv"
    xi_mundial.to_csv(caminho_mundial, index=False)
    print(f"\nTodos os XIs salvos em dados/processed/xi_*.csv")


if __name__ == "__main__":
    main()