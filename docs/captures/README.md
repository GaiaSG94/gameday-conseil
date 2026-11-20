# Captures — planche verrouillée vs produit

Preuves de l'étape « implémentation du design » (07b) : à gauche la planche
verrouillée `G-DESIGN/planches/v4/`, à droite l'écran réel du produit
(build local, données du jour chargées, 1440×900).

| Fichier | Page |
|---|---|
| `01-jeu-cote-a-cote.png` | Jeu (page principale) |
| `02-post-cote-a-cote.png` | Post (inline) |
| `03-carte-de-fin-cote-a-cote.png` | Carte de fin |
| `04-series-cote-a-cote.png` | Séries & quartier |
| `ecarts.json` | écarts mesurés (position, taille) de chaque élément clé, une ligne par élément |

## Reproduire

```sh
npm run build
node --experimental-strip-types --import ./tools/preview/resolve-ts.mjs tools/preview/server.ts
python tools/preview/compare.py <dossier-sortie> 5177
```

Le serveur de prévisualisation rejoue la vraie logique serveur sur un store
mémoire (générateur déterministe, une semaine de votes creds) : les captures
montrent le produit tel qu'il tourne, pas une maquette.

## Lire les écarts

- `dx`, `dy`, `dw`, `dh` : décalage du produit par rapport à la planche, en px,
  mesuré sur la planche 740×640 commune aux deux côtés.
- Les positions 3D (bulles, étiquettes, tag) varient de ±2 à ±4 px d'une
  capture à l'autre : la caméra respire (période ~25 s).
- Les écarts de largeur sur les textes longs viennent du contenu réel du jour
  (les répliques sont plus longues que les maquettes de la planche) : voir
  `DESIGN.md` § « Revue d'implémentation » du dossier projet.
