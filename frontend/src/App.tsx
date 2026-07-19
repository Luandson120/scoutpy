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
