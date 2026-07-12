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
