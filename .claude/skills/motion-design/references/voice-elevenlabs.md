# Voice with ElevenLabs v3

The voice is the clock of the whole film: every reveal is cued on it. It is made by the user in the ElevenLabs web app
(https://elevenlabs.io), no API key, nothing to install. The agent prepares the text and explains the settings.

## Prepare the text (agent)

Start from the validated script and write the **voice version** in `<project>/SCRIPT.md`, under the screen version:

- **Numbers in letters** for the voice ("mille euros", "six cents euros", "deux point zéro"); the screen keeps
  "1 000 €", "600 €", "2.0".
- **Tags in square brackets** to direct the reading (only Eleven v3 reads them): `[pause]`, `[short pause]`,
  `[long pause]` between sentences or acts, and a few emotions where the script plays a character: `[sarcastic]`,
  `[sighs]`, `[whispers]`, `[excited]`. One or two emotions per film, not more.
- `...` inside a sentence gives a short suspended pause ("Délai... quand il aura le temps.").
- One sentence per line; the brand spelled the way it must be spoken.

Example (film "Le devis"):

```
Une modification sur ton site... une journée. Mille euros.
Une nouvelle page : six cents euros.
Réparer une automatisation qui a planté : sur devis.
Délai... [sarcastic] quand il aura le temps.
[pause]
Pendant des années, c'était le prix à payer pour tout ce qui est technique.
[long pause]
Sauf qu'aujourd'hui, l'IA sait faire tout ça.
```

## Generate (user)

1. ElevenLabs, Text to Speech, model **Eleven v3** (the only one that reads the tags).
2. Pick a voice from the library that fits the brand (the example films use a warm male French voice). Stability
   **Natural**.
3. Paste the whole voice text in one go (the intonation carries from one sentence to the next).
4. Generate **3 or 4 takes**, listen, keep the best. Regenerate only the take, never sentence by sentence.
5. Download as MP3 (or WAV) and drop it as `<project>/assets/audio/voix.mp3`.

A paid plan is required for commercial use of the audio. Recording your own voice works the same way (quiet room,
phone close to the mouth, export MP3): the rest of the method does not change.

## After the voice

- Pauses are adjusted at the montage (`build-audio.sh`, `CUTS`), never by regenerating: lengthen the silence before the
  pivot (+0.6 to 0.8 s) and before the end card (+0.4 s), add about 4 s of tail for the end card.
- If one word is mispronounced, fix the spelling in the voice text (phonetic spelling is fine) and regenerate the whole
  take, then redo the timings (`onsets.py`) since every cue moves.
