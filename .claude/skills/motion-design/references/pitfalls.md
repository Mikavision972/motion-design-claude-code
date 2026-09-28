# Known pitfalls (and their fix)

Found while making the example films with this exact stack (HyperFrames 0.8.82, HeyGen skills at commit 93ab289).

## Timing

- **Whisper alone drifts by a few hundred ms.** The motion reveals words 0 to 2 frames before they are spoken, so a
  late cue is visible. Always take the cues from `onsets.py` (energy onsets), run on the final voice montage.
- **The agent's arithmetic on durations is not reliable** (a documented case announced 299 s and delivered 578 s).
  One source of truth: frame durations in `STORYBOARD.md`, `TOTAL` in `assemble.sh` and `build-audio.sh`. Compute the
  sum with a script, never in your head.
- **A voice cut on a word** clicks or swallows a syllable. Cut only in the middle of a silence (`cut point` printed by
  `onsets.py --no-whisper`), with 5 ms fades on every join (`build-audio.sh` does it). Every cue after a cut moves by the
  silence inserted before it: re-run `onsets.py` on the montage.
- **Same template for 10 s** reads as slow even with content changing inside. A new composition every 2 to 3 s:
  change the framing, the text position and the object, bring elements back as reminders but never in the same frame.

## Frames (workers)

- **A frame is not masked before its start.** Anything visible by default in its CSS shows during the previous frames
  (transitions overlap them). Every element that is not on screen at t=0 of its frame starts with `opacity: 0` in CSS,
  and every `fromTo` that starts after t=0 has `immediateRender: false`.
- **Never tween `letterSpacing`.** Frame-by-frame capture rounds it to device pixels and the text shakes; the lint
  blocks it. For a giant word whose letters tighten: split it into inline-block letters and tween their `x`. On a
  counting number keep only scale and blur.
- **Background on `#root` is not dependable**: at assembly the frame root is clip-gated, a dark frame can land on the
  black host page. The ground is its own full-duration `class="clip"` layer.
- **Packet over 48 KB** makes `frame-packets.mjs` fail. A blueprint weighs 5 to 29 KB, a rule 5 to 10 KB: 1 to 3 rules
  per frame. Every rule id written anywhere in the frame block (for example "(→ cursor-click-ripple)") is inlined too.
- **Infinite loops** (`repeat: -1`, yoyo, CSS animations, `Math.random`) break the seek-based render. Finite tweens,
  randomness derived from the index.
- **The core worker contract forbids narration text on screen** because HeyGen's default pipeline burns captions. This
  method disables captions and shows the sentence itself, word by word: the dispatch template says so explicitly.
- **CSS `transform` on an element that GSAP moves** is silently overwritten (the centering jumps). Center with margins
  or `xPercent` / `yPercent`.

## Assembly and transitions

- **The injector knows 5 CSS transitions** (crossfade, blur-crossfade, push-slide, zoom-through, squeeze) plus the cut.
  HeyGen's shader transitions need their whole engine: for the 2 or 3 key moments, use the orchestrator layer (light
  flash, iris) instead.
- **A frame extended under a transition must extend its internal clips too**, otherwise the iris opens on black (the
  frame root lives longer, its clips do not).
- **Two worlds of ground = grey crossfades.** The root is dark, so a crossfade between two light frames passes through
  grey. The paper bed of `assemble.sh` lies under the whole light world.
- **`index.html` is rebuilt from scratch** by the assembler: never edit it by hand, put every orchestrator change in
  `assemble.sh`.
- **A frame marked `animated` without its HTML file** stops the assembler. `assemble.sh` marks a frame animated only
  when its file exists, so a pilot or a partial build assembles.

## Checks

- **Always check the real render**, not only the preview: `contact-sheets.sh` (black segments + 4 images/s sheets).
  A black segment is almost always a clip that ends too early or a frame whose ground is on `#root`.
- **A stray element** whose origin is unclear: hide the frames one by one in `index.html` (temporarily) until it
  disappears, then fix that frame.
- **Precise feedback** makes precise fixes: moment, symptom, expected ("at 4 s, the blur passes in front of the text
  instead of behind").

## Look

- No linear motion: curves (`power3.out`, `expo.out`), never bounce or elastic.
- Each entry animates 2 or 3 properties together (position, opacity, scale); 3 to 6 frames of offset between
  elements that enter together; exits faster than entries.
- No gratuitous 3D or effect: the agent tends to add some. "Better no movement than a bad movement."
- Music: a library track can open on a quiet build that drains the first seconds. Start on a stronger, clean section
  (`MUSIC_START`), keep a short fade-in and a 3 s fade-out, volume 0.10 to 0.15 under the voice.

## Landing page

- No browser autoplays a video with sound: the top-of-page video is muted and must read without sound. Offer a silent
  loop of 8 to 18 s (MP4 H.264, 3 to 4 MB, no audio track, with a poster image) plus the full version with the voice,
  opened on click.
