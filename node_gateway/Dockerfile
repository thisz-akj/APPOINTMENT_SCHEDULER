FROM node:18-slim

WORKDIR /app

# Copy package files first (better caching)
COPY node_gateway/package*.json ./

# Install dependencies
RUN npm install

# Copy source code
COPY node_gateway/ .

# Expose gateway port
EXPOSE 3000

# Use nodemon in dev mode (hot reload)
CMD ["npm", "run", "dev"]
