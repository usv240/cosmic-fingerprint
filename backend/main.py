"""
Vedic Cognitive Fingerprint — FastAPI Backend
All routes in one place. Clean, centralized, no scattered logic.
"""

import os
import sys
import uuid
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional

# All project files live in backend/ — no path gymnastics needed
sys.path.insert(0, os.path.dirname(__file__))
from astrology_api import (
    BirthDetails, build_vedic_profile, score_behavioral_responses,
    cross_reference, NAKSHATRA_DESCRIPTIONS, DIMENSION_LABELS,
)

app = FastAPI(title="Vedic Cognitive Fingerprint API")

PORT = int(os.getenv("PORT", 8005))

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory session store (fine for hackathon)
SESSIONS: dict = {}


# ─── REQUEST / RESPONSE MODELS ───────────────────────────────────────────────

class BirthRequest(BaseModel):
    name:      str
    year:      int
    month:     int
    date:      int
    hours:     int
    minutes:   int
    seconds:   int = 0
    latitude:  float
    longitude: float
    timezone:  float


class AssessmentRequest(BaseModel):
    session_id: str
    responses:  dict   # { "s01": "A", "s02": "B", ... }


class InsightRequest(BaseModel):
    session_id: str


class ChatRequest(BaseModel):
    session_id:           str
    question:             str
    name:                 Optional[str]  = None
    moon_nakshatra_name:  Optional[str]  = None
    nakshatra_description: Optional[str] = None
    alignment_score:      Optional[int]  = None
    divergence_points:    Optional[list] = None
    aligned_traits:       Optional[list] = None
    predicted_scores:     Optional[dict] = None
    behavioral_scores:    Optional[dict] = None


class OracleRequest(BaseModel):
    session_id:           str
    decision:             str
    name:                 Optional[str]  = None
    moon_nakshatra_name:  Optional[str]  = None
    alignment_score:      Optional[int]  = None
    divergence_points:    Optional[list] = None
    aligned_traits:       Optional[list] = None
    predicted_scores:     Optional[dict] = None
    behavioral_scores:    Optional[dict] = None


# ─── ROUTES ──────────────────────────────────────────────────────────────────

@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/api/vedic-profile")
def vedic_profile(req: BirthRequest):
    """
    Takes birth details, calls astrology API, returns Vedic blueprint
    + predicted cognitive scores. Creates a session.
    """
    try:
        birth = BirthDetails(
            year=req.year, month=req.month, date=req.date,
            hours=req.hours, minutes=req.minutes, seconds=req.seconds,
            latitude=req.latitude, longitude=req.longitude,
            timezone=req.timezone,
        )
        profile = build_vedic_profile(birth)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Astrology API error: {str(e)}")

    session_id = str(uuid.uuid4())
    SESSIONS[session_id] = {
        "name":    req.name,
        "profile": profile,
        "birth":   birth,
    }

    nakshatra_num  = profile.moon_nakshatra_number
    description    = NAKSHATRA_DESCRIPTIONS.get(nakshatra_num, "")

    return {
        "session_id":             session_id,
        "name":                   req.name,
        "moon_nakshatra_number":  nakshatra_num,
        "moon_nakshatra_name":    profile.moon_nakshatra_name,
        "moon_sign":              profile.moon_sign,
        "mercury_sign":           profile.mercury_sign,
        "mercury_house":          profile.mercury_house,
        "ascendant_sign":         profile.ascendant_sign,
        "chart_svg_url":          profile.chart_svg_url,
        "nakshatra_description":  description,
        "predicted_scores":       profile.predicted_scores,
    }


@app.post("/api/score-assessment")
def score_assessment(req: AssessmentRequest):
    """
    Scores 12 scenario responses, cross-references with Vedic blueprint,
    returns fingerprint data ready for visualization.
    """
    session = SESSIONS.get(req.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    profile            = session["profile"]
    behavioral_scores  = score_behavioral_responses(req.responses)
    result             = cross_reference(profile.predicted_scores, behavioral_scores)

    # Store for insights step
    session["behavioral_scores"] = behavioral_scores
    session["cross_ref"]         = result

    return {
        "session_id":        req.session_id,
        "predicted_scores":  profile.predicted_scores,
        "behavioral_scores": behavioral_scores,
        "alignment_score":   result["alignment_score"],
        "divergence_points": result["divergence_points"],
        "aligned_traits":    result["aligned_traits"],
        "dimension_gaps":    result["dimension_gaps"],
        "dimension_labels":  DIMENSION_LABELS,
    }


@app.post("/api/generate-insights")
def generate_insights(req: InsightRequest):
    """
    Generates 3-4 human, personalized insights from the cross-reference data.
    No external AI call needed — deterministic insight engine keeps it fast.
    """
    session = SESSIONS.get(req.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    profile   = session["profile"]
    behavioral = session.get("behavioral_scores", {})
    cross_ref  = session.get("cross_ref", {})
    name       = session["name"].split()[0]  # first name only

    insights = _build_insights(
        name, profile, behavioral, cross_ref
    )

    session["insights"] = insights
    return {
        "session_id": req.session_id,
        "insights":   insights,
    }


@app.post("/api/oracle")
def oracle(req: OracleRequest):
    """
    Analyzes a real decision through three lenses:
    chart prediction, behavioral reality, and the gap.
    """
    session = SESSIONS.get(req.session_id)

    # Session not in memory — use directly passed state data
    if not session and req.name:
        class _FakeProfile:
            moon_nakshatra_name = req.moon_nakshatra_name or "your Nakshatra"
            predicted_scores    = req.predicted_scores or {}
        profile   = _FakeProfile()
        beh       = req.behavioral_scores or {}
        diverged  = req.divergence_points or []
        aligned   = req.aligned_traits or []
        alignment = req.alignment_score or 50
        name      = req.name.split()[0]
        pred      = profile.predicted_scores
        decision  = req.decision.strip()
        cross_ref = {"divergence_points": diverged, "aligned_traits": aligned, "alignment_score": alignment}
    elif not session:
        raise HTTPException(status_code=404, detail="Session not found")
    else:
        profile   = session["profile"]
        beh       = session.get("behavioral_scores", {})
        cross_ref = session.get("cross_ref", {})
        name      = session["name"].split()[0]
        pred      = profile.predicted_scores
        diverged  = cross_ref.get("divergence_points", [])
        aligned   = cross_ref.get("aligned_traits", [])
        alignment = cross_ref.get("alignment_score", 50)
        decision  = req.decision.strip()

    dim_labels = {
        "processing_speed": "processing speed",
        "reasoning_style":  "reasoning style",
        "risk_tolerance":   "risk tolerance",
        "focus_mode":       "focus mode",
        "decision_driver":  "decision driver",
        "certainty_need":   "certainty need",
        "thinking_mode":    "thinking mode",
        "time_horizon":     "time horizon",
    }

    top_div   = diverged[0] if diverged else None
    top_align = aligned[0]  if aligned  else None

    # Part 1 — What your chart says
    risk_pred = pred.get("risk_tolerance", 5)
    if risk_pred >= 7:
        chart_verdict = f"Your {profile.moon_nakshatra_name} blueprint points toward bold action. Your chart predicts you'd lean into this decision rather than away from it — your wiring is built for risk when the vision is clear."
    elif risk_pred <= 3:
        chart_verdict = f"Your {profile.moon_nakshatra_name} blueprint urges caution here. Your chart predicts you'd want more certainty before moving — gathering evidence, testing assumptions, building safety nets first."
    else:
        chart_verdict = f"Your {profile.moon_nakshatra_name} blueprint sits in the middle on this one. Your chart predicts measured consideration — neither rushing in nor pulling back, but weighing deliberately before committing."

    # Part 2 — What your behavior says
    risk_beh = beh.get("risk_tolerance", 5)
    driver   = beh.get("decision_driver", 5)
    if risk_beh >= 7:
        beh_verdict = f"But your actual choices tell a different story, {name}. Across 12 scenarios, you consistently leaned toward the bolder option. When the clock was ticking, you moved. Your behavioral pattern says you'll take this leap — probably sooner than feels comfortable."
    elif risk_beh <= 3:
        beh_verdict = f"Your choices revealed something important, {name}: you move carefully in practice, regardless of what your chart says. Even when the data pointed toward risk, you chose the measured path. Your pattern says you'll need more certainty before you act on this."
    else:
        beh_verdict = f"Your behavioral pattern here is honest, {name}: you're somewhere in the middle. You don't rush — but you don't stall either. Your choices suggest you'll move on this when you've gathered enough signal. Not yet — but not never."

    # Part 3 — What the gap reveals
    if top_div and top_div == "risk_tolerance":
        gap_verdict = f"Here's the most useful thing your fingerprint reveals about this specific decision: there's a {abs(int(risk_pred - risk_beh))}-point gap between how your chart expected you to handle risk and how you actually do. That gap is your decision-making signature. The chart expected {'more caution' if risk_beh > risk_pred else 'more boldness'} — you've built the opposite. Trust the pattern you've actually lived, not the one that was predicted."
    elif top_div:
        gap_insight = f"Your biggest divergence is in {dim_labels.get(top_div, top_div)}. That gap is directly relevant here — it's where your instincts have grown beyond your blueprint. Whatever your chart predicts for this decision, your actual behavioral pattern has more authority."
        gap_verdict = f"{gap_insight} One concrete move: before deciding, ask yourself which version of you is making this call — the one your chart predicted, or the one your choices have built. At {alignment:.0f}% alignment, {name}, you have real agency here. The stars gave you a starting point. You've already gone beyond it."
    else:
        gap_verdict = f"At {alignment:.0f}% alignment, {name}, your chart and your choices are largely in agreement. That's rare — and it means your instincts on this decision are probably trustworthy. The gap that exists is in your favor: you've grown in the direction your chart pointed. Act from that."

    return {
        "parts": [
            {
                "title": "What your chart says you'll do",
                "body":  chart_verdict,
                "color": "#C9A84C"
            },
            {
                "title": "What your choices say you'll actually do",
                "body":  beh_verdict,
                "color": "#4C8EC9"
            },
            {
                "title": "What the gap reveals",
                "body":  gap_verdict,
                "color": "#9C6FDB"
            },
        ]
    }


@app.post("/api/chat")
def chat(req: ChatRequest):
    """
    Answers a question about the user's fingerprint using their actual session data.
    Keyword-based routing gives genuinely personalised replies without an external AI call.
    """
    session = SESSIONS.get(req.session_id)

    # Session not in memory — use directly passed state data
    if not session and req.name:
        pred = req.predicted_scores or {}
        beh  = req.behavioral_scores or {}
        divp = req.divergence_points or []
        alig = req.aligned_traits or []
        alig_score = req.alignment_score or 50

        # Build a lightweight profile-like object for _chat_response
        class _FakeProfile:
            moon_nakshatra_name = req.moon_nakshatra_name or "your Nakshatra"
            predicted_scores    = pred

        name      = req.name.split()[0]
        cross_ref = {
            "alignment_score":   alig_score,
            "divergence_points": divp,
            "aligned_traits":    alig,
            "dimension_gaps":    {},
        }
        q        = req.question.lower()
        response = _chat_response(name, _FakeProfile(), beh, cross_ref, q)
        return {"response": response}

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    name      = session["name"].split()[0]
    profile   = session["profile"]
    beh       = session.get("behavioral_scores", {})
    cross_ref = session.get("cross_ref", {})
    q         = req.question.lower()

    response = _chat_response(name, profile, beh, cross_ref, q)
    return {"response": response}


@app.get("/api/share/{session_id}")
def get_share(session_id: str):
    """Returns shareable public profile data."""
    session = SESSIONS.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found or expired")

    profile   = session["profile"]
    cross_ref = session.get("cross_ref", {})
    insights  = session.get("insights", [])

    return {
        "name":                  session["name"],
        "moon_nakshatra_name":   profile.moon_nakshatra_name,
        "ascendant_sign":        profile.ascendant_sign,
        "alignment_score":       cross_ref.get("alignment_score", 0),
        "top_insight":           insights[0]["body"] if insights else "",
        "chart_svg_url":         profile.chart_svg_url,
        "predicted_scores":      profile.predicted_scores,
        "behavioral_scores":     session.get("behavioral_scores", {}),
        "dimension_labels":      DIMENSION_LABELS,
    }


# ─── INSIGHT ENGINE ──────────────────────────────────────────────────────────

def _build_insights(name, profile, behavioral, cross_ref):
    insights = []
    gaps     = cross_ref.get("dimension_gaps", {})
    aligned  = cross_ref.get("aligned_traits", [])
    diverged = cross_ref.get("divergence_points", [])
    pred     = profile.predicted_scores
    beh      = behavioral

    # 1. Strongest alignment — what you ARE exactly as predicted
    if aligned:
        dim   = max(aligned, key=lambda k: pred.get(k, 5))
        title, body = _alignment_insight(name, dim, pred.get(dim, 5))
        insights.append({"title": title, "body": body, "type": "aligned"})

    # 2. Biggest divergence — the most interesting gap
    if diverged:
        dim   = max(diverged, key=lambda k: gaps.get(k, 0))
        title, body = _divergence_insight(name, dim, pred.get(dim, 5), beh.get(dim, 5))
        insights.append({"title": title, "body": body, "type": "divergence"})

    # 3. Hidden strength — behavioral high that chart didn't predict
    hidden = [k for k in behavioral if behavioral[k] >= 7 and pred.get(k, 5) < 6]
    if hidden:
        dim   = max(hidden, key=lambda k: behavioral[k])
        title, body = _hidden_strength_insight(name, dim, beh.get(dim, 5))
        insights.append({"title": title, "body": body, "type": "hidden"})

    # 4. Growth edge — chart predicted high but behavior went low
    edges = [k for k in pred if pred[k] >= 7 and beh.get(k, 5) <= 4]
    if edges:
        dim   = max(edges, key=lambda k: pred[k])
        title, body = _growth_edge_insight(name, dim)
        insights.append({"title": title, "body": body, "type": "growth"})

    # Always return at least 3
    if len(insights) < 3:
        insights.append({
            "title": "You play the long game.",
            "body": f"Your choices showed patience and long-term thinking that most people talk about but don't actually practice. That's rarer than you think, {name}.",
            "type": "general",
        })

    return insights[:4]


def _alignment_insight(name, dim, score):
    copy = {
        "processing_speed": (
            "Your mind moves exactly as fast as your chart said it would.",
            f"The prediction was clear — you'd process quickly, trust the first read, move before others have finished thinking. Your choices confirmed it every time. That's not impulsiveness, {name}. That's a calibrated instinct. Most people spend years trying to develop what you already have."
        ),
        "reasoning_style": (
            "Your chart called it. Intuition runs your mind.",
            f"The prediction was intuitive processing, and your scenarios proved it — you chose feeling over data, pattern over proof, gut over spreadsheet. That's not irrational, {name}. Intuition is just pattern recognition that's too fast to show its work."
        ),
        "risk_tolerance": (
            "You take risks. Your chart knew before you answered.",
            f"Every scenario where risk was on the table, you leaned in. Your Nakshatra predicted this — and your choices matched it completely. The interesting question isn't whether you take risks, {name}. It's whether you know which risks are worth it."
        ),
        "focus_mode": (
            "Details are your territory. Your chart was right about that.",
            f"You see the small things others skip. Your chart predicted a detail-oriented mind and your choices confirmed it — you slow down where others rush, you check what others assume. That precision has a cost in speed. It pays out in accuracy."
        ),
        "decision_driver": (
            "You lead with data. Your Nakshatra called this accurately.",
            f"When facing choices with emotional stakes, you went logical. Consistently. Your chart predicted this analytical driver and your responses confirmed it. The edge case to watch, {name}: when data and humanity pull in opposite directions."
        ),
        "certainty_need": (
            "You need to be sure before you move. Your chart predicted exactly that.",
            f"Every ambiguous scenario, you paused. That's not weakness — that's the quality control function of your mind. Your chart predicted high certainty need, and your behavior matched it. The trade-off is speed. The payoff is reliability."
        ),
        "thinking_mode": (
            "You think best alone. Your Nakshatra saw that coming.",
            f"Collaborative scenarios didn't pull you in. You defaulted to internal processing — solo, quiet, thorough. Your chart predicted independent thinking and your choices confirmed it. Some of the best thinking in history happened in rooms with one person."
        ),
        "time_horizon": (
            "Future-you is always in the room when you decide.",
            f"You consistently chose the long option — invest over spend, build over collect, later over now. Your chart predicted this future orientation and your behavior matched it fully. The only risk, {name}: present-you sometimes needs things too."
        ),
    }
    title, body = copy.get(dim, ("Your chart and behavior are in sync.", f"The Vedic prediction and your real choices matched closely here, {name}. That's a stable foundation."))
    return title, body


def _divergence_insight(name, dim, pred_score, beh_score):
    went_higher = beh_score > pred_score
    copy = {
        "processing_speed": (
            "Your chart said slow. Your choices said fast." if went_higher else "Your chart said fast. Your choices said wait.",
            f"The prediction was deliberate, methodical processing. But when the clock was ticking, you moved fast — consistently. That gap is real, {name}. Somewhere you built speed that wasn't in your original wiring. It might be compensation. It might be growth. Worth knowing which." if went_higher
            else f"The prediction was fast, instinct-first processing. But your choices were careful, deliberate, patient. You've built a filter over your natural speed, {name}. Whether that's wisdom or hesitation depends on whether it's serving you."
        ),
        "reasoning_style": (
            "Your chart predicted logic. You chose intuition.",
            f"Mercury suggested analytical processing — breaking things down, following evidence. But your choices went intuitive, almost every time. That's a real gap, {name}. It could mean you've learned to trust feeling over proof. It could mean analysis hasn't worked for you in the past. The gap between who your chart said you'd be and how you actually think — that's your most interesting territory."
        ) if went_higher else (
            "Your chart predicted intuition. You went analytical.",
            f"The Vedic reading suggested intuitive, feeling-first processing. But you chose data over gut, evidence over instinct, consistently. That's a meaningful divergence, {name}. You may have trained analytical thinking as a survival skill, even though your natural frequency is more intuitive. The question: which one do you trust more when it really matters?"
        ),
        "risk_tolerance": (
            "Your chart said careful. You chose bold.",
            f"The prediction was risk-averse — cautious, measured, protective. But your choices leaned into risk, almost reflexively. You're operating outside your Nakshatra's comfort zone, {name}. That's either expansion — or it's a pattern of betting before you're ready. Worth sitting with."
        ) if went_higher else (
            "Your chart said bold. You chose safe.",
            f"The prediction was risk-tolerant — a mind that bets on itself. But your choices were cautious, measured, protective. There's a gap between who the stars say you are and how you currently operate, {name}. Something has made you more careful than your wiring intended. That's not bad — it's just worth knowing."
        ),
        "decision_driver": (
            "Your chart said data. You let emotion lead.",
            f"The Vedic prediction was analytical — logic, evidence, structure. But when the stakes were human, you went emotional first. Every time. That gap, {name}, is one of the most human things about you. Your head says data. Your heart moves first. Learning to use both, in sequence, is the work."
        ) if went_higher else (
            "Your chart said heart. You went head.",
            f"The prediction pointed to feeling-forward processing — empathy first, then analysis. But your choices were consistently data-driven, even in emotionally loaded scenarios. You've built a rational filter over a more sensitive core, {name}. The question is whether that filter is protecting you — or hiding you."
        ),
        "time_horizon": (
            "Your chart said now. Your choices said later.",
            f"The Vedic reading suggested present-focused processing — concrete, immediate, tangible. But your behavior was consistently future-oriented. You kept choosing delayed reward, long-term investment, patience over immediacy. That's not your default wiring, {name}. You've built it. That kind of self-discipline is rarer than the natural version."
        ) if went_higher else (
            "Your chart said later. You kept choosing now.",
            f"The prediction was long time horizon — the kind of mind that plants trees it won't sit under. But your choices went present-tense, consistently. Immediate reward, tangible gain, now over later. There's a gap between your chart's prediction and your current pattern, {name}. Something is pulling you toward the near-term. It might be circumstance. It might be fear. Worth asking which."
        ),
    }
    default = (
        "Here's where it gets interesting.",
        f"Your chart predicted one pattern. Your choices revealed another. That gap — between what ancient wisdom said about your mind and how you actually operate — is your most interesting territory, {name}. It's not a contradiction. It's the evidence of a life that has shaped you beyond your original wiring."
    )
    title, body = copy.get(dim, default)
    return title, body


def _hidden_strength_insight(name, dim, score):
    labels = {
        "processing_speed": "fast processing",
        "reasoning_style":  "intuitive reasoning",
        "risk_tolerance":   "risk appetite",
        "focus_mode":       "big-picture thinking",
        "decision_driver":  "emotional intelligence",
        "certainty_need":   "tolerance for ambiguity",
        "thinking_mode":    "collaborative thinking",
        "time_horizon":     "long-term orientation",
    }
    label = labels.get(dim, "this strength")
    return (
        f"You built {label}. Your chart didn't predict it.",
        f"This one isn't in your Vedic wiring — it's something you developed. Your chart didn't call {label} as a natural trait, but your behavior showed it clearly. Earned strengths are often more reliable than natural ones, {name}. You know how to use this because you learned it the hard way."
    )


def _growth_edge_insight(name, dim):
    labels = {
        "processing_speed": "the speed your Nakshatra is known for",
        "reasoning_style":  "the intuitive processing your chart predicted",
        "risk_tolerance":   "the risk tolerance your Nakshatra carries",
        "focus_mode":       "the big-picture thinking in your blueprint",
        "decision_driver":  "the emotional depth your chart indicated",
        "certainty_need":   "the patience with ambiguity your Nakshatra holds",
        "thinking_mode":    "the collaborative instinct your chart pointed to",
        "time_horizon":     "the long-term thinking your blueprint carries",
    }
    label = labels.get(dim, "a trait your chart strongly predicted")
    return (
        "Your chart sees something in you that your choices haven't caught up to yet.",
        f"The Vedic prediction pointed strongly toward {label}. Your behavior didn't reflect it — not yet. That gap isn't a failure, {name}. It's a direction. The chart isn't wrong about what's there. It's just waiting for the right conditions to come forward."
    )


# ─── CHAT ENGINE ─────────────────────────────────────────────────────────────

def _chat_response(name: str, profile, beh: dict, cross_ref: dict, q: str) -> str:
    nakshatra  = profile.moon_nakshatra_name
    alignment  = cross_ref.get("alignment_score", 50)
    diverged   = cross_ref.get("divergence_points", [])
    aligned    = cross_ref.get("aligned_traits", [])
    pred       = profile.predicted_scores

    dim_labels = {
        "processing_speed": "processing speed",
        "reasoning_style":  "reasoning style",
        "risk_tolerance":   "risk tolerance",
        "focus_mode":       "focus mode",
        "decision_driver":  "decision driver",
        "certainty_need":   "certainty need",
        "thinking_mode":    "thinking mode",
        "time_horizon":     "time horizon",
    }

    # Historical figure / cognitive twin question
    if any(w in q for w in ["historical", "figure", "resemble", "like", "similar to",
                              "twin", "match", "comparable", "who am i like"]):
        risk_beh   = beh.get("risk_tolerance", 5)
        reason_beh = beh.get("reasoning_style", 5)
        focus_beh  = beh.get("focus_mode", 5)
        time_beh   = beh.get("time_horizon", 5)
        speed_beh  = beh.get("processing_speed", 5)

        figures = [
            (risk_beh >= 7 and reason_beh >= 6, "Nikola Tesla",
             f"High risk tolerance, intuitive reasoning, future-oriented thinking — Tesla's mind worked exactly this way. He saw patterns others missed and bet everything on visions nobody else could see yet."),
            (reason_beh >= 7 and focus_beh <= 4, "Leonardo da Vinci",
             f"Intuitive, big-picture thinking combined with restless curiosity — da Vinci never stayed in one discipline long enough for people to catch up. Your mind moves similarly."),
            (speed_beh <= 4 and focus_beh >= 7, "Marie Curie",
             f"Deliberate, detail-focused, certainty-seeking — Curie's greatest strength was refusing to move until the evidence was complete. Your fingerprint shows that same methodical precision."),
            (risk_beh <= 3 and time_beh >= 7, "Warren Buffett",
             f"Cautious, future-oriented, patient — Buffett's cognitive signature is exactly this: low risk tolerance combined with extreme long-term thinking. He plays a different game at a different timescale."),
            (reason_beh >= 6 and beh.get("decision_driver", 5) >= 7, "Maya Angelou",
             f"Intuitive, emotion-led, collaborative — Angelou processed the world through feeling first and found universal truth in the personal. Your behavioral pattern shows the same emotional intelligence."),
            (speed_beh >= 8 and risk_beh >= 6, "Elon Musk",
             f"Fast processing, high risk tolerance, future-focused — the combination that defines someone who decides quickly and bets large. Your fingerprint shows similar cognitive velocity."),
            (focus_beh >= 7 and beh.get("certainty_need", 5) >= 7, "Isaac Newton",
             f"Detail-focused, certainty-seeking, independent thinking — Newton worked alone, went deep, and refused to publish until he was certain. Your fingerprint reflects that same standard."),
            (beh.get("thinking_mode", 5) >= 7 and beh.get("decision_driver", 5) >= 6, "Gandhi",
             f"Collaborative, emotion-driven, patient — Gandhi's cognitive strength was his ability to move with people rather than ahead of them. Your fingerprint shows similar collective intelligence."),
        ]

        for condition, figure_name, description in figures:
            if condition:
                return f"Your cognitive fingerprint most closely resembles {figure_name}. {description}"

        return (
            f"Your fingerprint is genuinely unusual, {name} — it doesn't map cleanly to a single historical figure. "
            f"At {alignment:.0f}% alignment with your {nakshatra} blueprint, you sit at an interesting intersection. "
            f"The closest parallel might be someone who defied easy categorization in their own time — "
            f"which is usually a sign of someone operating ahead of the frameworks available to describe them."
        )

    # Fortune telling / future prediction — redirect gracefully
    if any(w in q for w in ["when", "will i", "will i get", "job", "career", "marriage", "money",
                              "predict", "future", "fortune", "when will", "how long", "salary"]):
        top_div = dim_labels.get(diverged[0], "your biggest gap") if diverged else "your growth edges"
        return (
            f"I can't predict the future, {name} — that's not what your fingerprint does. "
            f"What it does tell you is HOW your mind operates when you're making the decisions that shape that future. "
            f"Your {top_div} score shows where your instincts and your wiring diverge most. "
            f"That's the data that actually matters for the choices in front of you."
        )

    # "Tell more" / "more" / "explain" / "expand" — expand on biggest divergence
    if any(w in q for w in ["more", "tell more", "explain", "expand", "elaborate", "go on",
                              "and", "so", "interesting", "really", "wow"]) and len(q.split()) <= 5:
        if diverged:
            top_div = diverged[0]
            top_label = dim_labels.get(top_div, top_div)
            pred_score = pred.get(top_div, 5)
            beh_score  = beh.get(top_div, 5)
            direction  = "higher" if beh_score > pred_score else "lower"
            gap        = abs(int(pred_score - beh_score))
            return (
                f"Let's go deeper on {top_label} — your biggest divergence, {name}. "
                f"Your {nakshatra} chart predicted {pred_score}/10. Your choices showed {beh_score}/10. "
                f"That's a {gap}-point gap. Your actual behavior ran {direction} than your blueprint expected. "
                f"A gap this size usually means something specific happened in your life that reshaped this trait. "
                f"It's not random — it's a response to experience. "
                f"{'You became more cautious than your wiring intended.' if beh_score < pred_score else 'You became bolder than your wiring intended.'} "
                f"That's earned. Not predicted."
            )
        return (
            f"The most interesting thing in your fingerprint, {name}: your {alignment:.0f}% alignment score. "
            f"That number means {'your chart and your actual mind are deeply in sync — rare.' if alignment > 75 else 'real divergence exists between who the stars said you would be and who your choices have made you.' if alignment < 55 else 'you are mostly who your chart predicted, with some genuinely surprising departures.'} "
            f"The departures are where the real story is."
        )

    # People / social / collaborative questions
    if any(w in q for w in ["people", "social", "friend", "relationship", "team",
                              "collaborate", "work with", "get along", "interpersonal",
                              "connect", "empathy", "others", "colleagues"]):
        think_pred = pred.get("thinking_mode", 5)
        think_beh  = beh.get("thinking_mode", 5)
        driver_beh = beh.get("decision_driver", 5)
        style = "collaborative" if think_beh >= 7 else "independent" if think_beh <= 3 else "selectively collaborative"
        empathy = "high empathy" if driver_beh >= 7 else "logic-first" if driver_beh <= 3 else "balanced"
        return (
            f"Your fingerprint shows a {style} thinking style with {empathy} in how you engage with people, {name}. "
            f"Thinking Mode: chart predicted {think_pred}/10, your choices showed {think_beh}/10 — "
            f"{'you matched your blueprint here' if abs(think_pred - think_beh) <= 2 else 'you diverged from your chart on this one'}. "
            f"{'You tend to process best with others around — collaboration energises rather than drains you.' if think_beh >= 7 else 'You tend to do your best thinking alone — collaboration is something you choose deliberately, not your default.' if think_beh <= 3 else 'You switch between solo and collaborative modes depending on the situation — which is actually a strength.'}"
        )

    # "Am I who the stars said I'd be" / identity questions
    if any(w in q for w in ["who am i", "who i am", "stars said", "supposed to be",
                              "meant to be", "am i who", "am i the", "am i really",
                              "identity", "who was i"]) or q.strip() in ["am i", "who am i"]:
        if alignment >= 75:
            return (
                f"At {alignment:.0f}% alignment, {name} — largely yes. "
                f"Your {nakshatra} blueprint made specific predictions about how your mind works, "
                f"and your choices confirmed most of them. "
                f"Your anchored traits are real. The foundation your chart predicted is the foundation you actually stand on. "
                f"The 25% that diverged? That's where you went beyond the prediction. That's yours, not the stars'."
            )
        elif alignment >= 55:
            return (
                f"Mostly, {name} — but not entirely, and that's the interesting part. "
                f"At {alignment:.0f}% alignment, your {nakshatra} chart called most of it right. "
                f"But in {len(diverged)} dimension{'s' if len(diverged) > 1 else ''}, your choices went a different direction than predicted. "
                f"You are who the stars said you'd be — plus something they didn't see coming."
            )
        else:
            return (
                f"Less than you might expect, {name}. At {alignment:.0f}% alignment, "
                f"your life has shaped you significantly beyond what your {nakshatra} chart predicted. "
                f"That's not a failure of astrology — it's evidence of everything you've lived through. "
                f"You've grown in directions the stars didn't fully anticipate. "
                f"That kind of person is harder to read — and usually more interesting."
            )

    # Hidden strength questions
    if any(w in q for w in ["hidden", "strength", "built", "earned", "developed",
                              "surprising", "surprise", "unexpected", "interesting"]):
        hidden = [k for k in beh if beh.get(k, 5) >= 7 and pred.get(k, 5) < 6]
        if hidden:
            dim   = hidden[0]
            label = dim_labels.get(dim, dim)
            score = beh.get(dim, 7)
            return (
                f"Your clearest hidden strength is {label}, {name}. "
                f"Your chart predicted {pred.get(dim, 5)}/10 here. Your choices showed {score}/10. "
                f"That gap isn't in your Vedic wiring — you built it. "
                f"Earned strengths are often more reliable than natural ones because you know exactly how you got there. "
                f"You've used this in ways your chart never anticipated."
            )
        return (
            f"Your most surprising result, {name}: {alignment:.0f}% alignment overall. "
            f"{'Most people expect more divergence. Your chart read you accurately.' if alignment > 70 else 'The gap between prediction and reality is where you have grown most — and that growth is entirely yours.'}"
        )

    # Nakshatra / astrology questions
    if any(w in q for w in ["nakshatra", "star", "astrology", "vedic", "chart",
                              "birth", "cosmos", "moon", "jyotish", "placement"]):
        return (
            f"Your Moon is in {nakshatra}. In Jyotish, the Moon Nakshatra is the primary indicator "
            f"of the mind's architecture — how you process information, make decisions, and respond under pressure. "
            f"It's more specific than a sun sign. "
            f"Your chart made predictions across 8 cognitive dimensions from this placement. "
            f"At {alignment:.0f}% alignment, {'it was right about most of them.' if alignment > 65 else 'your life has taken you in some genuinely different directions.'}"
        )

    # Risk questions
    if any(w in q for w in ["risk", "bold", "safe", "caution", "danger", "bet", "gamble"]):
        risk_pred = pred.get("risk_tolerance", 5)
        risk_beh  = beh.get("risk_tolerance", 5)
        direction = "more cautious than your chart predicted" if risk_beh < risk_pred else \
                    "bolder than your chart predicted" if risk_beh > risk_pred else \
                    "exactly as bold as your chart predicted"
        return (
            f"Risk tolerance: your chart predicted {risk_pred}/10. Your choices: {risk_beh}/10. "
            f"You ran {direction}. "
            f"{'Something taught you to be careful. That caution is a response to something real.' if risk_beh < risk_pred else 'Something pushed you to bet on yourself more than your wiring expected. That boldness is earned.' if risk_beh > risk_pred else f'That consistency is rare, {name}. Your instincts and your blueprint are in sync here.'}"
        )

    # Alignment / divergence questions
    if any(w in q for w in ["align", "match", "gap", "differ", "diverge",
                              "different", "percent", "%", "score", "number"]):
        if diverged:
            top_div = dim_labels.get(diverged[0], diverged[0])
            return (
                f"{alignment:.0f}% alignment, {name}. Your biggest gap is in {top_div}. "
                f"{'High alignment — your chart and your choices tell the same story.' if alignment > 70 else 'Real divergence — your life has shaped you beyond what your chart anticipated.'} "
                f"The gap isn't a flaw. It's where you grew."
            )
        return (
            f"Your alignment is {alignment:.0f}%, {name}. "
            f"{'Strong — your wiring and your behavior are deeply in sync.' if alignment > 70 else 'There is genuine divergence. That means your choices have taken you somewhere your chart did not fully predict.'}"
        )

    # Decision making / intuition / logic
    if any(w in q for w in ["decision", "choose", "logic", "intuition",
                              "feel", "analytical", "rational", "emotional"]):
        driver_pred = pred.get("decision_driver", 5)
        driver_beh  = beh.get("decision_driver", 5)
        style = "data and logic" if driver_beh <= 4 else \
                "emotion and empathy" if driver_beh >= 7 else \
                "a balance of logic and feeling"
        return (
            f"Your choices revealed that you lead with {style}, {name}. "
            f"Chart predicted {driver_pred}/10. You showed {driver_beh}/10. "
            f"{'Matched closely — your decision style is consistent with your blueprint.' if abs(driver_pred - driver_beh) <= 2 else 'A real gap — how you actually decide differs from what your chart expected. That difference is usually where the most interesting growth has happened.'}"
        )

    # Future / time horizon
    if any(w in q for w in ["long term", "patient", "present", "horizon", "short term", "now vs later"]):
        th_beh = beh.get("time_horizon", 5)
        return (
            f"Time horizon: {th_beh}/10 from your choices, {name}. "
            f"{'Future-oriented — you trade present comfort for long-term gain naturally.' if th_beh >= 7 else 'Present-focused — immediate, concrete outcomes drive you more than distant payoffs.' if th_beh <= 3 else 'Balanced — you can think long-term when it matters without ignoring what is in front of you.'} "
            f"Your chart predicted {pred.get('time_horizon', 5)}/10. "
            f"{'Close match.' if abs(pred.get('time_horizon', 5) - th_beh) <= 2 else 'A notable gap — one of your more interesting divergences.'}"
        )

    # Default — shorter, specific, not repetitive
    if diverged:
        top_div   = dim_labels.get(diverged[0], diverged[0])
        pred_score = pred.get(diverged[0], 5)
        beh_score  = beh.get(diverged[0], 5)
        return (
            f"Your fingerprint's most interesting data point, {name}: "
            f"a {abs(int(pred_score - beh_score))}-point gap in {top_div}. "
            f"Chart said {pred_score}/10. You showed {beh_score}/10. "
            f"Ask me about that gap — or about risk, decisions, your nakshatra, or what your alignment score means."
        )
    return (
        f"At {alignment:.0f}% alignment, {name}, your chart and your choices are "
        f"{'largely telling the same story' if alignment > 65 else 'in some genuinely interesting tension'}. "
        f"Ask me about risk tolerance, decision making, time horizon, or your nakshatra — I can go specific."
    )


# ─── SERVE FRONTEND ──────────────────────────────────────────────────────────

frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend")
frontend_path = os.path.abspath(frontend_path)

if os.path.exists(frontend_path):
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")
