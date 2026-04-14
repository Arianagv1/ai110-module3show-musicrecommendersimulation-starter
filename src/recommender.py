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

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

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
        explanation = ""
        scored.append((song, score, explanation))

    top_k = sorted(
        scored,
        key=lambda x: (-x[1], x[0]["title"]),  # high score first, then A→Z on ties
    )[:k]
    return top_k


def score_song(user_prefs: Dict, song: Dict) -> float:
    """Compute a relevance score for a song given a user preference profile."""
    # TODO: Implement scoring logic
    return 0.0
