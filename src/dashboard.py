"""
dashboard.py — Front-end simples em Streamlit pro ScoutPy.

Rodar com: streamlit run src/dashboard.py
"""

import pandas as pd
import streamlit as st
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DADOS_PROCESSED = RAIZ / "dados" / "processed"

st.set_page_config(page_title="ScoutPy", page_icon="⚽", layout="wide")


@st.cache_data
def carregar_ranking():
    return pd.read_csv(DADOS_PROCESSED / "ranking_geral.csv")


def main():
    st.title("⚽ ScoutPy — Descoberta de Jovens Talentos Sub-23")
    st.caption(
        "Premier League, La Liga, Bundesliga, Serie A, Ligue 1 e Brasileirão. "
        "Serie A e Brasileirão têm métricas mais limitadas (sem dados do FBRef) - "
        "ver README do projeto pra detalhes."
    )

    df = carregar_ranking()

    # --- Filtros na barra lateral ---
    st.sidebar.header("Filtros")

    ligas_disponiveis = sorted(df["liga"].unique())
    liga_selecionada = st.sidebar.selectbox(
        "Liga", options=["Todas"] + ligas_disponiveis
    )

    posicoes_disponiveis = sorted(df["posicao_projeto"].unique())
    posicao_selecionada = st.sidebar.selectbox(
        "Posição", options=["Todas"] + posicoes_disponiveis
    )

    idade_maxima = st.sidebar.slider(
        "Idade máxima", min_value=16, max_value=23, value=23
    )

    # --- Aplica filtros ---
    filtrado = df.copy()
    if liga_selecionada != "Todas":
        filtrado = filtrado[filtrado["liga"] == liga_selecionada]
    if posicao_selecionada != "Todas":
        filtrado = filtrado[filtrado["posicao_projeto"] == posicao_selecionada]
    filtrado = filtrado[filtrado["idade"] <= idade_maxima]

    filtrado = filtrado.sort_values("score", ascending=False)

    # --- Resultado ---
    st.subheader(f"Resultado ({len(filtrado)} jogadores)")

    colunas_exibir = [
        "name", "liga", "posicao_projeto", "idade", "current_club_name",
        "partidas_jogadas", "minutos_jogados", "gols", "assistencias",
        "market_value_in_eur", "score",
    ]
    st.dataframe(
        filtrado[colunas_exibir].reset_index(drop=True),
        use_container_width=True,
        height=600,
    )


if __name__ == "__main__":
    main()