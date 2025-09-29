from datetime import datetime, timedelta
from fastapi import APIRouter, Body
import pytz, re
from dateutil import parser as date_parser
from .models import EntitiesData

router = APIRouter()


TIME_OF_DAY_MAP = {
    "morning": "09:00",
    "afternoon": "13:00",
    "evening": "18:00",
    "night": "21:00",
    "noon": "12:00",
    "midnight": "00:00"
}


CONFIDENCE_THRESHOLD = 0.7

def normalize_date_phrase(date_phrase: str, time_phrase: str, tz_str="Asia/Kolkata"):
    tz = pytz.timezone(tz_str)
    now = datetime.now(tz)
    weekdays = {
        "monday": 0, "tuesday": 1, "wednesday": 2, "thursday": 3,
        "friday": 4, "saturday": 5, "sunday": 6
    }

    date_phrase_clean = date_phrase.lower().strip()
    time_phrase_clean = time_phrase.lower().strip() if time_phrase else ""
    confidence = 1.0
    ambiguous_flag = False

    #Date Parsing 
    try:
        if date_phrase_clean in ["today", "tomorrow"]:
            target_date = now.date() + (timedelta(days=1) if date_phrase_clean=="tomorrow" else timedelta(days=0))
            confidence *= 0.95
        else:
            match_next = re.match(r"next (\w+)", date_phrase_clean)
            match_this = re.match(r"this (\w+)", date_phrase_clean)

            if match_next:
                day_name = match_next.group(1)
                target_weekday = weekdays.get(day_name, None)
                if target_weekday is not None:
                    today_weekday = now.weekday()
                    days_ahead = (target_weekday - today_weekday + 7) % 7
                    days_ahead = days_ahead if days_ahead != 0 else 7
                    target_date = (now + timedelta(days=days_ahead)).date()
                    confidence *= 0.9
                else:
                    target_date = date_parser.parse(date_phrase_clean, default=now).date()
                    confidence *= 0.7
                    ambiguous_flag = True
            elif match_this:
                day_name = match_this.group(1)
                target_weekday = weekdays.get(day_name, None)
                if target_weekday is not None:
                    today_weekday = now.weekday()
                    days_ahead = (target_weekday - today_weekday) % 7
                    target_date = (now + timedelta(days=days_ahead)).date()
                    confidence *= 0.8
                    ambiguous_flag = True
                else:
                    target_date = date_parser.parse(date_phrase_clean, default=now).date()
                    confidence *= 0.6
                    ambiguous_flag = True
            else:
                target_date = date_parser.parse(date_phrase_clean, default=now).date()
                confidence *= 0.95
    except Exception:
        return None  

    # Time Parsing 
    try:
        dt_time = None
        if time_phrase_clean:
            for tod, tod_time in TIME_OF_DAY_MAP.items():
                if tod in time_phrase_clean:
                    h, m = map(int, tod_time.split(":"))
                    dt_time = datetime(now.year, now.month, now.day, h, m).time()
                    confidence *= 0.9
                    break
            if not dt_time:
                dt_time = date_parser.parse(time_phrase_clean).time()
                confidence *= 0.95
        if not dt_time:
            return None  
    except Exception:
        return None  

    if ambiguous_flag:
        confidence *= 0.9

    confidence = max(0.0, min(confidence, 1.0))

    return {
        "date": target_date.strftime("%Y-%m-%d"),
        "time": dt_time.strftime("%H:%M"),
        "tz": tz_str,
        "confidence": round(confidence, 2)
    }

@router.post("/normalize-datetime")
def normalize_datetime(data: EntitiesData = Body(...)):
    entities = data.entities
    if not entities or "date_phrase" not in entities or "time_phrase" not in entities:
        return {"status": "needs_clarification", "message": "Ambiguous date/time or department"}

    normalized = normalize_date_phrase(
        date_phrase=entities.get("date_phrase", ""),
        time_phrase=entities.get("time_phrase", ""),
        tz_str="Asia/Kolkata"
    )

    # 🚨 Guardrail: failed parsing
    if not normalized:
        return {"status": "needs_clarification", "message": "Ambiguous date/time or department"}

    # 🚨 Guardrail: low confidence
    if normalized["confidence"] < CONFIDENCE_THRESHOLD:
        return {"status": "needs_clarification", "message": "Ambiguous date/time or department"}

    return {
        "normalized": {
            "date": normalized["date"],
            "time": normalized["time"],
            "tz": normalized["tz"]
        },
        "normalization_confidence": normalized["confidence"]
    }
