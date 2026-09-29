---
name: motion-design
description: Makes an agency-grade launch motion design film (40 to 50 s, 16:9, voice-over) in this repository with HyperFrames and the pinned HeyGen skills, from a co-written script to the rendered MP4. Use when the user asks here for a launch, promo or product motion design video. Not for editing filmed footage or talking-head videos.
---

# Motion design: launch film, end to end

You are the orchestrator. You run every step yourself except building the frames (one sub-agent per frame). The detail
of each step is in `references/method.md`; this file is the order, the commands and the gates.

**Before anything**: follow `AGENTS.md` (pinned local CLI, forbidden commands, empty `.env` at the root). This skill
replaces Steps 0 to 3.1 of `product-launch-video` (no preset capture, no HeyGen voice or music API) and reuses its
packet builder, assembler and transition injector.

**The rule that makes it look like an agency**: a different image every 2 to 3 s. A new composition at every sentence
or half-sentence; never the same layout for more than 3 s, even if the content inside changes. Vary the framing (full
text, close-up on a detail, glass card, diagram, giant number), the text position and the object shown.

## Steps

0. **Preflight.** `test -f .env || cp .env.example .env` and `test -d node_modules || npm ci`. Pick a kebab-case
   `<project>` name (the brand or the film). All paths below are relative to the repository root.
1. **Script, co-imagined (gate).** Ask the few missing facts, propose 5 to 7 concepts in one line each, write 2 or 3 in
   full (110 to 130 words), let the user choose and correct word by word. Rules: `references/method.md` § 1.
2. **Project folder.**
   `npx hyperframes init <project> --non-interactive --example=blank`, then copy the templates, create
   `assets/{audio,fonts,icons}`, fetch the fonts and tool icons (commands: `references/method.md` § 2). Save the script
   as `<project>/SCRIPT.md`.
3. **Voice (user action, wait).** Write the ElevenLabs v3 version with tags and numbers in letters, explain the
   settings, wait for `<project>/assets/audio/voix.mp3`. `references/voice-elevenlabs.md`.
4. **Timings.**
   `python3 .claude/skills/motion-design/scripts/onsets.py <project>/assets/audio/voix.mp3 --no-whisper` (phrases and
   cut points), set `CUTS`, `TAIL`, `TOTAL` in `<project>/build-audio.sh`, `MUSIC= bash <project>/build-audio.sh`, then
   `python3 .claude/skills/motion-design/scripts/onsets.py <project>/assets/audio/voix-montage.wav --script <project>/SCRIPT.md --out <project>/onsets.json`.
   From now on every cue comes from `onsets.json` (`--transcript <project>/onsets.json --window START END` for
   frame-local cues).
5. **Frame spec.** Fill `<project>/frame.md`: colors as roles, one accent, one highlight mechanism (the traced pill),
   the product components. `grep -n "{{" <project>/frame.md` must print nothing.
6. **Storyboard (gate).** Fill `<project>/STORYBOARD.md`: frames of 3 to 7 s cut in the silences, exact voiceover,
   frame-local word cues, one blueprint and 1 to 3 rules per frame, Scene lines every 2 to 3 s, one [pill: ...] per
   sentence, 2 to 5 [giant: ...]. Pass the control grid below, check the sum of durations with a script
   (`references/method.md` § 6), show the frame list and wait for approval (autonomous: heads-up).
7. **Packets.** `node .claude/skills/product-launch-video/scripts/frame-packets.mjs --project <project> --storyboard <project>/STORYBOARD.md`
   (each packet under 48 KB, otherwise cut a rule from that frame).
8. **Frames, one sub-agent each.** Pilot first: frame 1 alone, `bash <project>/assemble.sh`,
   `cd <project> && npx hyperframes snapshot --at <3 or 4 times in frame 1>`, show it, lock the look. Then every other
   frame in parallel with the dispatch template below. Done = the file exists on disk. `references/worker-dispatch.md`.
   After a session cut: `python3 .claude/skills/motion-design/scripts/check-frames.py <project>` and re-dispatch only
   the frames that are MISSING or BROKEN (`references/variants.md` § Resume).
9. **Assembly + orchestrator layer.** Fill the settings of `<project>/assemble.sh` (first frame, end card, `TOTAL`,
   audio, flash time and center, iris time and center, paper and accent colors) and run `bash <project>/assemble.sh`:
   HeyGen assembler, transitions, then audio at the root, paper bed under the light world, light flash from the dark
   world into the light world, iris into the dark end card, and lint. `references/orchestrator-layer.md`.
10. **Audio, in 3 or 4 music options.** Sound effects in `<project>/assets/audio/sfx-events.json` placed on the visual
    events (format: `.claude/skills/motion-design/templates/sfx-events.json`, names from
    `.claude/skills/media-use/audio/assets/sfx/`). CC0 tracks in `<project>/assets/music/` (sources:
    `references/music.md`), drops found with `scripts/analyze-music.py --drop-at <flash time>`, then
    `templates/build-music-options.py` copied into the project: music cut on the pivot with a low impact, drop on the
    flash, ducked under the voice, -16 LUFS, one `mix-<id>.wav` per option with its pivot check. Then
    `MIX=mix-M1.wav bash <project>/assemble.sh`. `references/music.md`.
11. **Checks.** Lint clean (end of `assemble.sh`), `cd <project> && npx hyperframes check`, then
    `cd <project> && npx hyperframes snapshot --at <every frame midpoint, each cut -0.1 and +0.2>` and read
    `<project>/snapshots/contact-sheet.jpg`. Re-dispatch the frame concerned with the finding.
12. **Render and real control.** `cd <project> && npx hyperframes render --quality high --output renders/video.mp4`,
    then `bash .claude/skills/motion-design/scripts/contact-sheets.sh <project>/renders/video.mp4` (black segments,
    exit 2 if any; sheets at 4 images/s in `<project>/renders/contact-sheets/`). Open every sheet, pass the grid again,
    fix, re-assemble, re-render. The other music options need no render:
    `python3 <project>/build-music-options.py --mux <project>/renders/video.mp4`.
13. **Delivery.** MP4 path per music option, duration (`ffprobe`), contact sheets, frame ids for targeted revisions.
    For a website: web encode, poster, muted autoplay, framed player (`references/landing-integration.md`,
    `templates/LaunchFilm.tsx`). Offer the silent loop (8 to 18 s) too.
14. **Options, when asked for "better" or "other versions".** Same voice, same timings: a polished version, a restyle
    that keeps the choreography, a new direction; recurring objects built first. `references/variants.md`.

## Control grid (storyboard, then render)

From `patterns/PATTERNS.md` (56 launch films analyzed frame by frame):

- [ ] First image = a word alone, not the logo; the first word names the target or their pain.
- [ ] The image at second 1 illustrates exactly that first word.
- [ ] Every sentence of the voice has its composition; text arrives word by word, small and centered.
- [ ] One accent word per sentence, one accent color in the whole film, one highlight mechanism (the traced pill).
- [ ] 2 to 5 giant words, on the emotional peaks, behind an object when possible.
- [ ] The pain is shown in a tool the target recognizes, its volume by a swarm of objects.
- [ ] An explicit pivot (word alone, silence, question) before the brand, and the ground changes with it.
- [ ] The logo does not arrive before 5 s.
- [ ] 0 to 4 hard cuts, all at act changes; everything else chains through objects.
- [ ] Every number rolls to its value.
- [ ] The product is shown by gestures (type, tick, click), not by a static screenshot.
- [ ] An element of the hook comes back before the end.
- [ ] End card: one button, a cursor that clicks it, held 3 to 8 s.
- [ ] Readable without sound from start to end.
- [ ] A different image every 2 to 3 s.
- [ ] Render: no `letterSpacing` tween; a paper bed under the light world; no black segment.

## Dispatch template (one per frame, absolute paths)

```
You build ONE frame of a HyperFrames motion design. You do not see my conversation: these files are your whole world.

Read first, in this order, and follow them as your role:
1. <PROJECT_DIR>/.hyperframes/frame-packets/_role.md (worker contract)
2. <PROJECT_DIR>/.hyperframes/frame-packets/<frame_id>.md (your storyboard block, blueprint and motion rules)
3. <PROJECT_DIR>/frame.md (colors, fonts, components: the only style source)

## Dispatch context
- PROJECT_DIR: <PROJECT_DIR>
- frame_id: <frame_id>
- output: <PROJECT_DIR>/compositions/frames/<frame_id>.html (the only file you write)
- canvas: 1920x1080, 30 fps; frame duration: <D> s; world: <dark|light>
- confirmed sketch: none
- captions: disabled
- <frame-specific lines: flash point, iris hold, handoffs, retry findings (see worker-dispatch.md)>

## House rules of this repository (they override the contract where they differ)
- Captions are disabled: the narration IS the on-screen text. Show each sentence as `phrase` text, word by word,
  exactly as the Scene lines quote it, with the named [pill: ...] and [giant: ...]. Keep text above y = 900 px.
- Word cues are frame-local seconds: each word appears on its cue (0 to 2 frames early), never late.
- A frame is not masked before its start: every element not on screen at t=0 starts with `opacity: 0` in CSS, and
  every `fromTo` that starts after t=0 has `immediateRender: false`.
- A new composition every 2 to 3 s, as the Scene lines say. power3.out / expo.out, no bounce, exits faster than entries.
- Never tween `letterSpacing` (split the word into letters, tween `x`). No `repeat: -1`, no yoyo, no `Math.random`.
- Fonts and icons from `assets/...` (project-root relative), never from the network. No `<audio>`.
- Only the copy quoted in the Scene lines appears on screen, in the language and typography of the voice.
- Do not run any `npx hyperframes` command, do not edit any other file. Writing your file is your last action.
```

## References

| File | When |
|---|---|
| `references/method.md` | the detail and the exact commands of every step |
| `references/voice-elevenlabs.md` | step 3 |
| `references/worker-dispatch.md` | steps 7 and 8 |
| `references/orchestrator-layer.md` | step 9 |
| `references/music.md` | step 10: pick, sync and mix the music options, commercial-safe CC0 sources |
| `references/landing-integration.md` | step 13: put the film on a website |
| `references/variants.md` | step 14, and to resume after a session cut |
| `references/pitfalls.md` | before step 6, and whenever something looks wrong |
| `patterns/PATTERNS.md` (repository root) | steps 1 and 6 (choose patterns), 11 and 12 (control) |
| `templates/` | `frame.md`, `STORYBOARD.md`, `assemble.sh`, `build-audio.sh`, `sfx-events.json`, `build-music-options.py`, `LaunchFilm.tsx` |
| `scripts/` | `onsets.py` (timings), `analyze-music.py` (tempo, drops, sync), `contact-sheets.sh` (render control), `check-frames.py` (resume), `waveform.py` (real voice envelope) |
| `.claude/skills/hyperframes-animation/blueprints-index.md`, `rules-index.md` | step 6: shot shapes and motion recipes |
