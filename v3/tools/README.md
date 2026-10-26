# v3 tools (not needed to run the app)

- `verbs.py` – builds the Verbs deck data (verbs.json, embedded in index.html as `verbdb`):
  8 persons × past / present / future × affirmative / negative / question, from root + pattern
  (Kanafani table), with Latin and Russian in the style of Глаголы.pdf. Running it checks every
  form of كتب and درس against the PDF tables and example phrases.
  To add a regular verb: one line in VERBS (past stem, present stem, English, Russian forms).
  Hollow verbs (نام, قال) also give `past_short` / `pres_short` stems.
  Verbs from Глаголы 2.pdf take their Russian transcription from `PDF2_RUS` (as in the PDF);
  forms the PDF doesn't list (negative, future) are built from it.
- `words.py` – builds the Special words and Nouns data (words.json, embedded as `worddb`):
  9 question words with an example sentence, 4 prepositions (مع، بدون، عن، لدى) × 8 personal forms, 10 nouns.
- `genverbs.py <miro|dii> <male|female> [ids]` – generates the audio:
  `audio/verbs/<verb>/<voice>/<tense>-<pos|neg>-<person>.mp3`, `audio/verbs/common/<voice>/pron-<person>.mp3`, `hal.mp3`,
  `audio/special/<voice>/q-<id>.mp3`, `q-<id>-ex.mp3`, `prep-<id>.mp3`, `prep-<id>-<person>.mp3`,
  `audio/nouns/<voice>/<id>.mp3`.
  Optional third argument limits it, e.g. `nam,qal,words`. Questions are played as hal.mp3 + the affirmative clip.

Letters and numbers audio is not copied into v3: the app plays it from `../v2/audio/`.
