import ast
import re
import unicodedata
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parent.parent
DADOS_RAW = RAIZ / "dados" / "raw"
DADOS_PROCESSED = RAIZ / "dados" / "processed"

CAMINHO_CARTOES = DADOS_RAW / "brasileirao_alt" / "partidas_20_23.csv"

IDADE_MAXIMA = 23

# Mesmo mapeamento de posição usado no transform.py
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


def normalizar_nome(nome: str) -> str:
    if pd.isna(nome):
        return ""
    nome = unicodedata.normalize("NFKD", str(nome)).encode("ascii", "ignore").decode("utf-8")
    nome = nome.lower().strip()
    nome = re.sub(r"[^a-z\s]", "", nome)
    nome = re.sub(r"\s+", " ", nome)
    return nome


def tokens_significativos(nome_normalizado: str) -> set:
    """Remove conectivos comuns em nomes brasileiros (de, da, dos, e) que não ajudam a identificar."""
    IGNORAR = {"de", "da", "do", "das", "dos", "e"}
    return {t for t in nome_normalizado.split() if t not in IGNORAR and len(t) > 1}


def parse_lista_eventos(valor: str) -> list:
    """Converte a string tipo '[{"player": "X", "minute": "17\'"}]' numa lista de dicts."""
    if pd.isna(valor) or valor == "" or valor == "[]":
        return []
    try:
        return ast.literal_eval(valor)
    except (ValueError, SyntaxError):
        return []


def contar_eventos_por_jogador(df_partidas: pd.DataFrame) -> pd.DataFrame:
    """Percorre todas as partidas e conta gols/cartões por jogador (nome normalizado)."""
    contagem = {}  # nome_normalizado -> {"gols": int, "cartoes": int, "nome_original": str}

    colunas_gols = ["gols_home", "gols_away"]
    colunas_cartoes = ["yellow_cards_home", "red_cards_home", "yellow_cards_away", "red_cards_away"]

    for _, linha in df_partidas.iterrows():
        for coluna in colunas_gols:
            for evento in parse_lista_eventos(linha[coluna]):
                nome = evento.get("player", "")
                chave = normalizar_nome(nome)
                if not chave:
                    continue
                if chave not in contagem:
                    contagem[chave] = {"gols": 0, "cartoes": 0, "nome_original": nome}
                contagem[chave]["gols"] += 1

        for coluna in colunas_cartoes:
            for evento in parse_lista_eventos(linha[coluna]):
                nome = evento.get("player", "")
                chave = normalizar_nome(nome)
                if not chave:
                    continue
                if chave not in contagem:
                    contagem[chave] = {"gols": 0, "cartoes": 0, "nome_original": nome}
                contagem[chave]["cartoes"] += 1

    linhas = [
        {"nome_normalizado": chave, "gols_evento": dados["gols"], "cartoes_evento": dados["cartoes"]}
        for chave, dados in contagem.items()
    ]
    return pd.DataFrame(linhas)


def encontrar_correspondencia(nome_curto_tokens: set, eventos_df: pd.DataFrame) -> tuple:
    """
    Procura, entre os jogadores com eventos registrados, aquele cujo conjunto de
    tokens do nome completo CONTÉM todos os tokens do nome curto (Transfermarkt).
    Retorna (gols, cartoes) do único candidato encontrado, ou (0, 0) se não achar
    nenhum ou se achar mais de um (ambíguo demais pra arriscar).
    """
    if not nome_curto_tokens:
        return (0, 0)

    candidatos = []
    for _, linha in eventos_df.iterrows():
        tokens_evento = set(linha["nome_normalizado"].split())
        if nome_curto_tokens.issubset(tokens_evento):
            candidatos.append(linha)

    if len(candidatos) == 1:
        return (candidatos[0]["gols_evento"], candidatos[0]["cartoes_evento"])
    return (0, 0)


def main():
    print("Carregando jogadores sub-23 do Brasileirão (players.csv)...")
    players = pd.read_csv(DADOS_RAW / "players.csv")
    players["date_of_birth"] = pd.to_datetime(players["date_of_birth"], errors="coerce")

    from datetime import datetime
    hoje = datetime.now()
    players["idade"] = players["date_of_birth"].apply(
        lambda d: (hoje.year - d.year - ((hoje.month, hoje.day) < (d.month, d.day))) if pd.notna(d) else None
    )

    brasileirao = players[
        (players["current_club_domestic_competition_id"] == "BRA1")
        & (players["idade"] <= IDADE_MAXIMA)
        & (players["idade"].notna())
    ].copy()
    print(f"  Jogadores sub-{IDADE_MAXIMA} encontrados: {len(brasileirao)}")

    print("\nCarregando e parseando eventos de gols/cartões (2020-2023)...")
    df_partidas = pd.read_csv(CAMINHO_CARTOES)
    eventos = contar_eventos_por_jogador(df_partidas)
    print(f"  Jogadores únicos com pelo menos 1 evento registrado: {len(eventos)}")

    brasileirao["nome_normalizado"] = brasileirao["name"].apply(normalizar_nome)
    brasileirao["tokens_nome"] = brasileirao["nome_normalizado"].apply(tokens_significativos)

    print("\nCruzando por subconjunto de tokens (pode demorar um pouco)...")
    resultados_match = brasileirao["tokens_nome"].apply(lambda tks: encontrar_correspondencia(tks, eventos))
    brasileirao["gols_evento"] = resultados_match.apply(lambda x: x[0])
    brasileirao["cartoes_evento"] = resultados_match.apply(lambda x: x[1])

    resultado = brasileirao

    resultado["gols"] = resultado["gols_evento"].fillna(0).astype(int)
    resultado["cartoes"] = resultado["cartoes_evento"].fillna(0).astype(int)
    resultado["assistencias"] = 0  # não disponível nessa fonte
    resultado["partidas_jogadas"] = pd.NA  # desconhecido, não é zero
    resultado["minutos_jogados"] = pd.NA  # desconhecido, não é zero
    resultado["dados_completos"] = False  # flag usada pelo ranking.py

    resultado["posicao_projeto"] = resultado["sub_position"].map(MAPA_POSICOES)
    antes = len(resultado)
    resultado = resultado[resultado["posicao_projeto"].notna()].copy()
    print(f"\n  Descartados sem sub_position mapeável: {antes - len(resultado)}")

    colunas_finais = [
        "player_id", "name", "date_of_birth", "idade",
        "position", "sub_position", "posicao_projeto", "foot", "height_in_cm",
        "country_of_citizenship", "current_club_name",
        "market_value_in_eur", "highest_market_value_in_eur",
        "partidas_jogadas", "minutos_jogados", "gols", "assistencias", "cartoes",
        "dados_completos",
    ]
    resultado = resultado[colunas_finais]

    caminho_saida = DADOS_PROCESSED / "brasileirao.csv"
    resultado.to_csv(caminho_saida, index=False)
    print(f"\nSalvo em {caminho_saida} ({len(resultado)} jogadores)")

    com_gol_ou_cartao = (resultado["gols"] + resultado["cartoes"] > 0).sum()
    print(f"  Jogadores com ao menos 1 gol ou cartão registrado: {com_gol_ou_cartao}/{len(resultado)}")
    print("  (os demais ficam com 0 em tudo - não significa que não jogaram, só que não tiveram evento registrado)")


main()
if __name__ == "__main__":
    pass