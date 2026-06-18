FROM python:3.11-slim

WORKDIR /app

# Copy frontend files
COPY . .

# Expose port
EXPOSE 5500

# Run HTTP server
CMD ["python", "-m", "http.server", "5500"]
