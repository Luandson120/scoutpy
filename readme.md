    # ScoutPy — Descoberta de Jovens Talentos do Futebol Mundial

Projeto de scouting de jogadores Sub-23 nas 5 principais ligas europeias + Brasileirão,
usando dados públicos (Transfermarkt via Kaggle + FBRef via scraping) para gerar
rankings, scores e "melhores XIs" por liga e por posição.

## Status do projeto (atualizado)

- [x] Etapa 1 — Setup do projeto (venv, estrutura de pastas, Git/GitHub)
- [x] Etapa 2 — Extração Transfermarkt (`extract.py`) — funciona pras 6 ligas
- [x] Etapa 3 — Transformação (`transform.py`) — funciona, **exceto Brasileirão** (ver pendências)
- [x] Etapa 3.5 — Enriquecimento FBRef (`extract_fbref.py`) — funciona em **4 das 6 ligas**
- [ ] Etapa 4 — Ranking/Score (`ranking.py`) — não iniciado
- [ ] Etapa 5 — Montagem de times (`team_builder.py`) — não iniciado
- [ ] Etapa 6 — Dashboard (`dashboard.py`) — não iniciado
- [ ] Etapa 7 — Visualizações extras — não iniciado

## ⚠️ Pendências conhecidas (em aberto, sem solução ainda)

### 1. Brasileirão sem jogadores após `transform.py`
Os 511 jogadores sub-23 extraídos do Kaggle (Transfermarkt) para o Brasileirão zeraram
completamente ao aplicar o filtro de volume mínimo (3+ partidas, 180+ minutos). Diagnóstico
parcial (`src/diagnostico_brasileirao.py`) mostrou que esses jogadores têm poucas ou
nenhuma partida registrada em `appearances.csv` com `competition_id == "BRA1"` — sugere
que o dataset da Transfermarkt no Kaggle tem cobertura fraca de partidas do próprio
Brasileirão. **Ainda não investigado a fundo, nem resolvido.**

### 2. Serie A não retorna dados do FBRef
A biblioteca `soccerdata` falha ao tentar listar a competição "ITA-Serie A"
(`ValueError: No objects to concatenate` dentro de `read_seasons()`). Hipótese mais
provável: proteção anti-bot (Cloudflare) adicionada recentemente pelo FBRef, possivelmente
combinada com colisão de nome entre "Serie A" (Itália) e "Série A" (Brasil) na página de
listagem de competições do site. **Ainda não resolvido.** Scripts de diagnóstico:
`src/diagnostico_serie_a.py`, `src/diagnostico_ligas_fbref.py`.

## Decisões já tomadas ao longo do projeto

- **Fonte de dados primária**: Kaggle, dataset `davidcariboo/player-scores`
  ("Football Data from Transfermarkt") — cobre as 6 ligas com dados cadastrais
  (posição, idade, valor de mercado) e appearances (gols, assistências, minutos, cartões).
- **Fonte de dados secundária (enriquecimento)**: FBRef via biblioteca `soccerdata`,
  usada só nas 5 ligas europeias — adiciona finalizações, xG-proxy, desarmes,
  interceptações, cruzamentos. **Brasileirão foi planejado desde o início pra ficar
  só com Transfermarkt** (score mais simples) — isso não é uma pendência, é decisão
  de escopo.
- **Filtro de elegibilidade**: idade ≤ 23 anos, mínimo 3 partidas jogadas, mínimo
  180 minutos em campo.
- **Categorias de posição do projeto** (Goleiro, Zagueiro, Lateral, Volante, Meia,
  Ponta, Centroavante): mapeadas a partir do `sub_position` do Transfermarkt (mais
  granular), não do FBRef (que só tem GK/DF/MF/FW).
- **Cruzamento FBRef ↔ Transfermarkt**: feito por nome de jogador normalizado
  (sem acento, minúsculo). Taxa de correspondência varia entre ~71% e ~86% nas
  ligas que funcionam — perda esperada, não é bug.

## Fonte de dados

### Transfermarkt (Kaggle: `davidcariboo/player-scores`)

Tabelas usadas:
- `players.csv` — nome, data de nascimento, posição, sub_position, nacionalidade, valor de mercado, pé preferido
- `appearances.csv` — partidas jogadas, minutos, gols, assistências, cartões por jogador/jogo
- `competitions.csv` — mapeamento de competições/ligas (códigos: GB1, ES1, L1, IT1, FR1, BRA1)

### FBRef (via `soccerdata`, só nas 4 ligas que funcionam: Premier League, La Liga, Bundesliga, Ligue 1)

Tabelas usadas (`stat_type`): `standard`, `shooting`, `misc`. As tabelas `passing`,
`possession` e `defense` **não estão mais disponíveis** na versão atual da biblioteca
(removidas após o FBRef adicionar proteção Cloudflare em 2026 — ver commit
`7d1622da` no repositório `probberechts/soccerdata`).

## Nota sobre paths

Scripts em `src/` usam caminho relativo à raiz do projeto (`dados/raw/...`, `dados/processed/...`).
Configure o "Working directory" das Run Configurations do PyCharm para a raiz do projeto
(não a pasta `src/`), senão os scripts não encontram os arquivos.

## Como rodar (local)

```bash
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate no Windows
pip install -r requirements.txt

# Configurar credenciais do Kaggle (~/.kaggle/access_token ou kaggle.json)
python src/extract.py          # gera dados/processed/{liga}.csv (Transfermarkt, 6 ligas)
python src/transform.py         # filtra sub-23 + volume mínimo + mapeia posição
python src/extract_fbref.py     # enriquece 4 das 6 ligas com métricas do FBRef

# ainda não implementados:
python src/ranking.py
python src/team_builder.py
streamlit run src/dashboard.py
```

## Estrutura

```
dados/
├── raw/            # CSVs originais baixados do Kaggle (ignorado no Git, muito grande)
└── processed/       # CSVs já filtrados/tratados por liga, sub-23, com FBRef quando disponível

src/
├── extract.py                    # baixa/lê os dados brutos do Kaggle
├── transform.py                   # filtra sub-23, volume mínimo, mapeia posição
├── extract_fbref.py               # enriquece com métricas do FBRef (4 das 6 ligas)
├── diagnostico_brasileirao.py     # investigação da pendência #1 (não resolvido)
├── diagnostico_serie_a.py         # investigação da pendência #2 (não resolvido)
├── diagnostico_ligas_fbref.py     # investigação da pendência #2 (não resolvido)
├── ranking.py                     # [não implementado ainda]
├── team_builder.py                # [não implementado ainda]
└── dashboard.py                   # [não implementado ainda]
```