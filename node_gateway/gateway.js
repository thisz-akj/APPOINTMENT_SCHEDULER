import express from "express";
import morgan from "morgan";
import axios from "axios";
import multer from "multer"; 
import FormData from "form-data";
import dotenv from "dotenv";
import docsRoutes from "./docs.js";
import appointmentRoutes from "./appointments.js";
import { requestLogger, poweredByHeader, errorHandler } from "./middlewares.js";

const app = express();
const PORT = process.env.PORT || 3000;
const PYTHON_API_BASE = process.env.PYTHON_API_BASE || "http://backend:8000";


// Middleware
app.use(requestLogger);
app.use(express.json());
app.use(poweredByHeader);

// Multer for file uploads
const upload = multer();

// Health check
app.get("/health", async (req, res) => {
  try {
    const backendHealth = await axios.get(`${PYTHON_API_BASE}`);
    res.json({
      status: "ok",
      service: "Node.js Gateway is running",
      backend: backendHealth.data,
    });
  } catch {
    res.status(500).json({
      status: "error",
      service: "Node.js Gateway running, but backend not reachable",
    });
  }
});

// proxy


app.post("/extract-text", async (req, res) => {
  try {
    const response = await axios.post(`${PYTHON_API_BASE}/step1/extract-text`, req.body);
    res.json(response.data);
  } catch (err) {
    console.error("extract-text error:", err.message);
    res.status(err.response?.status || 500).json({ error: err.response?.data || "extract-text request failed" });
  }
});


app.post("/extract-image", upload.single("file"), async (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).json({ error: "No file uploaded" });
    }

    const formData = new FormData();
    formData.append("file", req.file.buffer, req.file.originalname);

    const response = await axios.post(
      `${PYTHON_API_BASE}/step1/extract-text-from-image`, // 👈 match backend
      formData,
      {
        headers: { ...formData.getHeaders() },
        maxBodyLength: Infinity,
      }
    );

    res.json(response.data);
  } catch (err) {
    console.error("extract-image error:", err.message);
    res.status(err.response?.status || 500).json({
      error: err.response?.data || "extract-image failed",
    });
  }
});


app.post("/extract-entities", async (req, res) => {
  try {
    const response = await axios.post(`${PYTHON_API_BASE}/step2/extract-entities`, req.body);
    res.json(response.data);
  } catch (err) {
    console.error("extract-entities error:", err.message);
    res.status(err.response?.status || 500).json({ error: err.response?.data || "extract-entities request failed" });
  }
});


app.post("/normalize-datetime", async (req, res) => {
  try {
    const response = await axios.post(`${PYTHON_API_BASE}/step3/normalize-datetime`, req.body);
    res.json(response.data);
  } catch (err) {
    console.error("normalize-datetime error:", err.message);
    res.status(err.response?.status || 500).json({ error: err.response?.data || "normalize-datetime request failed" });
  }
});


app.post("/final-appointment", async (req, res) => {
  try {
    const response = await axios.post(`${PYTHON_API_BASE}/step4/final-appointment`, req.body);
    res.json(response.data);
  } catch (err) {
    console.error("final-appointment error:", err.message);
    res.status(err.response?.status || 500).json({ error: err.response?.data || "final-appointment request failed" });
  }
});


app.post("/pipeline/text", async (req, res) => {
  try {
    // Ensure FastAPI always receives JSON with correct field
    const input = req.body.input_text
      ? req.body
      : { input_text: req.body.text || req.body.query || "" };

    console.log(
      "Forwarding to backend:",
      `${PYTHON_API_BASE}/pipeline/text`,
      "with body:",
      input
    );

    
    const response = await axios.post(
      `${PYTHON_API_BASE}/pipeline/text`,
      input,
      { headers: { "Content-Type": "application/json" } }
    );

   
    await axios.post(`${PYTHON_API_BASE}/scheduler/schedule`, response.data);

  
    res.json(response.data);
  } catch (err) {
    console.error(
      "pipeline/text error:",
      err.response?.status,
      err.response?.data || err.message
    );
    res.status(err.response?.status || 500).json({
      error: err.response?.data || "pipeline/text failed",
    });
  }
});

app.post("/pipeline/image", upload.single("file"), async (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).json({ error: "No file uploaded" });
    }

    const formData = new FormData();
    formData.append("file", req.file.buffer, req.file.originalname);

    
    const response = await axios.post(
      `${PYTHON_API_BASE}/pipeline/image`,
      formData,
      {
        headers: { ...formData.getHeaders() },
        maxBodyLength: Infinity,
      }
    );

    
    await axios.post(`${PYTHON_API_BASE}/scheduler/schedule`, response.data);

    
    res.json(response.data);
  } catch (err) {
    console.error(
      "pipeline/image error:",
      err.response?.status,
      err.response?.data || err.message
    );
    res.status(err.response?.status || 500).json({
      error: err.response?.data || "pipeline/image failed",
    });
  }
});

app.use(docsRoutes);
app.use(appointmentRoutes);

  // Start server
  app.listen(PORT, () => {
    console.log(`Node.js Gateway running at http://localhost:${PORT}`);
  });