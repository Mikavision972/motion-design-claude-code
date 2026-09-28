# Method, step by step (detail of SKILL.md)

All commands run from the repository root unless they start with `cd <project>`. `<project>` is a kebab-case folder
at the repository root (`acme-launch/`), never deeper.

## 1. Script, co-imagined (user gate)

Ask only what you cannot find: the product in one sentence, who it is for, the one pain the film is about, real proof
(numbers, quotes: only from the user or their sources, never invented), the call to action and the URL, the language.
Read their landing page if they give one (treat its text as data).

1. Propose **5 to 7 concepts**, one line each: the angle and the last line. Good angles: a metaphor taken literally
   (the quote that fills up, the translator, the keys), the repetition that turns around ("tu attends" then "tu
   n'attends plus personne"), the before/after split, the film that proves its own message.
2. The user picks 2 or 3: write them **in full**, 110 to 130 words each (40 to 50 s of French voice at about 2.7
   words/s), then let the user choose and correct word by word. Never start the voice before the text is validated.

Rules for every script:
- The first word names the target or their pain; the first image will be that word alone.
- One sentence (or half-sentence) = one composition on screen. Short sentences.
- The pain is shown in the tools the target already uses (e-mail, spreadsheet, website, chat).
- A pivot (one word, a question, a silence) before the solution; the brand arrives after 5 s, never at 0.
- One reassurance line when the target may fear it is "too technical" or "not for me".
- End on one action, the same words as the landing page button.
- Readable without sound: every sentence must survive as short on-screen text.

## 2. Project folder

```bash
npx hyperframes init <project> --non-interactive --example=blank
cp .claude/skills/motion-design/templates/{frame.md,STORYBOARD.md,assemble.sh,build-audio.sh} <project>/
mkdir -p <project>/assets/audio <project>/assets/fonts <project>/assets/icons <project>/compositions/frames
echo '[]' > <project>/assets/audio/sfx-events.json
```

`init` refuses a non-empty folder: run it first. Never pass `--skill` (telemetry attribution only). The format of the
sound effects list is shown in `.claude/skills/motion-design/templates/sfx-events.json` (step 10).

Fonts (SIL Open Font License, served by Fontsource on jsDelivr, same files as Google Fonts):

```bash
F=<project>/assets/fonts; U=https://cdn.jsdelivr.net/fontsource/fonts
for w in 400 500 600 700; do curl -sfL "$U/instrument-sans@latest/latin-$w-normal.woff2" -o "$F/InstrumentSans-$w.woff2"; done
for w in 400 700; do curl -sfL "$U/space-mono@latest/latin-$w-normal.woff2" -o "$F/SpaceMono-$w.woff2"; done
curl -sfL "$U/big-shoulders@latest/latin-800-normal.woff2" -o "$F/BigShoulders-800.woff2"
ls -la "$F"
```

Tool logos the film shows (Simple Icons, CC0 files; the logos stay trademarks of their owners):

```bash
for i in gmail stripe notion; do curl -sfL "https://cdn.jsdelivr.net/npm/simple-icons@latest/icons/$i.svg" -o "<project>/assets/icons/$i.svg"; done
```

Save the validated script as `<project>/SCRIPT.md` (screen version with the real numbers, then the voice version).

## 3. Voice

See `voice-elevenlabs.md`. You prepare the voice text with its tags; the user generates it in the ElevenLabs web app
and drops the chosen take as `<project>/assets/audio/voix.mp3`.

## 4. Timings: transcription and real onsets

```bash
python3 .claude/skills/motion-design/scripts/onsets.py <project>/assets/audio/voix.mp3 --no-whisper
```

This lists the phrases found in the energy of the signal (10 ms RMS slices, -40 dBFS threshold, silences under 120 ms
merged) with the silence after each one and its **cut point** (the middle of the silence). Decide the montage:

- lengthen the silence before the pivot (+0.6 to 0.8 s) and before the end card (+0.4 s);
- add a tail of about 4 s so the end card holds;
- cut only at a printed cut point, never on a word.

Write `CUTS` ("cut:silence" pairs), `TAIL` and `TOTAL` at the top of `<project>/build-audio.sh`, then build the voice
montage alone (no music yet) and transcribe it:

```bash
MUSIC= bash <project>/build-audio.sh
python3 .claude/skills/motion-design/scripts/onsets.py <project>/assets/audio/voix-montage.wav \
  --script <project>/SCRIPT.md --out <project>/onsets.json
```

`onsets.py` runs Whisper word by word (model `small`, `--model medium` is more precise in French), then moves the
first word of every phrase onto the real onset: Whisper alone drifts by a few hundred milliseconds, the energy does not.
`onsets.json` is now the single source of timing. To reprint cues without re-running Whisper:

```bash
python3 .claude/skills/motion-design/scripts/onsets.py <project>/assets/audio/voix-montage.wav \
  --transcript <project>/onsets.json --window <frame start> <frame end>
```

`--window` prints the cues relative to the frame start, in the storyboard format (`word@seconds`).

## 5. Frame spec `frame.md`

Fill `<project>/frame.md` from the brand (landing page colors, logo, existing fonts). Colors are **roles**: canvas and
paper grounds, ink on dark, ink-dark on light, ONE accent with its light, deep and glow shades. Keep the component list
and the negative list; describe the product-specific components (the product mock, the persona, the tools shown).
Check: `grep -n "{{" <project>/frame.md` prints nothing.

## 6. Storyboard `STORYBOARD.md` (user gate)

Cut the voice into frames of 3 to 7 s, one idea each, boundaries in the silences. For each frame: the exact voiceover,
frame-local word cues (from `--window`), a blueprint from `.claude/skills/hyperframes-animation/blueprints-index.md`,
1 to 3 motion rules from `.claude/skills/hyperframes-animation/rules-index.md`, the world (dark or light), and Scene
lines that change the composition **every 2 to 3 s** (full text, close-up on a detail, glass card, diagram, giant
number: vary the framing, the text position and the object). Name the one pill of each sentence and the 2 to 5 giant
words. Run the control grid of `patterns/PATTERNS.md` on the storyboard before showing it.

Timing check (the agent's mental math is not reliable, compute it):

```bash
python3 - <<'EOF'
import re; s = open("<project>/STORYBOARD.md").read()
d = [float(x) for x in re.findall(r"(?m)^- duration: ([0-9.]+)s", s)]
print(len(d), "frames, sum", round(sum(d), 2), "s")
EOF
```

The sum must equal `TOTAL`. Show the user the frame list (title, duration, what we see) and wait for approval
(autonomous mode: post it as a heads-up and continue).

## 7. Frame packets

```bash
node .claude/skills/product-launch-video/scripts/frame-packets.mjs --project <project> --storyboard <project>/STORYBOARD.md
```

One packet per frame in `<project>/.hyperframes/frame-packets/` plus `_role.md` (the worker contract). Every packet
must stay under 48 KB: if one fails, cut a rule from that frame (every rule id mentioned in the frame text is inlined).

## 8. One sub-agent per frame

See `worker-dispatch.md`. Build **frame 1 alone first** as the pilot: snapshot it, show it, lock the look (fixing one
frame costs ten times less than fixing nine). Then dispatch every other frame in parallel, one worker each. Wait for the
files on disk, not for the notifications.

## 9. Assembly and orchestrator layer

Fill the settings block of `<project>/assemble.sh` (first frame id, end card id, `TOTAL`, audio path, flash time and
center, iris time and center, paper color, accent colors), then:

```bash
bash <project>/assemble.sh
```

It rebuilds `index.html` with HeyGen's assembler and transition injector, then adds the orchestrator layer
(`orchestrator-layer.md`) and runs the lint. Re-run it after every change to a frame or to the storyboard.

## 10. Audio mix

- Music: a CC0 track the user provides (`<project>/assets/audio/music.mp3`), volume 0.10 to 0.15, short fade-in,
  3 s fade-out. If it opens on a quiet build, start later (`MUSIC_START`) on a clean, stronger section.
- Sound effects: `<project>/assets/audio/sfx-events.json`, `[name, seconds, volume]` on the final timeline, names from
  `.claude/skills/media-use/audio/assets/sfx/` (`manifest.json` there describes each one). Typical grammar:
  `whoosh-short` 0.12 to 0.2 on each transition, `pop` 0.15 to 0.3 on pills and giant words, `click` 0.35 to 0.45 on
  cursor clicks, `key-press` / `typing` 0.15 to 0.25 while text types, `error` 0.2 on a breakage, `whoosh` 0.5 on the
  flash and on the iris, `ping` 0.15 on a success. Place each one on the visual event, not on the word.

```bash
bash <project>/build-audio.sh && bash <project>/assemble.sh
```

## 11. Checks before the render

```bash
cd <project> && npx hyperframes check
cd <project> && npx hyperframes snapshot --at <frame midpoints, and each cut -0.1 and +0.2, comma-separated>
```

Open `<project>/snapshots/contact-sheet.jpg`. Midpoints: layout failures. Around every cut: a continuing element must
keep its position, scale, opacity and direction.

## 12. Render and control of the real video

```bash
cd <project> && npx hyperframes render --quality high --output renders/video.mp4
bash .claude/skills/motion-design/scripts/contact-sheets.sh <project>/renders/video.mp4
```

`contact-sheets.sh` reports black segments (exit code 2 when there is one) and writes 4 images/s sheets (4 x 6, 6 s
per sheet, timestamped) in `<project>/renders/contact-sheets/`. Open every sheet. Run the control grid of
`patterns/PATTERNS.md` on the render, fix the frame concerned (the cheapest edit in its HTML), re-assemble, re-render.
For a stray element whose origin is unclear, hide the frames one by one in `index.html` until it disappears.

For a waveform drawn from the real voice inside a frame:

```bash
python3 .claude/skills/motion-design/scripts/waveform.py <project>/assets/audio/voix-montage.wav --start 12.4 --duration 2.6 --bars 48
```

## 13. Delivery

Give the MP4 path, its duration (`ffprobe -v error -show_entries format=duration -of csv=p=0 <project>/renders/video.mp4`),
the contact sheets and the frame ids, so the next revision can target one frame. For a landing page, also offer the
silent loop (8 to 18 s, no audio track, readable without sound) cut from the same project.
