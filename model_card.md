# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

MoodMatcher 

---

## 2. Intended Use  

Based on a user profile, recommend top 5 songs from a catalog that most matches the vibe of the user.

---

## 3. How the Model Works  


Every song gets a score based on how well it matches four things that the user cares about: mood, genre, energy, and whether or not they like acoustic music. Mood is worth the most points, if the vibe is wrong, nothing else matters. Genre adds a smaller bonus. Energy is scored by closeness, so the closer a song's energy is to the target, the more points it earns. If they like acoustic music, any highly acoustic song gets a small extra boost. The five songs with the highest total score become their recommendations.

---

## 4. Data  

The catalog contains 18 songs, each listed with genre, mood, energy, tempo, danceability, valence, and acousticness. Genres include pop, lo-fi, rock, electronic, hip-hop, folk, jazz, classical, and a few others. Moods range from chill and happy to intense, melancholic, and romantic. The catalog skews toward high-energy tracks, half the songs have energy above 0.65 which disadvantages low energy listeners. Several moods and genres appear only once, so some users have very little to choose from.

---

## 5. Strengths  

The system works best when a user's mood and genre align with well represented parts of the catalog. The Chill Lo-Fi profile scored highest of all seven tested because mood, genre, energy, and acoustic preferenced were all used together, producing a clear top five. In general the scorer is most reliable when preferences are specific enough to match several attributes at once, making the ranking feel meaningful rather than arbitrary.

---

## 6. Limitations and Bias 

One weakness discovered during experimentation is that the energy score loses its ability to distinguish between songs when a user's preferred energy level sits near the middle of the scale (around 0.5). Because the energy score is calculated as the gap between the user's target and a song's actual energy, a midpoint target means every song in the catalog ends up with a fairly similar energy score — the best and worst songs differ by only about 17 points out of 40, compared to nearly 30 points of separation for users with a strong low or high energy preference. In practice this means the ranking for mid-energy users is almost entirely decided by mood and genre matches, making the energy preference effectively invisible. A user who genuinely wants moderately energetic music will receive the same recommendations as someone who never set an energy preference at all, because the categorical signals drown out the numeric one. This is a form of silent bias: the system appears to respect the user's energy setting, but it has almost no influence on the final output.



---

## 7. Evaluation  

Seven user profiles were tested: three standard profiles (High-Energy Pop, Chill Lo-Fi, and Deep Intense Rock) and four edge-case profiles designed to stress-test the scoring logic (Orphan Mood, Acoustic Contradiction, Midpoint Energy Trap, and Acoustic High-Energy Clash). For each profile the top five recommendations were inspected alongside their scores and reasons, and a side by side comparison was run after doubling the energy weight and halving the genre weight to see whether reweighting changed the rankings.

The most surprising result was that the Deep Intense Rock profile, which intuitively should produce the most distinct and intense recommendations, consistently returned the weakest scores of any profile with a maximum of around 44 points. The cause was that the mood value "angry" is not recognised by any synonym group in the code, so the 40 point mood bonus was never added for any song. A profile that felt clearly defined from a listener's perspective was nearly invisible to the scorer.

A second surprise came from the Acoustic Contradiction profile. The top recommendation was Spacewalk Thoughts, an ambient song with no folk genre connection. It beat River Bend Song, the only actual folk song in the top five. River Bend Song had a perfect genre match worth 12.5 points, but its mood tag "sad" did not share a synonym group with the user's preferred mood "calm", so it received zero mood points. Spacewalk Thoughts won purely because its energy value of 0.28 was marginally closer to the target of 0.20 than the other chill-mood songs, giving it a 1.4-point edge over Library Rain. A difference of less than two points in one feature decided the top rank, which made the result feel fragile rather than meaningful.

Finally, reweighting energy from 20 to 40 points and genre from 25 to 12.5 produced identical ranking orders across all six profiles, only the scores changed. This confirmed that the weight ratio matters less than the categorical attribute: once mood and genre matches are determined, numeric tuning rarely changes the order.

---

## 8. Future Work  

The most immediate fix would be expanding the mood synonym groups to cover moods like "angry" that the scorer currently ignores. Replacing the acoustic boolean with a continuous proximity score rather than just using an either or evaluation would have more meaning. Valence, danceability, and tempo are already stored in the catalog but unused in scoring so they could be used in the future as well. 

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
