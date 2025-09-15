from datetime import datetime, timedelta
import uuid

# Configurations
start_date = datetime(2025, 9, 14)
end_date = datetime(2025, 12, 31)

def get_risk(date):
    # Shot cycle: assume Friday shots, DSS=2 on Sundays
    dss = (date.weekday() - 4) % 7  # 0 = Friday shot
    is_dss2 = (dss == 2)

    # Period windows: Aug 19 start, alternating 28/29 days
    period_starts = [datetime(2025, 8, 19)]
    toggle = 28
    while period_starts[-1] < end_date:
        nxt = period_starts[-1] + timedelta(days=toggle)
        period_starts.append(nxt)
        toggle = 29 if toggle == 28 else 28

    period_days = set()
    for ps in period_starts:
        for off in (0, 1):  # 2-day period window
            period_days.add((ps + timedelta(days=off)).date())
    is_period = date.date() in period_days

    # Moon phases (simplified)
    full_moons = [datetime(2025, 9, 17), datetime(2025, 10, 6)]
    new_moons = [datetime(2025, 9, 21), datetime(2025, 10, 29)]
    is_moon = any(abs((date - m).days) <= 3 for m in full_moons + new_moons)

    # Storm forecasts
    g1_storms = [datetime(2025, 9, 15), datetime(2025, 9, 16)]
    active_storms = [
        datetime(2025, 9, 17), datetime(2025, 9, 18),
        datetime(2025, 9, 28), datetime(2025, 9, 29),
        datetime(2025, 10, 3), datetime(2025, 10, 4)
    ]
    is_g1 = date.date() in [d.date() for d in g1_storms]
    is_active = date.date() in [d.date() for d in active_storms]

    # Scoring
    score = 0
    if is_dss2: score += 2
    if is_g1: score += 2
    if is_active: score += 1
    if is_moon: score += 1
    if is_period: score += 2

    return score, is_dss2, is_g1, is_active, is_moon, is_period

def risk_category(score):
    if score >= 5: return ("🔥 High risk (stacked)", 4)
    if score >= 3: return ("⚠️ Moderate risk", 3)
    if score >= 1: return ("➖ Mild risk", 2)
    return ("✅ Low risk", 1)

# Build ICS
ics_lines = [
    "BEGIN:VCALENDAR",
    "VERSION:2.0",
    "PRODID:-//NG Risk Calendar//EN",
    "CALSCALE:GREGORIAN",
    "METHOD:PUBLISH"
]

current = start_date
while current <= end_date:
    score, is_dss2, is_g1, is_active, is_moon, is_period = get_risk(current)
    if score > 0:
        cat, level = risk_category(score)
        emoji = cat.split()[0]  # Extract just the symbol
        summary = f"{emoji} Risk Level: {level}"

        desc_parts = [
            f"Risk Score → {score} ({cat})",
            f"Geomagnetic Activity → {'G1 storm' if is_g1 else ('Active/Unsettled' if is_active else 'No')}",
            f"Period Forecasted → {'Yes' if is_period else 'No'}",
            f"Moon Phase → {'Near Full/New' if is_moon else 'Neutral'}",
            f"Shot Cycle → {'DSS=2' if is_dss2 else 'none'}",
        ]

        symptoms = []
        if is_dss2: symptoms += ["fatigue", "low mana", "irritability"]
        if is_g1: symptoms += ["anxious", "stressed", "sleep disruption", "low mana"]
        if is_active: symptoms += ["restless", "anxious", "low mana"]
        if is_moon: symptoms += ["energy volatility", "low mana"]
        if is_period: symptoms += ["low mana", "cramps", "emotional sensitivity"]

        desc_parts.append(
            "Likely Symptoms → " + ", ".join(sorted(set(symptoms)))
            if symptoms else "Likely Symptoms → (unspecified)"
        )

        desc = "\\n".join(desc_parts)
        uid = f"{uuid.uuid4()}@ng-risk"
        dstart = current.strftime("%Y%m%d")
        dend = (current + timedelta(days=1)).strftime("%Y%m%d")

        ics_lines += [
            "BEGIN:VEVENT",
            f"DTSTAMP:{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}",
            f"UID:{uid}",
            f"DTSTART;VALUE=DATE:{dstart}",
            f"DTEND;VALUE=DATE:{dend}",
            f"SUMMARY:{summary}",
            f"DESCRIPTION:{desc}",
            "TRANSP:TRANSPARENT",
            "END:VEVENT"
        ]
    current += timedelta(days=1)

ics_lines.append("END:VCALENDAR")

# Write file
ics_filename = "ng_risk_calendar_FIXED_SepDec2025.ics.txt"
with open(ics_filename, "w") as f:
    f.write("\n".join(ics_lines))

print(f"✅ Wrote {ics_filename}")
