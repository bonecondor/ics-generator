from datetime import datetime
import uuid
import os

# --- Astrology events Sept–Dec 2025 (collective + personal) ---
astrology_events = [
    # Collective
    ("2025-09-21", "🌑 New Moon in Virgo", "Practical resets, health/service themes."),
    ("2025-09-29", "🌕 Lunar Eclipse in Aries", "Heightened energy, confrontations, release cycles."),
    ("2025-10-02", "☉ Solar Eclipse in Libra", "Partnerships, balance, and justice themes intensified."),
    ("2025-10-06", "♂ Mars enters Scorpio", "Drive, focus, intensity sharpen."),
    ("2025-10-29", "🌑 New Moon in Scorpio", "Deep renewal, power themes."),
    ("2025-11-04", "♃ Jupiter stations retrograde in Gemini", "Review of growth, learning, and networks."),
    ("2025-11-17", "🌕 Full Moon in Taurus", "Stability vs. change."),
    ("2025-11-25", "♆ Neptune stations direct in Pisces", "Fog lifts, dreams reorient."),
    ("2025-12-01", "☿ Mercury retrograde in Capricorn begins", "Review of career, structure, goals."),
    ("2025-12-07", "🌕 Full Moon in Gemini", "Information overflow, clarity vs. gossip."),
    ("2025-12-24", "♄ Saturn sextile Uranus", "Innovation and structure harmonize."),
    ("2025-12-29", "☿ Mercury retrograde ends", "Clarity in career matters returns."),
    
    # Personalized (based on your chart)
    ("2025-09-17", "🌕 Lunar Eclipse in Aries hits Libra Moon", "Themes of relationship, belonging, collective awareness."),
    ("2025-10-02", "☉ Solar Eclipse in Libra activates 11th house", "Friendships, networks, collective involvement activated."),
    ("2025-11-04", "♃ Jupiter retrograde opposes Ascendant", "Partnerships and growth themes tested."),
    ("2025-12-07", "🌕 Full Moon in Gemini lights up 7th house", "Relationships and partnerships emphasized."),
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
    dend = (date.replace(hour=
