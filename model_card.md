# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

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

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
