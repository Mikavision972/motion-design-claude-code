---
format: 1920x1080
duration: "{{TOTAL}}s"
message: "{{ONE_LINE_THESIS}}"
arc: Hook → Problem → Pivot → Turn → Demo → Payoff → Reassurance → CTA
audience: "{{AUDIENCE}}"
mode: autonomous
captions: disabled
music: "pre-mixed with voice and SFX in assets/audio/mix.wav (mounted at root by the orchestrator)"
patterns: ../patterns/PATTERNS.md
---

<!--
Template of the motion-design skill. Replace every {{...}} (grep -n "{{" STORYBOARD.md must print nothing), delete
this comment, and keep the exact field names: HeyGen's packet builder, assembler and transition injector parse them.

Timing rules (all times come from onsets.py run on the FINAL voice montage, never from Whisper alone):
- A frame = one idea of the script, 3 to 7 s. Frame boundaries sit in the silences between sentences.
- Sum of all frame durations = duration above = TOTAL in assemble.sh and build-audio.sh (check it, do not trust mental math).
- Word cues are FRAME-LOCAL: cue = global onset - frame start (onsets.py --window START END prints them that way).
- Inside a frame, a NEW composition (Scene) every 2 to 3 s at most: never the same layout for more than 3 s.
- One blueprint per frame, 1 to 3 rules (each rule cited in the text also lands in the packet; packet limit 48 KB).
- transition_in: cut | crossfade | blur-crossfade | push-slide LEFT/RIGHT/UP/DOWN | zoom-through | squeeze.
  0 to 4 hard cuts in the film, at the act changes. The flash (dark to light) and the iris (light to the end card) are
  added by assemble.sh: the frame after the flash and the end card both use transition_in: cut.
- world: dark | light. Each frame paints its own full-bleed ground as a class="clip" layer.
- Visible copy: exactly the quoted copy of the Scene lines, in the language of the voice (French: typographic ’, « »,
  non-breaking spaces before : ? !), nothing else.
-->

## Video direction

- **Two worlds** (frame.md): frames 1-{{LAST_DARK}} = PROBLEM on the dark stage; frames {{FIRST_LIGHT}}-{{LAST_LIGHT}} = SOLUTION on the light ground (the light flash at the end of frame {{LAST_DARK}} floods into it); frame {{END}} = END CARD back on the dark stage (the iris from {{IRIS_OBJECT}}). Each frame paints its own full-bleed ground as a `class="clip"` layer.
- **Text** (readable without sound): every sentence of the voice is shown as small centered `phrase` text that arrives WORD BY WORD on the timestamps given in each frame (`word@seconds`, frame-local). Exactly ONE word or group per sentence sits in the traced `accent-pill` (named in the Scene lines as [pill: …]). No other colored or glowing text.
- **Giant words**: only the peaks named as [giant: …] ({{GIANT_WORDS}}, 2 to 5 in the whole film), entering with the letters converging.
- **Recurring objects** (frame.md): {{RECURRING_OBJECTS}}. They look the same in every frame they appear in, never in the same framing twice.
- **Motion grammar**: smooth long-tail settles (power3.out default, expo.out for fast arrivals), no bounce. Exits faster than entries. One camera move per scene at most. Holds are still.
- **Visible copy**: exactly the quoted copy of the Scene lines, nothing else.
- **Negative list**: slideshow (everything at t=0), screensaver (many things floating), colored text instead of the pill, big phrase text, any hue other than the accent except tool-tile brand colors.

## Frame 1: {{TITLE_1}}

- scene: {{ONE_LINE_CAPTION_1}}
- duration: {{D1}}s
- transition_in: cut
- status: outline
- src: compositions/frames/01-{{SLUG_1}}.html
- voiceover: "{{EXACT_SENTENCES_OF_THIS_FRAME}}"
- type: hook
- blueprint: {{BLUEPRINT_ID}} (Adapt)
- focal: {{HERO_ELEMENT}}
- rules: {{RULE_1}}, {{RULE_2}}
- world: dark

Word cues: {{Word@0.00 word@0.24 word@0.78 ...}}
Scene 1 (0.0-{{t}}s): first image = the word « {{FIRST_WORD}} » ALONE, small, dead center on the dark stage (no logo, no UI). « {{KEY_WORD}} » arrives at {{t}} in a traced accent pill [pill: {{KEY_WORD}}].
Scene 2 ({{t}}-{{t}}s): {{WHAT_WE_SEE, where the phrase sits, which object enters, the exact cue of each reveal (→ rule-id)}}.
Scene 3 ({{t}}-{{D1}}s): {{...}}. Hold.

## Frame 2: {{TITLE_2}}

- scene: {{ONE_LINE_CAPTION_2}}
- duration: {{D2}}s
- transition_in: push-slide LEFT
- status: outline
- src: compositions/frames/02-{{SLUG_2}}.html
- voiceover: "{{EXACT_SENTENCES_OF_THIS_FRAME}}"
- type: pain_point
- blueprint: {{BLUEPRINT_ID}} (Adapt)
- focal: {{HERO_ELEMENT}}
- rules: {{RULE_1}}, {{RULE_2}}
- world: dark

Word cues: {{...}}
Scene 1 (0.0-{{t}}s): {{...}}
Scene 2 ({{t}}-{{D2}}s): {{...}}

<!-- Repeat one block per frame, then delete this comment. The last dark frame ends on the pivot (a word alone, an
echo-stack, a caret in the dark) and brightens at the point where the flash starts (LEAK_X, LEAK_Y in assemble.sh). The
first light frame uses transition_in: cut. The last light frame ends on the object the iris grows from (IRIS_X, IRIS_Y). -->

## Frame {{END}}: {{END_CARD_TITLE}}

- scene: Back on the dark stage: the wordmark assembles, « {{PROMISE}} » lands, a cursor clicks « {{CTA_LABEL}} »
- duration: {{D_END}}s
- transition_in: cut
- status: outline
- src: compositions/frames/{{END}}-fin.html
- voiceover: "{{BRAND_SPOKEN_IN_LETTERS}}. {{PROMISE}}."
- type: cta
- blueprint: logo-assemble-lockup (Adapt)
- focal: the wordmark, then the CTA button
- rules: cursor-click-ripple, press-release-spring
- world: dark

Word cues: {{...}} (hold to {{D_END}})
Scene 1 (0.0-{{t}}s): dark stage with a soft accent texture across the top third and a warm halo; the wordmark « {{WORDMARK}} » cascades in letter by letter on its cue. Upper-center.
Scene 2 ({{t}}-{{t}}s): below it, phrase-size but larger (72px) « {{PROMISE_START}} » + [pill: {{PROMISE_END}}] on their cues.
Scene 3 ({{t}}-{{t}}s): the sub-line « {{SUB_LINE}} » (ui, ink-soft); the CTA button « {{CTA_LABEL}} » arrives on a smooth settle; mono URL « {{URL}} ».
Scene 4 ({{t}}-{{D_END}}s): a cursor glides in and clicks the button (→ cursor-click-ripple, → press-release-spring); then everything holds STILL to the end.
