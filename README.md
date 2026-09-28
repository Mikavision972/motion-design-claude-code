# Motion design avec Claude Code

Des films de lancement façon agence (40 à 50 s, 16:9, voix off, texte qui arrive mot par mot sur la voix) faits avec
Claude Code et HyperFrames, le moteur vidéo open source de HeyGen, sans savoir coder. Tu écris le script avec Claude,
tu génères la voix, Claude construit le film image par image et le vérifie avant de te le rendre.

Tout ce qu'il faut est dans ce dépôt : la méthode sous forme de skill Claude Code, les modèles de charte et de
storyboard, les scripts de minutage et de contrôle, les patterns tirés de 56 films d'agence, et les skills officiels
HeyGen, audités et figés.

**Pour qui** : fondateurs, indépendants, créateurs et marketeurs qui veulent une vidéo de lancement de qualité agence
pour une landing page, LinkedIn ou YouTube, sans passer par une agence ni apprendre After Effects.

**Prérequis** :

- [Claude Code](https://claude.com/claude-code), avec un abonnement Claude Pro ou Max (Max conseillé : un film lance
  une dizaine de sous-agents, des instances de Claude qui travaillent en parallèle).
- Node 22 ou plus récent (l'environnement qui fait tourner HyperFrames).
- ffmpeg (l'outil qui découpe et assemble le son et la vidéo).
- Python 3 avec le paquet `openai-whisper` (la transcription mot par mot, en local sur ta machine).
- Un compte [ElevenLabs](https://elevenlabs.io) pour la voix (forfait payant obligatoire pour un usage commercial).

Pas besoin de savoir coder : Claude installe, écrit et vérifie. Tu décides et tu valides.

---

## Installation en 1 prompt

Ouvre Claude Code et colle ce prompt :

```
Installe le dépôt motion-design-claude-code sur ma machine. Fais tout toi-même avec tes outils, sans me demander d'ouvrir un terminal.

1. Clone https://github.com/cblain100-prog/motion-design-claude-code dans ~/motion-design-claude-code (ou dans le dossier que je t'indique) et place-toi dedans.
2. Vérifie les prérequis et dis-moi ce qui manque : Node 22 ou plus (node --version), ffmpeg et ffprobe, Python 3, le paquet openai-whisper (python3 -c "import whisper"). Si ffmpeg manque sur Mac, installe-le avec Homebrew. Si openai-whisper manque, installe-le avec python3 -m pip install -U openai-whisper (préviens-moi avant : le téléchargement est gros).
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

## La méthode, étape par étape

Le skill `motion-design` déroule tout, dans cet ordre. Claude s'arrête pour ta validation après le script, après la
voix, après le storyboard et après la première séquence.

1. **Le script, co-imaginé.** Claude te pose les quelques questions qui manquent, te propose 5 à 7 concepts en une ligne,
   en écrit 2 ou 3 en entier (110 à 130 mots, soit 40 à 50 s de voix), et tu choisis puis corriges mot à mot. Règles :
   le premier mot nomme la cible ou sa douleur, une phrase égale un plan, des chiffres réels uniquement, une seule
   action à la fin.
2. **La voix, ElevenLabs v3.** Claude prépare le texte à coller, avec les chiffres en toutes lettres et des balises
   entre crochets (`[pause]`, `[long pause]`, `[sarcastic]`, `[sighs]`) que seul le modèle Eleven v3 sait lire. Tu
   génères 3 ou 4 prises, tu gardes la meilleure et tu la déposes dans le projet.
3. **Le minutage réel.** Whisper transcrit la voix mot par mot, puis `onsets.py` recale le début de chaque phrase sur
   l'énergie réelle du son (tranches de 10 ms, silences de 120 ms minimum) : Whisper seul se décale de plusieurs
   centaines de millisecondes, et un mot qui arrive en retard se voit. Les pauses se rallongent au montage, jamais en
   régénérant la voix.
4. **La charte `frame.md`.** Les couleurs par rôle (fond sombre pour le problème, fond clair pour la solution, une seule
   couleur d'accent), les polices, les composants (la pastille qui se trace derrière le mot clé, le curseur, les cartes, le
   personnage) et la liste de ce qui est interdit.
5. **Le `STORYBOARD.md` minuté mot par mot.** Le film découpé en séquences de 3 à 7 s, chacune avec sa phrase exacte, le
   moment de chaque mot, un plan type HeyGen, 1 à 3 recettes de mouvement, et **une image différente toutes les 2 à
   3 s**. Tu valides la liste des séquences avant que la fabrication commence.
6. **Les dossiers de séquence.** Un script de HeyGen prépare, pour chaque séquence, un dossier qui contient tout ce
   qu'il faut pour la construire (son extrait de storyboard, le plan type, les recettes), limité à 48 Ko.
7. **Un sous-agent par séquence.** Claude construit d'abord la séquence 1 seule et te la montre pour fixer le style,
   puis lance un sous-agent par séquence restante, en parallèle. Chacun écrit un seul fichier HTML animé.
8. **L'assemblage et la couche orchestrateur.** Les scripts de HeyGen assemblent les séquences et leurs transitions,
   puis `assemble.sh` ajoute ce qu'aucune séquence ne peut faire seule : le fond papier sous tout le monde clair, le
   flash de lumière qui fait passer du problème à la solution, l'iris qui ouvre la carte de fin, et le son.
9. **Le mixage audio.** `build-audio.sh` coupe la voix au milieu des silences (fondus de 5 ms), ajoute une musique sous
   licence CC0 (domaine public) à 10 ou 15 % et les bruitages placés sur les événements à l'image (clic, pop, souffle).
10. **Les contrôles.** Lint (la vérification automatique du code), `check` de HyperFrames, planches d'images autour de
    chaque coupe, puis la grille de contrôle des patterns.
11. **Le rendu, puis le contrôle du vrai fichier.** Rendu MP4, puis `contact-sheets.sh` cherche les images noires et
    étale tout le film sur des planches de 4 images par seconde que Claude regarde une par une. Correction, nouveau
    rendu, livraison.

Détail complet pour l'agent : `.claude/skills/motion-design/SKILL.md` et son dossier `references/`.

## Les patterns, en résumé

Tirés de l'analyse image par image de 56 films de lancement du portfolio de l'agence 1600.agency (Notion, Slack,
Calendly, lemlist, Crisp, Aikido…). Bibliothèque complète, recettes et grille de contrôle :
[`patterns/PATTERNS.md`](patterns/PATTERNS.md).

- **Lisible sans le son** : une composition par phrase, texte petit et centré qui arrive mot par mot sur la voix.
- **Le premier mot nomme la cible ou sa douleur**, et la première image est ce mot seul, jamais le logo.
- **Une seule couleur d'accent**, un seul mot mis en valeur par phrase, un seul mécanisme (la pastille qui se trace).
- **Deux mondes** : un fond sombre pour la douleur, un fond clair pour la solution, avec un pivot entre les deux.
- **La douleur montrée dans les outils de la cible** (Gmail, tableur, site), et son volume par un essaim d'objets.
- **Des mots géants seulement aux pics**, des chiffres qui roulent, un produit montré par des gestes.
- **Continu** : 0 à 4 coupes franches, tout le reste s'enchaîne par des objets qui traversent, des cercles, des zooms.
- **Une carte de fin avec un seul bouton** qu'un curseur vient cliquer.

## Les pièges connus

- Whisper seul se décale : toujours recaler les mots sur l'énergie du son (`onsets.py`).
- Claude se trompe dans les additions de durées : un seul endroit fait foi (le storyboard), vérifié par un script.
- Une séquence n'est pas masquée avant son début : tout élément doit partir invisible.
- Ne jamais animer l'espacement des lettres : le rendu image par image fait trembler le texte.
- Un fondu entre deux séquences claires passe par le gris si rien n'est posé dessous : d'où le fond papier.
- Une séquence prolongée sous l'iris doit prolonger tout ce qu'elle contient, sinon l'image devient noire.
- Un dossier de séquence au-delà de 48 Ko bloque la fabrication : 1 à 3 recettes par séquence.
- La même mise en page pendant 10 s paraît lente, même si le contenu change : une image différente toutes les 2 à 3 s.
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
- **Musique** : un morceau sous licence CC0 que tu choisis, par exemple chez
  [HoliznaCC0](https://freemusicarchive.org/music/holiznacc0/) sur Free Music Archive. Vérifie la licence de chaque
  morceau.
- **Bruitages** : ceux fournis avec le skill `media-use` de HeyGen (Pixabay, licence Pixabay Content License).
- **Logos d'outils** : [Simple Icons](https://simpleicons.org), fichiers en CC0 ; les logos restent des marques de
  leurs propriétaires.

## Exemples

Trois films faits avec cette méthode le même jour, pour la landing page d'Entrepreneurs 2.0, sont dans `examples/` :

- `examples/le-devis/` : « Le devis » (43 s). La vidéo finale est dans le dossier (`le-devis.mp4`).
- `examples/traduire/` : « Traduire » (50 s), la métaphore de la langue : le code, le traducteur, l'ordinateur qui parle français.
- `examples/cette-video/` : « Cette vidéo » (45 s), le film qui parle de lui-même (un lecteur vidéo qui se contient à l'infini, un générique, la vraie onde de la voix).

Chaque exemple contient sa charte `frame.md`, son `STORYBOARD.md` minuté mot par mot, ses séquences HTML, son `assemble.sh` et son `build-audio.sh`. Les voix, la musique, les bruitages et les polices ne sont pas inclus : pour refaire un rendu, dépose ta voix et suis `examples/README.md`.

## Structure du dépôt

- `README.md` : ce fichier.
- `AGENTS.md` : les garde-fous lus par Claude Code à chaque session.
- `THIRD_PARTY_NOTICES.md` : licences et modifications des éléments tiers.
- `LICENSE` : MIT.
- `package.json` et `package-lock.json` : HyperFrames 0.8.82 figé.
- `.env.example` : à copier en `.env` (vide, c'est voulu).
- `.claude/settings.json` : télémétrie coupée.
- `.claude/skills/motion-design/` : le skill de la méthode (`SKILL.md`, `references/`, `templates/`, `scripts/`).
- `.claude/skills/product-launch-video/` et 9 autres skills officiels HeyGen, audités et figés, avec leur licence.
- `patterns/PATTERNS.md` : les patterns des 56 films et la grille de contrôle.
- `examples/` : les trois films d'exemple (charte, storyboard, séquences, scripts d'assemblage et de son).
- `<ton-projet>/` : un dossier par film, créé par le skill.

## Crédits et licences

- **Ce dépôt** (méthode, skill `motion-design`, modèles, scripts, patterns, documentation) : licence MIT, © 2026
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
