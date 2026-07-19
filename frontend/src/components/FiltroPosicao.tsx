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
