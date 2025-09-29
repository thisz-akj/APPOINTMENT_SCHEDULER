import express from "express";
import axios from "axios";

const router = express.Router();
const PYTHON_API_BASE = process.env.PYTHON_API_BASE || "http://backend:8000";

router.get("/appointments", async (req, res, next) => {
  try {
    const response = await axios.get(`${PYTHON_API_BASE}/appointments`);
    res.json(response.data);
  } catch (err) {
    console.error("appointments error:", err.message);
    res.status(err.response?.status || 500).json({
      error: err.response?.data || "appointments request failed",
    });
  }
});

export default router;
