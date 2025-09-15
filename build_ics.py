from datetime import datetime, timedelta

def generate_ics():
    # Example: create a calendar with one event
    dtstamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    dtstart = (datetime.utcnow() + timedelta(days=1)).strftime("%Y%m%dT%H%M%SZ")
    dtend = (datetime.utcnow() + timedelta(days=1, hours=1)).strftime("%Y%m%dT%H%M%SZ")

    ics_content = f"""BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//YourApp//ICS Generator//EN
BEGIN:VEVENT
UID:1234@example.com
DTSTAMP:{dtstamp}
DTSTART:{dtstart}
DTEND:{dtend}
SUMMARY:Test Event
END:VEVENT
END:VCALENDAR
"""

    with open("calendar.ics", "w") as f:
        f.write(ics_content)

if __name__ == "__main__":
    generate_ics()
    print("✅ calendar.ics has been created!")
