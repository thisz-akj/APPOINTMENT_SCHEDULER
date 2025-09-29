from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from .database import Base

class AppointmentDB(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(String, unique=True, index=True, nullable=False)
    department = Column(String, nullable=False)
    date = Column(String, nullable=False)   # (ISO format)
    time = Column(String, nullable=False)   
    tz = Column(String, default="Asia/Kolkata")
    status = Column(String, default="scheduled")  
    
