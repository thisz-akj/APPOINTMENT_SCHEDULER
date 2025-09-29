from celery import Celery
from datetime import datetime
import pytz

celery = Celery(
    "scheduler",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0"
)

@celery.task(name="run_appointment")
def run_appointment(appointment: dict):
    tz = pytz.timezone("Asia/Kolkata")
    now = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S %Z")
    print(f"[Scheduler] 🔔 Appointment triggered at {now}: {appointment}")
    return {"status": "done", "appointment": appointment, "executed_at": now}
