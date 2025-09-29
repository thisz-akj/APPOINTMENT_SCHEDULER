#  AI-Powered Appointment Scheduler Assistant  

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
- **Postgress Storage**
  - All scheduled appointments are stored and can be tracked
- **Dockerized Architecture**
  - Backend, Gateway, and Scheduler run as services
  - Ready to deploy with `docker-compose`

---
##APPOINTMENT_SCHEDULER
<img width="324" height="767" alt="image" src="https://github.com/user-attachments/assets/bb1ae742-f10d-43f3-a66b-2fd703154677" />



---

## file to test the AI Scheduler system: https://docs.google.com/document/d/1Qx05CPWy4SKxkQ_MUCQGjEFYj1GBf6X1wIE3LnN4o_0/edit?usp=sharing

## App is live at this server: https://843be965d852.ngrok-free.app
Use that with /{URI}

URIs you can find at: https://843be965d852.ngrok-free.app/docs ----------------->use in postman WITH ### GET/ ###


OR


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

### Then go to localhost/3000  to access API gateway to use APIs

<img width="414" height="89" alt="image" src="https://github.com/user-attachments/assets/24729b36-c50d-4a93-9c3a-9512b7529ae8" />

### Start Celery worker: To check scheduled appointments alarms at scheduled time

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

## POST / extract-image

input: 

{
  "input_text": "multipart/form-data { file: <image> }"
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


## Complete AI Automated SCHEDULER (just use these pipeline APIs to run the whole system)

## For Text input

## POST /Pipeline/text

input:

{ input_text: "Book dentist tomorrow 5pm" }

response:

{
    "appointment": {
    
        "department": "dentist",
        
        "date": "2025-09-30",
        
        "time": "17:00",
        
        "tz": "Asia/Kolkata"
    },
    "status": "ok"
}

## For image input

## POST /Pipeline/text

input:

multipart/form-data { file: <image> }

response:

{
    "appointment": {
    
        "department": "dentist",
        
        "date": "2025-09-30",
        
        "time": "17:00",
        
        "tz": "Asia/Kolkata"
    },
    "status": "ok"
}

## To get details of all the apis and how to use them : GET /docs

## To get list of all the scheduled tasks/appointments: GET/appointments



















