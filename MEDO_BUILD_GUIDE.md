# MeDo Build Guide — Vedic Cognitive Fingerprint

Step-by-step instructions to build the hackathon submission on MeDo.

---

## Phase 1: Deploy the Backend (do this first)

The MeDo app will call our FastAPI backend via HTTP connector. It needs a public URL.

### 1A. Push to GitHub

```bash
# In your MeDo project folder:
gh repo create vedic-cognitive-fingerprint --public --source . --push
```
Or manually: go to github.com → New repo → `vedic-cognitive-fingerprint` → push this folder.

### 1B. Deploy to Railway

1. Go to **railway.app** → sign up / log in
2. Click **New Project** → **Deploy from GitHub repo**
3. Select `vedic-cognitive-fingerprint`
4. Railway auto-detects our `railway.json` → click **Deploy**
5. Go to **Variables** tab → add:
   - `ASTROLOGY_API_KEY` = `hzVpTo2Sqz4LvAqrokYxV1Q1TBtiewJY6gNBx5aA`
6. Go to **Settings** → **Networking** → **Generate Domain**
7. Copy the URL — looks like: `https://vedic-xxx.up.railway.app`

Test it: `curl https://your-url.up.railway.app/health` should return `{"status":"ok"}`

---

## Phase 2: Build in MeDo

Go to **medo.dev** → sign in → **Create new app**

Use these 5 prompts IN ORDER. Wait for MeDo to finish each one before sending the next.

---

### Prompt 1 — Foundation + Birth Form

```
Build a dark-themed multi-page web app called "Vedic Cognitive Fingerprint".

Color scheme: dark navy background (#0A0A12), gold accent (#C9A84C), deep blue (#4C8EC9).

Page 1 — Landing:
- Large title "Vedic Cognitive Fingerprint"
- Tagline: "What the stars predicted. What you actually chose. The gap between them is where you really live."
- Three bullet points:
  • Your Vedic birth chart maps a predicted cognitive blueprint
  • 12 honest scenarios reveal how your mind actually operates
  • See where ancient wisdom and your real choices align — and where they don't
- Small disclaimer text: "For reflection and self-discovery · Not scientific diagnosis"
- CTA button: "Map my mind →"

Page 2 — Birth Details form with:
- Text input: "What should we call you?"
- Date picker: "Date of birth"
- Time picker: "Time of birth" (with note: "Approximate hour works fine")
- Text input: "Place of birth" (city, country)
- Hidden fields for latitude, longitude, timezone
- Submit button: "Plot my cognitive coordinates →"

On submit, call this external API:
POST https://YOUR-RAILWAY-URL/api/vedic-profile
Headers: Content-Type: application/json
Body: { "name": [name field], "year": [year from dob], "month": [month from dob], "date": [day from dob], "hours": [hours from time], "minutes": [minutes from time], "seconds": 0, "latitude": 18.5204, "longitude": 73.8567, "timezone": 5.5 }

Store the API response (session_id, moon_nakshatra_name, moon_sign, mercury_sign, ascendant_sign, predicted_scores, nakshatra_description, chart_svg_url) in the app state.

Show a loading state while the API call is in progress.
```

> **After this:** Replace `YOUR-RAILWAY-URL` with your actual Railway URL. Also fix the geocoding — we'll add real lat/lon in Prompt 2.

---

### Prompt 2 — Blueprint Screen + Geocoding

```
Add Page 3 — Vedic Blueprint:

After the birth form API call succeeds, show:
- A badge with the Moon Nakshatra name (e.g., "Satabisha")
- Title: "[Name]'s Vedic Cognitive Blueprint"
- The nakshatra_description text from the API response
- Planet pills showing: Moon in [moon_sign], Mercury in [mercury_sign], Rising [ascendant_sign]
- The birth chart image loaded from chart_svg_url
- Transition text: "That's what the stars predicted about you. Now let's see what your actual choices reveal."
- Button: "Start the assessment →"

Also update the birth form:
- When the user types in the "Place of birth" field, after 700ms of no typing, call:
  GET https://nominatim.openstreetmap.org/search?q=[city input]&format=json&limit=1
  Extract lat, lon from the result
- Use the real lat/lon in the /api/vedic-profile call instead of hardcoded values
- For timezone, calculate from longitude: Math.round(longitude / 15 * 2) / 2
- Show a small status message under the city field: "✓ [City name] located" when geocoding succeeds
- Disable the submit button until geocoding succeeds
```

---

### Prompt 3 — 12-Scenario Assessment

```
Add Page 4 — Assessment:

Show 12 scenario cards one at a time with a progress bar at the top.

Each card shows:
- The scenario text
- 2-3 answer options as large tap-friendly buttons

Here are the 12 scenarios and answers (store the answer key, e.g. "A", "B", "C"):

Scenario s01: "You need to respond to an urgent message. You have 30 seconds."
A: Write fast, send it, deal with any clarification after
B: Take 2 minutes to think it through properly even if it's "late"
C: Send a quick "on it" placeholder while you think

Scenario s02: "You're solving a problem you've never seen before."
A: Look for patterns — something about this feels familiar
B: Break it down systematically, step by step
C: Google for similar problems first

Scenario s03: "A colleague asks your honest opinion on their work. It needs improvement."
A: Tell them directly — they asked, they deserve the truth
B: Find the good parts first, then mention what could be stronger
C: Ask questions to help them see the issues themselves

Scenario s04: "You have one hour of free time. You use it to..."
A: Catch up on something you've been putting off
B: Do something that has no outcome — just exists for itself
C: Plan the next thing

Scenario s05: "A decision needs to be made. You have 60% of the information."
A: Make the call — more data rarely changes the right answer
B: Push for more information before deciding
C: Make a provisional call but explicitly flag it as revisable

Scenario s06: "You're working on a long project. Your instinct is to..."
A: Map out the whole thing before starting
B: Start with what you know and let the shape emerge
C: Find the hardest part and solve that first

Scenario s07: "A rule exists that you think is wrong."
A: Follow it — rules exist for reasons you might not see
B: Break it quietly if the outcome is better
C: Push to change it through the right channels

Scenario s08: "Someone is upset. Your first move is..."
A: Ask what they need from you right now
B: Try to fix or solve the problem
C: Give them space and come back later

Scenario s09: "You have $500 to use by end of week."
A: Invest it in something with potential long-term value
B: Save it — you'll find a better use later
C: Spend it on something that improves your life right now

Scenario s10: "Your approach to long projects is..."
A: I prefer to see the whole map before I start
B: I prefer to start moving and figure it out as I go
C: I alternate between planning and doing

Scenario s11: "A project you care about is behind schedule."
A: Work longer hours to catch up
B: Cut scope — deliver less but on time
C: Be transparent about the delay and reset expectations

Scenario s12: "When you get feedback you disagree with..."
A: Listen fully, then explain your reasoning
B: Update your thinking if the argument is good
C: Acknowledge it and privately decide if it changes anything

After all 12 are answered, show a brief "Mapping your mind..." loading screen with a pulsing animation.

Then call:
POST https://YOUR-RAILWAY-URL/api/score-assessment
Body: { "session_id": [stored session_id], "responses": { "s01": [answer], "s02": [answer], ... "s12": [answer] } }

Store the response (behavioral_scores, predicted_scores, alignment_score, divergence_points, aligned_traits, dimension_labels).
```

---

### Prompt 4 — Fingerprint Radar Chart

```
Add Page 5 — Cognitive Fingerprint Reveal:

Show a radar/spider chart with these 8 axes (in order):
Processing Speed, Reasoning Style, Risk Tolerance, Focus Mode,
Decision Driver, Certainty Need, Thinking Mode, Time Horizon

Draw TWO overlapping shapes on the same chart:
- Gold shape: the predicted_scores from the Vedic blueprint
- Blue/steel shape: the behavioral_scores from the assessment
- Both shapes semi-transparent so overlap shows

Above the chart:
- Title: "Your Vedic Cognitive Fingerprint"
- Subtitle: "Gold is who your chart said you'd be. Blue is who you are when it counts."

Below the chart:
- Alignment badge showing the alignment_score as a percentage
  - 80-100%: "Deeply anchored" (gold)
  - 60-79%: "Mostly aligned" (blue-green)
  - 40-59%: "Interesting divergence" (orange)
  - Below 40%: "Significantly different" (purple)
- Legend row: Gold dot = "Vedic blueprint", Blue dot = "Your behavior", Overlap dot = "Anchored traits"
- Button: "See your insights →"
```

---

### Prompt 5 — ERNIE AI Insights + Share Card

```
Add Page 6 — Insights:

When the user clicks "See your insights →", use ERNIE AI to generate personalized insights.

Send ERNIE this prompt (fill in the real values):

"You are a wise, thoughtful friend helping someone understand their mind. Based on this data, write 3-4 short insights (each 2-3 sentences) about this person. Make them feel like genuine observations, not clinical reports. Use their first name. Sound like a perceptive human, not AI.

Person's name: [first name]
Moon Nakshatra: [moon_nakshatra_name]
Vedic blueprint scores (1-10 scale, 8 dimensions):
- Processing Speed: [value]
- Reasoning Style: [value] (1=analytical, 10=intuitive)
- Risk Tolerance: [value]
- Focus Mode: [value] (1=detail, 10=big picture)
- Decision Driver: [value] (1=data-driven, 10=emotion-driven)
- Certainty Need: [value]
- Thinking Mode: [value] (1=independent, 10=collaborative)
- Time Horizon: [value] (1=present, 10=future-oriented)

Behavioral scores from their actual choices:
[same 8 dimensions with behavioral values]

Alignment score: [alignment_score]%
Dimensions that diverged most: [divergence_points list]

Format: 3-4 paragraphs, each starting with a bold one-line title. No bullet points. No headers. Write like you're talking to them, not about them."

Display each insight as a card with the title on top and body text below.

Also add closing text: "This is a mirror, not a verdict. Use it however feels true."
Disclaimer: "For reflection and self-discovery · Not scientific diagnosis"

Then add Page 7 — Share:
- Show a shareable card with:
  - Title: "✦ Vedic Cognitive Fingerprint"
  - Person's name + Nakshatra
  - Mini version of the radar chart
  - Alignment score
  - First insight title
  - "Discover yours → vedic-fingerprint.app"
- Share buttons for X (Twitter) and LinkedIn that pre-fill text:
  "I just mapped my cognitive fingerprint. [X]% alignment between my Vedic chart and how I actually think. Take yours: [app URL] #BuiltWithMeDo #VedicFingerprint"
- Copy link button
- "Start over" ghost button
```

---

## Phase 3: After Building in MeDo

1. **Test** the full flow: birth → blueprint → assessment → fingerprint → insights → share
2. **Deploy** using MeDo's one-click deploy button → copy the public URL
3. **Share on Discord** in the #Showcase channel for the Community Choice Award
4. **Post on X / LinkedIn** with `#BuiltWithMeDo` for the Creative Content Award
5. **Record demo video** (3 min) — see outline in project_plan.md
6. **Submit on Devpost** at medo.devpost.com

---

## What to Write in the Devpost Submission

> Most self-discovery tools tell you WHO you are. Your Vedic Cognitive Fingerprint maps HOW your mind actually operates — then shows you how close that is to what your Vedic birth chart predicted.
>
> Built on MeDo using:
> - **ERNIE AI** — generates 3-4 personalized insights based on alignment data
> - **HTTP connector** — calls FreeAstrologyAPI (via our proxy) to calculate Moon Nakshatra, Mercury placement, and Ascendant from birth details
> - **Radar chart visualization** — dual-overlay spider chart showing predicted vs. behavioral cognitive fingerprint
> - **One-click deploy** — shareable public profile URL for every user
> - **Database** — stores user sessions, birth data, assessment responses, and fingerprint scores
>
> For reflection and self-discovery — not scientific diagnosis.

---

## Prize Targets

| Prize | Strategy |
|---|---|
| **Best Surprise Us!** ($4,500) | Primary — most unique concept |
| **1st/2nd/3rd Place** ($10K/$6K/$4K) | Secondary — aim for top 3 |
| **Community Choice** ($500 × 5) | Post in MeDo Discord #Showcase |
| **Creative Content** ($500 × 10) | Post on X/LinkedIn with #BuiltWithMeDo |
| **Social Blitz Prize** | Be in first 50 submitters |
