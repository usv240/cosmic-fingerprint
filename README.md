# Vedic Cognitive Fingerprint

> Your birth chart predicted one mind. Your choices built another. The gap is the most interesting part.

**Built for the Build with MeDo Hackathon — May 2026**

---

## What It Does

Vedic Cognitive Fingerprint cross-references 27 Nakshatra (Vedic astrology) predictions across 8 cognitive dimensions against your real-time behavioral assessment responses.

The result:
- An **Alignment Score** (0–100%) — how closely your ancient birth chart prediction matches your actual cognitive choices
- A **Cognitive Archetype** (one of 9 types) — The Catalyst, Visionary, Architect, Empath, Strategist, Craftsman, Conductor, Pioneer, or Paradox
- A **Cosmic Paradox** — one sentence that names your biggest contradiction
- An **AI-powered insight engine** that knows both your chart and your behavioral data

## Live Demo

**[https://app-bj6jz1le0s1t.appmedo.com](https://app-bj6jz1le0s1t.appmedo.com)**

## The 8 Cognitive Dimensions

| Dimension | What It Measures |
|---|---|
| Processing Speed | Deliberate ↔ Fast |
| Reasoning Style | Logic ↔ Intuition |
| Risk Tolerance | Cautious ↔ Bold |
| Focus Mode | Detail ↔ Big Picture |
| Decision Driver | Data ↔ Feeling |
| Certainty Need | Needs certainty ↔ Moves at 60% |
| Thinking Mode | Solo ↔ Collaborative |
| Time Horizon | Present ↔ Long-term |

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | MeDo (React/TypeScript) |
| Backend | Python FastAPI on Railway |
| Database | Supabase (PostgreSQL) |
| Primary AI | Groq — Llama 3.3 70B |
| Secondary AI | ERNIE AI (via Supabase Edge Functions) |
| Astrology Engine | Custom Vedic Jyotish × Behavioral mapping (27 Nakshatras × 8 dimensions) |
| Streaming | Server-Sent Events (SSE) for word-by-word AI chat |

## Architecture

```
User → MeDo Frontend
  → POST /api/birth     → Vedic chart calculation (Swiss Ephemeris)
  → POST /api/score     → Behavioral assessment scoring
  → POST /api/results   → Alignment score + archetype + paradox
  → POST /api/chat      → Groq AI (ERNIE fallback) with full fingerprint context
  → GET  /api/chat-stream → SSE streaming chat
```

## Backend Endpoints

| Endpoint | Purpose |
|---|---|
| `POST /api/birth` | Calculate Nakshatra from birth date/time/location |
| `POST /api/score` | Score 12 behavioral assessment responses |
| `POST /api/results` | Compute alignment, archetype, divergence points |
| `POST /api/chat` | AI chat with full cognitive context |
| `GET /api/chat-stream` | Streaming SSE chat (word-by-word) |
| `POST /api/oracle` | ERNIE AI oracle endpoint |
| `GET /share/{session_id}` | Public shareable fingerprint link |

## Repository Structure

```
cosmic-fingerprint/
├── main.py              # FastAPI backend (Railway)
├── requirements.txt     # Python dependencies
├── astrology_api.py     # Vedic chart calculation helpers
├── IMPROVEMENTS.md      # Feature backlog / what we'd build next
└── project_plan.md      # Hackathon planning notes
```

The frontend source lives in the MeDo platform (`app-bj6jz1le0s1t/`).

---

*For reflection and self-discovery · Not scientific diagnosis*
