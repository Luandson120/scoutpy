New-Item -ItemType Directory -Force -Path "src\types", "src\hooks", "src\components" | Out-Null

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
        if (!res.ok) throw new Error(`Erro ao carregar dados: ${res.status}`);
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
import { LIGAS, NOME_LIGA, type Liga } from "../types/jogador";

interface Props {
  ligaAtiva: Liga;
  aoTrocar: (liga: Liga) => void;
}

export function AbasLiga({ ligaAtiva, aoTrocar }: Props) {
  return (
    <div className="flex flex-wrap gap-2 border-b border-neutral-200 pb-3">
      {LIGAS.map((liga) => {
        const ativa = liga === ligaAtiva;
        return (
          <button
            key={liga}
            onClick={() => aoTrocar(liga)}
            className={`rounded-full px-4 py-1.5 text-sm font-medium transition-colors ${
              ativa
                ? "bg-neutral-900 text-white"
                : "bg-neutral-100 text-neutral-600 hover:bg-neutral-200"
            }`}
          >
            {NOME_LIGA[liga]}
          </button>
        );
      })}
    </div>
  );
}
'@ | Set-Content -Path "src\components\AbasLiga.tsx" -Encoding utf8

@'
import { POSICOES, type Posicao } from "../types/jogador";

interface Props {
  posicaoAtiva: Posicao | "Todas";
  aoTrocar: (posicao: Posicao | "Todas") => void;
}

export function FiltroPosicao({ posicaoAtiva, aoTrocar }: Props) {
  const opcoes: (Posicao | "Todas")[] = ["Todas", ...POSICOES];

  return (
    <select
      value={posicaoAtiva}
      onChange={(e) => aoTrocar(e.target.value as Posicao | "Todas")}
      className="rounded-lg border border-neutral-300 px-3 py-2 text-sm text-neutral-800 focus:outline-none focus:ring-2 focus:ring-neutral-900"
    >
      {opcoes.map((posicao) => (
        <option key={posicao} value={posicao}>
          {posicao}
        </option>
      ))}
    </select>
  );
}
'@ | Set-Content -Path "src\components\FiltroPosicao.tsx" -Encoding utf8

@'
import type { Jogador } from "../types/jogador";

interface Props {
  jogadores: Jogador[];
}

function formatarValor(valor: number | null): string {
  if (valor === null) return "-";
  if (valor >= 1000000) return "€" + (valor / 1000000).toFixed(1) + "M";
  if (valor >= 1000) return "€" + (valor / 1000).toFixed(0) + "K";
  return "€" + valor;
}

export function TabelaJogadores({ jogadores }: Props) {
  if (jogadores.length === 0) {
    return (
      <p className="py-8 text-center text-sm text-neutral-500">
        Nenhum jogador encontrado com esse filtro.
      </p>
    );
  }

  return (
    <div className="overflow-x-auto rounded-lg border border-neutral-200">
      <table className="w-full text-left text-sm">
        <thead className="bg-neutral-50 text-neutral-600">
          <tr>
            <th className="px-4 py-2 font-medium">Jogador</th>
            <th className="px-4 py-2 font-medium">Posicao</th>
            <th className="px-4 py-2 font-medium">Idade</th>
            <th className="px-4 py-2 font-medium">Clube</th>
            <th className="px-4 py-2 font-medium text-right">Gols</th>
            <th className="px-4 py-2 font-medium text-right">Assist.</th>
            <th className="px-4 py-2 font-medium text-right">Valor</th>
            <th className="px-4 py-2 font-medium text-right">Score</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-neutral-100">
          {jogadores.map((j) => (
            <tr key={j.name + "-" + j.liga} className="hover:bg-neutral-50">
              <td className="px-4 py-2 font-medium text-neutral-900">{j.name}</td>
              <td className="px-4 py-2 text-neutral-600">{j.posicao}</td>
              <td className="px-4 py-2 text-neutral-600">{j.idade ?? "-"}</td>
              <td className="px-4 py-2 text-neutral-600">{j.clube}</td>
              <td className="px-4 py-2 text-right text-neutral-600">{j.gols}</td>
              <td className="px-4 py-2 text-right text-neutral-600">{j.assistencias}</td>
              <td className="px-4 py-2 text-right text-neutral-600">{formatarValor(j.valorMercado)}</td>
              <td className="px-4 py-2 text-right font-semibold text-neutral-900">{j.score.toFixed(2)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
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
      <div className="flex min-h-screen items-center justify-center text-neutral-500">
        Carregando dados...
      </div>
    );
  }

  if (erro) {
    return (
      <div className="flex min-h-screen items-center justify-center text-red-600">
        Erro ao carregar dados: {erro}
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-white px-6 py-8">
      <div className="mx-auto max-w-5xl">
        <header className="mb-6">
          <h1 className="text-2xl font-bold text-neutral-900">
            ScoutPy - Jovens Talentos Sub-23
          </h1>
          <p className="mt-1 text-sm text-neutral-500">
            Premier League, La Liga, Bundesliga, Serie A, Ligue 1 e Brasileirao
          </p>
        </header>

        <AbasLiga ligaAtiva={ligaAtiva} aoTrocar={setLigaAtiva} />

        {ligaTemDadosIncompletos && (
          <p className="mt-3 rounded-md bg-amber-50 px-3 py-2 text-sm text-amber-700">
            Aviso: essa liga usa uma fonte de dados alternativa e criterio mais fraco
            (sem partidas/minutos reais).
          </p>
        )}

        <div className="my-4 flex items-center justify-between">
          <span className="text-sm text-neutral-500">
            {jogadoresFiltrados.length} jogador(es) sub-23 elegivel(is)
          </span>
          <FiltroPosicao posicaoAtiva={posicaoAtiva} aoTrocar={setPosicaoAtiva} />
        </div>

        <TabelaJogadores jogadores={jogadoresFiltrados} />
      </div>
    </div>
  );
}

export default App;
'@ | Set-Content -Path "src\App.tsx" -Encoding utf8

Write-Host "Todos os 6 arquivos foram recriados com sucesso."