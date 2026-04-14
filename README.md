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
Every Song object will have the following 10 features. The first one being id, the second title, the third artist, the fourth genre (pop, lofi, rock, jazz, ambient, synthwave, and indie pop), the fifth mood (emotion mood tag-happy, chill, intense, relaxed, focused, moody), the sixth energy (intensity/activity level from 0.0 - 1.0), the seventh tempo beats per minute, the eighth valence (musical positivity/happiness), the ninth danceability (suitability for dancing on scale 0.0 - 1.0), and the tenth acousticness (acoustic vs electronic 0.0 - 1.0).

- What information does your `UserProfile` store
Based off of the AI's analysis of apps like youtube, spotify, and apple music, it suggested that the four most significant and effective features for the recommender are energy, mood, acousticness, and tempo_bmp. 

- How does your `Recommender` compute a score for each song
The formula derived is:
  feature_score = 1 - |song_value - user_preference|

This allows the score to stay within 0 and 1, where songs close to the user's preference score near 1.0 and distant songs score near 0.0.

The weighted total score for one song is calculated as follows: 
total_score = (w_energy   × energy_score)
            + (w_acousticness × acousticness_score)
            + (w_tempo    × tempo_score)
            + (w_valence  × valence_score)
            + (w_genre    × genre_match)
            + (w_mood     × mood_match)


In addition, each of the songs will have different weights for their features, which copilot recommended as: 
w_energy        = 0.20
w_acousticness  = 0.20
w_tempo         = 0.15
w_valence       = 0.10
w_genre         = 0.25   ← highest categorical weight
w_mood          = 0.10
                --------
Total           = 1.00

One important thing to note is that a scoring rule and ranking rule is needed to make a recommender. Scoring will operate on a single song isolation and produce a numeric value encoding what the user wants via preferenecs and weights, and the ranking rule with operate on the entire catalog after scoring, from highest to lowest giving us a recommendation list (avoids randomness).

- How do you choose which songs to recommend
The intended scoring approach would compare each userProfile field against the matchign Song field. As follows:

Genre match would receieve points if song.genre == user.fav_genre

Mood match would receieve points if song.mood == user.fav_mood

And so on for energy closeness (reference the formula) and acoustic preference. 

Thus, each component contributes a partial score, which are summed into a total score per song. Then, we sort all songs by descending score and return the top k (ex: top three).

Note: this is content-based filtering approach where recommendations are driven entirely by how well a song's attributes are matched with user's stated preferences.
You can include a simple diagram or bullet list if helpful.


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


---

## 7. `model_card_template.md`

Combines reflection and model card framing from the Module 3 guidance. :contentReference[oaicite:2]{index=2}  

```markdown
# 🎧 Model Card - Music Recommender Simulation

## 1. Model Name

Give your recommender a name, for example:

> VibeFinder 1.0

---

## 2. Intended Use

- What is this system trying to do
- Who is it for

Example:

> This model suggests 3 to 5 songs from a small catalog based on a user's preferred genre, mood, and energy level. It is for classroom exploration only, not for real users.

---

## 3. How It Works (Short Explanation)

Describe your scoring logic in plain language.

Overview: 
My recommender is a content-based ranker that reads all songs from the csv file, and for each song, it will compute a total score : {0,1} and sort songs
that score highest first, returning the top k. This k represents every feature contributing to a partial score, signiffying how well this song matches the user on this feature. It also implements a weighting strategy for how important each feature is. 

- What features of each song does it consider & What information about the user does it use

Every user profile will need to be defined by the following characteristics: fav_genre, fav_mood, target_energy, target_acousticness, target_valence, target_tempo_bpm, and target_danceability. 

- How does it turn those into a number
The first part of this algorithm deals with normalizing fields into the same scale. The formula will calculate the feature score by subtracting 1 - (song value - user preference), which behaves correctly when both values are on the same 0.1 scale. Next, the similarity scores are computed. For each numeric feature, we follow this formula: score = 1 - abs(song norm - user norm). The same follows for acousticness, valence, temp norm, and danceability. From this, we conclude that if a song is close to the usser preference it should score near 1.0 and if its far, it trends towards 0. The next part of the formula will compute categorical matches (genre & mood matches using binary system), and finally we combine everything with weights where the total score is finally calculated (formula listed in How Everything Works Section). 

Try to avoid code in this section, treat it like an explanation to a non programmer.

---

## 4. Data

Describe your dataset.

- How many songs are in `data/songs.csv`
- Did you add or remove any songs
- What kinds of genres or moods are represented
- Whose taste does this data mostly reflect

---

## 5. Strengths

Where does your recommender work well

You can think about:
- Situations where the top results "felt right"
- Particular user profiles it served well
- Simplicity or transparency benefits

---

## 6. Limitations and Bias

Where does your recommender struggle

Some prompts:
- Does it ignore some genres or moods
- Does it treat all users as if they have the same taste shape
- Is it biased toward high energy or one genre by default
- How could this be unfair if used in a real product

---

## 7. Evaluation

How did you check your system

Examples:
- You tried multiple user profiles and wrote down whether the results matched your expectations
- You compared your simulation to what a real app like Spotify or YouTube tends to recommend
- You wrote tests for your scoring logic

You do not need a numeric metric, but if you used one, explain what it measures.

---

## 8. Future Work

If you had more time, how would you improve this recommender

Examples:

- Add support for multiple users and "group vibe" recommendations
- Balance diversity of songs instead of always picking the closest match
- Use more features, like tempo ranges or lyric themes

---

## 9. Personal Reflection

A few sentences about what you learned:

- What surprised you about how your system behaved
- How did building this change how you think about real music recommenders
- Where do you think human judgment still matters, even if the model seems "smart"

