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
