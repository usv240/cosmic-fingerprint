# Your Vedic Cognitive Fingerprint — Project Plan

> *"What the stars predicted. What you actually chose. The gap between them is where you really live."*

---

## The One-Line Pitch

An AI experience that cross-references your Vedic birth chart against your real behavioral choices — and reveals the gap between who you're cosmically wired to be and how your mind actually operates.

---

## What Makes This Win

| Factor | Why |
|---|---|
| Zero competitors | No app has ever combined Vedic astrology with live cognitive behavioral mapping |
| Two reveal moments | Chart reveal + fingerprint reveal = two jaw-drop points in the demo |
| Most shareable format | Astrology + personality test = highest viral content category on social media |
| Every MeDo feature used | API + multi-turn + AI + database + visualization + deploy = full technical depth |
| Humanized | Feels like a wise friend telling you something true, not a clinical report |

---

## Core Promise to the User

> "Most tools tell you WHO you are. This maps HOW your mind actually works — then shows you how close that is to what an ancient framework predicted about you."

Disclaimer shown throughout: *For reflection and self-discovery, not scientific diagnosis.*

---

# Architecture

## Centralized Data Model

One single user object flows through the entire app. Nothing is scattered.

```
UserSession {
  // Identity
  id: string
  name: string
  createdAt: timestamp

  // Birth Data
  birthDate: date
  birthTime: time
  birthPlace: string

  // Vedic Layer (from API)
  moonNakshatra: string
  moonSign: string
  mercurySign: string
  mercuryHouse: number
  ascendant: string
  vedicCognitiveBlueprint: object {
    processingSpeed: number       // 1-10
    reasoningStyle: number        // 1-10 (analytical ↔ intuitive)
    riskTolerance: number         // 1-10
    focusMode: number             // 1-10 (detail ↔ big-picture)
    decisionDriver: number        // 1-10 (data ↔ emotion)
    certaintyNeed: number         // 1-10
    thinkingMode: number          // 1-10 (independent ↔ collaborative)
    timeHorizon: number           // 1-10 (present ↔ future)
  }

  // Behavioral Layer (from scenarios)
  scenarioResponses: array
  responseTimes: array            // timing adds to the data
  behavioralFingerprint: object { // same 8 dimensions
    processingSpeed: number
    reasoningStyle: number
    riskTolerance: number
    focusMode: number
    decisionDriver: number
    certaintyNeed: number
    thinkingMode: number
    timeHorizon: number
  }

  // Output
  alignmentScore: number          // 0-100% overlap
  divergencePoints: array         // which dimensions diverged most
  insights: array                 // 3-4 written insights
  shareableUrl: string
}
```

## API Architecture

All external calls go through one centralized API handler — not scattered across pages.

```
API Calls:
1. AstrologyAPI (freeastrologyapi.com — CONFIRMED)
   POST https://json.freeastrologyapi.com/planets           → moonSign, mercurySign, mercuryHouse, ascendant
   POST https://json.freeastrologyapi.com/nakshatra-durations → moonNakshatra name + number
   POST https://json.freeastrologyapi.com/horoscope-chart-url → SVG chart image URL
   Auth: x-api-key header | Ayanamsha: lahiri
   Input: year, month, date, hours, minutes, seconds, latitude, longitude, timezone
   Note: birth place name → lat/long needs geocoding step first

2. ERNIE AI (via MeDo)
   Call 1: Map Nakshatra → 8 cognitive dimension scores (vedicCognitiveBlueprint)
   Call 2: Map scenarioResponses → 8 behavioral dimension scores (behavioralFingerprint)
   Call 3: Cross-reference both → generate 3-4 human insights

3. MeDo Database
   Store: full UserSession object
   Retrieve: by shareableUrl for public profile
```

---

# Screens

## Screen 1 — Landing

**Purpose:** Make someone feel understood before they've even started.

**Copy (humanized):**
> "You've taken personality tests. You know your MBTI. Maybe your Enneagram.
> But here's what none of them told you:
> **How your mind actually makes decisions under pressure.**
> Enter your birth details. Answer 12 honest scenarios.
> We'll show you where ancient wisdom and your actual choices agree — and where they don't.
> That gap? That's the most interesting thing about you."

**CTA:** "Map my mind →"

**Elements:**
- App name + tagline
- 3-line explainer
- Sample fingerprint visual (blurred/teaser)
- CTA button

---

## Screen 2 — Birth Details

**Purpose:** Collect data warmly, not clinically.

**Copy (humanized):**
> "First, the cosmic coordinates.
> Your birth details let us calculate your Moon Nakshatra — what Vedic astrology says about the architecture of your mind.
> We'll compare that prediction against your actual choices in a few minutes."

**Fields:**
- Full name ("What should we call you?")
- Date of birth
- Time of birth ("As close as you know — even an approximate hour works")
- Place of birth (city + country)

**On submit:** Spinner with copy: *"Plotting your cognitive coordinates..."*

**API call:** Astrology API → returns Nakshatra, Mercury, Lagna

---

## Screen 3 — Your Vedic Blueprint

**Purpose:** The first reveal. Make it feel like looking in a mirror, not reading a report.

**Visual:** Animated radar chart builds slowly, one dimension at a time. Gold color.

**Copy structure (one block per trait):**

> **Your Moon is in [Nakshatra Name].**
> [One sentence on what this Nakshatra says about how you think — written as observation, not diagnosis.]

> **Your Mercury sits in [Sign], [House] house.**
> [One sentence on communication style and how you process information.]

> **Your Ascendant is [Sign].**
> [One sentence on the lens through which you take in the world.]

**Example (Ashwini Moon):**
> "Your Moon is in Ashwini. You were built to move fast. Your mind doesn't wait for all the information — it picks up the first clear signal and goes. Some people call that impulsive. You call it momentum."

**Transition copy:**
> "That's what the stars predicted about you.
> Now let's see what your actual choices reveal.
> **12 quick scenarios. No right answers. Just you.**"

**CTA:** "Start the assessment →"

---

## Screen 4 — Behavioral Assessment

**Purpose:** Map real cognitive behavior through honest, human scenarios.

**Design:** One card at a time. Clean. Timer running (but not visible to user — anxiety kills honesty). Progress bar at top.

**Tone:** Scenarios feel like real life, not a psych test.

### The 12 Scenarios

**1. Processing Speed**
> "You have 10 minutes before a big meeting. Someone sends you a long brief.
> Do you: (A) Skim the key points and trust your instincts in the room, or (B) Read carefully and take notes even if you're slightly late?"

**2. Logic vs. Intuition**
> "You're choosing between two job offers. The data clearly points to Option A — better salary, more stability. But something about Option B just feels right.
> Do you: (A) Go with the data, or (B) Trust the feeling?"

**3. Risk Tolerance**
> "You have savings you've been sitting on. A friend with a strong track record pitches you an investment — high risk, possibly high reward.
> Do you: (A) Put in a comfortable amount, (B) Go all in, or (C) Politely pass?"

**4. Detail vs. Big Picture**
> "You're planning a trip. Do you: (A) Map out every day in advance — hotels, times, backup options, or (B) Book the flights and figure out the rest when you're there?"

**5. Decision Driver**
> "A colleague made a mistake that hurt the team. You have to give feedback.
> Do you lead with: (A) The facts — what went wrong and what needs to change, or (B) How it affected people — starting with empathy before the correction?"

**6. Certainty Need**
> "You're 70% sure about a decision. Not 100%. Do you: (A) Wait until you're more certain, or (B) Move with 70% — that's enough?"

**7. Thinking Mode**
> "You're stuck on a hard problem. Do you: (A) Go quiet and work it through alone, or (B) Call someone to think out loud with?"

**8. Time Horizon**
> "You can take a bonus now, or invest it in a course that would double your earning potential in 3 years.
> Do you: (A) Take the bonus — three years is a long time, or (B) Invest — future you will thank present you?"

**9. Pressure Response**
> "Your flight is boarding in 8 minutes and you're still in line at security.
> Your mind goes: (A) Run through the options fast and act, or (B) Stay calm and trust it'll work out?"

**10. Conflict Style**
> "Someone publicly disagrees with your idea in a meeting. Do you: (A) Defend your position with evidence, (B) Ask them to explain their concern first, or (C) Let it go — not worth it in public?"

**11. Information Style**
> "You're learning something new. Do you prefer: (A) Getting the full picture first, then the details, or (B) Learning step-by-step — no jumping ahead?"

**12. Instinct vs. Process**
> "You meet someone new. Within 5 minutes you have a strong read on them.
> Do you: (A) Trust that read completely, (B) Hold it lightly while you gather more data, or (C) Ignore it — first impressions are usually wrong?"

---

## Screen 5 — Processing Animation

**Copy:**
> "Mapping your mind...
> Comparing your Ashwini blueprint to your actual choices...
> Looking for where they match — and where they don't."

Animation: Two shapes slowly forming, then overlapping.

---

## Screen 6 — The Fingerprint Reveal

**Purpose:** The main visual moment. The entire app leads to this.

**Visual:**
- Radar/spider chart with 8 axes
- **Gold shape** = Vedic prediction (labeled: *"What your chart said"*)
- **Blue shape** = Behavioral reality (labeled: *"What your choices revealed"*)
- Overlap zone highlighted: *"Your anchored traits"*
- Divergence zones highlighted: *"Your growth edges"*

**Copy above the chart:**
> "Here's your Vedic Cognitive Fingerprint.
> Gold is who the stars said you'd be.
> Blue is who you actually are when it counts.
> The overlap is your foundation. The gap is where you grow."

**Alignment score shown:**
> "Your blueprint and behavior align **72%** — you're largely who your chart predicted, with some fascinating exceptions."

---

## Screen 7 — Insights Report

**Purpose:** 3–4 written insights that feel like a wise friend talking, not a report being filed.

**Format per insight:**
- Title (one short line)
- 2-3 sentences of human observation
- One actionable note

**Example Insights:**

---

**"You decide fast — and that's real, not just your chart talking."**
Your Ashwini Moon predicted quick, instinct-driven processing. Your scenario responses confirmed it: you moved fast, you committed early, you didn't second-guess. Most people fight this about themselves. You shouldn't. Fast decisions made with good instincts are a genuine skill.
*Worth knowing: your edge isn't analysis. It's momentum. Protect it.*

---

**"Your biggest surprise: you think more rationally than you feel."**
Your chart suggested emotion-forward processing — Ashwini energy often leads with feeling. But your choices were consistently data-driven. When given the choice between empathy and efficiency, you chose efficiency almost every time. This isn't coldness. It's a coping style you've built — possibly because feeling first has cost you before.
*Worth exploring: when did you start trusting data more than feeling?*

---

**"You're comfortable with uncertainty — more than you probably admit."**
You chose ambiguous options, moved at 70% certainty, and picked open-ended plans over locked-in ones. Your chart didn't fully predict this. It's something you've built, not something you were born with. That's harder to develop than a natural trait. You've done real work here.

---

**Closing line:**
> "This is a mirror, not a verdict. Use it however feels true."
> *For reflection and self-discovery, not scientific diagnosis.*

---

## Screen 8 — Share

**Shareable card contains:**
- App name
- User's name + Nakshatra
- Mini fingerprint visual
- Alignment score
- One-line top insight
- "Discover yours →" CTA

**Copy:**
> "Your fingerprint is live at [public URL].
> Share it — or keep it. Either way, you know something now that most people spend years figuring out."

**Share buttons:** Twitter/X, LinkedIn, WhatsApp, Copy link

---

# Humanization Guide

The single most important thing: **the app should sound like a smart friend who's been studying you, not a system generating output.**

## Rules for All Copy

| Instead of... | Write... |
|---|---|
| "Your cognitive processing style is..." | "Here's how your mind actually works..." |
| "Divergence detected in dimension: Reasoning Style" | "Here's where it gets interesting." |
| "Your behavioral data indicates..." | "When the clock was ticking, you..." |
| "Analytical processing tendency confirmed" | "You think in patterns. You can't help it." |
| "Result: High risk tolerance" | "You bet on yourself. Consistently." |
| "Assessment complete." | "That's everything we needed." |

## Tone Throughout
- **Curious, not clinical.** The app is discovering something alongside the user, not evaluating them.
- **Specific, not generic.** Every insight should feel like it could only be for this person.
- **Honest, not flattering.** The divergence points should feel like a gentle truth, not a criticism.
- **Conversational.** Short sentences. Occasional fragments. Like thinking out loud.

---

# 13-Day Build Timeline

Today: May 7 | Deadline: May 20

| Day | Date | Task |
|---|---|---|
| Day 1 | May 7 | Set up MeDo project. Build landing screen. Confirm astrology API works with HTTP connector. |
| Day 2 | May 8 | Build birth details form. Wire up API call. Display raw Nakshatra + Mercury + Lagna output. |
| Day 3 | May 9 | Build Nakshatra → 8 dimension mapping logic (all 27 Nakshatras). Store in database. |
| Day 4 | May 10 | Build Vedic Blueprint screen. Animated radar chart (gold). Humanized copy per Nakshatra. |
| Day 5 | May 11 | Build all 12 scenario cards. Response capture + timing. Progress bar. |
| Day 6 | May 12 | Build behavioral scoring engine. Map responses → 8 dimension scores. Store in database. |
| Day 7 | May 13 | Build cross-reference logic. Calculate alignment score + divergence points. |
| Day 8 | May 14 | Build Fingerprint Reveal screen. Dual radar chart (gold + blue). Overlap visualization. |
| Day 9 | May 15 | Build Insights Report screen. ERNIE AI generates 3-4 personalized insights. Humanize copy. |
| Day 10 | May 16 | Build Share screen. Shareable card generator. Public profile URL. |
| Day 11 | May 17 | Full flow test. Fix any broken steps. Polish all copy — remove every clinical phrase. |
| Day 12 | May 18 | Visual polish. Make every screen beautiful. Test on mobile. Check all edge cases. |
| Day 13 | May 19 | Record demo video (3 min). Write submission text. Post on Discord + social with #BuiltWithMeDo. |
| **Submit** | **May 20** | Submit by 9:00am EDT. |

---

# Submission Strategy

## Text Description (what judges read first)

> Most self-discovery tools tell you WHO you are. Your Vedic Cognitive Fingerprint maps HOW your mind actually operates — then shows you how close that is to what your Vedic birth chart predicted.
>
> We built a 3-layer AI experience on MeDo:
> **Layer 1:** Enter your birth details. The app calculates your Moon Nakshatra, Mercury placement, and Ascendant, then generates a Vedic cognitive blueprint — what ancient Jyotish tradition predicts about your thinking style.
> **Layer 2:** Complete 12 honest behavioral scenarios. No right answers. AI maps your actual cognitive mechanics from your real choices.
> **Layer 3:** The reveal. A visual "Vedic Cognitive Fingerprint" — two overlapping shapes showing where your chart and behavior align, and where they diverge. The gap is the insight.
>
> Built entirely on MeDo using ERNIE AI, external astrology API integration, centralized database, radar chart visualization, and one-click shareable public profiles.
>
> For reflection and self-discovery — not scientific diagnosis.

## Demo Video Outline

| Time | Content |
|---|---|
| 0:00–0:20 | Hook line spoken to camera. Show the finished fingerprint. "This is what we built." |
| 0:20–0:50 | Enter birth details → watch blueprint build (screen recording) |
| 0:50–1:40 | Answer 4 of the 12 scenarios — pick the most interesting ones |
| 1:40–2:20 | The fingerprint reveal — slow animation, speak over it |
| 2:20–2:45 | Read one insight out loud — the divergence one |
| 2:45–3:00 | Show shareable card. "Built with MeDo." |

## Prize Targets
- **Best Surprise Us!** — $4,500 (primary)
- **1st / 2nd / 3rd Place** — $10K / $6K / $4K (aim for this too)
- **Community Choice Award** — $500 × 5 (post fingerprint on Discord)
- **Creative Content Award** — $500 × 10 (post on X/LinkedIn with #BuiltWithMeDo)
- **Social Blitz Prize** — post on social media immediately

---

# MeDo Prompting Strategy

When building in MeDo, prompt it in layers — not all at once.

**Prompt 1 — Foundation**
> "Build a multi-page web app called 'Vedic Cognitive Fingerprint'. Page 1 is a landing page with a tagline, 3-bullet description, and a CTA button. Page 2 is a form collecting name, date of birth, time of birth, and place of birth. On form submit, call an external astrology API with those details and store the response in a database table called 'user_sessions'."

**Prompt 2 — Assessment**
> "Add a 12-card scenario assessment flow. Each card shows a situation and 2-3 answer options. Capture the selected answer and response time for each card. Store all responses in the user_sessions table. Show a progress bar across all 12 cards."

**Prompt 3 — Scoring**
> "After the assessment, use ERNIE AI to score the responses across 8 dimensions: Processing Speed, Reasoning Style, Risk Tolerance, Focus Mode, Decision Driver, Certainty Need, Thinking Mode, Time Horizon. Each dimension scored 1-10. Also map the user's Moon Nakshatra to scores on the same 8 dimensions using a predefined mapping table. Store both score sets in user_sessions."

**Prompt 4 — Visualization**
> "Build the fingerprint reveal page. Display a radar/spider chart with 8 axes. Draw two overlapping shapes — one gold (Vedic blueprint scores) and one blue (behavioral scores). Calculate and display an alignment percentage. Highlight the 2 dimensions with the largest divergence."

**Prompt 5 — Insights + Share**
> "Use ERNIE AI to generate 3-4 personalized written insights based on the alignment and divergence data. Each insight should feel conversational and specific, not clinical. Then build a share screen with a generated card image showing the fingerprint visual, the user's Nakshatra, and their alignment score. Generate a unique public URL for each user's result."
