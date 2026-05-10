# MeDo Prompts — Vedic Cognitive Fingerprint
# Paste each prompt into MeDo one at a time. Wait for it to finish before sending the next.
# BACKEND_URL placeholder = https://placeholder-backend.example.com (swap to Railway URL later)

---

## PROMPT 1 — Design System + Landing Screen + Birth Form

```
Build a web app called "Vedic Cognitive Fingerprint". I will describe the full app now. Build only what I describe in this message — I will send more screens in follow-up messages.

─── DESIGN SYSTEM ───────────────────────────────────────────

Colors (use these EXACTLY):
- Page background: #0A0A12
- Primary gold: #C9A84C
- Primary blue: #4C8EC9
- Card background: rgba(255, 255, 255, 0.04)
- Card border: rgba(255, 255, 255, 0.08)
- Body text: #E8E8E8
- Muted text: rgba(255, 255, 255, 0.55)
- Input background: rgba(255, 255, 255, 0.06)
- Input border: rgba(255, 255, 255, 0.12)
- Input border (focused): #C9A84C
- Gold button: background linear-gradient(135deg, #C9A84C, #A8873E), text #0A0A12, font-weight 600
- Success green: #4CAF50

Typography:
- Headings (h1, h2): font-family "Playfair Display", Georgia, serif — looks elegant and mystical
- Body text: font-family "Inter", system-ui, sans-serif
- All text: white or near-white on the dark background

Spacing: generous padding. Every section has at least 24px padding. Cards have 28px padding.

Buttons: rounded corners (border-radius 12px), 52px tall, bold text, no uppercase.

Global style: The whole app feels like a premium dark-mode experience — like a high-end personality assessment meets ancient wisdom. Nothing should look cheap or clinical.

─── SCREEN 1: LANDING ───────────────────────────────────────

Full-page dark screen (#0A0A12 background).

At the top center, a small decorative symbol: ✦ (in gold, font-size 28px)

Main heading (Playfair Display, 48px on desktop / 36px mobile, white):
"Vedic Cognitive
Fingerprint"

Tagline below (18px, muted white, line-height 1.8):
"What the stars predicted.
What you actually chose.
The gap between them is where you really live."

Below the tagline, 3 bullet points (each on its own row, 16px body text):
◎  Your Vedic birth chart maps a predicted cognitive blueprint
◎  12 honest scenarios reveal how your mind actually operates
◎  See where ancient wisdom and your real choices align — and where they don't

The ◎ symbol should be gold (#C9A84C). The text is muted white.

Small disclaimer below the bullets (13px, very muted, rgba(255,255,255,0.4)):
"For reflection and self-discovery · Not scientific diagnosis"

Gold button below (full-width on mobile, 280px on desktop):
"Map my mind →"

Clicking this button navigates to Screen 2 (Birth Form).

─── SCREEN 2: BIRTH FORM ────────────────────────────────────

Dark screen, centered content, max-width 540px, auto margins.

Back button top-left: "← Back" (small, muted, clicking returns to Screen 1)

Step indicator (small label, gold, uppercase, 11px letter-spacing):
"Step 1 of 3"

Screen heading (Playfair Display, 32px):
"Your cosmic coordinates"

Subtext below heading (16px, muted white):
"Your birth details let us calculate your Moon Nakshatra — what Vedic astrology predicts about the architecture of your mind."

─── FORM FIELDS ───

Field 1 — Name:
Label: "What should we call you?"
Input type: text, placeholder: "Your name"
Required.

Field 2 — Date of birth:
Label: "Date of birth"
Input type: date
Required.

Field 3 — Time of birth (same row as date on desktop, stacked on mobile):
Label: "Time of birth"
Input type: time
Required.
Small hint text below: "Approximate hour works fine"

Field 4 — Place of birth:
Label: "Place of birth"
Input type: text, placeholder: "City, Country (e.g. Mumbai, India)"
Required.

As the user types in this field (after 700ms pause in typing), call the Nominatim geocoding API:
GET https://nominatim.openstreetmap.org/search?q={userInput}&format=json&limit=1&addressdetails=1
Headers: User-Agent: VedicCognitiveFingerprint/1.0

From the response, extract:
- lat (as float, e.g. 19.0760)
- lon (as float, e.g. 72.8777)
- display_name (for confirmation message)

Store lat and lon as hidden values in the form.

Compute timezone offset from longitude: timezone = Math.round(lon / 15 * 2) / 2

Show a small status line below the city field:
- While geocoding: "Locating..." (muted text)
- On success: "✓ [First part of display_name] located" (green text, #4CAF50)
- On failure: "Location not found. Try a different spelling." (amber text)

The submit button should be DISABLED until:
- All fields are filled
- Geocoding has succeeded (lat/lon are stored)

Submit button (gold, full width):
"Plot my cognitive coordinates →"

─── ON FORM SUBMIT ───

Show a full-screen loading overlay with:
- Pulsing gold circle animation in the center
- Text: "Reading your cosmic coordinates..." (18px, white)
- Subtext: "Calculating your Moon Nakshatra and Vedic blueprint" (14px, muted)

While showing this overlay, call:
POST https://placeholder-backend.example.com/api/vedic-profile
Content-Type: application/json
Body:
{
  "name": [name field value],
  "year": [year extracted from date field, e.g. 1990],
  "month": [month extracted from date field, e.g. 6],
  "date": [day extracted from date field, e.g. 15],
  "hours": [hours from time field, e.g. 10],
  "minutes": [minutes from time field, e.g. 30],
  "seconds": 0,
  "latitude": [lat from geocoding, as float],
  "longitude": [lon from geocoding, as float],
  "timezone": [computed timezone offset, as float, e.g. 5.5]
}

The API will return a JSON object. Store ALL of this in app state:
{
  "session_id": "...",
  "name": "...",
  "moon_nakshatra_number": ...,
  "moon_nakshatra_name": "...",
  "moon_sign": "...",
  "mercury_sign": "...",
  "mercury_house": ...,
  "ascendant_sign": "...",
  "chart_svg_url": "...",
  "nakshatra_description": "...",
  "predicted_scores": {
    "processing_speed": ...,
    "reasoning_style": ...,
    "risk_tolerance": ...,
    "focus_mode": ...,
    "decision_driver": ...,
    "certainty_need": ...,
    "thinking_mode": ...,
    "time_horizon": ...
  }
}

If the API call succeeds, hide the loading overlay and navigate to Screen 3 (Blueprint).
If the API call fails, hide the overlay and show an error message on the form: "Something went wrong. Please check your details and try again."

─── APP STATE ───

Create a global app state object that persists across all screens:
{
  session_id: null,
  name: null,
  moon_nakshatra_name: null,
  moon_sign: null,
  mercury_sign: null,
  mercury_house: null,
  ascendant_sign: null,
  chart_svg_url: null,
  nakshatra_description: null,
  predicted_scores: null,
  assessment_responses: {},
  behavioral_scores: null,
  alignment_score: null,
  divergence_points: [],
  aligned_traits: [],
  dimension_gaps: {},
  insights: []
}
```

---

## PROMPT 2 — Vedic Blueprint Screen

```
Add Screen 3 — the Vedic Blueprint screen. This screen is shown after the birth form API call succeeds.

─── SCREEN 3: VEDIC BLUEPRINT ───────────────────────────────

Dark screen, centered, max-width 600px.

Step indicator (small, gold, top):
"Step 1 of 3 · Complete"

─── NAKSHATRA HEADER ───

A large badge/chip in the center:
- Background: rgba(201, 168, 76, 0.15) with border 1px solid rgba(201, 168, 76, 0.4)
- Border-radius: 40px
- Padding: 10px 24px
- Text: [moon_nakshatra_name from state] (e.g. "Satabisha")
- Font: Playfair Display, 20px, gold color (#C9A84C)

Below the badge, the main heading (Playfair Display, 28px, white):
"[First name from state]'s Vedic Cognitive Blueprint"

─── NAKSHATRA DESCRIPTION ───

A card with the nakshatra_description text from the API response.
Card styling: background rgba(255,255,255,0.04), border rgba(255,255,255,0.08), border-radius 16px, padding 24px.
Text: 16px, line-height 1.7, muted white (rgba(255,255,255,0.85)).

─── PLANET PILLS ───

A row of 3 small pill chips below the description card:

Pill 1: "Moon in [moon_sign]"
Pill 2: "Mercury in [mercury_sign]"
Pill 3: "Rising [ascendant_sign]"

Pill styling: background rgba(76, 142, 201, 0.15), border 1px solid rgba(76, 142, 201, 0.3), border-radius 20px, padding 6px 16px, font-size 13px, color #4C8EC9.
Pills wrap on mobile.

─── BIRTH CHART IMAGE ───

Display the birth chart image using chart_svg_url from state:
<img src="{chart_svg_url}" alt="Your Vedic birth chart" />

Image styling: max-width 340px, width 100%, border-radius 12px, display block, margin 0 auto.
Wrap it in a container with background rgba(255,255,255,0.03), padding 20px, border-radius 16px.

─── TRANSITION SECTION ───

Below the chart, a text block (centered):

Bold text (18px, white):
"That's what the stars predicted about you."

Regular text below (16px, muted white):
"Now let's see what your actual choices reveal."

Then a detail line (14px, muted, margin-top 16px):
"12 quick scenarios. No right answers. Just you."

Gold button below:
"Start the assessment →"

Clicking this button navigates to Screen 4 (Assessment).
```

---

## PROMPT 3 — 12-Scenario Assessment

```
Add Screen 4 — the Assessment. This is a series of 12 scenario cards shown one at a time.

─── SCREEN 4: ASSESSMENT ────────────────────────────────────

─── PROGRESS BAR ───

At the very top of the screen, a thin progress bar:
- Full width, height 3px
- Background: rgba(255,255,255,0.1)
- Fill: gold (#C9A84C)
- Fill width: (currentQuestion / 12) * 100%

Below the bar, a small label (13px, muted white, centered):
"Question [currentQuestion] of 12"

─── SCENARIO CARD ───

Centered card, max-width 560px, margin auto.
Card: background rgba(255,255,255,0.04), border rgba(255,255,255,0.08), border-radius 20px, padding 40px 36px.

Scenario text (Playfair Display, 22px, white, line-height 1.5, centered):
[scenario text — see scenarios below]

Below the scenario text, the answer options as large tap-friendly buttons.
Each option button:
- Full width
- Background: rgba(255,255,255,0.06)
- Border: 1px solid rgba(255,255,255,0.12)
- Border-radius: 12px
- Padding: 16px 20px
- Font: 15px, white
- Text-align: left
- Margin-bottom: 10px

When an option is clicked:
- Highlight it: background rgba(201, 168, 76, 0.15), border-color #C9A84C, text color #C9A84C
- Wait 350ms
- Store the answer key (e.g. "A", "B", "C") in assessment_responses under the scenario ID (e.g. "s01")
- Advance to the next scenario card with a smooth fade transition
- Update the progress bar

─── THE 12 SCENARIOS ───

Show these scenarios in order:

SCENARIO s01:
Text: "You need to respond to an urgent message. You have 30 seconds."
Option A: "Write fast, send it, deal with any clarification after"
Option B: "Take 2 minutes to think it through properly even if it's 'late'"
Option C: "Send a quick 'on it' placeholder while you think"

SCENARIO s02:
Text: "You're solving a problem you've never seen before. Your first move is..."
Option A: "Look for patterns — something about this feels familiar"
Option B: "Break it down systematically, step by step"
Option C: "Search for how others have solved similar problems first"

SCENARIO s03:
Text: "A colleague asks your honest opinion on their work. It needs improvement."
Option A: "Tell them directly — they asked, they deserve the truth"
Option B: "Find what's good first, then mention what could be stronger"
Option C: "Ask questions to help them see the issues themselves"

SCENARIO s04:
Text: "You have one hour of completely free time. No obligations. You use it to..."
Option A: "Catch up on something you've been putting off"
Option B: "Do something that has no outcome — just exists for itself"
Option C: "Plan the next thing on your list"

SCENARIO s05:
Text: "A decision needs to be made. You have 60% of the information."
Option A: "Make the call — more data rarely changes the right answer"
Option B: "Push for more information before committing"
Option C: "Make a provisional call but flag it as revisable"

SCENARIO s06:
Text: "You're starting a long, complex project. Your natural instinct is to..."
Option A: "Map out the whole thing before touching anything"
Option B: "Start with what you know and let the shape emerge"
Option C: "Find the hardest part and solve that first"

SCENARIO s07:
Text: "A rule exists that you think is clearly wrong."
Option A: "Follow it anyway — rules exist for reasons you might not see"
Option B: "Break it quietly if the outcome is better"
Option C: "Push to change it through the right channels"

SCENARIO s08:
Text: "Someone close to you is visibly upset. Your first move is..."
Option A: "Ask what they need from you right now"
Option B: "Try to identify and fix the problem"
Option C: "Give them space and check in later"

SCENARIO s09:
Text: "You unexpectedly have $500 to use this week."
Option A: "Invest it in something with long-term potential"
Option B: "Save it — you'll find a better use later"
Option C: "Spend it on something that improves your life right now"

SCENARIO s10:
Text: "How do you approach large projects with no clear deadline?"
Option A: "I build the full map before I start — I need to see the whole picture"
Option B: "I start moving and figure it out as I go — the plan reveals itself"
Option C: "I alternate — plan a bit, do a bit, plan again"

SCENARIO s11:
Text: "A project you care about is two weeks behind schedule."
Option A: "Work longer hours to catch up without telling anyone yet"
Option B: "Cut scope — deliver less, but deliver on time"
Option C: "Be transparent about the delay and reset expectations openly"

SCENARIO s12:
Text: "You receive feedback you strongly disagree with."
Option A: "Listen fully, then explain your reasoning clearly"
Option B: "Update your thinking if the argument is genuinely good"
Option C: "Acknowledge it and privately decide if it changes anything"

─── AFTER ALL 12 ARE ANSWERED ───

Show Screen 4b — Processing:
Full-screen centered layout.
A pulsing animated circle (80px, gold, slow pulse glow animation — like a heartbeat).
Inside the circle, a smaller inner circle (gold, rotating slowly).

Heading (Playfair Display, 24px, white):
"Mapping your mind..."

Subtext (14px, muted white):
"Cross-referencing your choices with your Vedic blueprint"

While showing this screen, call:
POST https://placeholder-backend.example.com/api/score-assessment
Content-Type: application/json
Body:
{
  "session_id": [session_id from app state],
  "responses": [assessment_responses object from app state — all 12 answers]
}

The API returns:
{
  "behavioral_scores": { "processing_speed": N, "reasoning_style": N, "risk_tolerance": N, "focus_mode": N, "decision_driver": N, "certainty_need": N, "thinking_mode": N, "time_horizon": N },
  "predicted_scores": { same 8 keys },
  "alignment_score": N,
  "divergence_points": ["key1", "key2", ...],
  "aligned_traits": ["key1", ...],
  "dimension_gaps": { "processing_speed": N, ... },
  "dimension_labels": { "processing_speed": "Processing Speed", "reasoning_style": "Reasoning Style", "risk_tolerance": "Risk Tolerance", "focus_mode": "Focus Mode", "decision_driver": "Decision Driver", "certainty_need": "Certainty Need", "thinking_mode": "Thinking Mode", "time_horizon": "Time Horizon" }
}

Store all of this in app state (behavioral_scores, alignment_score, divergence_points, aligned_traits, dimension_gaps).

Show the processing screen for at least 2.5 seconds even if the API responds faster (so the user feels the weight of the calculation).

Then navigate to Screen 5 (Fingerprint Reveal).
```

---

## PROMPT 4 — Fingerprint Radar Chart + Reveal

```
Add Screen 5 — the Cognitive Fingerprint Reveal. This is the centrepiece of the app.

─── SCREEN 5: FINGERPRINT REVEAL ────────────────────────────

Dark screen, centered, max-width 600px.

Step indicator (small, gold):
"Step 3 of 3 · Complete"

Main heading (Playfair Display, 32px, white, centered):
"Your Vedic Cognitive Fingerprint"

Subtext below (15px, muted white, centered):
"Gold is who your chart said you'd be. Blue is who you are when it counts."

─── RADAR CHART ───

Display a radar (spider) chart using Chart.js.
The chart must have these 8 labels in this order going clockwise from the top:
1. Processing Speed
2. Reasoning Style
3. Risk Tolerance
4. Focus Mode
5. Decision Driver
6. Certainty Need
7. Thinking Mode
8. Time Horizon

The chart has TWO datasets overlaid on the same radar:

Dataset 1 — Vedic Blueprint (gold):
- Data: the values from predicted_scores in app state, in the same order as labels
- Background color: rgba(201, 168, 76, 0.25)
- Border color: #C9A84C
- Border width: 2px
- Point background color: #C9A84C
- Point radius: 4px
- Label: "Vedic Blueprint"

Dataset 2 — Your Behavior (blue):
- Data: the values from behavioral_scores in app state, in the same order as labels
- Background color: rgba(76, 142, 201, 0.25)
- Border color: #4C8EC9
- Border width: 2px
- Point background color: #4C8EC9
- Point radius: 4px
- Label: "Your Behavior"

Chart options:
- Scale: min 0, max 10, step 2
- Grid lines: rgba(255,255,255,0.1)
- Tick labels: rgba(255,255,255,0.5), font-size 11px
- Legend: hidden (we show our own legend below)
- All radial axis labels: white, font-size 12px
- Chart size: 360px × 360px (scales down on mobile)
- Background of chart area: transparent

Wrap the chart in a container: background rgba(255,255,255,0.03), border-radius 20px, padding 20px.

─── ALIGNMENT BADGE ───

Below the chart, a prominent badge showing the alignment score.

Compute the label and color based on alignment_score:
- 80-100: label "Deeply Anchored", color #C9A84C (gold)
- 60-79: label "Mostly Aligned", color #4CAF50 (green)
- 40-59: label "Interesting Divergence", color #FF9800 (amber)
- Below 40: label "Significantly Different", color #9C27B0 (purple)

Badge design: large pill shape, border 2px solid [computed color], background transparent.
Inside: "[alignment_score]% · [computed label]"
Font: Playfair Display, 20px, [computed color].
Padding: 14px 32px, border-radius 40px.

─── LEGEND ───

Below the badge, a horizontal legend row (centered, gap 24px):

Legend item 1:
- Gold circle (12px)
- Text: "Vedic blueprint"

Legend item 2:
- Blue circle (12px)
- Text: "Your behavior"

Legend item 3:
- Circle half gold half blue (or a blended purple, 12px)
- Text: "Anchored traits"

─── CTA BUTTON ───

Gold button below legend:
"See your insights →"

Clicking this button navigates to Screen 6 (Insights).
Do NOT call the insights API yet — wait until the user clicks this button.
```

---

## PROMPT 5 — ERNIE AI Insights + Share Card

```
Add Screen 6 (Insights) and Screen 7 (Share). These are the final two screens.

─── SCREEN 6: INSIGHTS ──────────────────────────────────────

When the user clicks "See your insights →" on the fingerprint screen:

First show a brief loading state (2 seconds):
- Pulsing gold orb animation (same as the processing screen)
- Text: "Writing your insights..." (Playfair Display, 22px, white)
- Subtext: "Almost there" (14px, muted)

─── ERNIE AI CALL ───

Use ERNIE AI to generate the insights. Send this prompt to ERNIE (fill in all [values] from app state):

System message to ERNIE:
"You are a perceptive, warm, and honest writer helping someone understand how their mind works. You are not clinical, not corporate, not generic. You write like a wise friend who has been quietly observing this person and finally has something true to say. Use short sentences. Be specific. Never use words like 'cognitive', 'indicates', 'aligns', 'demonstrates', 'suggests', or 'data'. Sound fully human."

User message to ERNIE:
"Write exactly 4 insights for [name from state — first name only]. Format each insight as:

**[One-line title — punchy, specific, 6-10 words]**
[2-3 sentences of human, honest observation]

Here is their data:

Moon Nakshatra: [moon_nakshatra_name]
Ascendant: [ascendant_sign]

Vedic blueprint scores (1-10 scale):
- Processing Speed: [predicted_scores.processing_speed] — how fast they think (1=deliberate, 10=instant)
- Reasoning Style: [predicted_scores.reasoning_style] — how they think (1=pure logic/data, 10=pure intuition/feeling)
- Risk Tolerance: [predicted_scores.risk_tolerance] — comfort with uncertainty (1=very cautious, 10=bold risk-taker)
- Focus Mode: [predicted_scores.focus_mode] — attention scope (1=deep detail, 10=big picture)
- Decision Driver: [predicted_scores.decision_driver] — what drives choices (1=pure data/logic, 10=pure emotion/empathy)
- Certainty Need: [predicted_scores.certainty_need] — need for certainty before acting (1=comfortable with ambiguity, 10=needs certainty)
- Thinking Mode: [predicted_scores.thinking_mode] — thinking preference (1=prefers working alone, 10=prefers collaboration)
- Time Horizon: [predicted_scores.time_horizon] — time orientation (1=present-focused, 10=far-future-focused)

Actual behavioral scores from their 12 scenario choices:
- Processing Speed: [behavioral_scores.processing_speed]
- Reasoning Style: [behavioral_scores.reasoning_style]
- Risk Tolerance: [behavioral_scores.risk_tolerance]
- Focus Mode: [behavioral_scores.focus_mode]
- Decision Driver: [behavioral_scores.decision_driver]
- Certainty Need: [behavioral_scores.certainty_need]
- Thinking Mode: [behavioral_scores.thinking_mode]
- Time Horizon: [behavioral_scores.time_horizon]

Overall alignment: [alignment_score]% (how closely their choices matched their chart)
Dimensions that diverged most: [divergence_points joined by comma]
Dimensions that aligned closely: [aligned_traits joined by comma]

Rules for the 4 insights:
1. First insight: the dimension where their chart and behavior matched best — what this says about them
2. Second insight: the biggest gap between their chart and their choices — the most interesting divergence
3. Third insight: something their behavior revealed that their chart did NOT predict — a hidden or earned trait
4. Fourth insight: something their chart strongly predicted that their behavior hasn't yet caught up to — a latent potential

Make each insight feel like it could ONLY be for this specific person. No generic personality test language."

─── DISPLAY INSIGHTS ───

Display the 4 insights as cards:
- Each card: background rgba(255,255,255,0.04), border rgba(255,255,255,0.08), border-radius 16px, padding 28px
- Card title (Playfair Display, 20px, white, margin-bottom 12px)
- Card body (Inter, 16px, muted white rgba(255,255,255,0.82), line-height 1.7)
- Small colored top border per card:
  - Card 1: 3px solid #C9A84C (gold — aligned)
  - Card 2: 3px solid #4C8EC9 (blue — divergence)
  - Card 3: 3px solid #4CAF50 (green — hidden strength)
  - Card 4: 3px solid rgba(201, 168, 76, 0.5) (muted gold — growth edge)

Page heading above cards:
"[First name], here's what your fingerprint reveals."
(Playfair Display, 28px, white)

Sub-heading below main heading (16px, muted white):
"What your fingerprint reveals."

Below all 4 cards:
Italic text (14px, rgba(255,255,255,0.4)):
"This is a mirror, not a verdict. Use it however feels true."

Disclaimer:
"For reflection and self-discovery · Not scientific diagnosis"

Gold button:
"See your shareable card →"

Clicking this navigates to Screen 7.

─── SCREEN 7: SHARE ─────────────────────────────────────────

Heading (Playfair Display, 28px):
"Your fingerprint is ready."

Subtext (16px, muted white):
"Share it — or keep it. Either way, you know something now that most people spend years figuring out."

─── SHARE CARD ───

A styled card that looks like something you'd screenshot and share.
Card design: dark background #0D0D1A, border 1px solid rgba(201, 168, 76, 0.3), border-radius 20px, padding 32px, max-width 360px, centered.

Inside the card:
1. App logo line: "✦ Vedic Cognitive Fingerprint" (13px, gold, letter-spacing 0.05em)
2. Person's name (Playfair Display, 26px, white, margin-top 16px)
3. Nakshatra line: "Moon in [moon_nakshatra_name] · Rising [ascendant_sign]" (14px, muted gold, rgba(201,168,76,0.7))
4. A mini radar chart (240px × 240px) — same two-dataset chart as Screen 5 but smaller
5. Alignment score line: "[alignment_score]% alignment" (18px, gold, bold, centered, margin-top 16px)
6. Top insight title: the title of the first insight card (14px, muted white, italic, max 2 lines)
7. CTA line at the bottom: "Discover yours → vedic-fingerprint.app" (12px, very muted, rgba(255,255,255,0.35))

─── SHARE BUTTONS ───

Below the card, 3 share buttons in a row:

Button 1 — "Share on X":
Background #000000, text white, icon X logo.
On click, open: https://x.com/intent/tweet?text=I%20just%20mapped%20my%20Vedic%20Cognitive%20Fingerprint.%20[alignment_score]%25%20alignment%20between%20my%20birth%20chart%20and%20how%20I%20actually%20think.%20%23BuiltWithMeDo%20%23VedicFingerprint&url=[current page URL]

Button 2 — "Share on LinkedIn":
Background #0077B5, text white.
On click, open: https://www.linkedin.com/sharing/share-offsite/?url=[current page URL]

Button 3 — "Copy link":
Background rgba(255,255,255,0.08), border rgba(255,255,255,0.15), text white.
On click, copy the current URL to clipboard and change button text to "✓ Copied!" for 2 seconds.

Below the share buttons, a ghost/text button:
"Start over"
On click, reset all app state and navigate back to Screen 1 (Landing).

─── GLOBAL RULES FOR THE ENTIRE APP ───

1. Every screen transition: smooth fade (opacity 0 → 1, duration 300ms)
2. No sharp white backgrounds anywhere. Everything is dark.
3. All inputs: dark background, gold focus ring
4. All loading states: use the pulsing gold orb animation
5. The app should work on mobile (375px wide) as well as desktop
6. Fonts: load "Playfair Display" and "Inter" from Google Fonts
7. No page reloads — this is a single-page app with screen transitions
8. Store BACKEND_URL as a configurable variable so it can be changed easily
```

---

## AFTER ALL 5 PROMPTS

Once all screens are built:

1. In MeDo's settings/secrets, add: `BACKEND_URL = https://your-actual-railway-url.up.railway.app`
2. Test the full flow from landing to share card
3. Click MeDo's "Deploy" button to get a public URL
4. Copy that URL — it's your submission URL for Devpost
