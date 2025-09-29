import morgan from "morgan";

export const requestLogger = morgan("dev");

export const poweredByHeader = (req, res, next) => {
  res.setHeader("X-Powered-By", "Node-Gateway");
  next();
};

// Centralized error handler
export const errorHandler = (err, req, res, next) => {
  console.error("Error:", err.message);

  res.status(err.response?.status || 500).json({
    error: err.response?.data || "Internal server error",
  });
};
