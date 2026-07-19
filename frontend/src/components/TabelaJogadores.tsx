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
