# TaskBoard Lite - Getting Started Guide

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Starting Without Docker](#starting-without-docker)
3. [Starting With Docker](#starting-with-docker)
4. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### System Requirements
- Windows 10/11, macOS, or Linux
- At least 2GB RAM
- Internet connection (for initial setup)

---

## Starting Without Docker

### Option 1: Manual Setup (Recommended for Development)

#### Step 1: Open Terminal/Command Prompt
```bash
cd path/to/taskboard-lite
```

#### Step 2: Backend Setup

##### 2.1 Navigate to Backend Directory
```bash
cd backend
```

##### 2.2 Create Virtual Environment
**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

##### 2.3 Install Dependencies
```bash
pip install -r requirements.txt
```

##### 2.4 Start Backend Server
```bash
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

You should see output like:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

The API will be available at:
- **API Base URL:** `http://127.0.0.1:8000`
- **Swagger Docs:** `http://127.0.0.1:8000/docs`
- **ReDoc Docs:** `http://127.0.0.1:8000/redoc`

#### Step 3: Frontend Setup

##### 3.1 Open New Terminal/Command Prompt (keep backend running)
```bash
cd path/to/taskboard-lite/frontend
```

##### 3.2 Start Local Server
**Option A: Using Python HTTP Server**
```bash
python -m http.server 3000
```

**Option B: Using Node.js http-server (if installed)**
```bash
npx http-server -p 3000
```

**Option C: Using VS Code Live Server (Recommended)**
- Right-click on `index.html` in VS Code
- Select "Open with Live Server"
- Default URL: `http://127.0.0.1:5500/frontend/`

##### 3.3 Access Application
Open your browser and go to:
```
http://127.0.0.1:5500/frontend/
```
(or the port shown by your server)

---

## Starting With Docker

### Prerequisites for Docker
- Docker installed ([Download here](https://www.docker.com/products/docker-desktop))
- Docker daemon running

### Option 1: Docker Compose (Easiest)

#### Step 1: Create docker-compose.yml

Create a file named `docker-compose.yml` in the project root:

```yaml
version: '3.8'

services:
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=sqlite:///./taskboard.db
    volumes:
      - ./backend:/app
    command: python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
    networks:
      - taskboard

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "5500:5500"
    depends_on:
      - backend
    networks:
      - taskboard

networks:
  taskboard:
    driver: bridge
```

#### Step 2: Create Backend Dockerfile

Create `backend/Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```

#### Step 3: Create Frontend Dockerfile

Create `frontend/Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY . .

EXPOSE 5500

CMD ["python", "-m", "http.server", "5500"]
```

#### Step 4: Start All Services

```bash
docker-compose up
```

Or run in background:
```bash
docker-compose up -d
```

**Access the application:**
- Frontend: `http://localhost:5500`
- Backend API: `http://localhost:8000`
- Swagger Docs: `http://localhost:8000/docs`

#### Step 5: Stop Services

```bash
docker-compose down
```

---

### Option 2: Individual Docker Containers

#### Step 1: Build Backend Image

```bash
cd backend
docker build -t taskboard-backend .
```

#### Step 2: Run Backend Container

```bash
docker run -d -p 8000:8000 \
  -v %cd%:/app \
  --name taskboard-backend \
  taskboard-backend
```

Or on macOS/Linux:
```bash
docker run -d -p 8000:8000 \
  -v $(pwd):/app \
  --name taskboard-backend \
  taskboard-backend
```

#### Step 3: Build Frontend Image

```bash
cd ../frontend
docker build -t taskboard-frontend .
```

#### Step 4: Run Frontend Container

```bash
docker run -d -p 5500:5500 \
  --name taskboard-frontend \
  taskboard-frontend
```

#### Step 5: Verify Containers Running

```bash
docker ps
```

You should see both `taskboard-backend` and `taskboard-frontend` listed.

#### Step 6: Access Application

- Frontend: `http://localhost:5500`
- Backend API: `http://localhost:8000`

#### Step 7: Stop Containers

```bash
docker stop taskboard-backend taskboard-frontend
docker rm taskboard-backend taskboard-frontend
```

---

## Quick Start Commands Cheat Sheet

### Without Docker (Manual)

```bash
# Terminal 1: Backend
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
# or: source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
python -m uvicorn main:app --reload

# Terminal 2: Frontend
cd frontend
python -m http.server 3000
```

### With Docker Compose

```bash
# Start all services
docker-compose up

# Stop all services
docker-compose down

# View logs
docker-compose logs -f

# Rebuild images
docker-compose build
```

### With Individual Docker Containers

```bash
# Build images
docker build -t taskboard-backend ./backend
docker build -t taskboard-frontend ./frontend

# Run containers
docker run -d -p 8000:8000 taskboard-backend
docker run -d -p 5500:5500 taskboard-frontend

# View running containers
docker ps

# Stop containers
docker stop <container_id>
```

---

## Environment Variables

### Backend Configuration

You can customize the backend by setting environment variables:

```bash
# Database URL (default: sqlite:///./taskboard.db)
set DATABASE_URL=sqlite:///./taskboard.db

# JWT Secret Key (for production, use a strong secret)
set JWT_SECRET=your-secret-key-here

# JWT Algorithm
set JWT_ALGORITHM=HS256

# Token Expiration (in minutes)
set ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

## Troubleshooting

### Issue: "Port 8000 is already in use"

**Solution:**
```bash
# Find process using port 8000
netstat -ano | findstr :8000  # Windows
# or
lsof -i :8000  # macOS/Linux

# Kill the process
taskkill /PID <PID> /F  # Windows
# or
kill -9 <PID>  # macOS/Linux

# Use a different port
python -m uvicorn main:app --port 8001
```

### Issue: "Port 5500 is already in use"

**Solution:**
```bash
python -m http.server 3001  # Use different port
```

### Issue: Module not found error

**Solution:**
```bash
# Ensure virtual environment is activated
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue: Database locked error

**Solution:**
- Close all instances of the application
- Delete `taskboard.db` and restart (this will lose all data)
- Or ensure only one backend instance is running

### Issue: CORS errors in browser console

**Solution:**
- Ensure backend is running on `http://127.0.0.1:8000`
- Ensure frontend is accessing the correct backend URL
- Check `api.js` has correct `API_URL` setting

### Issue: Docker container exits immediately

**Solution:**
```bash
# Check logs
docker logs <container_id>

# Verify Dockerfile is correct
docker build --no-cache -t taskboard-backend ./backend
```

---

## Performance Tips

### Without Docker
- Use `--reload` flag only during development
- For production, remove `--reload` flag
- Use a production ASGI server like Gunicorn

### With Docker
- Use volumes for development (automatic reload)
- Build images without `--reload` for production
- Use `.dockerignore` to exclude unnecessary files

---

## Next Steps

1. **Access Swagger Documentation:** `http://localhost:8000/docs`
2. **Create your first account:** Register at the login page
3. **Create a board:** Start managing your tasks
4. **Explore the API:** Use Swagger UI to test endpoints

---

## Getting Help

If you encounter issues:
1. Check the [Troubleshooting](#troubleshooting) section above
2. Check backend logs in terminal
3. Check browser console for frontend errors
4. Review the Business Specification document for feature details

---

**Happy Task Managing! 📋**
