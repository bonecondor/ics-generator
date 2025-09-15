from datetime import datetime, timedelta
import csv
import os
import uuid

CSV_PATH = "data/astrology_events.csv"
OUTPUT_PATH = "calendar/astrology_events.ics"

def load_events(csv_path):
    events = []
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(
            (line for line in f if line.strip() and not line.strip().startswith("#"))
        )
        for row in reader:
            # Basic validation
            try:
                date_obj = datetime.strptime(row["date"].strip(), "%Y-%m-%d")
            except Exception as e:
                print(f"Skipping row with bad date: {row} ({e})")
                continue

            title = (row.get("title", "") or "").strip()
            cdesc = (row.get("collective_desc", "") or "").strip()
            pdesc = (row.get("personal_desc", "") or "").strip()

            # Build description with both layers
            lines = []
            if cdesc:
                lines.append(f"Collective: {cdesc}")
            if pdesc:
                lines.append(f"Personal: {pdesc}")
            desc = "\\n".join(lines) if lines else " "

            events.append({
                "date": date_obj,
                "title": title,
                "desc": desc
            })

    # Sort by date just in case
    events.sort(key=lambda e: e["date"])
    return events

def build_ics(events):
    ics_lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//Astrology Calendar//EN",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
        "X-PUBLISHED-TTL:PT1H",
        "REFRESH-INTERVAL;VALUE=DURATION:PT1H",
    ]

    for ev in events:
        dstart = ev["date"].strftime("%Y%m%d")
        dend = (ev["date"] + timedelta(days=1)).strftime("%Y%m%d")
        uid = f"{uuid.uuid4()}@astrology"

        title = ev["title"]
        desc = ev["desc"]

        # Inject highlight legend for ✨ (collective) or ⭐ (personal)
        legend_line = ""
        if title.lstrip().startswith("✨"):
            legend_line = "Highlight: Collective (✨) — everyone feels this"
        elif title.lstrip().startswith("⭐"):
            legend_line = "Highlight: Personal (⭐) — this directly hits your chart"

        if legend_line:
            # Prepend the legend line above the existing description
            desc = f"{legend_line}\\n{desc}"

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
    return "\n".join(ics_lines)

def main():
    events = load_events(CSV_PATH)
    if not events:
        print("No events loaded from CSV.")
        return
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(build_ics(events))
    print(f"✅ Wrote {OUTPUT_PATH} with {len(events)} events")

if __name__ == "__main__":
    main()
