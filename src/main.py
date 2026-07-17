"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from tabulate import tabulate

from recommender import load_songs, recommend_songs


# --- User Preference Profiles ---
# Categorical fields are matched exactly; numeric fields use a 0.0–1.0 scale
# where the scorer rewards proximity to the target value.

HIGH_ENERGY_POP = {
    "favorite_genre": "pop",
    "favorite_mood": "happy",
    "target_energy": 0.90,          # very high energy
    "target_valence": 0.85,         # uplifting and positive
    "target_danceability": 0.88,    # highly dance-friendly
    "target_acousticness": 0.10,    # electronic over acoustic
    "target_tempo_norm": 0.70,      # fast tempo (~150 BPM range)
    "likes_acoustic": False,
    "likes_high_tempo": True,
}

CHILL_LOFI = {
    "favorite_genre": "lo-fi",
    "favorite_mood": "chill",
    "target_energy": 0.25,          # low energy
    "target_valence": 0.50,         # neutral / laid-back mood
    "target_danceability": 0.40,    # gentle groove, not dance-floor
    "target_acousticness": 0.70,    # warm, acoustic-leaning textures
    "target_tempo_norm": 0.25,      # slow tempo (~75 BPM range)
    "likes_acoustic": True,
    "likes_high_tempo": False,
}

DEEP_INTENSE_ROCK = {
    "favorite_genre": "rock",
    "favorite_mood": "angry",
    "target_energy": 0.95,          # maximum intensity
    "target_valence": 0.20,         # dark and brooding
    "target_danceability": 0.35,    # raw power over groove
    "target_acousticness": 0.05,    # heavily electric / distorted
    "target_tempo_norm": 0.80,      # aggressive tempo (~165 BPM range)
    "likes_acoustic": False,
    "likes_high_tempo": True,
}


# --- Edge Case Profiles ---
# Each one is designed to expose a specific gap or unexpected behavior in score_song.

# EDGE 1: "angry" is not in any MOOD_GROUP synonym cluster, so it only matches songs
# whose CSV mood field is the exact string "angry". If no songs use that exact value,
# the +40 mood bonus is never awarded — this affects DEEP_INTENSE_ROCK too.
ORPHAN_MOOD = {
    "favorite_genre": "rock",
    "favorite_mood": "angry",      # not in MOOD_GROUPS → no synonym benefit
    "target_energy": 0.90,
    "likes_acoustic": False,
    "target_acousticness": 0.05,
    "target_valence": 0.10,
    "target_danceability": 0.30,
    "target_tempo_norm": 0.80,
    "likes_high_tempo": True,
}

# EDGE 2: Exposes the likes_acoustic / target_acousticness split. Setting likes_acoustic=False
# disables the +15 bonus, but target_acousticness=0.95 is still silently ignored.
# The score is identical regardless of what target_acousticness is set to.
ACOUSTIC_CONTRADICTION = {
    "favorite_genre": "folk",
    "favorite_mood": "calm",
    "target_energy": 0.20,
    "likes_acoustic": False,       # acoustic bonus disabled...
    "target_acousticness": 0.95,   # ...but this has zero effect on scoring anyway
    "target_valence": 0.60,
    "target_danceability": 0.20,
    "target_tempo_norm": 0.15,
    "likes_high_tempo": False,
}

# EDGE 3: target_energy=0.5 minimizes energy score variance to at most 10 pts across
# ALL songs (vs 20 pts at the extremes). Categorical matches dominate even harder here —
# numeric tuning is nearly meaningless and the top-5 are decided almost entirely by mood/genre.
MIDPOINT_ENERGY_TRAP = {
    "favorite_genre": "electronic",
    "favorite_mood": "energetic",
    "target_energy": 0.50,         # max energy spread = 10 pts, not 20
    "likes_acoustic": False,
    "target_acousticness": 0.10,
    "target_valence": 0.70,
    "target_danceability": 0.75,
    "target_tempo_norm": 0.60,
    "likes_high_tempo": True,
}

# EDGE 4: likes_acoustic=True awards +15 to any song with acousticness > 0.6, while
# target_energy=1.0 wants maximum energy. High-acoustic and high-energy songs are rare,
# so the scorer may rank a quiet acoustic song above a high-energy one — the boolean
# bonus outweighs a 15-pt energy gap.
ACOUSTIC_HIGH_ENERGY_CLASH = {
    "favorite_genre": "folk",
    "favorite_mood": "energetic",
    "target_energy": 1.0,
    "likes_acoustic": True,        # +15 fires for acousticness > 0.6, no energy check
    "target_acousticness": 0.90,
    "target_valence": 0.70,
    "target_danceability": 0.60,
    "target_tempo_norm": 0.85,
    "likes_high_tempo": True,
}


def main() -> None:
    songs = load_songs("data/songs.csv")

    # Switch between profiles to test different recommendation results.
    user_prefs = HIGH_ENERGY_POP
    # user_prefs = CHILL_LOFI
    # user_prefs = DEEP_INTENSE_ROCK
    # --- edge cases ---
    # user_prefs = ORPHAN_MOOD                 # "angry" is outside all synonym groups
    # user_prefs = ACOUSTIC_CONTRADICTION      # target_acousticness is silently ignored
    # user_prefs = MIDPOINT_ENERGY_TRAP        # categorical matches dominate when energy=0.5
    # user_prefs = ACOUSTIC_HIGH_ENERGY_CLASH  # acoustic bonus overrides energy mismatch

    recommendations = recommend_songs(user_prefs, songs, k=5)

    energy = user_prefs['target_energy']
    energy_label = "high energy" if energy >= 0.7 else "medium energy" if energy >= 0.4 else "low energy"
    acoustic_label = "acoustic" if user_prefs.get('likes_acoustic', False) else "non-acoustic"
    print(f"\nUser profile: genre={user_prefs['favorite_genre']}, mood={user_prefs['favorite_mood']}, "
          f"{energy_label}, {acoustic_label}")
    print("\nTop 5 recommendations:\n")

    rows = []
    for i, (song, score, explanation) in enumerate(recommendations, start=1):
        rows.append([
            i,
            song['title'],
            song['artist'],
            song['genre'],
            song['mood'],
            f"{song['energy']:.2f}",
            f"{song['acousticness']:.2f}",
            f"{score:.1f}",
            explanation,
        ])

    headers = ["#", "Title", "Artist", "Genre", "Mood", "Energy", "Acoustic", "Score", "Reasons"]
    print(tabulate(rows, headers=headers, tablefmt="grid"))
    print()


if __name__ == "__main__":
    main()
