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

export const LIGAS = [
  "premier_league",
  "la_liga",
  "bundesliga",
  "serie_a",
  "ligue_1",
  "brasileirao",
] as const;

export type Liga = (typeof LIGAS)[number];

export const NOME_LIGA: Record<Liga, string> = {
  premier_league: "Premier League",
  la_liga: "La Liga",
  bundesliga: "Bundesliga",
  serie_a: "Serie A",
  ligue_1: "Ligue 1",
  brasileirao: "Brasileirao",
};
