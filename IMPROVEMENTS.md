# MeDo Hackathon — Critical Improvements

## Priority 1 — Prize Killers (Fix These First)

### 1. Chat is keyword routing, not real AI
**Problem:** Every chat response is a pre-written template selected by if/else keyword matching. No ERNIE, no LLM. A judge who probes for 2 minutes sees through it.
**Fix:** Add ERNIE API call to Railway `/api/chat`. Use deterministic engine as fallback only.
**Status:** IN PROGRESS

### 2. No shareable image
**Problem:** "Share on X" sends text. No visual card is generated or downloadable. Viral sharing needs an image.
**Fix:** Add `html2canvas` to SharePage to export the radar card as a PNG download.
**Status:** PENDING

### 3. Alignment score has no emotional context
**Problem:** "74% alignment" — is that high? Low? Users have no reference point.
**Fix:** Add benchmark text: "Higher than X% of people who've taken this." Makes the number feel earned.
**Status:** PENDING

### 4. Assessment questions feel like HR corporate quiz
**Problem:** "You receive an urgent message while working..." — standard psychometric filler. Kills the cosmic/unique angle.
**Fix:** Rewrite all 12 scenarios to feel atmospheric and specific to the Vedic framing.
**Status:** PENDING

### 5. Cognitive twin matching is too broad
**Problem:** risk >= 7 AND reason >= 6 → Tesla. Too many users get the same figure. Feels like flattery.
**Fix:** Tighten conditions, add a "mixed profile" figure, ensure no more than ~30% of profiles match any single figure.
**Status:** PENDING

---

## Priority 2 — UX Friction

### 6. 8+ screens before first insight
**Problem:** Landing → Birth form → Blueprint → 12 questions → Processing → Reveal → Truth → Insights. Too long. Drop-off is brutal.
**Fix:** Merge Blueprint into the Birth Form result (show inline). Cut to 8 assessment questions.

### 7. Truth sentence reads like a fortune cookie
**Problem:** "${nakshatra} predicted patience. ${name} chose speed." — feels thin after 8 screens.
**Fix:** Show 3 variations, ask "which resonates?" — adds interactivity and makes it feel personal.

### 8. No persistence
**Problem:** Close tab = everything gone. No shareable link, no "come back later."
**Fix:** Save fingerprint to Supabase with a public `/share/:sessionId` URL (already partially built).

---

## Priority 3 — Credibility

### 9. Vedic-to-score mapping is invisible
**Problem:** Users don't understand why Rohini → processing_speed = 7. Looks arbitrary.
**Fix:** Add a "how this works" tooltip or section on the Blueprint page explaining the 27×8 mapping.

### 10. Vedic framing may alienate judges
**Problem:** Nakshatra names mean nothing to non-South-Asian judges. "Vedic" sounds pseudoscientific.
**Fix:** Lead with "Cognitive Fingerprint" everywhere. Use Nakshatra as supporting detail, not the headline.

---

## What Would Actually Win

1. Real AI generating genuinely unique responses per user (not templates)
2. A beautiful downloadable/shareable image card
3. The "gap" concept made viscerally clear with a single surprising sentence
4. Under 5 minutes start to finish
5. One memorable demo moment judges can't forget (the reveal animation is close — keep it)
