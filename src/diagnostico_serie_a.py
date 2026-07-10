
import soccerdata as sd

fbref = sd.FBref()  # sem filtro de liga - pega tudo que o FBRef reconhece

print("Listando todas as competições reconhecidas pelo FBRef...")
todas_ligas = fbref.read_leagues()

print(f"\nTotal de competições encontradas: {len(todas_ligas)}")

# Procura por qualquer coisa que contenha "Serie A" ou "Série A" no índice
import re

filtro = todas_ligas[todas_ligas.index.str.contains("Serie", case=False, na=False)]
print(f"\nCompetições com 'Serie' no nome:")
print(filtro.to_string())
