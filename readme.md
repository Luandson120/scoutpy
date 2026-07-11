# ScoutPy — Descoberta de Jovens Talentos do Futebol Mundial

Projeto de scouting de jogadores Sub-23 nas 5 principais ligas europeias + Brasileirão,
usando dados públicos (Transfermarkt via Kaggle + FBRef via scraping) para gerar
rankings, scores e "melhores XIs" por liga e por posição.

## Status do projeto (atualizado)

- [x] Etapa 1 — Setup do projeto (venv, estrutura de pastas, Git/GitHub)
- [x] Etapa 2 — Extração Transfermarkt (`extract.py`) — funciona pras 6 ligas
- [x] Etapa 3 — Transformação (`transform.py`) — funciona pras 5 ligas europeias
- [x] Etapa 3.5 — Enriquecimento FBRef (`extract_fbref.py`) — funciona em **4 das 5 ligas europeias**
- [x] Etapa 3.6 — Correção Brasileirão (`extract_brasileirao_fix.py`) — resolvido com fonte alternativa (ver limitação abaixo)
- [x] Etapa 4 — Ranking/Score (`ranking.py`) — funciona pras 6 ligas, com tratamento especial pro Brasileirão
- [x] Etapa 5 — Montagem de times (`team_builder.py`) — funciona pras 6 ligas + XI mundial
- [x] Etapa 6 — Dashboard (`dashboard.py`) — funcional, com 7 abas (busca + 6 visualizações)
- [x] Etapa 7 — Visualizações extras — implementadas no dashboard.py

## ⚠️ Limitações conhecidas (aceitas, documentadas, não são bugs)

### 1. Brasileirão usa fonte de dados diferente e critério mais fraco
O dataset principal (Transfermarkt/Kaggle) não tem **nenhuma** partida registrada pro
Brasileirão em `appearances.csv` (confirmado via `diagnostico_brasileirao.py`). A solução
(`extract_brasileirao_fix.py`) usa um dataset alternativo (Kaggle: `lucasbral/brasileirao-cartoes-20-23`,
temporadas 2020-2023) que registra apenas eventos de gol e cartão por partida - não a
escalação completa. Isso significa:
- **Não há dado de minutos jogados nem partidas jogadas** para o Brasileirão - o filtro de
  volume mínimo (3+ partidas, 180+ minutos) usado nas outras 5 ligas não pode ser aplicado aqui.
- O cruzamento entre o nome curto do Transfermarkt e o nome completo desse dataset (via
  matching de subconjunto de tokens) recuperou eventos pra ~12% dos jogadores sub-23
  (57 de 491) - os demais aparecem com 0 gols/cartões, o que **não significa que não jogaram**,
  só que não tiveram gol ou cartão registrado nessa fonte entre 2020-2023.
- O **score do Brasileirão é calculado com uma fórmula/escala separada** das outras 5 ligas
  (total bruto de gols, normalizado só entre os próprios jogadores do Brasileirão) - ver
  `ranking.py`, coluna `dados_completos`. Não é diretamente comparável ao score das ligas
  europeias, embora apareça na mesma escala numérica no "XI mundial".

### 2. Serie A não tem métricas do FBRef
A biblioteca `soccerdata` falha ao tentar listar a competição "ITA-Serie A"
(`ValueError: No objects to concatenate` dentro de `read_seasons()`). Hipótese mais
provável: proteção anti-bot (Cloudflare) adicionada recentemente pelo FBRef, possivelmente
combinada com colisão de nome entre "Serie A" (Itália) e "Série A" (Brasil) na página de
listagem de competições do site. **Não resolvido - aceito como limitação.** A Serie A usa
só métricas do Transfermarkt (gols, assistências), igual o Brasileirão em termos de riqueza
de dados, mas com filtro de volume mínimo aplicado normalmente (tem appearances.csv completo).
Scripts de diagnóstico: `src/diagnostico_serie_a.py`, `src/diagnostico_ligas_fbref.py`.

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

### Brasileirão - fonte alternativa (Kaggle: `lucasbral/brasileirao-cartoes-20-23`)

Dataset com eventos de gol/cartão por partida (2020-2023), baseado em dados da Opta.
Usado só pro Brasileirão, já que o Transfermarkt não tem `appearances.csv` pra essa
competição. Ver limitação #1 acima.

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
python src/extract.py                    # gera dados/processed/{liga}.csv (Transfermarkt, 6 ligas)
python src/transform.py                   # filtra sub-23 + volume mínimo + mapeia posição
python src/extract_fbref.py               # enriquece 4 das 6 ligas com métricas do FBRef
python src/extract_brasileirao_fix.py     # corrige o Brasileirão com fonte alternativa

python src/ranking.py                     # calcula score por posição, todas as 6 ligas
python src/team_builder.py                # monta os melhores XIs por liga + XI mundial

streamlit run src/dashboard.py            # abre o dashboard interativo
```

## Estrutura

```
dados/
├── raw/            # CSVs originais baixados do Kaggle (ignorado no Git, muito grande)
│   └── brasileirao_alt/   # dataset alternativo de gols/cartões do Brasileirão
└── processed/       # CSVs finais por liga, ranking_geral.csv, xi_*.csv

src/
├── extract.py                    # baixa/lê os dados brutos do Kaggle
├── transform.py                   # filtra sub-23, volume mínimo, mapeia posição
├── extract_fbref.py               # enriquece com métricas do FBRef (4 das 6 ligas)
├── extract_brasileirao_fix.py     # corrige o Brasileirão com fonte alternativa
├── ranking.py                      # calcula taxas por 90min + score ponderado por posição
├── team_builder.py                # monta os melhores XIs (por liga + mundial)
├── dashboard.py                    # app Streamlit com 7 abas de visualização
├── diagnostico_brasileirao.py     # investigação da limitação #1 (resolvida)
├── diagnostico_serie_a.py         # investigação da limitação #2 (aceita, não resolvida)
└── diagnostico_ligas_fbref.py     # investigação da limitação #2 (aceita, não resolvida)
```