FROM node:18-alpine

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm install \
    @mui/material \
    @emotion/react \
    @emotion/styled \
    @mui/icons-material \
    @react-oauth/google \
    react-router-dom \
    react-toastify \
    && npm install

# Copy application code
COPY . .

# Ensure public directory exists
RUN mkdir -p /app/public

# Set environment variables
ENV NODE_ENV=development
ENV PORT=3000

# Expose port
EXPOSE 3000

# Start the application
CMD ["npm", "start"]

# Add healthcheck
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD wget -q --spider http://localhost:3000 || exit 1 