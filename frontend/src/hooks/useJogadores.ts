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
