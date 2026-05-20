"""
Vedic Cognitive Fingerprint — Astrology API Integration
Centralized module: all API calls go through here, nothing scattered.

Endpoints used:
  - /planets              → Moon sign, Mercury sign/house, Ascendant
  - /nakshatra-durations  → Moon Nakshatra name + number
  - /horoscope-chart-url  → SVG birth chart image URL
"""

import os
import json
import requests
from dataclasses import dataclass, field
from dotenv import load_dotenv

load_dotenv()

# ─── CONFIG ──────────────────────────────────────────────────────────────────

BASE_URL = "https://json.freeastrologyapi.com"
API_KEY  = os.getenv("ASTROLOGY_API_KEY")

HEADERS = {
    "Content-Type": "application/json",
    "x-api-key": API_KEY,
}

DEFAULT_CONFIG = {
    "observation_point": "topocentric",
    "ayanamsha": "lahiri",
}

ZODIAC_SIGNS = {
    1: "Aries", 2: "Taurus", 3: "Gemini", 4: "Cancer",
    5: "Leo", 6: "Virgo", 7: "Libra", 8: "Scorpio",
    9: "Sagittarius", 10: "Capricorn", 11: "Aquarius", 12: "Pisces",
}

DIMENSION_KEYS = [
    "processing_speed", "reasoning_style", "risk_tolerance", "focus_mode",
    "decision_driver", "certainty_need", "thinking_mode", "time_horizon",
]

DIMENSION_LABELS = {
    "processing_speed": "Processing Speed",
    "reasoning_style":  "Reasoning Style",
    "risk_tolerance":   "Risk Tolerance",
    "focus_mode":       "Focus Mode",
    "decision_driver":  "Decision Driver",
    "certainty_need":   "Certainty Need",
    "thinking_mode":    "Thinking Mode",
    "time_horizon":     "Time Horizon",
}


# ─── DATA CLASSES ────────────────────────────────────────────────────────────

@dataclass
class BirthDetails:
    year:      int
    month:     int
    date:      int
    hours:     int
    minutes:   int
    seconds:   int
    latitude:  float
    longitude: float
    timezone:  float


@dataclass
class VedicProfile:
    moon_nakshatra_number: int
    moon_nakshatra_name:   str
    moon_sign:             str
    mercury_sign:          str
    mercury_house:         int
    ascendant_sign:        str
    chart_svg_url:         str
    predicted_scores:      dict = field(default_factory=dict)


# ─── NAKSHATRA COGNITIVE MAP ──────────────────────────────────────────────────
# All 27 Nakshatras mapped to 8 cognitive dimensions (1–10 scale)
# Sources: Jyotish Nakshatra trait literature (Bepin Behari, Hart de Fouw)

NAKSHATRA_COGNITIVE_MAP = {
    1:  {"name": "Ashwini",           "processing_speed": 9, "reasoning_style": 7, "risk_tolerance": 8, "focus_mode": 6, "decision_driver": 5, "certainty_need": 3, "thinking_mode": 4, "time_horizon": 3},
    2:  {"name": "Bharani",           "processing_speed": 5, "reasoning_style": 5, "risk_tolerance": 7, "focus_mode": 7, "decision_driver": 8, "certainty_need": 5, "thinking_mode": 5, "time_horizon": 5},
    3:  {"name": "Krittika",          "processing_speed": 7, "reasoning_style": 3, "risk_tolerance": 6, "focus_mode": 4, "decision_driver": 3, "certainty_need": 3, "thinking_mode": 3, "time_horizon": 5},
    4:  {"name": "Rohini",            "processing_speed": 4, "reasoning_style": 7, "risk_tolerance": 4, "focus_mode": 8, "decision_driver": 8, "certainty_need": 6, "thinking_mode": 7, "time_horizon": 4},
    5:  {"name": "Mrigashira",        "processing_speed": 6, "reasoning_style": 6, "risk_tolerance": 5, "focus_mode": 5, "decision_driver": 5, "certainty_need": 4, "thinking_mode": 5, "time_horizon": 6},
    6:  {"name": "Ardra",             "processing_speed": 7, "reasoning_style": 4, "risk_tolerance": 7, "focus_mode": 6, "decision_driver": 4, "certainty_need": 3, "thinking_mode": 3, "time_horizon": 6},
    7:  {"name": "Punarvasu",         "processing_speed": 5, "reasoning_style": 5, "risk_tolerance": 5, "focus_mode": 6, "decision_driver": 5, "certainty_need": 5, "thinking_mode": 6, "time_horizon": 7},
    8:  {"name": "Pushya",            "processing_speed": 3, "reasoning_style": 3, "risk_tolerance": 2, "focus_mode": 8, "decision_driver": 6, "certainty_need": 8, "thinking_mode": 7, "time_horizon": 7},
    9:  {"name": "Ashlesha",          "processing_speed": 5, "reasoning_style": 3, "risk_tolerance": 6, "focus_mode": 7, "decision_driver": 4, "certainty_need": 5, "thinking_mode": 3, "time_horizon": 6},
    10: {"name": "Magha",             "processing_speed": 5, "reasoning_style": 4, "risk_tolerance": 5, "focus_mode": 6, "decision_driver": 5, "certainty_need": 6, "thinking_mode": 4, "time_horizon": 6},
    11: {"name": "Purva Phalguni",    "processing_speed": 6, "reasoning_style": 7, "risk_tolerance": 6, "focus_mode": 5, "decision_driver": 7, "certainty_need": 4, "thinking_mode": 8, "time_horizon": 3},
    12: {"name": "Uttara Phalguni",   "processing_speed": 5, "reasoning_style": 4, "risk_tolerance": 4, "focus_mode": 7, "decision_driver": 5, "certainty_need": 6, "thinking_mode": 6, "time_horizon": 6},
    13: {"name": "Hasta",             "processing_speed": 6, "reasoning_style": 4, "risk_tolerance": 4, "focus_mode": 8, "decision_driver": 4, "certainty_need": 6, "thinking_mode": 5, "time_horizon": 5},
    14: {"name": "Chitra",            "processing_speed": 7, "reasoning_style": 6, "risk_tolerance": 6, "focus_mode": 7, "decision_driver": 5, "certainty_need": 4, "thinking_mode": 4, "time_horizon": 6},
    15: {"name": "Swati",             "processing_speed": 5, "reasoning_style": 6, "risk_tolerance": 5, "focus_mode": 5, "decision_driver": 5, "certainty_need": 5, "thinking_mode": 6, "time_horizon": 5},
    16: {"name": "Vishakha",          "processing_speed": 7, "reasoning_style": 4, "risk_tolerance": 7, "focus_mode": 6, "decision_driver": 5, "certainty_need": 4, "thinking_mode": 5, "time_horizon": 7},
    17: {"name": "Anuradha",          "processing_speed": 4, "reasoning_style": 4, "risk_tolerance": 5, "focus_mode": 7, "decision_driver": 6, "certainty_need": 6, "thinking_mode": 6, "time_horizon": 7},
    18: {"name": "Jyeshtha",          "processing_speed": 6, "reasoning_style": 3, "risk_tolerance": 6, "focus_mode": 6, "decision_driver": 4, "certainty_need": 4, "thinking_mode": 3, "time_horizon": 5},
    19: {"name": "Mula",              "processing_speed": 6, "reasoning_style": 3, "risk_tolerance": 8, "focus_mode": 4, "decision_driver": 4, "certainty_need": 2, "thinking_mode": 3, "time_horizon": 6},
    20: {"name": "Purva Ashadha",     "processing_speed": 6, "reasoning_style": 6, "risk_tolerance": 7, "focus_mode": 5, "decision_driver": 6, "certainty_need": 3, "thinking_mode": 7, "time_horizon": 6},
    21: {"name": "Uttara Ashadha",    "processing_speed": 4, "reasoning_style": 3, "risk_tolerance": 4, "focus_mode": 6, "decision_driver": 4, "certainty_need": 7, "thinking_mode": 5, "time_horizon": 9},
    22: {"name": "Shravana",          "processing_speed": 4, "reasoning_style": 5, "risk_tolerance": 3, "focus_mode": 7, "decision_driver": 5, "certainty_need": 7, "thinking_mode": 6, "time_horizon": 6},
    23: {"name": "Dhanishtha",        "processing_speed": 7, "reasoning_style": 5, "risk_tolerance": 7, "focus_mode": 5, "decision_driver": 5, "certainty_need": 3, "thinking_mode": 5, "time_horizon": 5},
    24: {"name": "Shatabhisha",       "processing_speed": 5, "reasoning_style": 3, "risk_tolerance": 6, "focus_mode": 6, "decision_driver": 3, "certainty_need": 4, "thinking_mode": 2, "time_horizon": 7},
    25: {"name": "Purva Bhadrapada",  "processing_speed": 6, "reasoning_style": 6, "risk_tolerance": 7, "focus_mode": 5, "decision_driver": 6, "certainty_need": 3, "thinking_mode": 4, "time_horizon": 7},
    26: {"name": "Uttara Bhadrapada", "processing_speed": 3, "reasoning_style": 5, "risk_tolerance": 3, "focus_mode": 7, "decision_driver": 5, "certainty_need": 7, "thinking_mode": 5, "time_horizon": 9},
    27: {"name": "Revati",            "processing_speed": 4, "reasoning_style": 7, "risk_tolerance": 4, "focus_mode": 6, "decision_driver": 7, "certainty_need": 5, "thinking_mode": 7, "time_horizon": 6},
}

# Human-readable descriptions per Nakshatra for the Blueprint screen
NAKSHATRA_DESCRIPTIONS = {
    1:  "Your mind is built for speed. Ashwini doesn't wait for all the information — it catches the first clear signal and moves. That's not recklessness. That's momentum.",
    2:  "You feel before you think. Bharani holds experiences deeply and makes decisions with the whole body, not just the head. Intensity is your natural frequency.",
    3:  "Krittika cuts through noise. You see what others politely ignore, and you're not afraid to say it. Your mind is a blade — precise, direct, sometimes sharp.",
    4:  "Rohini processes the world through the senses. Detail, texture, beauty, memory — your mind absorbs everything and holds it close. Patience is your strength.",
    5:  "Mrigashira is always searching. You think in questions, not conclusions. Curiosity pulls you forward — always one more door to open, one more idea to chase.",
    6:  "Ardra thinks in storms. Confusion comes first, then a breakthrough. Your mind works best under pressure — when everything is uncertain, you find the pattern.",
    7:  "Punarvasu returns to principles. When lost, you go back to what you know is true. Your thinking is cyclical, generous, and deeply rooted in meaning.",
    8:  "Pushya is methodical and nurturing. You build slowly and build well. Your mind is a planner — thorough, caring, and focused on what lasts.",
    9:  "Ashlesha is strategic to its core. You observe before you act, and you rarely show your full hand. Deep pattern recognition is your superpower.",
    10: "Magha carries authority naturally. You think in legacy — what has been built, what should be honored, what's worth protecting. History informs your judgment.",
    11: "Purva Phalguni is creative and social. Your best thinking happens in pleasure, play, and connection. Deadlines and pressure are enemies of your mind's best work.",
    12: "Uttara Phalguni is practical and principled. You think in service — what's fair, what's useful, what actually helps. You don't overthink. You decide and act.",
    13: "Hasta is precise and skillful. You think with your hands as much as your head — working through problems by doing, not just pondering. Craft is cognition for you.",
    14: "Chitra sees the whole picture — and wants it to be beautiful. You think in design and vision. If it isn't elegant, it isn't right.",
    15: "Swati balances. You see multiple sides naturally, which makes you diplomatic — and occasionally indecisive. But when you land, you land well.",
    16: "Vishakha is goal-driven. Once you know what you want, your mind becomes a laser. You tolerate discomfort and delay better than most because the target is always visible.",
    17: "Anuradha is devoted and disciplined. Your mind works best inside structure, commitment, and deep loyalty to what — and who — you believe in.",
    18: "Jyeshtha leads and protects. You think strategically about power — who has it, how it flows, how to guard what matters. You're a natural behind-the-scenes architect.",
    19: "Mula digs to the root. You're not satisfied with surface answers. You need to know *why*, and you'll pull everything apart to find out. Transformation is your mode.",
    20: "Purva Ashadha is persuasive and optimistic. You think in possibility, not constraint. Your conviction is contagious — others follow your thinking because you believe it completely.",
    21: "Uttara Ashadha plays the long game. Your mind is focused on what's universal, lasting, principled. Short-term wins don't interest you as much as building something that endures.",
    22: "Shravana listens deeply. Your greatest cognitive strength is absorption — you take in more than you let on, process quietly, and speak with weight when you do.",
    23: "Dhanishtha moves with rhythm. Your mind works in patterns, beats, and momentum. You think best when things are moving — stillness makes your thinking go flat.",
    24: "Shatabhisha is the scientist. Independent, unconventional, and tireless in investigation. Your mind draws its own conclusions, often well ahead of everyone else.",
    25: "Purva Bhadrapada thinks with intensity. You hold ideals fiercely and feel the weight of your own thoughts. Transformation — including the painful kind — doesn't scare you.",
    26: "Uttara Bhadrapada is deep and patient. Your mind operates on a long timescale. You're comfortable sitting with complexity while others panic. Wisdom accrues quietly in you.",
    27: "Revati sees the whole journey. Compassionate, imaginative, and quietly creative — your mind works best when guided by meaning and care, not just logic or speed.",
}


# ─── HELPERS ─────────────────────────────────────────────────────────────────

def _build_payload(birth: BirthDetails) -> dict:
    return {
        "year": birth.year, "month": birth.month, "date": birth.date,
        "hours": birth.hours, "minutes": birth.minutes, "seconds": birth.seconds,
        "latitude": birth.latitude, "longitude": birth.longitude,
        "timezone": birth.timezone,
        "config": DEFAULT_CONFIG,
    }


def _post(endpoint: str, payload: dict) -> dict:
    url = f"{BASE_URL}/{endpoint}"
    response = requests.post(url, headers=HEADERS, json=payload, timeout=15)
    response.raise_for_status()
    return response.json()


# ─── API CALLS ────────────────────────────────────────────────────────────────

def fetch_nakshatra(birth: BirthDetails) -> dict:
    data = _post("nakshatra-durations", _build_payload(birth))
    # output is a JSON string — parse it
    output = data.get("output", "{}")
    return json.loads(output) if isinstance(output, str) else output


def fetch_planets(birth: BirthDetails) -> dict:
    payload = _build_payload(birth)
    payload.pop("config", None)
    payload["settings"] = DEFAULT_CONFIG
    data = _post("planets", payload)
    # output is a list of single-key dicts like [{"0": {...}}, {"1": {...}}]
    raw = data.get("output", [])
    planets = {}
    for item in raw:
        for planet_data in item.values():
            name = planet_data.get("name", "")
            if name:
                planets[name] = planet_data
    return planets


def fetch_chart_url(birth: BirthDetails) -> str:
    data = _post("horoscope-chart-url", _build_payload(birth))
    output = data.get("output", "")
    return output if isinstance(output, str) else ""


# ─── MAIN ORCHESTRATOR ────────────────────────────────────────────────────────

def build_vedic_profile(birth: BirthDetails) -> VedicProfile:
    nakshatra  = fetch_nakshatra(birth)
    planets    = fetch_planets(birth)
    chart_url  = fetch_chart_url(birth)

    nakshatra_num  = nakshatra.get("number", 1)
    nakshatra_name = nakshatra.get("name", "Unknown")

    moon      = planets.get("Moon",      {})
    mercury   = planets.get("Mercury",   {})
    ascendant = planets.get("Ascendant", {})

    moon_sign      = ZODIAC_SIGNS.get(moon.get("current_sign", 0), "Unknown")
    mercury_sign   = ZODIAC_SIGNS.get(mercury.get("current_sign", 0), "Unknown")
    ascendant_sign = ZODIAC_SIGNS.get(ascendant.get("current_sign", 0), "Unknown")

    # Mercury house: derived from position relative to Ascendant sign number
    asc_num      = ascendant.get("current_sign", 1)
    merc_num     = mercury.get("current_sign", 1)
    mercury_house = ((merc_num - asc_num) % 12) + 1

    # Predicted cognitive scores from Nakshatra lookup
    entry = NAKSHATRA_COGNITIVE_MAP.get(nakshatra_num, {})
    predicted_scores = {k: entry.get(k, 5) for k in DIMENSION_KEYS}

    return VedicProfile(
        moon_nakshatra_number = nakshatra_num,
        moon_nakshatra_name   = nakshatra_name,
        moon_sign             = moon_sign,
        mercury_sign          = mercury_sign,
        mercury_house         = mercury_house,
        ascendant_sign        = ascendant_sign,
        chart_svg_url         = chart_url,
        predicted_scores      = predicted_scores,
    )


# ─── BEHAVIORAL SCORER ───────────────────────────────────────────────────────

SCENARIO_SCORE_MAP = {
    "s01": {"A": {"processing_speed": +4}, "B": {"processing_speed": -3}},
    "s02": {"A": {"reasoning_style": -4},  "B": {"reasoning_style": +4}},
    "s03": {"A": {"risk_tolerance": +2},   "B": {"risk_tolerance": +4},  "C": {"risk_tolerance": -3}},
    "s04": {"A": {"focus_mode": -4},       "B": {"focus_mode": +4}},
    "s05": {"A": {"decision_driver": -4},  "B": {"decision_driver": +4}},
    "s06": {"A": {"certainty_need": +3},   "B": {"certainty_need": -3}},
    "s07": {"A": {"thinking_mode": -4},    "B": {"thinking_mode": +4}},
    "s08": {"A": {"time_horizon": -4},     "B": {"time_horizon": +4}},
    "s09": {"A": {"processing_speed": +3}, "B": {"processing_speed": -2}},
    "s10": {"A": {"reasoning_style": -3, "decision_driver": -2}, "B": {"reasoning_style": +2, "decision_driver": +3}, "C": {"certainty_need": +2}},
    "s11": {"A": {"focus_mode": +3},       "B": {"focus_mode": -3}},
    "s12": {"A": {"reasoning_style": +4},  "B": {"reasoning_style": +1}, "C": {"reasoning_style": -3}},
}


def score_behavioral_responses(responses: dict) -> dict:
    scores = {k: 5 for k in DIMENSION_KEYS}
    for scenario_id, answer in responses.items():
        deltas = SCENARIO_SCORE_MAP.get(scenario_id, {}).get(answer, {})
        for dim, delta in deltas.items():
            scores[dim] = max(1, min(10, scores[dim] + delta))
    return scores


# ─── CROSS-REFERENCE ─────────────────────────────────────────────────────────

def cross_reference(predicted: dict, behavioral: dict) -> dict:
    gaps = {k: abs(predicted.get(k, 5) - behavioral.get(k, 5)) for k in DIMENSION_KEYS}
    alignment = (1 - sum(gaps.values()) / (9 * len(DIMENSION_KEYS))) * 100
    return {
        "alignment_score":   round(alignment, 1),
        "divergence_points": [k for k, v in gaps.items() if v > 3],
        "aligned_traits":    [k for k, v in gaps.items() if v <= 1],
        "dimension_gaps":    gaps,
    }


# ─── QUICK TEST ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    sample = BirthDetails(
        year=2022, month=8, date=11,
        hours=6, minutes=0, seconds=0,
        latitude=17.38333, longitude=78.4666, timezone=5.5,
    )
    print("Building Vedic profile...")
    profile = build_vedic_profile(sample)
    print(f"Nakshatra  : {profile.moon_nakshatra_name} (#{profile.moon_nakshatra_number})")
    print(f"Moon       : {profile.moon_sign}")
    print(f"Mercury    : {profile.mercury_sign}, House {profile.mercury_house}")
    print(f"Ascendant  : {profile.ascendant_sign}")
    print(f"Chart URL  : {profile.chart_svg_url}")
    print(f"\nPredicted scores:")
    for k, v in profile.predicted_scores.items():
        print(f"  {k:<22}: {v}/10")
