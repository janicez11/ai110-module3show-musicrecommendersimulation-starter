# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Explain your design in plain language.

Some prompts to answer:

- What features does each `Song` use in your system
  - For example: genre, mood, energy, tempo
Response: mood, genre, energy, acousticness

- What information does your `UserProfile` store
Response: favorite_genre, favorite_mood, target_energy, likes_acoustic

- How does your `Recommender` compute a score for each song
1. Mood match — up to 40 points
The song's mood and your preferred mood are first normalized (lowercased, whitespace stripped), then checked for membership in the same synonym group. So a user who wants "chill" will match a song tagged "relaxed" or "calm". A match awards the full 40 points; no match awards zero.

2. Genre match — up to 25 points
Same approach as mood. "hip-hop" matches "hip hop", and "indie pop" falls in the same group as "pop". Full 25 for a match, zero otherwise.

3. Energy proximity — 0 to 20 points
This is the only gradual signal. It computes 20 × (1 − |your_target_energy − song_energy|) where both values sit on a 0–1 scale. A perfect energy match gives the full 20; a song at the opposite extreme gives 0; everything in between is proportional. Songs within 5 points of the max (≥15 pts) are flagged as "energy close" in the explanation.

4. Acoustic bonus — 0 or 15 points
If you have likes_acoustic = True and the song's acousticness exceeds 0.6, add 15 points. Both conditions must hold; there is no penalty for disliking acoustic music.


- How do you choose which songs to recommend
The four values above are summed into a final score out of a maximum of 100. Every song in the library gets scored this way, then they're sorted highest-to-lowest and the top results are returned.

You can include a simple diagram or bullet list if helpful.

songs.csv
    │
    ▼
load_songs()
    │
    └── List[Dict]  ←────────────────────────────────┐
            │                                         │
            │          user_prefs Dict                │
            │        ┌──────────────────┐             │
            │        │ favorite_genre   │             │
            │        │ favorite_mood    │             │
            │        │ target_energy    │             │
            │        │ likes_acoustic   │             │
            │        └────────┬─────────┘             │
            │                 │                       │
            ▼                 ▼                       │
        score_song(user_prefs, song)  ◄── called once per song
            │
            │   ┌─ _normalize() ──────────────────────────────┐
            │   │  lowercase + strip both sides               │
            │   └─────────────────────────────────────────────┘
            │
            ├── _same_group(song.mood, user.mood, MOOD_GROUPS)
            │       │ exact match after normalize?  → yes ──┐
            │       │ both in same synonym set?     → yes ──┤ +40 or +0
            │       │ neither?                      → no  ──┘
            │
            ├── _same_group(song.genre, user.genre, GENRE_GROUPS)
            │       │ exact match after normalize?  → yes ──┐
            │       │ both in same synonym set?     → yes ──┤ +25 or +0
            │       │ neither?                      → no  ──┘
            │
            ├── 20 × (1 - |Δenergy|)                → 0 to +20
            │
            └── likes_acoustic AND acousticness>0.6 → +15 or +0
                                                          │
                                                          └── sum → score (float)
                                                              reasons (List[str])
            │
            ▼
    returns (score, reasons)
            │
            ▼
recommend_songs(user_prefs, songs, k=5)
    │
    ├── calls score_song() for every song
    ├── sorts by score descending
    └── slices top-k
            │
            ▼
    List[ (song_dict, score, explanation_str) ]
            │
            ▼
        main.py / display



---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
User profile: genre=pop, mood=happy, high energy, non-acoustic

Top recommendations:

1. Sunrise City - Score: 85.00
   Because: mood match, genre match, energy close

2. Rooftop Lights - Score: 83.80
   Because: mood match, genre match, energy close

3. Gym Hero - Score: 42.80
   Because: genre match, energy close

4. Fuego del Sur - Score: 19.40
   Because: energy close

5. Street Anthem - Score: 19.00
   Because: energy close
```

=======================================================
Profile: HIGH_ENERGY_POP
  genre=pop, mood=happy, high energy, non-acoustic
=======================================================
  1. Sunrise City - Score: 89.30
     Because: mood match, genre match, energy close
  2. Rooftop Lights - Score: 86.90
     Because: mood match, genre match, energy close
  3. Gym Hero - Score: 51.30
     Because: genre match, energy close
  4. Storm Runner - Score: 39.60
     Because: energy close
  5. Pulse Wave - Score: 39.20
     Because: energy close

=======================================================
Profile: CHILL_LOFI
  genre=lo-fi, mood=chill, low energy, acoustic
=======================================================
  1. Library Rain - Score: 103.50
     Because: mood match, genre match, energy close, acoustic match
  2. Midnight Coding - Score: 100.70
     Because: mood match, genre match, energy close, acoustic match
  3. Spacewalk Thoughts - Score: 93.80
     Because: mood match, energy close, acoustic match
  4. Coffee Shop Stories - Score: 90.20
     Because: mood match, energy close, acoustic match
  5. Focus Flow - Score: 61.50
     Because: genre match, energy close, acoustic match

=======================================================
Profile: DEEP_INTENSE_ROCK
  genre=rock, mood=angry, high energy, non-acoustic
=======================================================
  1. Storm Runner - Score: 50.90
     Because: genre match, energy close
  2. Iron Cathedral - Score: 39.60
     Because: energy close
  3. Gym Hero - Score: 39.20
     Because: energy close
  4. Pulse Wave - Score: 37.20
     Because: energy close
  5. Street Anthem - Score: 36.80
     Because: energy close

=======================================================
Profile: ORPHAN_MOOD
  genre=rock, mood=angry, high energy, non-acoustic
=======================================================
  1. Storm Runner - Score: 52.10
     Because: genre match, energy close
  2. Pulse Wave - Score: 39.20
     Because: energy close
  3. Gym Hero - Score: 38.80
     Because: energy close
  4. Street Anthem - Score: 38.80
     Because: energy close
  5. Iron Cathedral - Score: 37.60
     Because: energy close

=======================================================
Profile: ACOUSTIC_CONTRADICTION
  genre=folk, mood=calm, low energy, non-acoustic
=======================================================
  1. Spacewalk Thoughts - Score: 76.80
     Because: mood match, energy close
  2. Library Rain - Score: 74.00
     Because: mood match, energy close
  3. Coffee Shop Stories - Score: 73.20
     Because: mood match, energy close
  4. Midnight Coding - Score: 71.20
     Because: mood match, energy close
  5. River Bend Song - Score: 48.50
     Because: genre match, energy close

=======================================================
Profile: MIDPOINT_ENERGY_TRAP
  genre=electronic, mood=energetic, medium energy, non-acoustic
=======================================================
  1. Pulse Wave - Score: 77.30
     Because: mood match, genre match
  2. Storm Runner - Score: 63.60
     Because: mood match
  3. Gym Hero - Score: 62.80
     Because: mood match
  4. Iron Cathedral - Score: 61.60
     Because: mood match
  5. Night Drive Loop - Score: 42.50
     Because: genre match, energy close

=======================================================
Profile: ACOUSTIC_HIGH_ENERGY_CLASH
  genre=folk, mood=energetic, high energy, acoustic
=======================================================
  1. Iron Cathedral - Score: 78.40
     Because: mood match, energy close
  2. Gym Hero - Score: 77.20
     Because: mood match, energy close
  3. Storm Runner - Score: 76.40
     Because: mood match, energy close
  4. Pulse Wave - Score: 75.20
     Because: mood match, energy close
  5. Dusty Roads - Score: 49.10
     Because: genre match, acoustic match


---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



