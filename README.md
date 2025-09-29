# 🗓️ AI-Powered Appointment Scheduler Assistant  

# 🗓️ Appointment Scheduler – Backend + Node Gateway

This project is an **AI-powered Appointment Scheduling System** that combines a **FastAPI backend** (Python) with a **Node.js Gateway**. It leverages **Google Gemini LLM** (via LangChain) to process natural language input, extract key appointment details, normalize them, and finally **schedule appointments**.  

The system can parse user input like:  
> "Schedule my dermatology appointment next Monday at 5 PM"  

and produce a structured **appointment JSON**, then schedule it in the backend via Celery workers.

---

## ✨ Features
- **Natural Language Understanding**
  - Extracts clean text from user queries
  - Identifies entities like date, time, and department
- **Normalization**
  - Converts relative expressions ("tomorrow", "next Monday") into structured ISO date/time
- **Appointment Scheduling**
  - Stores and schedules final appointments using Celery
  - Supports async task execution
- **Node.js Gateway**
  - Single unified entry point for client requests
  - API documentation via Swagger
- **Dockerized Architecture**
  - Backend, Gateway, and Scheduler run as services
  - Ready to deploy with `docker-compose`

---
##APPOINTMENT_SCHEDULER
│
├── backend/
│ ├── modules/
│ │ ├── entities_module.py
│ │ ├── final_appointment_module.py
│ │ ├── image_pipeline_module.py
│ │ ├── models.py
│ │ ├── normalize_module.py
│ │ ├── ocr_module.py
│ │ ├── scheduler_module.py # Scheduling logic
│ │ ├── text_pipeline_module.py
│ │ └── init.py
│ ├── database/
│ ├── main.py # FastAPI entry point
│ ├── celery_app.py # Celery configuration
│ ├── tasks.py # Scheduling tasks
│ ├── utils.py
│ ├── requirements.txt
│ └── Dockerfile
│
├── node_gateway/
│ ├── gateway.js
│ ├── appointments.js
│ ├── docs.js
│ ├── middlewares.js
│ ├── package.json
│ ├── package-lock.json
│ ├── Dockerfile
│ └── .env
│
├── docker-compose.yml
├── .gitignore
├── .env



---

## ⚙️ Setup Instructions

### 1. Clone the Repository

git clone https://github.com/thisz-akj/APPOINTMENT_SCHEDULER.git
cd APPOINTMENT_SCHEDULER


### Configure Environment Variables

GOOGLE_API_KEY=your_google_api_key_here (in Root .env)

(In node_gateway/.env)
PORT=3000
BACKEND_URL=http://backend:8000

### Run with Docker Compose

docker-compose up --build

<img width="414" height="89" alt="image" src="https://github.com/user-attachments/assets/24729b36-c50d-4a93-9c3a-9512b7529ae8" />

Start Celery worker:

celery -A celery_app worker --loglevel=info


# API Endpoints

Pipeline Endpoint (extract → normalize → schedule)

## POST / extract-text
input: 
{
  "input_text": "Schedule my appointment with dermatology next Monday at 5 PM"
}

response:
{
  "raw_text": "Schedule my appointment with dermatology next Monday at 5pm",
  "confidence": 1
}

## Post / extract-entities
input:
{
  "raw_text": "Schedule my appointment with dermatology next Monday at 5pm",
  "confidence": 1
}

response:
{
  "entities": {
    "date_phrase": "next Monday",
    "time_phrase": "5pm",
    "department": "dermatology"
  },
  "entities_confidence": 1
}

## POST /normalize-datetime
input:
{
  "entities": {
    "date_phrase": "next Monday",
    "time_phrase": "5pm",
    "department": "dermatology"
  },
  "entities_confidence": 1
}

response:
{
  "normalized": {
    "date": "2025-10-06",
    "time": "17:00",
    "tz": "Asia/Kolkata"
  },
  "normalization_confidence": 0.85
}

## POST /final-appointment
input:
{
  "normalized":{
  "normalized": {
    "date": "2025-10-06",
    "time": "17:00",
    "tz": "Asia/Kolkata"
  },
  "normalization_confidence": 0.85
},
  "entities":{
  "entities": {
    "date_phrase": "next Monday",
    "time_phrase": "5pm",
    "department": "dermatology"
  },
  "entities_confidence": 1
}
}

response:
{
  "appointment": {
    "department": "dermatology",
    "date": "2025-10-06",
    "time": "17:00",
    "tz": "Asia/Kolkata"
  },
  "status": "ok"
  }
















