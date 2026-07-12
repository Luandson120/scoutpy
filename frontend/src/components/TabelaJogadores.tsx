import type { Jogador } from "../types/jogador";

interface Props {
  jogadores: Jogador[];
}

function formatarValor(valor: number | null): string {
  if (valor === null) return "-";
  if (valor >= 1000000) return "â‚¬" + (valor / 1000000).toFixed(1) + "M";
  if (valor >= 1000) return "â‚¬" + (valor / 1000).toFixed(0) + "K";
  return "â‚¬" + valor;
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
