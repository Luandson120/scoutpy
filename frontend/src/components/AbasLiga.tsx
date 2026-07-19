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
