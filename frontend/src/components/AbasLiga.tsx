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
