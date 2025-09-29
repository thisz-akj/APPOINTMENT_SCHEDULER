from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime
import pytz
from celery_app import run_appointment
# scheduler_module.py
from tasks import schedule_appointment  # instead of run_appointment

# importing db dependencies
from sqlalchemy.orm import Session
from database.database import SessionLocal
from database import crud

router = APIRouter()

#Getting DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/scheduler/schedule")
async def schedule_task(payload: dict):
    appointment = payload.get("appointment")
    if not appointment:
        raise HTTPException(status_code=400, detail="Missing appointment data")

    tz = pytz.timezone("Asia/Kolkata")
    run_time = tz.localize(datetime.strptime(
        f"{appointment['date']} {appointment['time']}", "%Y-%m-%d %H:%M"
    ))

    print(f"[Scheduler] Appointment scheduled for {run_time.strftime('%Y-%m-%d %H:%M:%S %Z')}")

   
    task = run_appointment.apply_async(args=[appointment], eta=run_time)

   
    db = next(get_db())
    crud.create_appointment(db, task.id, appointment, run_time)
    db.close()

    return {
        "task_id": task.id,
        "status": "scheduled",
        "run_at": run_time.isoformat()
    }

@router.get("/appointments")
def get_appointments(db: Session = Depends(get_db)):
    tasks = crud.get_all_appointments(db)
    return tasks

@router.get("/appointments/{task_id}")
def get_appointment(task_id: str, db: Session = Depends(get_db)):
    task = crud.get_appointment(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return task