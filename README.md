# 🗓️ AI-Powered Appointment Scheduler Assistant  

> End-to-end backend system for scheduling appointments from **text or image inputs** using **FastAPI + Node.js Gateway + LangChain + Gemini + OCR + Celery + Redis + PostgreSQL**.  

---

## 📌 Features  

- Handles both **typed text** and **noisy image inputs** (scanned notes, hand-written notes, emails).  
- Pipeline: **OCR → Entity Extraction → Normalization → Final Structured Appointment JSON**.  
- Guardrails for ambiguity (asks clarification when confidence is low).  
- Schedules tasks using **Celery + Redis**.  
- Stores all scheduled tasks in **PostgreSQL** (with status updates).  
- **Node.js Gateway** to manage routing, logging, and file uploads.  
- Ready for **cloud deployment** (tested on Google Cloud VM with Docker).  

---

## ⚙️ Tech Stack  

- **Backend API**: FastAPI (Python)  
- **LLM**: Google Gemini via LangChain  
- **OCR**: EasyOCR + LLM corrections  
- **Scheduling**: Celery + Redis  
- **Database**: PostgreSQL (task persistence)  
- **Gateway**: Node.js (Express, Multer, Axios, Morgan)  
- **Containerization**: Docker & Docker Compose  

---

## Environment Setup

###backend/.env

GOOGLE_API_KEY=your_gemini_api_key
DATABASE_URL=postgresql+psycopg2://postgres:postgres@postgres:5432/appointments


###Node.js Gateway

PORT=3000
PYTHON_API_BASE=http://backend:8000

docker compose up --build

<img width="394" height="73" alt="image" src="https://github.com/user-attachments/assets/94f60ba7-6940-4ad5-9a98-8f6aed691566" />

## API EndPoints


<img width="250" height="122" alt="image" src="https://github.com/user-attachments/assets/a2c02383-7171-40d1-8bc7-e0290a9ad3b9" />



input: <img width="420" height="188" alt="image" src="https://github.com/user-attachments/assets/d93a9e4b-d51f-4248-ad2c-8e4b349d2a96" />

output: <img width="408" height="152" alt="image" src="https://github.com/user-attachments/assets/3bb7a5c5-4054-46f0-a281-75f907dadb70" />


input: <img width="445" height="179" alt="image" src="https://github.com/user-attachments/assets/c3a225b5-9fea-48ca-a22f-22ea8a9c33f4" />

output: <img width="413" height="156" alt="image" src="https://github.com/user-attachments/assets/db16b100-1773-4124-9316-45a1653525a4" />



input: <img width="400" height="227" alt="image" src="https://github.com/user-attachments/assets/d1075964-9603-47ca-ade5-deea4069bd87" />


output: <img width="324" height="257" alt="image" src="https://github.com/user-attachments/assets/ef544baf-1ee1-4780-9271-111f59d01c20" />



input: <img width="426" height="328" alt="image" src="https://github.com/user-attachments/assets/33e0d668-2827-46c9-8c96-b37b97976ca3" />


output: <img width="452" height="464" alt="image" src="https://github.com/user-attachments/assets/dcdedebe-00e0-4959-973f-4d855cc8ad8a" />


input:<img width="450" height="421" alt="image" src="https://github.com/user-attachments/assets/43637bc3-0255-4193-8dba-efbae1958921" />

output: <img width="283" height="268" alt="image" src="https://github.com/user-attachments/assets/dffb3a7b-8b1b-4707-8596-78d203e1e4d4" />


input: <img width="460" height="198" alt="image" src="https://github.com/user-attachments/assets/0247d905-6949-4d9b-baf3-28071f9b652c" />

output: <img width="368" height="278" alt="image" src="https://github.com/user-attachments/assets/89f02471-f63a-436d-8fc6-4d74b868fdf3" />


image: <img width="319" height="172" alt="image" src="https://github.com/user-attachments/assets/7f5ec384-ca44-4920-9cf8-30a4171ddbec" />


output: -<img width="270" height="269" alt="image" src="https://github.com/user-attachments/assets/e6c8e2f5-f06a-4d2e-a7eb-5589f3cebdba" />


input: <img width="358" height="308" alt="image" src="https://github.com/user-attachments/assets/0b15257f-d383-4c9c-b092-cc95525a993f" />


output: <img width="432" height="167" alt="image" src="https://github.com/user-attachments/assets/da6eedf5-c53d-4b72-935a-56d7fff6d96f" />


<img width="300" height="137" alt="image" src="https://github.com/user-attachments/assets/483a0830-410b-4e82-8c74-aae1e1d80877" />

## Vewing Scheduled Logs:

###When Scheduled: [Scheduler] Appointment scheduled for 2025-09-29 23:06:00 IST
###When triggered: [Scheduler] Appointment triggered at 2025-09-29 23:06:00 IST: {department: "teacher", ...}














