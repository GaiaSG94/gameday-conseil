# DESIGN — journal Conseil

Les versions sont datées et ne sont jamais écrasées. Ce journal est tenu par le designer uniquement.

## V4 — 2026-11-18 · Foule + Stickers fusionnées, en 3D (style validé, pages déclinées en revue)

Retour de Gaia sur la V3 : *Foule* et *Stickers* sont « très bien ». Demande : passer en 3D et fusionner les deux.

- `planches/v4/01-quartier-3d.html` : une scène 3D en temps réel (Three.js 0.170.0, licence MIT, intégré dans le fichier, aucune requête réseau).
  - De *Foule* : les six voisins autour du terrain, chacun avec sa bulle cernée (les bulles suivent la tête de leur voisin), des passants grisés, et la motion choisie **construite en orange sur le terrain** (parterres, terrain de jeu avec paniers, ou les deux), avec un rebond.
  - De *Stickers* : le cadre de sélection orange à poignées sur le titre et sur la motion choisie, les motions en stickers-pilules, et une **pastille-sticker** de couleur sous chaque figurine, rappelée dans sa bulle.
  - Rendu : pâte claire en trois tons (rendu cartoon) avec contour encre, ombres douces, caméra qui respire, voisins qui bougent légèrement et sautillent quand on change de motion.
- Le kit montre le casting rendu en 3D par le même moteur.
- Testé : capture en Chromium headless (rendu logiciel SwiftShader) et dans le navigateur de l'app avec le GPU ; un clic sur « Community garden » construit bien les parterres. Aucune erreur dans la console.

### V4 · déclinaison (2026-11-18)

Gaia a validé le style. J'ai écrit `STYLE.md` (palette, typographie, grille, composants, mouvement, états, technique) et décliné les trois autres pages avec la même scène 3D, configurée pour chaque page :
- `planches/v4/02-post.html` — **Post** : la scène vivante, le terrain encore en friche, et des bulles « … » au-dessus de chaque voisin (sans rien dévoiler). Un seul bouton, *Take the chair*, avec la preuve sociale.
- `planches/v4/03-carte-de-fin.html` — **Carte de fin** : ceux qui soutiennent la motion lèvent le bras, les autres tournent le dos, chacun avec une étiquette Yes/No et sa raison. Un gros sticker `3/6`, la meilleure motion du jour (5/6), la répartition du quartier (la barre du joueur en orange), et une accroche à commentaire qui nomme un voisin (*Ruth said no. Make your case.*), suivie du compte à rebours.
- `planches/v4/04-series.html` — **Séries & classement** : les six « habitués » en rang, chacun avec son `x/7` de soutien au joueur ; la série (7, record 12, moyennes) ; les 7 dernières séances avec leur score en pastilles.

Moteur : `gen4.py` est désormais paramétrable (`window.CONSEIL_OPTS` : caméra, cible, motion construite, qui dit oui, positions, terrain affiché ou non), et l'arrivée du bras levé est animée. Pages générées par `_src/gen5.py`.

Hypothèses (questions de `PAGES.md` encore ouvertes) : 3 motions, score sur 6, un vote par jour, casting récurrent, pas de classement nominatif.

Pour le jeu Devvit, Three.js serait embarqué dans le bundle (environ 690 Ko non compressé ; on pourra l'alléger plus tard en ne gardant que ce qu'on utilise).

Sources : `_src/gen4.py` (réutilise `gen3.py`) et `_src/vendor/three-0.170.0.module.min.js` avec sa licence.

## V3 — 2026-11-18 · exploration à partir des références jeu (Foule + Stickers retenues)

Références : catégorie `narratif-jeu` du hub (voir `REFS.md`, section V3). Les V1 et V2 habillaient un formulaire ; la V3 construit **un monde, des personnages et un objet qu'on manipule**.

- **Un casting commun** : six voisins dessinés en SVG, reconnaissables chacun à un seul détail (toque, enfant, canne et chignon, casque et sacoche, arrosoir, casquette). C'est le socle de l'identité ; seuls le rendu et la scène changent selon la direction.
  - `planches/v3/01-foule.html` — *Foule* (Don't Look Up, Gapsy) : personnages au trait autour du terrain vu en iso, chacun avec sa bulle, passants grisés. La motion choisie se **dessine sur le terrain** en orange. Boutons à ombre pleine décalée.
  - `planches/v3/02-maquette.html` — *Maquette* (Dairy Food, Matchball, Raben Rifaie) : pâté de maisons en maquette iso (boulangerie, rue, terrain en pointillé), voisins en **figurines de bois peint**. Les motions sont des pièces de maquette ; celle qu'on choisit tombe sur le terrain avec un rebond.
  - `planches/v3/03-stickers.html` — *Stickers* (Gemeos) : voisins en **stickers découpés** sur pastille pâle, motions en stickers-pilules un peu de travers ; celle qu'on choisit se redresse et prend un **cadre de sélection** orange avec ses poignées et un curseur.
- Desktop seul, avec le kit d'identité sous l'écran. Polices : Archivo et DM Mono, intégrées dans chaque fichier.

Sources : `_src/gen3.py` (`python3 G-DESIGN/_src/gen3.py G-DESIGN/planches/v3`).

En attente : choix d'une direction, puis les questions produit de `PAGES.md` (dont la nouvelle question 5 sur le casting récurrent).

## V2 — 2026-11-18 · nouvelle exploration (rejetée : toujours du slop, pas d'identité)

Retour de Gaia : même verdict que pour la V1. Gaia part chercher des références dans la catégorie jeu. Prochaine version : à partir de ces références, pas avant.

Diagnostic du designer : les deux tours habillent la même structure de formulaire web (titre, liste de citations, 3 options, bouton) avec une texture. Il n'y a ni monde, ni personnages, ni objet de jeu : rien qui se lise comme un jeu.

Retour de Gaia sur la V1 : « slop IA ». La matière, les couleurs et les motifs n'avaient pas été travaillés et il n'y avait pas d'identité visuelle. Le mobile n'est pas exigé par le hackathon.

Changements :
- **Desktop seul** : chaque planche est l'écran 1440 × 900 (le post dans le feed), suivi en dessous du **kit d'identité** de la direction (matière, couleur, typo, motifs). Le cadre mobile est supprimé.
- On part d'**objets réels d'une réunion de quartier** au lieu de cartes d'interface :
  - `planches/v2/01-feutre.html` — *Feutre* : le paperboard (bloc quadrillé sur chevalet, pince et restes de feuilles arrachées), avec des traits au feutre marine qui tremblent un peu (cercle, bâtons, séparateurs, bouton gribouillé). Le joueur vote avec une **gommette orange**, comme dans un vote par gommettes.
  - `planches/v2/02-riso.html` — *Riso* : une affiche de réunion en risographie deux encres (bleu, orange en trame), avec grain, décalage de calage, surimpression et scotch sur un mur. Les motions sont des **languettes à arracher** : celle qu'on choisit se détache.
  - `planches/v2/03-tampon.html` — *Tampon* (s'écarte du brief) : un formulaire de mairie vert pâle perforé, les avis tapés à la machine dans un registre, la série sur une carte poinçonnée et un **coup de tampon « MOVED »** rouge quand on choisit.
- Typo : **Archivo** variable (largeurs 62–125 %, graisses 100–900, OFL) et **DM Mono** (OFL), sous-ensemblées et intégrées en base64. Ubuntu Sans est abandonnée.
- Les motions restent cliquables : gommette posée, languette arrachée ou tampon appliqué.

Sources : `_src/gen2.py` (`python3 G-DESIGN/_src/gen2.py G-DESIGN/planches/v2`). La V1 est conservée telle quelle.

En attente : choix d'une direction et réponses aux questions produit de `PAGES.md`.

## V1 — 2026-11-18 · exploration (rejetée : slop, pas d'identité)

Livré :
- `PAGES.md` : 4 pages proposées (Post, Jeu, Carte de fin, Séries & classement) et 4 questions produit ouvertes.
- `REFS.md` : Concept Studio et Teko ouverts et décodés à partir des styles calculés.
- 3 planches de la page principale **Jeu**, chacune avec le cadre desktop 1440 × 900 (motion B choisie, vote prêt) et le cadre mobile 390 × 844 (aucune motion choisie). Les motions sont cliquables dans les deux cadres.
  - `planches/v1/01-paperboard.html` — *Paperboard* : la direction du brief. Kraft, notes punaisées légèrement de travers, titres condensés marine, orange réservé à la motion choisie, série comptée en bâtons.
  - `planches/v1/02-affiche.html` — *Affiche* : bandeau marine avec le sujet du jour en très grand titre condensé, aplats crème / marine / orange sans texture, avis numérotés 01–06 séparés par des filets.
  - `planches/v1/03-proces-verbal.html` — *Procès-verbal* : s'écarte du brief. Fond clair, mono pour la méta, titre en minuscules, voisins assis autour d'une table ovale avec le joueur à la place du président, accent vert d'encre `#1f6b4f`.

Données de démo (fictives, écrites à la main) : séance 47, « The empty lot on Alder Street », 6 voisins (Ines, Theo, Ruth, Sam, Odile, Kofi), 3 motions, série de 6 jours, 1 284 participants du jour. Aucune personne réelle ni marque.

Décisions :
- La page principale est **Jeu** : c'est là que la règle doit se comprendre en 5 secondes.
- **Police embarquée** : Ubuntu Sans (axe de largeur 75–100 %, donc une seule famille pour les titres condensés et les citations) et Ubuntu Sans Mono. Elles sont sous-ensemblées en latin, encodées en woff2 et intégrées en base64 dans chaque planche (aucune requête réseau, compatible avec la CSP de Devvit). Licence : Ubuntu Font Licence 1.0, libre de redistribution et d'intégration.
- Le cadre hôte du post (barre, rail, actions) est volontairement gris et générique : aucun logo ni couleur de tiers.
- Le bouton « Call the vote » reste inactif (« Pick a motion ») tant qu'aucune motion n'est choisie.
- Un seul accent par direction : orange (01, 02) ou vert (03).

Sources : `_src/gen.py` génère les 3 fichiers (`python3 G-DESIGN/_src/gen.py G-DESIGN/planches/v1`). Les fichiers HTML livrés sont autonomes et s'ouvrent d'un double-clic.

En attente : validation de `PAGES.md`, réponses aux 4 questions produit, choix d'une direction.
