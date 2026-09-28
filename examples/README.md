# Exemples

Trois films faits avec la méthode de ce dépôt, le 2026-09-28, pour la landing page d'[Entrepreneurs 2.0](https://entrepreneurs2-0.com).

| Dossier | Film | Durée | Idée |
| --- | --- | --- | --- |
| `le-devis/` | Le devis | 43 s | Le devis qui gonfle, la panne, l'attente, puis « Stop. » et l'IA qui fait tout. Vidéo finale : `le-devis/le-devis.mp4`. |
| `traduire/` | Traduire | 50 s | Pendant des décennies il fallait parler la langue de l'ordinateur (le code) et payer un traducteur ; aujourd'hui il parle français. |
| `cette-video/` | Cette vidéo | 45 s | Le film parle de lui-même : un lecteur vidéo qui se contient à l'infini, un générique où tous les noms sont « aucun », la vraie onde de la voix. |

Chaque dossier contient :

- `frame.md` : la charte (couleurs par rôle, typographie, composants, interdits).
- `STORYBOARD.md` : le film découpé en séquences, minuté mot par mot sur la voix.
- `compositions/frames/*.html` : une séquence animée par fichier, écrite par un sous-agent.
- `assemble.sh` : l'assemblage (scripts HeyGen, transitions, puis la couche orchestrateur : fond papier, flash de lumière, iris, son).
- `build-audio.sh` (+ `assets/audio/sfx-events.json`) : le montage de la voix et le mixage (musique, bruitages).
- `index.html` : le résultat de l'assemblage, tel qu'il a servi au rendu.

## Refaire un rendu

Les voix (ElevenLabs), la musique, les bruitages et les polices ne sont pas inclus. Pour refaire un rendu d'un exemple :

1. Dépose ta voix dans `assets/audio/` sous le nom attendu par `build-audio.sh` (`voix-C-devis.mp3`, `voix-B-traduire.mp3` ou `voix-A-cette-video.mp3`). Avec une autre voix, recale d'abord les temps avec `.claude/skills/motion-design/scripts/onsets.py` et mets à jour le storyboard et les séquences.
2. Mets les polices dans `assets/fonts/` (Instrument Sans 400/500/600/700, Space Mono 400/700, Big Shoulders 800 en `.woff2`, voir `.claude/skills/motion-design/references/method.md`).
3. Indique où sont tes bruitages et ta musique : `export SFX_DIR=/chemin/vers/bruitages MUSIC=/chemin/vers/musique.mp3` (les noms de fichiers attendus sont dans `assets/audio/sfx-events.json` : `pop.wav`, `click.wav`, `click-soft.wav`, `whoosh.wav`, `whoosh-short.wav`, `typing.wav`, `key-press.wav`, `ping.wav`, `error.wav`).
4. Depuis le dossier de l'exemple : `./build-audio.sh && ./assemble.sh`, puis `HYPERFRAMES_NO_TELEMETRY=1 DO_NOT_TRACK=1 HYPERFRAMES_SKIP_SKILLS=1 HYPERFRAMES_NO_UPDATE_CHECK=1 npx hyperframes render -q high -o renders/film.mp4`.

Le plus simple reste de demander à Claude Code, ouvert à la racine du dépôt : « Refais le rendu de l'exemple traduire avec ma voix ».
