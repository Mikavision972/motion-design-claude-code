# Motion design avec Claude Code

Des films de lancement façon agence (40 à 50 s, 16:9, voix off, texte qui arrive mot par mot sur la voix) faits avec
Claude Code et HyperFrames, le moteur vidéo open source de HeyGen, sans savoir coder. Tu écris le script avec Claude,
tu génères la voix, tu choisis une direction de storyboard sur image, puis Claude construit le film séquence par
séquence et le vérifie avant de te le rendre.

Tout ce qu'il faut est dans ce dépôt : la méthode sous forme de skill Claude Code, la grammaire de storyboard tirée de
films d'agence décortiqués au dixième de seconde, les modèles de directions, de charte et de storyboard, les scripts de
minutage et de contrôle, les patterns tirés de 56 films d'agence, des films d'exemple, et les skills officiels HeyGen,
audités et figés.

**Le guide pas à pas**, avec les 5 étapes, leurs prompts et les pièges :
[le guide Notion](https://www.notion.so/3e9bd65124ec816e9c39f5c1b3cc8b67).

**Pour qui** : fondateurs, indépendants, créateurs et marketeurs qui veulent une vidéo de lancement de qualité agence
pour une landing page, LinkedIn ou YouTube, sans passer par une agence ni apprendre After Effects.

**Prérequis** :

- [Claude Code](https://claude.com/claude-code), avec un abonnement Claude Pro ou Max (Max conseillé : un film lance
  une dizaine de sous-agents, des instances de Claude qui travaillent en parallèle).
- Node 22 ou plus récent (l'environnement qui fait tourner HyperFrames).
- ffmpeg (l'outil qui découpe et assemble le son et la vidéo).
- Python 3 avec le paquet `openai-whisper` (la transcription mot par mot, en local sur ta machine) et le paquet
  `playwright` (le rendu des images de style en PNG, à l'étape du storyboard).
- Un compte [ElevenLabs](https://elevenlabs.io) pour la voix (forfait payant obligatoire pour un usage commercial).

Pas besoin de savoir coder : Claude installe, écrit et vérifie. Tu décides et tu valides.

---

## Installation en 1 prompt

Ouvre Claude Code et colle ce prompt :

```
Installe le dépôt motion-design-claude-code sur ma machine. Fais tout toi-même avec tes outils, sans me demander d'ouvrir un terminal.

1. Clone https://github.com/cblain100-prog/motion-design-claude-code dans ~/motion-design-claude-code (ou dans le dossier que je t'indique) et place-toi dedans.
2. Vérifie les prérequis et dis-moi ce qui manque : Node 22 ou plus (node --version), ffmpeg et ffprobe, Python 3, le paquet openai-whisper (python3 -c "import whisper"). Si ffmpeg manque sur Mac, installe-le avec Homebrew. Si openai-whisper manque, installe-le avec python3 -m pip install -U openai-whisper (préviens-moi avant : le téléchargement est gros). Si le paquet playwright manque (python3 -c "import playwright"), installe-le avec python3 -m pip install playwright puis python3 -m playwright install chromium.
3. Lance npm ci (HyperFrames est figé en version 0.8.82 par le fichier package-lock.json).
4. Crée le fichier .env vide à la racine avec cp .env.example .env. Il est voulu : ne le supprime jamais et n'y écris aucune clé.
5. Préfixe chaque commande npx hyperframes par HYPERFRAMES_NO_TELEMETRY=1 DO_NOT_TRACK=1 HYPERFRAMES_SKIP_SKILLS=1 HYPERFRAMES_NO_UPDATE_CHECK=1, puis lance dans l'ordre : npx hyperframes telemetry disable, npx hyperframes doctor, npx hyperframes browser ensure.
6. Lis AGENTS.md et .claude/skills/motion-design/SKILL.md, puis résume-moi en 5 lignes ce qui est installé et ce que je dois préparer avant mon premier film.

Ne lance jamais npx hyperframes skills update, upgrade, feedback, publish, ni npx skills add.
```

Ensuite, ouvre Claude Code **dans ce dossier** (`cd ~/motion-design-claude-code && claude`) : c'est là que le skill et
les garde-fous se chargent. Puis demande par exemple :

> Je veux un motion design de lancement de 45 secondes pour mon produit. Voici ma page : https://...

---

## La méthode en 5 étapes

Les 5 étapes de la vidéo YouTube, avec leur prompt à copier (deux pour l'étape 4). Le guide pas à pas, avec les
explications, les exemples et les pièges : **[le guide Notion](https://www.notion.so/3e9bd65124ec816e9c39f5c1b3cc8b67)**.
Claude s'arrête pour ta validation après le script, après la voix, après le choix de la direction, après le storyboard
et après la première séquence.

### 1. Récupérer la bibliothèque de skills

```
Installe dans ce dossier les skills HyperFrames de HeyGen (github.com/heygen-com/hyperframes) et récupère la méthode de github.com/cblain100-prog/motion-design-claude-code. Audite d'abord ce que font les skills avant de les installer, et dis-moi ce qui touche à mes fichiers ou au réseau.
```

Deux bibliothèques : les skills officiels HyperFrames de HeyGen (Claude écrit chaque scène comme une page web,
HyperFrames la filme image par image) et cette méthode. Un skill, c'est du code qui tourne sur ta machine : fais-le
auditer avant, dans un dossier à part de tes autres projets. Ce dépôt contient déjà les skills HeyGen audités et figés
(voir [Sécurité](#sécurité)) : le prompt d'installation ci-dessus fait tout en une fois.

### 2. Créer le script

```
On imagine ensemble le script d'une vidéo animée de 40 secondes pour [ton offre]. Propose-moi 5 pistes vraiment différentes : le concept, la première phrase, la dernière phrase. On ne fabrique rien tant que je n'ai pas choisi.
```

Claude écrit en entier les pistes que tu gardes (110 à 130 mots, 40 à 50 s de voix) et tu corriges mot à mot. Les
meilleures phrases viennent de tes appels clients, mot pour mot. Le premier mot nomme ta cible ou sa douleur, chaque
phrase se lit à l'écran sans le son, une seule action à la fin.

### 3. Créer la voix

```
Voici la voix. Relève le moment exact de chaque mot et range tout le minutage dans un seul fichier : chaque animation tombera sur un mot, jamais après.
```

La voix se fait sur ElevenLabs, modèle Eleven v3 (le seul qui lit les balises `[pause]`, `[sarcastic]`, `[sighs]`),
chiffres en toutes lettres, 3 ou 4 essais : tu déposes le meilleur dans le projet. C'est l'horloge du film : Whisper
transcrit mot par mot sur ta machine, `onsets.py` recale chaque début de phrase sur le vrai son (Whisper seul se décale
de plusieurs centaines de millisecondes), et tout le minutage tient dans un seul fichier, `onsets.json`.

### 4. Créer le storyboard et les prompts pour l'animation

```
Propose-moi 3 directions de storyboard vraiment différentes pour ce script, avec 3 images de style chacune (une image figée du futur film, en qualité finale). Applique la grammaire de STORYBOARD-CRAFT.md.
```

```
Écris le storyboard complet de la direction A : une séquence de 3 à 6 secondes par idée, une étape toutes les 0,5 seconde, la caméra, l'objet qui fait le pont vers la séquence suivante, le bruitage. Puis découpe-le en un prompt par séquence.
```

Le cœur de la méthode. Claude applique [`patterns/STORYBOARD-CRAFT.md`](patterns/STORYBOARD-CRAFT.md), la grammaire tirée
de six films d'agence décortiqués au dixième de seconde, propose trois directions avec trois images de style chacune
([`templates/DIRECTIONS-TEMPLATE.md`](templates/DIRECTIONS-TEMPLATE.md)) et tu choisis sur image. Puis il écrit le
storyboard séquence par séquence ([`templates/STORYBOARD-TEMPLATE.md`](templates/STORYBOARD-TEMPLATE.md)) : une caméra
qui ne s'arrête jamais, un objet-pont à chaque transition, un passage de relais écrit à chaque couture, la grille de
contrôle en 15 points, puis un prompt par séquence. Exemple complet : [`examples/C-le-devis-v7a/`](examples/C-le-devis-v7a/).

### 5. Lancer l'animation, et vérifier

```
Lance un agent par séquence, en parallèle. Puis assemble, fais le rendu, et vérifie avant de me dire que c'est fini : les images noires, une planche contact toutes les 0,5 seconde, et les raccords entre séquences image par image.
```

Un sous-agent par séquence, en parallèle, après une première séquence que tu valides ; HyperFrames assemble et fait le
rendu, et la musique se choisit à la fin, en 3 ou 4 options sur la même voix, sans refaire l'image. Rien n'est fini
avant la vérification du vrai fichier (images noires, planche contact, raccords image par image) ; après une coupure de
session, Claude relance seulement les séquences qui manquent.

Ensuite, si tu veux : des variantes sur la même voix (`.claude/skills/motion-design/references/variants.md`) et le film
sur ton site, lecture muette automatique et cadre de couleur (`references/landing-integration.md`, composant React
`templates/LaunchFilm.tsx`). Détail complet pour l'agent, commande par commande : `.claude/skills/motion-design/SKILL.md`
et son dossier `references/`.

## Les patterns, en résumé

Tirés de l'analyse image par image de 56 films de lancement du portfolio de l'agence 1600.agency (Notion, Slack,
Calendly, lemlist, Crisp, Aikido…). Bibliothèque complète, recettes et grille de contrôle :
[`patterns/PATTERNS.md`](patterns/PATTERNS.md). Comment écrire le storyboard au dixième de seconde (caméra,
objets-ponts, profondeur, calage sur la voix, gabarit, grille en 15 points), d'après six de ces films refaits à
l'envers : [`patterns/STORYBOARD-CRAFT.md`](patterns/STORYBOARD-CRAFT.md).

- **Lisible sans le son** : une composition par phrase, texte petit et centré qui arrive mot par mot sur la voix.
- **Le premier mot nomme la cible ou sa douleur**, et la première image est ce mot seul, jamais le logo.
- **Une couleur d'accent par rôle** (le plus souvent une seule pour tout le film), un seul mot mis en valeur par phrase,
  un seul mécanisme (la pastille qui se trace).
- **Deux mondes** : un fond sombre pour la douleur, un fond clair pour la solution, avec un pivot entre les deux.
- **La douleur montrée dans les outils de la cible** (Gmail, tableur, site), et son volume par un essaim d'objets.
- **Des mots géants seulement aux pics**, des chiffres qui roulent, un produit montré par des gestes.
- **Le rythme se compte en événements** : quelque chose de neuf toutes les 0,5 à 1 s, une caméra qui ne s'arrête
  jamais, des éléments qui arrivent trop grands et flous puis se posent, trois niveaux de profondeur.
- **Continu** : avec une voix narrative, 0 à 4 coupes franches et 0 à 2 fondus ; tout le reste passe par un objet qui
  change de rôle (l'objet-pont) ou par la caméra.
- **Une carte de fin avec un seul bouton** qu'un curseur vient cliquer après une hésitation, puis 2 à 3 s d'image qui
  vit encore avant le noir.

## Les pièges connus

- Whisper seul se décale : toujours recaler les mots sur l'énergie du son (`onsets.py`).
- Claude se trompe dans les additions de durées : un seul endroit fait foi (le storyboard), vérifié par un script.
- Une séquence n'est pas masquée avant son début : tout élément doit partir invisible.
- Ne jamais animer l'espacement des lettres : le rendu image par image fait trembler le texte.
- Un fondu entre deux séquences claires passe par le gris si rien n'est posé dessous : d'où le fond papier.
- Une séquence prolongée sous l'iris doit prolonger tout ce qu'elle contient, sinon l'image devient noire.
- Une coupe franche ne doit jamais tomber sur une image vide : la séquence qui arrive est visible dès sa première image.
- Un dossier de séquence au-delà de 48 Ko bloque la fabrication : 1 à 3 recettes par séquence.
- La même mise en page pendant 10 s paraît lente, même si le contenu change : une image différente toutes les 2 à 3 s.
- Assez de plans ne suffit pas : sans caméra qui bouge ni événement toutes les demi-secondes, le film fait encore
  « vidéo d'IA ». D'où le storyboard écrit avant d'animer.
- Deux agents, une couture : sans passage de relais écrit, l'image saute. La dernière image d'une séquence
  (`handoff_out`) est recopiée mot pour mot comme première image de la suivante (`handoff_in`).
- Un modèle HTML interne (`<template id>`) posé à côté du bloc racine d'une séquence : elle reste noire, et seul
  `npx hyperframes validate` le signale. Il vit dans le bloc racine.
- Jamais `style.visibility = "visible"` dans une séquence : l'élément s'affiche par-dessus tout le film. Toujours
  `"inherit"`.
- Une coupure de session coupe les agents en plein travail : relancer seulement les séquences manquantes ou cassées
  (`check-frames.py`), et demander aux agents d'écrire tôt une première version complète.
- Toujours contrôler le vrai rendu, pas seulement l'aperçu.

Liste complète et corrections : `.claude/skills/motion-design/references/pitfalls.md`.

## Sécurité

Les skills officiels de HeyGen ont été audités le 2026-09-28 avant d'être inclus ici. Rien de malveillant, mais
plusieurs consignes envoyaient des données ou mettaient le logiciel à jour sans demander. Ce qui a été fait :

- **Skills figés** au commit audité `93ab289` (`.claude/skills/AUDITED_COMMIT.txt`), avec les passages à risque
  neutralisés (envois de « feedback » vers un canal public, mises à jour automatiques, installation d'un skill tiers
  non audité, serveur local ouvert sur le réseau). La liste exacte est dans `THIRD_PARTY_NOTICES.md`.
- **Version figée** : HyperFrames 0.8.82, toutes dépendances verrouillées par `package-lock.json`. Jamais de
  `@latest`.
- **Télémétrie coupée** : variables d'environnement dans `.claude/settings.json` et `npx hyperframes telemetry disable`
  à l'installation.
- **`.env` vide à la racine** : un des skills HeyGen charge le premier fichier `.env` qu'il trouve en remontant les
  dossiers ; celui-ci arrête la recherche, aucune clé d'un dossier parent n'est lue.
- **Commandes interdites** dans `AGENTS.md` (feedback, publish, cloud, upgrade, skills update…) sauf demande explicite.
- **Aucune clé d'API nécessaire** : la voix se fait sur le site d'ElevenLabs, tout le reste tourne sur ta machine.

## Polices, musique, bruitages

Aucune police, aucune musique ni aucune voix n'est fournie pour tes films (seuls les skills HeyGen embarquent leurs
propres fichiers d'exemple).

- **Polices** : Instrument Sans, Space Mono et Big Shoulders, sur [Google Fonts](https://fonts.google.com), licence SIL
  Open Font License. Claude les télécharge dans chaque projet au bon format (commandes dans
  `.claude/skills/motion-design/references/method.md`). Tu peux aussi les récupérer à la main sur Google Fonts.
- **Musique** : des morceaux sous licence CC0 (domaine public, usage commercial sans mention obligatoire), sur Free
  Music Archive : [HoliznaCC0](https://freemusicarchive.org/music/holiznacc0/),
  [Loyalty Freak Music](https://freemusicarchive.org/music/Loyalty_Freak_Music/) et
  [Komiku](https://freemusicarchive.org/music/Komiku/) (seulement ses morceaux marqués CC0). Vérifie la licence sur la
  page de chaque morceau. Les dix morceaux utilisés pour le devis, avec leurs liens, sont dans
  `.claude/skills/motion-design/references/music.md`.
- **Bruitages** : ceux fournis avec le skill `media-use` de HeyGen (Pixabay, licence Pixabay Content License).
- **Logos d'outils** : [Simple Icons](https://simpleicons.org), fichiers en CC0 ; les logos restent des marques de
  leurs propriétaires.

## Exemples

Des films faits avec cette méthode pour la landing page d'Entrepreneurs 2.0 sont dans `examples/` (détail et marche à
suivre pour refaire un rendu : [`examples/README.md`](examples/README.md)) :

- `examples/le-devis/` : « Le devis » (43 s). La vidéo finale est dans le dossier (`le-devis.mp4`).
- `examples/traduire/` : « Traduire » (50 s), la métaphore de la langue : le code, le traducteur, l'ordinateur qui parle français.
- `examples/cette-video/` : « Cette vidéo » (45 s), le film qui parle de lui-même (un lecteur vidéo qui se contient à l'infini, un générique, la vraie onde de la voix).
- `examples/C-le-devis-v7a/` : « Le devis est le décor » (43,2 s), le devis refait à partir d'un vrai storyboard, le film du début de la vidéo YouTube. Le devis devient le lieu du film, la caméra le parcourt ligne par ligne. On y trouve les trois directions proposées, la charte, le storyboard complet (10 séquences, 27 plans, passages de relais), la grille de contrôle passée point par point, le code exécutable du décor et le script de rendu des images de style.

Les trois premiers contiennent leur charte `frame.md`, leur `STORYBOARD.md` minuté mot par mot, leurs séquences HTML, leur `assemble.sh` et leur `build-audio.sh` ; le quatrième montre l'étape 4 (directions, storyboard, grille de contrôle). Les voix, la musique, les bruitages et les polices ne sont pas inclus : pour refaire un rendu, dépose ta voix et suis `examples/README.md`.

Le devis a ensuite été décliné en trois options sur la même voix, dans `examples/le-devis-options/` : « Poli » (la première version mise en ligne sur le site, vidéo incluse : `poli/le-devis-poli.mp4`), « Nuit » (tout en sombre) et « Le bureau » (vue du dessus d'un bureau, vrais objets), avec les quatre musiques dans `poli/build-music-options.py`.

## Structure du dépôt

- `README.md` : ce fichier.
- `AGENTS.md` : les garde-fous lus par Claude Code à chaque session.
- `THIRD_PARTY_NOTICES.md` : licences et modifications des éléments tiers.
- `LICENSE` : MIT.
- `package.json` et `package-lock.json` : HyperFrames 0.8.82 figé.
- `.env.example` : à copier en `.env` (vide, c'est voulu).
- `.claude/settings.json` : télémétrie coupée.
- `.claude/skills/motion-design/` : le skill de la méthode (`SKILL.md`, `references/` dont `music.md`, `variants.md` et `landing-integration.md`, `templates/` dont `STORYBOARD.md`, `build-music-options.py` et `LaunchFilm.tsx`, `scripts/` dont `onsets.py`, `render-styleframes.py`, `analyze-music.py` et `check-frames.py`).
- `.claude/skills/product-launch-video/` et 9 autres skills officiels HeyGen, audités et figés, avec leur licence.
- `patterns/PATTERNS.md` : les patterns des 56 films et la grille de contrôle.
- `patterns/STORYBOARD-CRAFT.md` : la grammaire de storyboard (10 lois, chiffres, recettes GSAP, format, grille en 15 points).
- `templates/` : `DIRECTIONS-TEMPLATE.md` (les trois directions et leurs images de style) et `STORYBOARD-TEMPLATE.md` (l'en-tête du film et le bloc d'une séquence, avec un exemple rempli).
- `examples/` : les trois films d'exemple (charte, storyboard, séquences, scripts d'assemblage et de son), `examples/le-devis-options/` : les trois options du devis et ses quatre musiques, et `examples/C-le-devis-v7a/` : le devis refait à partir d'un vrai storyboard.
- `<ton-projet>/` : un dossier par film, créé par le skill.

## Crédits et licences

- **Ce dépôt** (méthode, skill `motion-design`, modèles, scripts, patterns, grammaire de storyboard, documentation) : licence MIT, © 2026
  Colin Blain. Voir `LICENSE`.
- **Skills HyperFrames** : © HeyGen, Inc., licence Apache 2.0, source https://github.com/heygen-com/hyperframes,
  copie du commit audité avec les modifications listées dans `THIRD_PARTY_NOTICES.md`.
- **Patterns** : analyse des films publics de 1600.agency (https://www.1600.agency/portfolio). Aucune image ni vidéo
  reproduite ; les films appartiennent à leurs auteurs, les marques citées à leurs propriétaires.
- **Polices** : SIL Open Font License. **Bruitages** : Pixabay Content License. **Logos** : Simple Icons (CC0),
  marques de leurs propriétaires. **Voix** : conditions d'ElevenLabs.
- Ce dépôt n'est affilié ni à HeyGen, ni à ElevenLabs, ni à 1600.agency.

## Auteur

**Colin Blain**, [Entrepreneurs 2.0](https://entrepreneurs2-0.com).
