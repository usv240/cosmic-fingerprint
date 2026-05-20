# Vedic Cognitive Fingerprint

Your birth chart predicted one version of your mind. Your actual choices built another. This app measures the gap between them — and turns it into something useful.

**Live → [https://app-bj6jz1le0s1t.appmedo.com](https://app-bj6jz1le0s1t.appmedo.com)**

---

## What it does

Enter your birth details. The system calculates your Moon Nakshatra using Vedic Jyotish and generates a predicted cognitive profile across 8 dimensions — how fast you process, how much risk you tolerate, whether you lead with logic or feeling, and so on.

Then you take a 12-scenario behavioral assessment. Not HR questions. Atmospheric, specific situations designed to reveal how your mind actually operates under real conditions.

The two profiles get cross-referenced. You get:

- An **alignment score** — what percentage of your chart's predictions your actual choices confirmed
- A **cognitive archetype** — one of 9 types drawn from your behavioral scores
- A **cosmic paradox** — a single sentence naming your biggest contradiction
- An **insight engine** that generates 4 personalized insights from the gap data
- A **decision oracle** that analyzes any real decision through three lenses: what your chart predicts, what your behavioral pattern says, and what the gap between them reveals
- An **AI chat** that knows both your Vedic chart and your behavioral fingerprint — ask it anything about how you think

---

## The 8 cognitive dimensions

Each Nakshatra (27 total in Vedic Jyotish) maps to predicted scores across these dimensions on a 1–10 scale:

| Dimension | What it measures |
|---|---|
| Processing Speed | Deliberate ↔ Fast |
| Reasoning Style | Logic-first ↔ Intuition-first |
| Risk Tolerance | Cautious ↔ Bold |
| Focus Mode | Detail-oriented ↔ Big picture |
| Decision Driver | Data-led ↔ Emotion-led |
| Certainty Need | Needs certainty before moving ↔ Comfortable at 60% |
| Thinking Mode | Solo processor ↔ Collaborative thinker |
| Time Horizon | Present-focused ↔ Long-term oriented |

The Nakshatra-to-dimension mapping is sourced from Jyotish literature (Bepin Behari, Hart de Fouw) and encoded in `astrology_api.py`.

---

## How alignment is calculated

```
gap_per_dimension = |predicted_score - behavioral_score|   (1–10 scale)
max_possible_gap  = 9 × 8 dimensions = 72
alignment_score   = (1 - total_gap / 72) × 100
```

A dimension with gap > 3 becomes a **divergence point**. Gap ≤ 1 is an **aligned trait**.

---

## Tech stack

| Layer | What's running |
|---|---|
| Backend | Python 3.11, FastAPI, deployed on Railway |
| AI — primary | Groq API (Llama 3.3 70B Versatile) |
| AI — fallback | ERNIE 4.5 8K (Baidu, via access token) |
| AI — final fallback | Deterministic response engine (no external call) |
| Astrology API | [Free Astrology API](https://json.freeastrologyapi.com) — Lahiri ayanamsha, topocentric |
| Session storage | In-memory dict (Railway instance) |
| Frontend | React / TypeScript, deployed on [MeDo](https://medo.dev) |
| Streaming | Server-Sent Events (SSE) for word-by-word chat output |

---

## API reference

All endpoints accept and return JSON. CORS is open.

### `GET /health`
```json
{ "status": "ok" }
```

---

### `POST /api/vedic-profile`
Takes birth details, calls the astrology API, returns the Vedic chart + predicted cognitive scores. Creates a session.

**Request:**
```json
{
  "name": "Ujwal",
  "year": 1999, "month": 8, "date": 11,
  "hours": 6, "minutes": 30, "seconds": 0,
  "latitude": 17.383, "longitude": 78.466,
  "timezone": 5.5
}
```

**Response:**
```json
{
  "session_id": "uuid",
  "moon_nakshatra_name": "Ashwini",
  "moon_nakshatra_number": 1,
  "moon_sign": "Aries",
  "mercury_sign": "Leo",
  "mercury_house": 4,
  "ascendant_sign": "Cancer",
  "chart_svg_url": "https://...",
  "nakshatra_description": "Your mind is built for speed...",
  "predicted_scores": {
    "processing_speed": 9, "reasoning_style": 7,
    "risk_tolerance": 8, "focus_mode": 6,
    "decision_driver": 5, "certainty_need": 3,
    "thinking_mode": 4, "time_horizon": 3
  }
}
```

---

### `POST /api/score-assessment`
Scores 12 scenario responses and cross-references them with the Vedic predicted scores.

**Request:**
```json
{
  "session_id": "uuid",
  "responses": { "s01": "A", "s02": "B", "s03": "C", ... }
}
```

**Response:**
```json
{
  "predicted_scores":  { ... },
  "behavioral_scores": { ... },
  "alignment_score": 68.5,
  "divergence_points": ["risk_tolerance", "time_horizon"],
  "aligned_traits": ["reasoning_style", "focus_mode"],
  "dimension_gaps": { "processing_speed": 2, "risk_tolerance": 5, ... },
  "dimension_labels": { "processing_speed": "Processing Speed", ... }
}
```

---

### `POST /api/generate-insights`
Generates up to 4 personalized insights from the cross-reference data. Deterministic — fast, no external API call.

Four insight types, in priority order:
1. **Aligned** — your strongest chart match
2. **Divergence** — your biggest gap and what it likely means
3. **Hidden strength** — a behavioral high your chart didn't predict
4. **Growth edge** — something your chart predicted strongly but your behavior hasn't reflected yet

Accepts either `session_id` (if session is live in memory) or raw state data passed directly in the request body (for clients that can't rely on server-side session persistence).

---

### `POST /api/oracle`
Analyzes a real decision through three lenses. Returns three structured parts.

**Request:**
```json
{
  "session_id": "uuid",
  "decision": "I'm deciding whether to start something new."
}
```

**Response:**
```json
{
  "parts": [
    { "title": "What your chart says you'll do",           "body": "...", "color": "#C9A84C" },
    { "title": "What your choices say you'll actually do", "body": "...", "color": "#4C8EC9" },
    { "title": "What the gap reveals",                     "body": "...", "color": "#9C6FDB" }
  ]
}
```

---

### `POST /api/chat`
Answers questions about the user's fingerprint. Tries Groq first, then ERNIE, then falls back to the deterministic chat engine.

The system prompt injects the user's full fingerprint data — Nakshatra, alignment score, all 8 predicted and behavioral scores, divergence points, aligned traits. The AI has complete context.

**Request:**
```json
{
  "session_id": "uuid",
  "question": "Am I who the stars said I'd be?"
}
```

**Response:**
```json
{ "response": "At 68% alignment, mostly yes — but the divergences are the interesting part..." }
```

The chat engine handles specific question types with targeted logic: identity questions, risk questions, decision-making style, historical figure matching, hidden strength, nakshatra/astrology questions, fortune-telling redirects, and alignment/gap questions. Anything outside those falls back to a specific, number-grounded default.

**Cognitive twin matching** maps behavioral scores to 8 historical figures (Elon Musk, Tesla, da Vinci, Curie, Buffett, Maya Angelou, Newton, Mandela) using strict multi-criteria matching — each figure requires 3+ conditions to match.

---

### `GET /api/chat-stream`
Streaming version of `/api/chat`. Returns Server-Sent Events.

Uses Groq's native streaming API. Each `data:` event contains a token or word fragment. Final event is `data: [DONE]`.

If Groq is unavailable, falls back to the deterministic engine and streams word-by-word with 40ms delay.

```
data: At
data:  68%
data:  alignment,
data:  mostly
data:  yes...
data: [DONE]
```

---

### `GET /api/share/{session_id}`
Returns the public shareable profile — name, Nakshatra, alignment score, top insight, chart URL, and both score sets. Session must still be in memory (in-memory store, not persisted to disk).

---

## Session handling

Sessions live in a Python dict on the Railway instance. They persist until the process restarts. The frontend mirrors all session state to localStorage and re-sends it on every request, so most endpoints work even if the server-side session has expired — they accept the full state payload directly in the request body and construct a temporary profile from it.

---

## Running locally

```bash
git clone https://github.com/usv240/cosmic-fingerprint
cd cosmic-fingerprint

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file:
```
ASTROLOGY_API_KEY=your_key_here
GROQ_API_KEY=your_key_here
ERNIE_ACCESS_TOKEN=your_token_here   # optional
```

```bash
cd backend
uvicorn main:app --reload --port 8005
```

API is at `http://localhost:8005`. Health check: `http://localhost:8005/health`.

**Getting API keys:**
- Astrology API: [freeastrologyapi.com](https://freeastrologyapi.com) (free tier available)
- Groq: [console.groq.com](https://console.groq.com) (free, no credit card)
- ERNIE: optional — the system works fine with just Groq

---

## Repository structure

```
cosmic-fingerprint/
├── backend/
│   ├── main.py           # FastAPI app — all routes, AI orchestration, chat/insight engines
│   └── astrology_api.py  # Vedic chart calculation, Nakshatra map, behavioral scorer, cross-reference
├── requirements.txt
└── IMPROVEMENTS.md       # What we'd build next
```

---

*For reflection and self-discovery. Not a clinical tool.*
