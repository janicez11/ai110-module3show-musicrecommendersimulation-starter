"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv") 

    # User taste profile — reference values used for scoring each song.
    # Categorical fields are matched exactly; numeric fields (0.0–1.0 scale)
    # are compared by proximity to the song's actual feature value.
    user_prefs = {
        # Categorical preferences
        "favorite_genre": "pop",             # preferred genre for an exact-match bonus
        "favorite_mood": "happy",           # preferred mood for an exact-match bonus

        # Numeric feature targets (0.0 = low, 1.0 = high)
        "target_energy": 0.82,             # how energetic the music should feel
        "target_valence": 0.80,            # emotional positivity (low = darker, high = uplifting)
        "target_danceability": 0.80,       # how rhythm-driven / dance-friendly
        "target_acousticness": 0.15,       # preference for acoustic vs. electronic sound
        "target_tempo_norm": 0.55,         # normalized tempo (0 ≈ 60 BPM, 1 ≈ 180 BPM)

        # Boolean flag that influences scoring logic
        "likes_high_tempo": True,          # if True, boosts songs above ~130 BPM
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    energy = user_prefs['target_energy']
    energy_label = "high energy" if energy >= 0.7 else "medium energy" if energy >= 0.4 else "low energy"
    acoustic_label = "acoustic" if user_prefs.get('likes_acoustic', False) else "non-acoustic"
    print(f"\nUser profile: genre={user_prefs['favorite_genre']}, mood={user_prefs['favorite_mood']}, "
          f"{energy_label}, {acoustic_label}")
    print("\nTop recommendations:\n")
    for i, rec in enumerate(recommendations, start=1):
        song, score, explanation = rec
        print(f"{i}. {song['title']} - Score: {score:.2f}")
        print(f"   Because: {explanation}")
        print()


if __name__ == "__main__":
    main()
