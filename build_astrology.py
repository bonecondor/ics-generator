from datetime import datetime, timedelta
import uuid
import os

# --- Astrology events Sept–Dec 2025 (collective + personal) ---
astrology_events = [
    # Collective
    ("2025-09-21", "🌑 New Moon — Virgo",
     "Collective: Practical resets, health/service themes.\nPersonal: Supports routines and body alignment.\nKeywords: purification, grounding, new cycles."),
    
    ("2025-09-29", "🌕 Full Moon Eclipse — Aries",
     "Collective: Heightened energy, confrontations, release cycles.\nPersonal: Lights up self vs. other dynamics in relationships.\nKeywords: courage, independence, closure."),
    
    ("2025-10-02", "☉ Solar Eclipse — Libra",
     "Collective: Partnerships, balance, justice themes intensified.\nPersonal: Activates your 11th house (friends, networks, collective involvement).\nKeywords: renewal, social shifts, relationship clarity."),
    
    ("2025-10-06", "♂ Mars → Scorpio",
     "Collective: Drive, focus, and intensity sharpen.\nPersonal: Stirs unconscious material, inner drive (12th house themes).\nKeywords: determination, shadow work, persistence."),
    
    ("2025-10-29", "🌑 New Moon — Scorpio",
     "Collective: Deep renewal, power themes.\nPersonal: Resonates with inner psychological growth and healing.\nKeywords: transformation, depth, regeneration."),
    
    ("2025-11-04", "♃ Retrograde Station — Gemini",
     "Collective: Review of growth, learning, and networks.\nPersonal: Opposes your Ascendant — testing partnerships and identity balance.\nKeywords: reevaluation, duality, perspective shift."),
    
    ("2025-11-17", "🌕 Full Moon — Taurus",
     "Collective: Stability vs. change tensions.\nPersonal: Activates your values and resource axis.\nKeywords: grounding, release, security."),
    
    ("2025-11-25", "♆ Neptune Direct — Pisces",
     "Collective: Fog lifts slowly, dreams reorient.\nPersonal: Subtle influence on family/roots sector.\nKeywords: intuition, clarity, spiritual flow."),
    
    ("2025-12-01", "☿ Retrograde Begins — Capricorn",
     "Collective: Career, structure, goals under review.\nPersonal: Revisiting 2nd house matters (finances, possessions, values).\nKeywords: delays, reflection, restructuring."),
    
    ("2025-12-07", "🌕 Full Moon — Gemini",
     "Collective: Information overflow, clarity vs. gossip.\nPersonal: Lights up your 7th house (partnerships).\nKeywords: communication, relationship focus, decision-making."),
    
    ("2025-12-24", "♄ ✧ Uranus Sextile",
     "Collective: Innovation and structure harmonize.\nPersonal: Supports your Moon trine Saturn pattern (stability in friendships and networks).\nKeywords: balance, opportunity, growth."),
    
    ("2025-12-29", "☿ Retrograde Ends — Capricorn",
     "Collective: Clarity in career and structure returns.\nPersonal: Forward movement in finances and values sector.\nKeywords: resolution, progress, regained clarity."),
]

# --- Build ICS ---
ics_lines = [
    "BEGIN:VCALENDAR",
    "VERSION:2.0",
    "PRODID:-//Astrology Calendar//EN",
    "CALSCALE:GREGORIAN",
    "METHOD:PUBLISH"
]

for date_str, title, desc in astrology_events:
    date = datetime.strptime(date_str, "%Y-%m-%d")
    dstart = date.strftime("%Y%m%d")
    dend = (date + timedelta(days=1)).strftime("%Y%m%d")
    uid = f"{uuid.uuid4()}@astrology"
    
    ics_lines += [
        "BEGIN:VEVENT",
        f"DTSTAMP:{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}",
        f"UID:{uid}",
        f"DTSTART;VALUE=DATE:{dstart}",
        f"DTEND;VALUE=DATE:{dend}",
        f"SUMMARY:{title}",
        f"DESCRIPTION:{desc}",
        "TRANSP:TRANSPARENT",
        "END:VEVENT"
    ]

ics_lines.append("END:VCALENDAR")

# --- Save file ---
ics_filename = "calendar/astrology_events.ics"
os.makedirs("calendar", exist_ok=True)

with open(ics_filename, "w") as f:
    f.write("\n".join(ics_lines))

print(f"✅ Wrote {ics_filename}")


