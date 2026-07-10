
"""
extract_fbref.py — Puxa métricas avançadas do FBRef (standard, shooting, misc)
pras 5 ligas europeias e cruza com os dados já filtrados do Transfermarkt
(dados/processed/{liga}.csv), usando nome do jogador normalizado como chave.

Pré-requisito: rodar extract.py + transform.py antes (precisa dos CSVs
já filtrados sub-23 em dados/processed/).
"""

import re
import unicodedata
from pathlib import Path

import pandas as pd
import soccerdata as sd

RAIZ = Path(__file__).resolve().parent.parent
DADOS_PROCESSED = RAIZ / "dados" / "processed"

TEMPORADA = "2025-2026"

# Mapeamento nome_do_projeto -> nome exato aceito pelo soccerdata/FBRef
LIGAS_FBREF = {
    "premier_league": "ENG-Premier League",
    "la_liga": "ESP-La Liga",
    "bundesliga": "GER-Bundesliga",
    "serie_a": "ITA-Serie A",
    "ligue_1": "FRA-Ligue 1",
}

# Colunas de identificação/contexto que se repetem nas 3 tabelas do FBRef
# (não precisamos duplicar essas ao juntar shooting e misc no standard)
COLUNAS_CONTEXTO = {"nation", "pos", "age", "born", "90s"}


def normalizar_nome(nome: str) -> str:
    """Remove acentos, pontuação e padroniza minúsculo pra facilitar o match."""
    if pd.isna(nome):
        return ""
    nome = unicodedata.normalize("NFKD", str(nome)).encode("ascii", "ignore").decode("utf-8")
    nome = nome.lower().strip()
    nome = re.sub(r"[^a-z\s]", "", nome)
    nome = re.sub(r"\s+", " ", nome)
    return nome


def achatar_colunas(df: pd.DataFrame) -> pd.DataFrame:
    """Transforma o MultiIndex de colunas do FBRef em nomes simples tipo 'Performance_Gls'."""
    df = df.copy()
    novas_colunas = []
    for col in df.columns:
        partes = [str(c) for c in col if c not in ("", None)]
        novas_colunas.append("_".join(partes))
    df.columns = novas_colunas
    return df.reset_index()  # traz league/season/team/player pra colunas normais


def carregar_fbref_5_ligas() -> pd.DataFrame:
    """Puxa standard+shooting+misc pras 5 ligas de uma vez e junta num único DataFrame."""
    print("Conectando ao FBRef pras 5 ligas europeias (pode demorar)...")
    fbref = sd.FBref(leagues=list(LIGAS_FBREF.values()), seasons=TEMPORADA)

    print("  Puxando standard...")
    standard = achatar_colunas(fbref.read_player_season_stats(stat_type="standard"))

    print("  Puxando shooting...")
    shooting = achatar_colunas(fbref.read_player_season_stats(stat_type="shooting"))

    print("  Puxando misc...")
    misc = achatar_colunas(fbref.read_player_season_stats(stat_type="misc"))

    chaves = ["league", "season", "team", "player"]

    colunas_shooting = [
        c for c in shooting.columns
        if c not in chaves and c.split("_")[0] not in COLUNAS_CONTEXTO
    ]
    colunas_misc = [
        c for c in misc.columns
        if c not in chaves and c.split("_")[0] not in COLUNAS_CONTEXTO
    ]

    df = standard.merge(shooting[chaves + colunas_shooting], on=chaves, how="left")
    df = df.merge(misc[chaves + colunas_misc], on=chaves, how="left")

    df["nome_normalizado"] = df["player"].apply(normalizar_nome)
    return df


def processar_liga(nome_liga: str, fbref_todas_ligas: pd.DataFrame) -> None:
    print(f"\nProcessando {nome_liga}...")

    caminho = DADOS_PROCESSED / f"{nome_liga}.csv"
    tm = pd.read_csv(caminho)
    tm["nome_normalizado"] = tm["name"].apply(normalizar_nome)

    liga_fbref_nome = LIGAS_FBREF[nome_liga]
    fb = fbref_todas_ligas[fbref_todas_ligas["league"] == liga_fbref_nome].copy()

    # Descarta nomes duplicados após normalização (dois jogadores com nome
    # muito parecido na mesma liga) - preferimos não casar errado a casar errado
    duplicados = fb["nome_normalizado"].duplicated(keep=False)
    if duplicados.any():
        nomes_duplicados = fb.loc[duplicados, "nome_normalizado"].unique()
        print(f"  Aviso: {len(nomes_duplicados)} nome(s) duplicado(s) no FBRef, descartados do cruzamento: {list(nomes_duplicados)}")
    fb_unico = fb[~duplicados].copy()

    resultado = tm.merge(
        fb_unico.drop(columns=["league", "season", "team"]),
        on="nome_normalizado",
        how="left",
        suffixes=("", "_fbref"),
    )

    total = len(resultado)
    encontrados = resultado["player"].notna().sum()
    print(f"  Correspondência FBRef: {encontrados}/{total} jogadores ({encontrados/total*100:.1f}%)")

    resultado = resultado.drop(columns=["nome_normalizado"])
    resultado.to_csv(caminho, index=False)
    print(f"  Salvo em {caminho}")


def main():
    fbref_todas_ligas = carregar_fbref_5_ligas()

    for nome_liga in LIGAS_FBREF:
        processar_liga(nome_liga, fbref_todas_ligas)

    print("\nExtração FBRef concluída!")


if __name__ == "__main__":
    main()