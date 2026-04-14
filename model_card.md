# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

## 2. Intended Use  

- What kind of recommendations does it generate  
Classroom simulation designed to explore how preference-based scoring systems work, not a production music service. It is built for students and developers learing how recommendation logic is designed, weighted, and evaluated. 
- What assumptions does it make about the user 
It assumes users can express preferences as explicit key value pairs (genre, mood, energy level).  
- Is this for real users or classroom exploration  
Classroom exploration, the dataset is small and hand curated and the scoring is fully transparent and inspectable. Edge case profiles are deliberately adversarial.

---

## 3. How the Model Works  

Each song in the catalog has a set of descriptive attributes: genre, mood, energy level, acousticness, valence (how positive or upbeat it sounds), and tempo in BPM. When a user provides their preferences, the system compares each song's attributes against what the user asked for and produces a score between 0 and 1.

Genre and mood are treated as yes-or-no matches — a song either matches your preferred genre or it doesn't. Energy, acousticness, valence, and tempo are treated as a sliding scale — the closer the song's value is to what you asked for, the higher it scores on that factor.

Each factor carries a different weight reflecting how much it should matter. Genre is the strongest signal (25%), followed by energy and acousticness (20% each), tempo (15%), and mood and valence (10% each).

The final score is a weighted average of only the factors the user actually specified. If a user doesn't mention acousticness, that factor is dropped entirely and the remaining weights are rescaled to still add up to 100% — this prevents unspecified preferences from silently influencing results.

The top-k highest scoring songs are returned with a plain-language explanation showing which factors matched, which didn't, and by how much.

**Changes from the starter logic:**
The original system defaulted unspecified fields to midpoint values (0.5 for numeric fields, 120 bpm for tempo), which meant every recommendation was secretly influenced by preferences the user never expressed. The updated system only scores what the user explicitly provides, and renormalizes weights accordingly.

---

## 4. Data  

The catalog contains **19 songs** across 15 genres: pop, lofi, rock, ambient, jazz, synthwave, indie pop, classical, hip-hop, r&b, country, metal, folk, reggae, and latin.

Moods represented include: happy, chill, intense, focused, peaceful, confident, romantic, nostalgic, angry, melancholic, uplifting, energetic, moody, and relaxed.

No songs were added or removed from the original dataset.

**Gaps in musical taste coverage:**
- Several genres have only one song (ambient, jazz, synthwave, classical, hip-hop, r&b, country, metal, folk, reggae, latin), meaning users who prefer those genres have almost no competition among candidates — recommendations are less meaningful with a pool that small.
- Electronic subgenres (house, drum and bass, techno) are entirely absent.
- No two songs share the same genre *and* mood combination, so the system can never reward a perfect categorical double-match.
- Tempo ranges cluster around 60–170 bpm with no representation of very slow (under 60) or extremely fast (over 170) music.

---

## 5. Strengths  

The system works best for users with **clear, specific preferences** across multiple factors. A user who specifies genre, mood, and energy gets a score that meaningfully differentiates songs — the renormalized weighting ensures all three factors carry real influence rather than being diluted by phantom defaults.

**User types it handles well:**
- **Pop or lofi listeners** — these genres have multiple songs in the catalog, so the recommender has real candidates to rank rather than defaulting to partial matches.
- **Energy-first listeners** — the continuous energy scoring captures gradations well; a user wanting `energy: 0.9` will consistently see high-energy songs rise to the top.
- **Users who specify only a few preferences** — thanks to the null-default fix, a user who only cares about genre and mood gets a clean two-factor score rather than one polluted by acousticness and valence they never expressed.

**Patterns the scoring captures correctly:**
- Genre loyalty: a user who strongly identifies with one genre will reliably see that genre dominate their top results.
- The explanation output makes it easy to spot when a high score is driven by a single strong match versus several partial matches — useful for understanding why a recommendation surfaced.

---

## 6. Limitations and Bias 

**Features it does not consider:**
The system has no concept of an artist, release year, song popularity, listening history, or user feedback. Two songs by the same artist score identically to two songs by different artists. There is also no notion of discovery — a song the user has already heard ranks the same as one they haven't.

**Genres or moods that are underrepresented:**
11 of the 15 genres have exactly one song in the catalog. A user who prefers ambient, jazz, metal, classical, or latin music will always see the same one song at the top of their results, with the remaining four slots filled by partial matches from unrelated genres. Moods like "confident," "nostalgic," "romantic," and "melancholic" each appear only once, so a mood-first listener has almost no meaningful competition among candidates.

**Cases where the system overfits to one preference:**
Genre is the heaviest single factor at 25%. A song that matches genre but misses on every other dimension can still outscore a song with near-perfect energy, mood, and tempo alignment that simply belongs to a different genre. The Midnight Coding example illustrated this directly — a lofi song with a mismatched mood scored 0.79 for an "energetic" user purely because genre matched.

**Ways the scoring might unintentionally favor some users:**
- Pop listeners benefit from having the largest genre pool (3 songs), giving the system real candidates to differentiate.
- Users who think to specify more preferences get more accurate and meaningful scores than users who only set one or two fields, since renormalization gives each specified factor more influence. A minimalist user profile produces a shallower ranking.
- The binary genre and mood matching penalizes users whose taste sits between categories (e.g. someone who likes both indie pop and pop gets no credit for the overlap).

---

## 7. Evaluation  

**Profiles tested:**
Seven profiles were run: three standard users (upbeat pop fan, late-night studier, workout listener) and four adversarial edge cases (classical/angry/high-energy, lofi/energetic, metal/chill/zero-energy, unknown genre and mood).

**What we looked for:**
For standard profiles, we checked whether the top results were intuitively reasonable — that a pop/happy/high-energy user received upbeat pop songs, and that a lofi/chill/low-energy user received calm, acoustic songs. For edge cases, we looked for scoring failures: results that ranked high despite clearly mismatching the user's intent.

**What was surprising:**
The most revealing result came from the lofi/energetic edge case (edge 2). Midnight Coding by LoRoom — a chill, low-energy lofi track — scored 0.79 as the top recommendation for a user explicitly wanting energetic music. The genre match alone (worth 0.25) outweighed the mood mismatch (worth only 0.10), demonstrating that categorical weight dominance can override obvious incompatibilities.

The unknown genre/mood profile (edge 4) also revealed how the original system's defaults created artificial score variation even when nothing the user wanted existed in the catalog. After the null-default fix, this profile now correctly produces near-flat scores, making the failure mode transparent rather than hidden.

**Comparisons run:**
The before/after contrast between the original default-0.5 scoring and the renormalized null-default scoring was the most informative comparison. For users who only specified genre and energy, scores shifted noticeably because acousticness and valence (previously worth 30% combined) were removed from the calculation entirely.

---

## 8. Future Work  

**Additional features or preferences:**
The most impactful addition would be **genre adjacency** — a similarity map that treats rock and metal as closer than rock and jazz, allowing partial credit for related genres rather than a hard binary match. Adding **danceability** as an optional user preference would also serve a meaningful segment of users that the current system cannot distinguish.

**Better ways to explain recommendations:**
The current explanation shows factor-by-factor matches but doesn't tell the user what *weight* each factor carried in their specific scoring context. A future explanation could show the weighted contribution per factor (e.g. "genre contributed 0.25 of your 0.79 score"), making it immediately clear when a single factor is dominating the result.

**Improving diversity among the top results:**
The current system can return five songs from the same genre if they all outscore songs from other genres. A diversity penalty — reducing the score of a song if a higher-ranked result already shares its genre — would force broader exploration across the catalog.

**Handling more complex user tastes:**
Real listeners rarely have a single fixed profile. A future version could support **blended profiles** (e.g. "I want lofi for studying but pop for working out") or **negative preferences** (e.g. "never recommend metal"), neither of which the current scoring model can express.

---

## 9. Personal Reflection  

Building this simulation made it clear that recommendation systems are less about finding the "best" song and more about deciding which definition of "best" to encode — and that every weight, default, and fallback is a quiet design choice with real consequences for who gets good results and who doesn't.

The most unexpected discovery was how much influence unspecified preferences had in the original system. A user who said nothing about acousticness was still being quietly sorted by it, with songs near 0.5 acousticness getting a silent boost. It looked like the system was working, but for the wrong reasons.

This changed how I think about apps like Apple Music. When a playlist feels surprisingly accurate, it likely isn't because the algorithm understood your taste — it's because your listening history gave it enough explicit signal to score on real preferences rather than defaults. When recommendations feel off, it may be that the system is filling in gaps with assumptions you never made.
