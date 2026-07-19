@'
export interface Jogador {
  name: string;
  liga: string;
  posicao: Posicao;
  idade: number | null;
  clube: string;
  nacionalidade: string | null;
  dadosCompletos: boolean;
  partidasJogadas: number | null;
  minutosJogados: number | null;
  gols: number;
  assistencias: number;
  valorMercado: number | null;
  score: number;
}

export type Posicao =
  | "Goleiro"
  | "Zagueiro"
  | "Lateral"
  | "Volante"
  | "Meia"
  | "Ponta"
  | "Centroavante";

export const POSICOES: Posicao[] = [
  "Goleiro",
  "Zagueiro",
  "Lateral",
  "Volante",
  "Meia",
  "Ponta",
  "Centroavante",
];

export const COR_POSICAO: Record<Posicao, string> = {
  Goleiro: "var(--color-pos-goleiro)",
  Zagueiro: "var(--color-pos-zagueiro)",
  Lateral: "var(--color-pos-lateral)",
  Volante: "var(--color-pos-volante)",
  Meia: "var(--color-pos-meia)",
  Ponta: "var(--color-pos-ponta)",
  Centroavante: "var(--color-pos-centroavante)",
};

export const LIGAS = [
  "premier_league",
  "la_liga",
  "bundesliga",
  "serie_a",
  "ligue_1",
  "brasileirao",
  "portugal",
  "argentina",
] as const;

export type Liga = (typeof LIGAS)[number];

export const NOME_LIGA: Record<Liga, string> = {
  premier_league: "Premier League",
  la_liga: "La Liga",
  bundesliga: "Bundesliga",
  serie_a: "Serie A",
  ligue_1: "Ligue 1",
  brasileirao: "Brasileirao",
  portugal: "Liga Portugal",
  argentina: "Primera Division",
};

export const CODIGO_LIGA: Record<Liga, string> = {
  premier_league: "ENG",
  la_liga: "ESP",
  bundesliga: "GER",
  serie_a: "ITA",
  ligue_1: "FRA",
  brasileirao: "BRA",
  portugal: "POR",
  argentina: "ARG",
};
'@ | Set-Content -Path "src\types\jogador.ts" -Encoding utf8

Write-Host "Argentina adicionada ao types/jogador.ts com sucesso."