from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import csv

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


def score_song(user_prefs: Dict, song: Dict) -> float:
    """Compute a relevance score for a song given a user preference profile.

    Only factors the user explicitly specified contribute to the score.
    Weights are renormalized so unspecified factors don't silently influence results.
    """
    BASE_WEIGHTS = {
        "genre":        0.25,
        "mood":         0.10,
        "energy":       0.20,
        "acousticness": 0.20,
        "valence":      0.10,
        "tempo_bpm":    0.15,
    }

    factors = {}

    if "genre" in user_prefs and user_prefs["genre"]:
        factors["genre"] = 1.0 if song["genre"] == user_prefs["genre"] else 0.0

    if "mood" in user_prefs and user_prefs["mood"]:
        factors["mood"] = 1.0 if song["mood"] == user_prefs["mood"] else 0.0

    if "energy" in user_prefs:
        factors["energy"] = 1.0 - abs(song["energy"] - user_prefs["energy"])

    if "acousticness" in user_prefs:
        factors["acousticness"] = 1.0 - abs(song["acousticness"] - user_prefs["acousticness"])

    if "valence" in user_prefs:
        factors["valence"] = 1.0 - abs(song["valence"] - user_prefs["valence"])

    if "tempo_bpm" in user_prefs:
        tempo_norm      = (song["tempo_bpm"]        - 60) / 140
        user_tempo_norm = (user_prefs["tempo_bpm"]  - 60) / 140
        factors["tempo_bpm"] = 1.0 - abs(tempo_norm - user_tempo_norm)

    if not factors:
        return 0.0

    total_weight = sum(BASE_WEIGHTS[k] for k in factors)
    score = sum(v * (BASE_WEIGHTS[k] / total_weight) for k, v in factors.items())

    return round(score, 4)


def _build_explanation(user_prefs: Dict, song: Dict) -> str:
    """Build a human-readable explanation of why a song was recommended.

    Only shows factors the user explicitly specified.
    """
    parts = []

    if "genre" in user_prefs and user_prefs["genre"]:
        hit = song["genre"] == user_prefs["genre"]
        parts.append(f"genre {'✓' if hit else '✗'} ({user_prefs['genre']} → {song['genre']})")

    if "mood" in user_prefs and user_prefs["mood"]:
        hit = song["mood"] == user_prefs["mood"]
        parts.append(f"mood {'✓' if hit else '✗'} ({user_prefs['mood']} → {song['mood']})")

    if "energy" in user_prefs:
        hit = abs(song["energy"] - user_prefs["energy"]) <= 0.15
        parts.append(f"energy {'✓' if hit else '✗'} {song['energy']:.2f} (target {user_prefs['energy']:.2f})")

    if "acousticness" in user_prefs:
        parts.append(f"acousticness {song['acousticness']:.2f} (target {user_prefs['acousticness']:.2f})")

    if "valence" in user_prefs:
        parts.append(f"valence {song['valence']:.2f} (target {user_prefs['valence']:.2f})")

    if "tempo_bpm" in user_prefs:
        hit = abs(song["tempo_bpm"] - user_prefs["tempo_bpm"]) <= 15
        parts.append(f"tempo {'✓' if hit else '✗'} {song['tempo_bpm']:.0f} bpm (target {user_prefs['tempo_bpm']:.0f})")

    if not parts:
        return "no preferences specified — scores reflect no stated preferences"

    return " | ".join(parts)


class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top-k songs ranked by how well they match the user profile."""
        user_prefs = {
            "genre": user.favorite_genre,
            "mood": user.favorite_mood,
            "energy": user.target_energy,
            "acousticness": 0.8 if user.likes_acoustic else 0.2,
        }
        ranked = sorted(
            self.songs,
            key=lambda s: (-score_song(user_prefs, vars(s)), s.title)
        )
        return ranked[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a human-readable explanation of why a song matches the user profile."""
        user_prefs = {
            "genre": user.favorite_genre,
            "mood": user.favorite_mood,
            "energy": user.target_energy,
            "acousticness": 0.8 if user.likes_acoustic else 0.2,
        }
        return _build_explanation(user_prefs, vars(song))


def load_songs(csv_path: str) -> List[Dict]:
    """Load and validate songs from a CSV file, returning a list of typed dicts."""
    print(f"Loading songs from {csv_path}...")

    with open(csv_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        if not reader.fieldnames:
            raise ValueError("The CSV file is empty or missing a header row.")

        required_columns = ["id", "title", "artist", "genre", "mood", "energy", "tempo_bpm", "valence", "danceability", "acousticness"]
        if not all(col in reader.fieldnames for col in required_columns):
            raise ValueError("Missing one or more required columns in the CSV file.")

        songs = []
        for row in reader:
            song = {k: v.strip() if isinstance(v, str) else v for k, v in row.items()}
            # Cast numeric fields
            song["id"] = int(song["id"])
            for field in ("energy", "tempo_bpm", "valence", "danceability", "acousticness"):
                song[field] = float(song[field])
            songs.append(song)

        if not songs:
            raise ValueError("The CSV file contains no song data.")

    return songs


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score all songs against user preferences and return the top-k ranked results."""
    scored = []
    for song in songs:
        score = score_song(user_prefs, song)
        explanation = _build_explanation(user_prefs, song)
        scored.append((song, score, explanation))

    top_k = sorted(
        scored,
        key=lambda x: (-x[1], x[0]["title"]),  # high score first, then A→Z on ties
    )[:k]
    return top_k
