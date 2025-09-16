import csv
from datetime import datetime

def build_astrology_ics(csv_path="data/astrology_events.csv", ics_path="calendar/astrology_events.ics"):
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    lines = []
    lines.append("BEGIN:VCALENDAR")
    lines.append("VERSION:2.0")
    lines.append("PRODID:-//Astrology Events//EN")

    for row in rows:
        date = datetime.strptime(row["date"], "%Y-%m-%d").strftime("%Y%m%d")
        uid = f"{row['title'].replace(' ', '')}-{date}@astro"
        desc_parts = []
        if row.get("collective_desc"):
            desc_parts.append("Collective: " + row["collective_desc"])
        if row.get("personal_desc"):
            desc_parts.append("Personal: " + row["personal_desc"])
        if row.get("themes"):
            desc_parts.append("Themes: " + row["themes"])
        description = "\\n".join(desc_parts)

        lines.append("BEGIN:VEVENT")
        lines.append(f"UID:{uid}")
        lines.append(f"DTSTAMP:{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}")
        lines.append(f"DTSTART;VALUE=DATE:{date}")
        lines.append(f"SUMMARY:{row['title']}")
        lines.append(f"DESCRIPTION:{description}")
        lines.append("END:VEVENT")

    lines.append("END:VCALENDAR")

    with open(ics_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

if __name__ == "__main__":
    build_astrology_ics()
