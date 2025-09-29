import os
from fastapi import FastAPI
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from database.database import Base, engine


load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("Please set GOOGLE_API_KEY in .env file")

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

app = FastAPI(title="Appointment Scheduler API")

# Routers
from modules.ocr_module import router as ocr_router
from modules.entities_module import router as entities_router
from modules.normalize_module import router as normalize_router
from modules.final_appointment_module import router as appointment_router
from modules.text_pipeline_module import router as text_pipeline_router
from modules.image_pipeline_module import router as image_pipeline_router
from modules.scheduler_module import router as scheduler_router


Base.metadata.create_all(bind=engine)

app.include_router(ocr_router, prefix="/step1", tags=["OCR/Text Extraction"])
app.include_router(entities_router, prefix="/step2", tags=["Entity Extraction"])
app.include_router(normalize_router, prefix="/step3", tags=["Normalization"])
app.include_router(appointment_router, prefix="/step4", tags=["Appointment"])
app.include_router(text_pipeline_router, tags=["Text Pipeline"])
app.include_router(image_pipeline_router,  tags=["Image Pipeline"])
app.include_router(scheduler_router, tags=["Scheduler"])



if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
