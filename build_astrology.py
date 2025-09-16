import csv
from ics import Calendar, Event
from datetime import datetime

def build_astrology_ics(csv_path="astrology_events.csv", ics_path="astrology_events.ics"):
    cal = Calendar()

    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            event = Event()
            # Title
            event.name = row["title"]

            # Date → all-day
            event.begin = datetime.strptime(row["date"], "%Y-%m-%d")
            event.make_all_day()

            # Description → combine collective, personal, and themes
            desc_parts = []
            if row.get("collective_desc"):
                desc_parts.append("Collective: " + row["collective_desc"])
            if row.get("personal_desc"):
                desc_parts.append("Personal: " + row["personal_desc"])
            if row.get("themes"):
                desc_parts.append("Themes: " + row["themes"])

            event.description = "\n".join(desc_parts)
            cal.events.add(event)

    with open(ics_path, "w", encoding="utf-8") as f:
        f.writelines(cal)

if __name__ == "__main__":
    build_astrology_ics()
