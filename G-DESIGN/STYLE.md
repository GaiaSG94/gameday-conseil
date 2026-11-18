# STYLE — Conseil « Quartier 3D »

Style validé par Gaia le 2026-11-18 (V4 : *Foule* et *Stickers* fusionnées, en 3D). Référence : `planches/v4/01-quartier-3d.html`. Toutes les pages le suivent à la lettre.

## Principe

Le quartier est une petite scène 3D en pâte claire cernée d'encre. Les six voisins sont les personnages ; l'interface est faite de **stickers** posés par-dessus la scène. On ne voit l'orange que sur ce que propose ou choisit le joueur.

## Palette

| Rôle | Nom | Hex | Règle |
|---|---|---|---|
| Fond | Crème | `#f3eee2` | Avec un grain multiplié (bruit fractal, opacité ≈ 16 %). |
| Encre | Encre | `#151515` | Texte, contours 3D, ombres pleines des bulles, boutons principaux. |
| Accent | Orange | `#ff5a1f` | Uniquement la motion proposée ou choisie, le cadre de sélection et l'ombre du bouton principal. Jamais décoratif. |
| Pâte | Clay | `#f6f2e9` | Toutes les figurines et les objets neutres en 3D. |
| Blanc | Blanc | `#ffffff` | Stickers, bulles, bord des pastilles. |
| Pastilles des voisins | Ines `#f6c9b5` · Theo `#bfd6e8` · Ruth `#d9cdea` · Sam `#bfe0cc` · Odile `#f3dc9a` · Kofi `#d5d6d8` | — | Toujours pâles, toujours attachées à un voisin (sous ses pieds, dans sa bulle, sur son résultat). Jamais en aplat d'interface. |

## Typographie

Deux familles intégrées dans chaque fichier : **Archivo** variable (OFL) et **DM Mono** (OFL).

| Niveau | Police | Taille / graisse | Usage |
|---|---|---|---|
| Titre | Archivo 900, largeur 100 %, approche −3 %, capitales | 50 px (36–64 selon la page) | Le sujet du jour, un score. |
| Chiffre héros | Archivo 900 | 64–96 px | `3/6`, série. |
| Consigne | Archivo 500 + 800 | 14,5 px | Une phrase ; la partie actionnable en gras. |
| Bulle | Archivo 550 | 13 px / 1,24 | Ce que dit un voisin. |
| Sticker-pilule | Archivo 850 / 450 | 15 px / 11,5 px | Titre et détail d'une motion. |
| Méta | DM Mono 500, capitales, +6 % | 9,5–11 px | Séance, date, compteurs, étiquettes. |

## Grille

Zone de jeu : 740 × 640 px dans le post. Marges latérales de 28 px. Méta en haut à 22 px, titre à 40 px, consigne à 94 px. Barre d'action en bas à 18 px, motions à 80 px du bas. La scène 3D occupe tout le fond ; les stickers se posent dessus.

## Composants

- **Figurine** : capsule et tête ronde, deux yeux, un seul accessoire par voisin. Rendu cartoon en trois tons, contour encre (épaisseur 0,065 en unités locales), ombre douce au sol. Elle se tient sur sa **pastille** (disque blanc, intérieur à sa couleur).
- **Bulle** : blanche, rayon 14, contour encre 1,6 px avec une ombre pleine de 3 px dessous, et une pointe vers le voisin. Elle suit la tête du voisin à l'écran. Le pied de bulle porte la pastille et `NOM · RÔLE` en DM Mono.
- **Étiquette au-dessus de la tête** : une bulle courte (`Yes` / `No`, `…`) centrée au-dessus du voisin.
- **Sticker-pilule** : blanc, bord blanc de 5 px, ombre portée douce, légèrement tourné (−1,5° / +1° / −0,6°). Une pastille noire porte la lettre.
- **Cadre de sélection** : contour orange de 1,5 px avec 4 poignées blanches de 8 px et un curseur noir. Il sert pour la motion choisie et pour le mot-clé du titre.
- **Bouton principal** : pilule encre, texte blanc en capitales, ombre pleine orange de 4 px dessous.
- **Tag** : DM Mono sur crème, contour encre de 1,4 px, rayon 3.
- **Le terrain** : dalle beige `#e8dcc2`, piquets d'encre, herbes folles tant que rien n'est proposé. Ce qu'on propose y est construit **en orange**.

## Mouvement

- Caméra : un balancement lent (±0,06 rad, période d'environ 25 s). Jamais de rotation libre.
- Figurines : une respiration (2 % de leur hauteur), la tête qui oscille un peu.
- Choisir une motion : la construction apparaît avec un ressort (amortissement e^(−7t), environ 0,6 s), l'ancienne se replie, et les voisins sautillent en vague.
- Résultat : ceux qui soutiennent lèvent le bras, ceux qui refusent tournent le dos.
- Survol d'un sticker : il se redresse et monte de 2 px.

## États

| Élément | Repos | Survol | Choisi | Désactivé |
|---|---|---|---|---|
| Sticker-pilule | Tourné, pastille noire | Droit, −2 px | Droit, ×1,04, pastille orange, cadre de sélection | Opacité 40 %, pas de cadre |
| Bouton principal | Encre + ombre orange | −1 px | Enfoncé (ombre 2 px) | Crème, contour encre en pointillé |
| Terrain | Herbes folles | — | Construction orange | — |
| Figurine | Respire | — | Sautille une fois | (résultat) bras levé ou dos tourné |

## Technique

Three.js 0.170.0 (MIT) est intégré dans chaque planche (`_src/vendor/`). La scène est partagée par toutes les pages (`_src/gen4.py`) et se configure par page avec `window.CONSEIL_OPTS` : caméra, cible, motion construite, qui dit oui, positions, terrain affiché ou non. Sans WebGL, un message remplace la scène.
