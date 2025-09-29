from sqlalchemy.orm import Session
from .models import AppointmentDB

def create_appointment(db: Session, task_id: str, appointment: dict, scheduled_for):
    new_task = AppointmentDB(
        task_id=task_id,
        department=appointment["department"],
        date=appointment["date"],
        time=appointment["time"],
        tz=appointment.get("tz", "Asia/Kolkata"),
        status="scheduled"
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

def update_status(db: Session, task_id: str, status: str):
    task = db.query(AppointmentDB).filter(AppointmentDB.task_id == task_id).first()
    if task:
        task.status = status
        db.commit()
        db.refresh(task)
    return task

def get_all_appointments(db: Session):
    return db.query(AppointmentDB).all()

def get_appointment(db: Session, task_id: str):
    return db.query(AppointmentDB).filter(AppointmentDB.task_id == task_id).first()
