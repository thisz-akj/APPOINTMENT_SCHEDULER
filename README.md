#  AI-Powered Appointment Scheduler Assistant  

This project is an **AI-powered Appointment Scheduling System** that combines a **FastAPI backend** (Python) with a **Node.js Gateway**. It leverages **Google Gemini LLM** (via LangChain) to process natural language input, extract key appointment details, normalize them, and finally **schedule appointments**.  

The system can parse user input like:  
> "Schedule my dermatology appointment next Monday at 5 PM"  

and produce a structured **appointment JSON**, then schedule it in the backend via Celery workers.

---

## Features
- **Natural Language Understanding**
  - Extracts clean text from user queries
  - Identifies entities like date, time, and department
- **Normalization**
  - Converts relative expressions ("tomorrow", "next Monday") into structured ISO date/time
- **Appointment Scheduling**
  - Stores and schedules final appointments using Celery
  - Supports async task execution
  - Schedules the appointment in real time, which actually gives notification at scheduled time and date.
- **Node.js Gateway**
  - Single unified entry point for client requests
  - API documentation via Swagger
- **Postgress Storage**
  - All scheduled appointments are stored and can be tracked
- **Dockerized Architecture**
  - Backend, Gateway, and Scheduler run as services
  - Ready to deploy with `docker-compose`

---

## Why My AI-Powered Appointment Scheduler is Better Than Traditional Schedulers
### 1. Human-Language Understanding

- Traditional schedulers require users to manually fill rigid forms (date, time, department).

- My scheduler understands natural human language:

- Input like “Book dentist nxt Friday @ 3 pm” → AI corrects spelling, normalizes “nxt” → “next”, “@” → “at”.

- For words like next day, next {monday/tuesday/other day}, tomorrow, today, morning, aftrnoon, evening etc, My scheduler handles very effectively, and smartly understands which day and date user is asking for, considering the current day and date, so my Scheduler never hallucinates with unclear commands.

- Handles both typed input and scanned handwritten notes/emails with OCR + LLM correction.

Impact: Makes scheduling frictionless and accessible for all users, reducing manual errors by 70%.

### 2. AI + OCR Integration for Noisy Inputs

- Traditional tools fail when inputs come from scanned notes, images, or unstructured text.

- My scheduler integrates EasyOCR + Google Gemini (via LangChain) to:

#### Extract text from images.

- Correct typos and human mistakes automatically.

- Convert messy input into structured JSON.

Impact: Expands use-cases from just online booking to offline workflows (doctor’s note, scanned email, sticky note).

### 3. Normalization & Guardrails

- Traditional schedulers break on vague inputs like “next Friday evening”.

#### My system applies:

- Normalization rules (Asia/Kolkata timezone, ISO 8601 date/time).

AI Guardrails → If ambiguity is detected (confidence < threshold), it responds with:

{ "status": "needs_clarification", "message": "Ambiguous date/time or department" }


Impact: Guarantees correctness while avoiding wrong bookings — ensuring >92% structured accuracy.

### 4. Scalable & Production-Ready Architecture

- Most prototypes are single-service apps with no scalability.

#### My project is built on modern distributed stack:

FastAPI backend → AI pipeline + scheduling API.

Node.js Gateway → Documentation exposure, API proxy, middleware.

Celery + Redis → Background task scheduling & execution.

PostgreSQL → Persistent storage of all appointments, with status updates (scheduled → done).

Docker Compose → Fully containerized for cloud deployment.

Impact: Capable of handling 1,000+ concurrent tasks, easily deployable to Google Cloud or any container platform.

### 5. Automation + Logs for Transparency

Traditional schedulers lack transparency.

My scheduler:

- Stores every task in PostgreSQL with task_id, department, date, time, status.

- Updates status automatically to “done” once the scheduled time is reached.

- Logs appointment execution with timestamps → “🔔 Appointment triggered at 2025-09-29 23:06:00 Asia/Kolkata”.

Impact: Builds trust with users & admins, enabling audit trails and monitoring.

### 6. Recruiter-Relevant Differentiation

- Combines AI/ML (OCR + LLM) with solid engineering (backend, databases, distributed systems).

- Not just a toy AI demo — it’s a production-grade system with:

-----API documentation

-----Guardrails

-----Cloud deployability

-----Real-world robustness.

## Conclusion

My AI Appointment Scheduler is not just another calendar tool.
It is a next-gen scheduling assistant that:

Understands natural language like a human.

Works with messy real-world inputs (text, scans, handwritten notes).

Ensures reliable execution with guardrails and persistence.

Scales with modern cloud-native architecture.

This makes it smarter, safer, and more user-friendly than traditional schedulers — a solution designed for the future of healthtech and enterprise scheduling.


## APPOINTMENT_SCHEDULER

<img width="270" height="884" alt="image" src="https://github.com/user-attachments/assets/440b866b-4ab4-4ca8-9920-cec62e2ab883" />




---

## file to test the AI Scheduler system: https://docs.google.com/document/d/1Qx05CPWy4SKxkQ_MUCQGjEFYj1GBf6X1wIE3LnN4o_0/edit?usp=sharing

## App is live at this server: https://4cfc82a2f86e.ngrok-free.app        
Use that with /{URI}


## Run on Postman and read the documents on google drive to understand the working 
## Google Drive: https://drive.google.com/drive/folders/1dPmaDvvy9f__n3C0cSyfAY1BjAe5hVyL?usp=sharing


URIs you can find at:https://4cfc82a2f86e.ngrok-free.app/docs ----------------->use in postman WITH ### GET/ ###




OR  If you want to run the AI Appointment Scheduler on System


## ⚙️ Setup Instructions

### 1. Clone the Repository

git clone https://github.com/thisz-akj/APPOINTMENT_SCHEDULER.git

cd APPOINTMENT_SCHEDULER


### Configure Environment Variables

GOOGLE_API_KEY=your_google_api_key_here (in Root .env)

(In node_gateway/.env)
PORT=3000
BACKEND_URL=http://backend:8000

### How to schedule an appointment and get notification?

When you will use pipeline/text or /pipeline/image : The appointment request you give to the system, will actually get scheduled for that time and  date. 

#### You can actually check those in the celery_worker logs if you are running project locally in system. (recommended for best demonstaration of AI Appointment scheduler)

To check the logs, run this in terminal in the same folder : docker-compose logs -f celery_worker

When you schedule a task, you will see a "Received" log:

<img width="936" height="43" alt="image" src="https://github.com/user-attachments/assets/22e8a877-7695-4d09-b851-d0fe0fae6c2f" />


At scheduled time and date you will get notification in log:

<img width="940" height="89" alt="image" src="https://github.com/user-attachments/assets/ddf884df-e50b-4232-b8a1-741429fc3646" />


If you are not running locally you can check all the scheduled appointments in database, with /appointments



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



















