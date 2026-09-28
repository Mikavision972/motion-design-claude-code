# Mentions tierces

Tout ce dépôt est sous licence MIT (`LICENSE`, © 2026 Colin Blain), **sauf** les éléments tiers listés ici, qui gardent leur propre licence.

## Skills HyperFrames (HeyGen)

- **Auteur** : HeyGen, Inc. (© 2026 HeyGen, Inc.)
- **Licence** : Apache License 2.0, texte complet dans `.claude/skills/LICENSE-HEYGEN-APACHE-2.0` (récupéré sur la branche `main` du dépôt amont, identique à celui du commit audité).
- **Source** : https://github.com/heygen-com/hyperframes, dossier `skills/`
- **Commit audité** : `93ab2899f13a1120002986793a7b11b657841b69` (court : `93ab289`, repris dans `.claude/skills/AUDITED_COMMIT.txt`), audit de sécurité du 2026-09-28.
- **Dossiers copiés** dans `.claude/skills/` : `hyperframes`, `hyperframes-animation`, `hyperframes-audio`, `hyperframes-cli`, `hyperframes-core`, `hyperframes-creative`, `hyperframes-keyframes`, `hyperframes-registry`, `media-use`, `product-launch-video`.
- **Non tiers** : `.claude/skills/motion-design/` (le skill de ce dépôt, MIT) et `.claude/skills/AUDITED_COMMIT.txt`.

### Fichiers modifiés (Apache 2.0, section 4 b)

La copie n'est pas identique à l'amont : elle a été durcie pendant l'audit du 2026-09-28, dans l'atelier de travail où l'audit a été fait (nommé `motion-launch`, d'où ce nom dans les consignes ajoutées). Tous les autres fichiers sont identiques octet pour octet à ceux du commit `93ab289` (vérifié par `diff -r` le 2026-09-28).

| Fichier | Changement |
|---|---|
| `hyperframes/SKILL.md` | description resserrée (point d'entrée de l'atelier, plus « obligatoire pour toute vidéo ») ; plus de mise à jour du logiciel sans le « oui » explicite de l'utilisateur ; `npx hyperframes skills update` remplacé par la règle du commit audité figé |
| `hyperframes-animation/adapters/animate-text.md` | installation du skill tiers `animate-text` (non audité, sans licence) retirée ; les effets se codent en GSAP |
| `hyperframes-animation/adapters/lottie.md` | `@lottiefiles/dotlottie-web` épinglé en `0.80.0` |
| `hyperframes-cli/SKILL.md` | envois `feedback` (notes, recherches ratées) vers un canal public remplacés par une règle d'interdiction |
| `hyperframes-cli/references/preview-render.md` | section `feedback` remplacée par la même règle |
| `hyperframes-creative/references/design-picker.md` | petit serveur local limité à `127.0.0.1` au lieu de tout le réseau |
| `hyperframes-registry/SKILL.md` | envoi des recherches ratées remplacé par la règle d'interdiction |
| `media-use/scripts/eval.mjs` | supprimé |

### Contenus embarqués dans ces skills

- `media-use/audio/assets/sfx/*.mp3` : bruitages de [Pixabay](https://pixabay.com/sound-effects/), [Pixabay Content License](https://pixabay.com/service/license-summary/) (détail dans `CREDITS.md` du même dossier). Ce sont les bruitages utilisés par le mixage de la méthode.
- `hyperframes-creative/frame-presets/code-editorial/fonts/` : EB Garamond, Inter, JetBrains Mono, SIL Open Font License 1.1 (textes de licence dans le même dossier).

## Éléments que tu récupères toi-même (non inclus)

- **Polices** : Instrument Sans, Space Mono et Big Shoulders, [Google Fonts](https://fonts.google.com), SIL Open Font License 1.1. Téléchargées dans chaque projet (commandes dans `.claude/skills/motion-design/references/method.md`).
- **Logos d'outils** : [Simple Icons](https://simpleicons.org), licence CC0 pour les fichiers SVG. Les logos restent des marques de leurs propriétaires : ne les utilise que pour montrer l'outil tel qu'il est.
- **Musique** : un morceau sous licence CC0 (domaine public) de ton choix, par exemple [HoliznaCC0](https://freemusicarchive.org/music/holiznacc0/) sur Free Music Archive. Vérifie la licence de chaque morceau.
- **Voix** : générée par toi sur [ElevenLabs](https://elevenlabs.io), soumise à leurs conditions (forfait payant obligatoire pour un usage commercial).

## Patterns (`patterns/PATTERNS.md`)

Texte original tiré de l'analyse image par image de 56 films du portfolio public de l'agence 1600.agency (https://www.1600.agency/portfolio). Aucune image ni vidéo n'est reproduite ici : les films appartiennent à leurs auteurs, les noms cités sont ceux des marques clientes, qui appartiennent à leurs propriétaires. Ce dépôt n'est affilié ni à 1600.agency, ni à HeyGen, ni à ElevenLabs.
