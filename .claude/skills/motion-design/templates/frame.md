---
version: 2
name: "{{BRAND}}: launch frame"
description: >
  Video-first frame spec for the {{BRAND}} launch motion design, built on ../patterns/PATTERNS.md. {{METAPHOR_IN_ONE_SENTENCE}}.
  Two worlds: the PROBLEM lives on a warm near-black stage, the SOLUTION on a light ground; the end card returns to the
  dark stage. One accent only, {{ACCENT_NAME}}, used for ONE traced pill per sentence. Small centered phrase text that
  arrives word by word on the voice; a few giant words only at emotional peaks.
  Template of the motion-design skill: replace every {{...}} placeholder (grep -n "{{" frame.md must print nothing).
  Reference values in the comments are those of the Entrepreneurs 2.0 example films (terracotta on warm black and paper).
unit: 1920×1080
principle: readable without sound · one accent, one highlight mechanism · the voice cues every reveal

colors:
  canvas: "{{CANVAS}}"                # dark world (problem + end card), ref "#0d0b0a"
  canvas-2: "{{CANVAS_2}}"            # ref "#141010"
  paper: "{{PAPER}}"                  # light world (solution) full-bleed ground, ref "#f6f1e9"
  paper-2: "{{PAPER_2}}"              # secondary light surface, ref "#efe7dc"
  card-light: "{{CARD_LIGHT}}"        # cards on the light world, ref "#fffdf9"
  ink: "{{INK}}"                      # text on dark, ref "#f5efe7"
  ink-soft: "{{INK_SOFT}}"            # ref "#cdbfb2"
  ink-mute: "{{INK_MUTE}}"            # ref "#9b9289"
  ink-dark: "{{INK_DARK}}"            # text on light, ref "#1a1612"
  ink-dark-soft: "{{INK_DARK_SOFT}}"  # ref "#5a5348"
  hairline-light: "{{HAIRLINE}}"      # ref "#e2d9cc"
  accent: "{{ACCENT}}"                # THE brand accent, ref "#c25b28"
  accent-light: "{{ACCENT_LIGHT}}"    # ref "#d4703f"
  accent-deep: "{{ACCENT_DEEP}}"      # ref "#a84d22"
  accent-glow: "{{ACCENT_GLOW}}"      # ref "#e08a5c"

# Local woff2 files only, never a network @import (fetch commands: references/method.md, step 2).
# Default trio of the method (all SIL Open Font License): swap only if the brand has its own fonts.
fonts:
  Instrument Sans: { files: ["assets/fonts/InstrumentSans-400.woff2 (400)", "assets/fonts/InstrumentSans-500.woff2 (500)", "assets/fonts/InstrumentSans-600.woff2 (600)", "assets/fonts/InstrumentSans-700.woff2 (700)"] }
  Space Mono: { files: ["assets/fonts/SpaceMono-400.woff2 (400)", "assets/fonts/SpaceMono-700.woff2 (700)"] }
  Big Shoulders: { files: ["assets/fonts/BigShoulders-800.woff2 (800)"] }

typography:
  phrase:     { fontFamily: "Instrument Sans", px: 54, weight: 600, lineHeight: 1.18, tracking: "-0.02em", note: "the sentence of the voice, SMALL and centered (or anchored as the Scene says), arrives word by word on its timestamp" }
  giant:      { fontFamily: "Instrument Sans", px: 260, weight: 700, lineHeight: 0.9, tracking: "-0.05em", note: "ONLY for the 2-5 emotional peaks named in the storyboard; may overflow or sit BEHIND an object" }
  numeral-jumbo: { fontFamily: "Instrument Sans", px: 300, weight: 600, lineHeight: 0.9, tracking: "-0.02em", tabularNums: true }
  ui:         { fontFamily: "Instrument Sans", px: 28, weight: 500, lineHeight: 1.3 }
  title:      { fontFamily: "Instrument Sans", px: 44, weight: 600, lineHeight: 1.1, tracking: "-0.02em" }
  code:       { fontFamily: "Space Mono", px: 26, weight: 400, lineHeight: 1.5, note: "only if the film shows code; keywords in accent-light" }
  price:      { fontFamily: "Space Mono", px: 30, weight: 700, tabularNums: true }
  micro:      { fontFamily: "Space Mono", px: 18, weight: 400, tracking: "0.2em", upper: true }
  wordmark:   { fontFamily: "Big Shoulders", px: 64, weight: 800, upper: true, note: "{{WORDMARK_RULE}}, e.g. 'BRAND' in ink + ' 2.0' in accent-light" }
  cta:        { fontFamily: "Big Shoulders", px: 34, weight: 800, upper: true }

components:
  ground-dark:
    background: "solid canvas + 1-2 soft radial accent halos (14-28% opacity, blur 100px+) behind the focal element + static film grain 4-6%. Painted as a full-duration class=\"clip\" layer, never on #root."
  ground-light:
    background: "solid paper + one very soft warm radial (accent at 6-10%) behind the focal element + grain 3%. Text is ink-dark. Full-duration class=\"clip\" layer."
  word-by-word:
    rule: "Each word of the phrase appears ON its voice timestamp: fromTo {opacity:0, y:10, filter:blur(8px)} → {opacity:1, y:0, blur(0)} in 0.3 s power3.out, immediateRender:false. Never the whole sentence at once."
  accent-pill (THE highlight mechanism, one per sentence):
    look: "filled accent rectangle, radius 12px, padding 0.06em 0.32em, white text, same font as the phrase"
    motion: "the pill traces first: scaleX 0→1 from the left in 0.28 s power3.out (optionally starting at rotation -8deg and straightening to 0 in 0.4 s), THEN the word's letters write inside with a 0.02 s stagger. Starts 0-2 frames before the word is spoken."
    rule: "ONE pill per sentence, on the word the storyboard names. No other colored text anywhere."
  giant-word:
    motion: "enters with its letters converging + opacity 0→1 + blur 12px→0 over 0.5 s expo.out; may sit behind a card or object (z-order) for depth. NEVER tween letterSpacing (it snaps to device pixels under seek capture and the lint blocks it): keep letter-spacing -0.05em static, split the word into inline-block letters and tween each letter's x from (i - (n-1)/2) × 0.4em to 0. A counting number keeps only scale + blur."
  echo-stack:
    look: "the word sharp in the center + 4 copies above and below at 60/35/20/10% opacity, slightly blurred"
    motion: "copies start spread (±180px) and converge to ±70px in 0.4 s power3.out while the center word lands"
  glass-card-dark:
    background: "linear-gradient(160deg, rgba(40,33,28,.92), rgba(24,20,17,.9) 45%, rgba(20,16,14,.9) 80%, rgba(30,24,20,.92)); 1px rgba(245,239,231,.10) border; inset 0 1px 0 rgba(255,255,255,.14); shadow 0 50px 120px rgba(0,0,0,.7); radius 14px (retint to canvas)"
  card-light:
    background: "card-light, 1px hairline-light border, radius 14px, shadow 0 30px 80px rgba(60,40,20,.14), 0 2px 6px rgba(60,40,20,.08)"
  counter:
    description: "numeral-jumbo number that rolls to its value (tabular digits, grows slightly with the value), with a micro unit label under it. Every number on screen rolls, none is simply posed."
  tool-tiles:
    description: "Real tool logos from assets/icons/*.svg (Simple Icons, CC0): inline SVG path in an 88px white rounded tile (radius 20px, soft shadow), filled with the tool's own brand color ({{TOOL_COLORS}}, e.g. Gmail #EA4335, Stripe #635BFF). Brand colors are the ONLY exception to the one-accent rule, only inside tool tiles."
  persona:
    description: "{{PERSONA}}: a flat vector character in inline SVG, head + shoulders, simple hair, NO detailed face (two small dot eyes max), ~340px tall, friendly and simple, not childish. The same drawing in every frame where it appears."
  pain-pills:
    description: "Small dark pills (Space Mono 20px, white text on a dark warm grey, radius 999px) that pop around the persona one by one (≈0.12 s apart), slight deterministic rotation from the index, each with a tiny ✕ in accent."
  chat-input:
    description: "Large card with micro label '{{CHAT_LABEL}}', prompt typed char by char behind an accent caret, square accent send button with a white up-arrow. card-light on the light world."
  caret:
    description: "the text caret: a 4px × 58px accent-light bar, blinks as finite on/off steps (0.5 s period, NEVER a repeat:-1 loop)."
  product-mock:
    description: "{{PRODUCT_MOCK}}: the product or the user's own tool as the viewer knows it, rebuilt in HTML (browser card with 3 dots + mono url, or app window). Accent elements only for the thing the voice points at."
  cursor:
    description: "White macOS arrow with dark outline + drop shadow; click = press (scale .85) + accent ripple ring that expands and fades."
  light-point:
    description: "a white-hot point (radial #fff3ea → accent-glow → transparent) used where the orchestrator's light flash starts."
  end-card:
    description: "dark stage, wordmark assembled letter by letter, one-line promise in phrase size with ONE pill, sub-line in ui ink-soft, ONE CTA button '{{CTA_LABEL}}' (paper fill, accent-deep Big Shoulders text, soft accent glow), mono URL '{{URL}}' in small, a cursor that glides in and clicks the button, then everything holds still 3 to 8 s."

negative:
  - "No second highlight mechanism: the traced accent pill is the ONLY way a word is emphasized (no colored text, no glow text)."
  - "No big phrase text: sentences are 'phrase' size; only the storyboard's named peaks use 'giant' / 'numeral-jumbo'."
  - "No hue other than the accent, except real brand colors inside tool tiles."
  - "No Inter, Space Grotesk, Geist, system-ui. No emoji. No icons in round pills."
  - "No bouncy/elastic/back.out eases. No breathing loops, no slow push on every scene, no repeat:-1."
  - "No visible text that is not listed in the frame's Scene lines (component labels above are allowed)."
  - "Never tween letterSpacing."
---

# {{BRAND}}: frame spec

The film has two worlds. **The problem** plays on the warm black stage: {{PROBLEM_WORLD_IN_TWO_SENTENCES}}. A single
**pivot** ({{PIVOT}}, a word alone or a caret in the dark) freezes everything, then light floods the screen and we land
on **the solution**, on the light ground: {{SOLUTION_WORLD_IN_TWO_SENTENCES}}. The iris from {{IRIS_OBJECT}} takes us
back to the dark stage for the **end card**.

Everything the viewer reads is Instrument Sans: small sentences that arrive word by word on the voice, with exactly one
word per sentence written inside an accent pill that traces itself first. A handful of giant words mark the peaks.
Numbers, labels and code are Space Mono; the wordmark and the CTA are Big Shoulders.
