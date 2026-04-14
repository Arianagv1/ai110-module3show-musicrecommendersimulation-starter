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

    # User 1: upbeat pop fan who wants high-energy happy songs
    user_prefs_1 = {"genre": "pop", "mood": "happy", "energy": 0.8}

    # User 2: late-night study session — prefers calm lofi with low energy
    user_prefs_2 = {"genre": "lofi", "mood": "chill", "energy": 0.3}

    # User 3: workout listener — wants intense, high-energy rock or metal
    user_prefs_3 = {"genre": "rock", "mood": "intense", "energy": 0.95}

    # Edge case 1: contradictory energy + mood (no classical song is angry/high-energy)
    user_prefs_edge1 = {"genre": "classical", "mood": "angry", "energy": 0.95}

    # Edge case 2: genre + mood combo that doesn't exist in the dataset
    user_prefs_edge2 = {"genre": "lofi", "mood": "energetic", "energy": 0.5}

    # Edge case 3: maximally contradictory — metal genre but chill mood and zero energy
    user_prefs_edge3 = {"genre": "metal", "mood": "chill", "energy": 0.0}

    # Edge case 4: fully unknown genre and mood — nothing in the dataset matches
    user_prefs_edge4 = {"genre": "k-pop", "mood": "euphoric", "energy": 0.7}

    all_users = [
        ("Upbeat Pop Fan", user_prefs_1),
        ("Late-Night Studier", user_prefs_2),
        ("Workout Listener", user_prefs_3),
        ("[EDGE] Classical but Angry & High-Energy", user_prefs_edge1),
        ("[EDGE] Lofi but Energetic", user_prefs_edge2),
        ("[EDGE] Metal but Chill & Zero Energy", user_prefs_edge3),
        ("[EDGE] Unknown Genre & Mood", user_prefs_edge4),
    ]

    for name, user_prefs in all_users:
        recommendations = recommend_songs(user_prefs, songs, k=5)

        print("\n" + "=" * 40)
        print(f"  RECOMMENDATIONS FOR: {name}")
        print("=" * 40)
        for i, (song, score, explanation) in enumerate(recommendations, start=1):
            print(f"\n#{i}  {song['title']} by {song['artist']}")
            print(f"    Genre: {song['genre']} | Mood: {song['mood']}")
            print(f"    Score: {score:.2f}")
            print(f"    Why:   {explanation if explanation else 'No explanation yet.'}")
        print("\n" + "=" * 40)


if __name__ == "__main__":
    main()
