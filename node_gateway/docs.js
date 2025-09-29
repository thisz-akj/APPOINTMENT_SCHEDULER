import express from "express";

const router = express.Router();

router.get("/docs", (req, res) => {
  res.json({
    service: "Node.js Gateway",
    description:
      "Gateway for AI-powered Appointment Scheduler. Proxies requests to FastAPI backend for OCR, entity extraction, normalization, final appointment creation, and scheduling.",

    routes: [
      {
        category: "Health Check",
        endpoints: [
          {
            method: "GET",
            path: "/",
            description: "Check if the gateway is running",
          },
        ],
      },
      {
        category: "Core Pipeline Steps",
        endpoints: [
          {
            method: "POST",
            path: "/extract-text",
            body: {
                "input_text": "Book dentist tomorrow at 5pm"
              },
            description: "Extract raw text & confidence score",
          },
          {
            method: "POST",
            path: "/extract-image",
            description: "Extract text from uploaded image (OCR)",
            body: "multipart/form-data, field=file",
            example: "curl -X POST http://localhost:3000/extract-image -F 'file=@note.jpg'",
          },
          {
            method: "POST",
            path: "/extract-entities",
            body: {
              raw_text: "Book dentist tomorrow 5pm",
              confidence: 0.9,
            },
            description: "Extract entities like date, time, department",
          },
          {
            method: "POST",
            path: "/normalize-datetime",
            body:{
                "entities": {
                  "date_phrase": "tomorrow",
                  "time_phrase": "5pm",
                  "department": "dentist"
                },
                "entities_confidence": 1
              },
            description: "Normalize phrases to ISO date/time in Asia/Kolkata",
          },
          {
            method: "POST",
            path: "/final-appointment",
            body:{
                "normalized": {
                "normalized": {
                  "date": "2025-09-30",
                  "time": "17:00",
                  "tz": "Asia/Kolkata"
                },
                "normalization_confidence": 0.9
              },
                "entities":{
                "entities": {
                  "date_phrase": "tomorrow",
                  "time_phrase": "5pm",
                  "department": "dentist"
                },
                "entities_confidence": 1
              }
              },
            description: "Combine entities & normalized values into final JSON",
          },
        ],
      },
      {
        category: "Pipelines",
        endpoints: [
          {
            method: "POST",
            path: "/pipeline/text",
            body: { input_text: "Book dentist tomorrow 5pm" },
            description:
              "Runs the full text pipeline (OCR → Entities → Normalize → Final JSON)",
          },
          {
            method: "POST",
            path: "/pipeline/image",
            body: "multipart/form-data { file: <image> }",
            description:
              "Runs the full image pipeline (OCR on image → Entities → Normalize → Final JSON)",
          },
        ],
      },
      {
        category: "Scheduler",
        endpoints: [
          {
            method: "GET",
            path: "/appointments",
            description: "Get all scheduled appointments from Postgres",
          },
          {
            method: "GET",
            path: "/appointments/{task_id}",
            description: "Get details of a single scheduled appointment",
          },
        ],
      },
    ],

    scheduler_logs: {
      explanation:
        "When an appointment is scheduled, it is stored in Postgres and a Celery task is created with ETA (scheduled time).",
      how_to_check: [
        "1. Call POST /pipeline/text or /pipeline/image → this will automatically schedule the task.",
        "2. Verify it is stored → GET /appointments (status will be 'scheduled').",
        "3. When the scheduled time is reached, Celery Worker will trigger it.",
        "4. Check logs: `docker-compose logs -f celery_worker` → you will see '[Scheduler]  Appointment triggered at....at the time you have scheduled the appointment, we can  easily connect it with any notification system on phone to give notifications to users'.",
        
      ],
    },

    notes:
      "All requests should be made to the Gateway (http://localhost:3000). The Gateway internally calls the FastAPI backend.",
  });
});

export default router;
