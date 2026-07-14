import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, asdict

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        """Store the song catalog for scoring."""
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top-k songs ranked by score for the given user."""
        user_prefs = {
            "favorite_genre": user.favorite_genre,
            "favorite_mood": user.favorite_mood,
            "target_energy": user.target_energy,
            "likes_acoustic": user.likes_acoustic,
        }
        scored = [(song, score_song(user_prefs, asdict(song))[0]) for song in self.songs]
        scored.sort(key=lambda x: x[1], reverse=True)
        return [song for song, _ in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a human-readable score and reason string for a song."""
        user_prefs = {
            "favorite_genre": user.favorite_genre,
            "favorite_mood": user.favorite_mood,
            "target_energy": user.target_energy,
            "likes_acoustic": user.likes_acoustic,
        }
        score, reasons = score_song(user_prefs, asdict(song))
        label = ", ".join(reasons) if reasons else "no strong match"
        return f"Score: {score}/100 — {label}"

MOOD_GROUPS: List[set] = [
    {"happy", "upbeat", "joyful", "cheerful"},
    {"chill", "relaxed", "calm", "mellow"},
    {"intense", "energetic", "powerful", "aggressive"},
    {"melancholic", "sad", "somber"},
    {"focused", "concentrated"},
    {"moody", "brooding"},
    {"confident", "bold"},
    {"romantic", "loving"},
    {"nostalgic", "wistful"},
    {"passionate", "fierce"},
]

GENRE_GROUPS: List[set] = [
    {"pop", "indie pop", "synth pop"},
    {"electronic", "synthwave", "edm"},
    {"hip-hop", "hip hop", "rap"},
    {"r&b", "rnb", "soul"},
    {"folk", "country"},
    {"lofi", "lo-fi"},
    {"classical", "orchestral"},
]

def _normalize(value: str) -> str:
    """Lowercase and strip whitespace for consistent comparisons."""
    return value.strip().lower()

def _same_group(a: str, b: str, groups: List[set]) -> bool:
    """Return True if both values are equal or belong to the same synonym group."""
    a, b = _normalize(a), _normalize(b)
    if a == b:
        return True
    return any(a in group and b in group for group in groups)

def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file and cast numeric fields to the correct types."""
    print(f"Loading songs from {csv_path}...")
    songs = []
    with open(csv_path, newline='', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            row['id'] = int(row['id'])
            row['energy'] = float(row['energy'])
            row['tempo_bpm'] = float(row['tempo_bpm'])
            row['valence'] = float(row['valence'])
            row['danceability'] = float(row['danceability'])
            row['acousticness'] = float(row['acousticness'])
            songs.append(row)
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score a single song against user preferences, returning (score, reasons)."""
    score = 0.0
    reasons = []

    if _same_group(song['mood'], user_prefs['favorite_mood'], MOOD_GROUPS):
        score += 40
        reasons.append("mood match")

    if _same_group(song['genre'], user_prefs['favorite_genre'], GENRE_GROUPS):
        score += 25
        reasons.append("genre match")

    energy_pts = 20 * (1 - abs(user_prefs['target_energy'] - song['energy']))
    score += energy_pts
    if energy_pts >= 15:
        reasons.append("energy close")

    if user_prefs.get('likes_acoustic', False) and song['acousticness'] > 0.6:
        score += 15
        reasons.append("acoustic match")

    return round(score, 1), reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score all songs, sort by score descending, and return the top k results."""
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = ", ".join(reasons) if reasons else "no strong match"
        scored.append((song, score, explanation))
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:k]
