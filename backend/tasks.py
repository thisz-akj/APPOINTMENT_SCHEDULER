from celery_app import celery
from datetime import datetime
import pytz

@celery.task(name="tasks.schedule_appointment")
def schedule_appointment(department: str, date: str, time: str, tz: str):
    try:
        tzinfo = pytz.timezone(tz)
        dt = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
        localized = tzinfo.localize(dt)

        print(f"Scheduled: {department} at {localized}")

        return {
            "appointment": {
                "department": department,
                "date": date,
                "time": time,
                "tz": tz,
            },
            "status": "ok",
        }
    except Exception as e:
        return {"status": "error", "detail": str(e)}
