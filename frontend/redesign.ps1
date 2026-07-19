@'
<!doctype html>
<html lang="pt-BR">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/vite.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>ScoutPy - Dossie de Scouting Sub-23</title>
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link
      href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap"
      rel="stylesheet"
    />
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
'@ | Set-Content -Path "index.html" -Encoding utf8

@'
@import "tailwindcss";

@theme {
  --color-bg: #0D1512;
  --color-surface: #16211C;
  --color-surface-hover: #1E2C25;
  --color-line: #2A3830;
  --color-ink: #EDEAE0;
  --color-ink-muted: #8A9C90;
  --color-amber: #F2A93B;
  --color-amber-soft: #3A2E14;

  --color-pos-goleiro: #9B8AC4;
  --color-pos-zagueiro: #5A7FA6;
  --color-pos-lateral: #4FA6A0;
  --color-pos-volante: #7C8A4C;
  --color-pos-meia: #D6A73B;
  --color-pos-ponta: #E0613F;
  --color-pos-centroavante: #C23B3B;

  --font-display: "Bebas Neue", sans-serif;
  --font-body: "Inter", sans-serif;
  --font-mono: "JetBrains Mono", monospace;
}

body {
  background-color: var(--color-bg);
  color: var(--color-ink);
  font-family: var(--font-body);
}

::-webkit-scrollbar {
  height: 6px;
  width: 6px;
}
::-webkit-scrollbar-thumb {
  background-color: var(--color-line);
  border-radius: 999px;
}

.scroll-sem-barra {
  scrollbar-width: none;
  -ms-overflow-style: none;
}
.scroll-sem-barra::-webkit-scrollbar {
  display: none;
}
'@ | Set-Content -Path "src\index.css" -Encoding utf8

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

export const CODIGO_LIGA: Record<Liga, string> = {
  premier_league: "ENG",
  la_liga: "ESP",
  bundesliga: "GER",
  serie_a: "ITA",
  ligue_1: "FRA",
  brasileirao: "BRA",
};
'@ | Set-Content -Path "src\types\jogador.ts" -Encoding utf8

@'
import { useEffect, useState } from "react";
import type { Jogador } from "../types/jogador";

interface EstadoJogadores {
  jogadores: Jogador[];
  carregando: boolean;
  erro: string | null;
}

export function useJogadores(): EstadoJogadores {
  const [jogadores, setJogadores] = useState<Jogador[]>([]);
  const [carregando, setCarregando] = useState(true);
  const [erro, setErro] = useState<string | null>(null);

  useEffect(() => {
    fetch("/data/ranking.json")
      .then((res) => {
        if (!res.ok) throw new Error("Erro ao carregar dados: " + res.status);
        return res.json();
      })
      .then((data: Jogador[]) => {
        setJogadores(data);
        setCarregando(false);
      })
      .catch((err: Error) => {
        setErro(err.message);
        setCarregando(false);
      });
  }, []);

  return { jogadores, carregando, erro };
}
'@ | Set-Content -Path "src\hooks\useJogadores.ts" -Encoding utf8

@'
import { LIGAS, NOME_LIGA, CODIGO_LIGA, type Liga } from "../types/jogador";

interface Props {
  ligaAtiva: Liga;
  aoTrocar: (liga: Liga) => void;
}

export function AbasLiga({ ligaAtiva, aoTrocar }: Props) {
  return (
    <div className="scroll-sem-barra flex gap-1 overflow-x-auto border-b border-line">
      {LIGAS.map((liga) => {
        const ativa = liga === ligaAtiva;
        return (
          <button
            key={liga}
            onClick={() => aoTrocar(liga)}
            className={
              "flex shrink-0 flex-col items-start gap-0.5 border-b-2 px-4 py-2 text-left transition-colors " +
              (ativa
                ? "border-amber text-ink"
                : "border-transparent text-ink-muted hover:text-ink")
            }
          >
            <span className="font-mono text-[10px] tracking-widest text-ink-muted">
              {CODIGO_LIGA[liga]}
            </span>
            <span className="font-display text-lg leading-none tracking-wide">
              {NOME_LIGA[liga]}
            </span>
          </button>
        );
      })}
    </div>
  );
}
'@ | Set-Content -Path "src\components\AbasLiga.tsx" -Encoding utf8

@'
import { POSICOES, COR_POSICAO, type Posicao } from "../types/jogador";

interface Props {
  posicaoAtiva: Posicao | "Todas";
  aoTrocar: (posicao: Posicao | "Todas") => void;
}

export function FiltroPosicao({ posicaoAtiva, aoTrocar }: Props) {
  return (
    <div className="scroll-sem-barra flex gap-2 overflow-x-auto">
      <button
        onClick={() => aoTrocar("Todas")}
        className={
          "shrink-0 rounded-full border px-3 py-1.5 text-xs font-medium transition-colors " +
          (posicaoAtiva === "Todas"
            ? "border-ink bg-ink text-bg"
            : "border-line text-ink-muted hover:border-ink-muted hover:text-ink")
        }
      >
        Todas
      </button>
      {POSICOES.map((posicao) => {
        const ativa = posicaoAtiva === posicao;
        return (
          <button
            key={posicao}
            onClick={() => aoTrocar(posicao)}
            className={
              "flex shrink-0 items-center gap-1.5 rounded-full border px-3 py-1.5 text-xs font-medium transition-colors " +
              (ativa
                ? "border-transparent text-bg"
                : "border-line text-ink-muted hover:border-ink-muted hover:text-ink")
            }
            style={ativa ? { backgroundColor: COR_POSICAO[posicao] } : undefined}
          >
            <span
              className="h-2 w-2 rounded-full"
              style={{ backgroundColor: COR_POSICAO[posicao] }}
            />
            {posicao}
          </button>
        );
      })}
    </div>
  );
}
'@ | Set-Content -Path "src\components\FiltroPosicao.tsx" -Encoding utf8

@'
import type { Jogador } from "../types/jogador";
import { COR_POSICAO } from "../types/jogador";

interface Props {
  jogadores: Jogador[];
}

function formatarValor(valor: number | null): string {
  if (valor === null) return "-";
  if (valor >= 1000000) return "\u20ac" + (valor / 1000000).toFixed(1) + "M";
  if (valor >= 1000) return "\u20ac" + (valor / 1000).toFixed(0) + "K";
  return "\u20ac" + valor;
}

function Badge({ posicao }: { posicao: Jogador["posicao"] }) {
  return (
    <span
      className="inline-flex items-center gap-1.5 rounded-full px-2 py-0.5 text-xs font-medium"
      style={{
        backgroundColor: COR_POSICAO[posicao] + "26",
        color: COR_POSICAO[posicao],
      }}
    >
      <span
        className="h-1.5 w-1.5 rounded-full"
        style={{ backgroundColor: COR_POSICAO[posicao] }}
      />
      {posicao}
    </span>
  );
}

export function TabelaJogadores({ jogadores }: Props) {
  if (jogadores.length === 0) {
    return (
      <div className="rounded-lg border border-line bg-surface px-6 py-12 text-center">
        <p className="font-display text-2xl tracking-wide text-ink-muted">
          Nenhum jogador em campo
        </p>
        <p className="mt-1 text-sm text-ink-muted">
          Ajuste os filtros de liga ou posicao pra ver resultados.
        </p>
      </div>
    );
  }

  return (
    <>
      {/* Tabela - telas medias/grandes */}
      <div className="hidden overflow-x-auto rounded-lg border border-line md:block">
        <table className="w-full text-left text-sm">
          <thead className="bg-surface text-xs uppercase tracking-wider text-ink-muted">
            <tr>
              <th className="px-4 py-3 font-medium">Jogador</th>
              <th className="px-4 py-3 font-medium">Posicao</th>
              <th className="px-4 py-3 font-medium text-right">Idade</th>
              <th className="px-4 py-3 font-medium">Clube</th>
              <th className="px-4 py-3 text-right font-medium">Gols</th>
              <th className="px-4 py-3 text-right font-medium">Assist.</th>
              <th className="px-4 py-3 text-right font-medium">Valor</th>
              <th className="px-4 py-3 text-right font-medium">Score</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-line">
            {jogadores.map((j, i) => (
              <tr
                key={j.name + "-" + j.liga}
                className={
                  "transition-colors hover:bg-surface-hover " +
                  (i % 2 === 1 ? "bg-surface/40" : "")
                }
              >
                <td className="px-4 py-3 font-medium text-ink">{j.name}</td>
                <td className="px-4 py-3">
                  <Badge posicao={j.posicao} />
                </td>
                <td className="px-4 py-3 text-right font-mono text-ink-muted">
                  {j.idade ?? "-"}
                </td>
                <td className="px-4 py-3 text-ink-muted">{j.clube}</td>
                <td className="px-4 py-3 text-right font-mono tabular-nums text-ink">
                  {j.gols}
                </td>
                <td className="px-4 py-3 text-right font-mono tabular-nums text-ink">
                  {j.assistencias}
                </td>
                <td className="px-4 py-3 text-right font-mono tabular-nums text-ink-muted">
                  {formatarValor(j.valorMercado)}
                </td>
                <td className="px-4 py-3 text-right font-mono text-base font-semibold tabular-nums text-amber">
                  {j.score.toFixed(2)}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Cartoes - telas pequenas (mobile) */}
      <div className="flex flex-col gap-2 md:hidden">
        {jogadores.map((j) => (
          <div
            key={j.name + "-" + j.liga}
            className="rounded-lg border border-line bg-surface p-4"
          >
            <div className="flex items-start justify-between gap-2">
              <div>
                <p className="font-medium text-ink">{j.name}</p>
                <p className="text-xs text-ink-muted">{j.clube}</p>
              </div>
              <span className="font-mono text-lg font-semibold tabular-nums text-amber">
                {j.score.toFixed(2)}
              </span>
            </div>
            <div className="mt-3 flex flex-wrap items-center gap-3">
              <Badge posicao={j.posicao} />
              <span className="text-xs text-ink-muted">
                {j.idade ?? "-"} anos
              </span>
              <span className="font-mono text-xs text-ink-muted">
                {j.gols}G {j.assistencias}A
              </span>
              <span className="font-mono text-xs text-ink-muted">
                {formatarValor(j.valorMercado)}
              </span>
            </div>
          </div>
        ))}
      </div>
    </>
  );
}
'@ | Set-Content -Path "src\components\TabelaJogadores.tsx" -Encoding utf8

@'
import { useMemo, useState } from "react";
import { useJogadores } from "./hooks/useJogadores";
import { AbasLiga } from "./components/AbasLiga";
import { FiltroPosicao } from "./components/FiltroPosicao";
import { TabelaJogadores } from "./components/TabelaJogadores";
import type { Liga, Posicao } from "./types/jogador";

function App() {
  const { jogadores, carregando, erro } = useJogadores();
  const [ligaAtiva, setLigaAtiva] = useState<Liga>("premier_league");
  const [posicaoAtiva, setPosicaoAtiva] = useState<Posicao | "Todas">("Todas");

  const jogadoresFiltrados = useMemo(() => {
    return jogadores
      .filter((j) => j.liga === ligaAtiva)
      .filter((j) => posicaoAtiva === "Todas" || j.posicao === posicaoAtiva)
      .sort((a, b) => b.score - a.score);
  }, [jogadores, ligaAtiva, posicaoAtiva]);

  const ligaTemDadosIncompletos = useMemo(() => {
    const daLiga = jogadores.filter((j) => j.liga === ligaAtiva);
    return daLiga.length > 0 && daLiga.some((j) => !j.dadosCompletos);
  }, [jogadores, ligaAtiva]);

  if (carregando) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-bg font-mono text-sm text-ink-muted">
        carregando dossie...
      </div>
    );
  }

  if (erro) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-bg font-mono text-sm text-red-400">
        erro ao carregar dados: {erro}
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-bg">
      <header className="border-b border-line px-4 py-6 sm:px-8">
        <div className="mx-auto max-w-6xl">
          <p className="font-mono text-xs uppercase tracking-[0.3em] text-amber">
            Dossie de Scouting
          </p>
          <h1 className="font-display text-4xl tracking-wide text-ink sm:text-5xl">
            SCOUTPY
          </h1>
          <p className="mt-1 text-sm text-ink-muted">
            Descoberta de talentos Sub-23 em 6 ligas do futebol mundial
          </p>
        </div>
      </header>

      <main className="mx-auto max-w-6xl px-4 py-6 sm:px-8">
        <AbasLiga ligaAtiva={ligaAtiva} aoTrocar={setLigaAtiva} />

        {ligaTemDadosIncompletos && (
          <p className="mt-4 rounded-md border border-amber-soft bg-amber-soft px-3 py-2 text-xs text-amber">
            Aviso: essa liga usa uma fonte de dados alternativa e criterio mais
            fraco (sem partidas/minutos reais).
          </p>
        )}

        <div className="my-5 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
          <FiltroPosicao posicaoAtiva={posicaoAtiva} aoTrocar={setPosicaoAtiva} />
          <span className="font-mono text-xs text-ink-muted">
            {jogadoresFiltrados.length} jogador(es)
          </span>
        </div>

        <TabelaJogadores jogadores={jogadoresFiltrados} />
      </main>
    </div>
  );
}

export default App;
'@ | Set-Content -Path "src\App.tsx" -Encoding utf8

Write-Host "Redesign aplicado com sucesso nos 7 arquivos."