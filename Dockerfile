# ============================================================================
# Single-service production image (UI + API + SQLite + ML models in one box)
# Used for Render / Railway / Fly.io / any Docker-based PaaS.
#
# Build:  docker build -t ci-web .   (root Dockerfile; Dockerfile.web is an identical copy)
# Run:    docker run -p 8000:8000 -e JWT_SECRET_KEY=change-me ci-web
# ============================================================================

# ---- Stage 1: build the React frontend ------------------------------------
FROM node:20-alpine AS frontend-build

WORKDIR /build
COPY frontend/package.json frontend/package-lock.json* ./
RUN npm ci || npm install

COPY frontend/ .
RUN npm run build          # outputs to /build/dist

# ---- Stage 2: backend + static frontend ------------------------------------
FROM python:3.11-slim

WORKDIR /app

# System deps (gcc needed by some wheels)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Python deps
COPY backend/requirements.txt ./backend/requirements.txt
RUN pip install --no-cache-dir -r backend/requirements.txt

# Backend code
COPY backend/ ./backend/

# Built frontend
COPY --from=frontend-build /build/dist ./frontend/dist

# Seed SQLite DB + train ML models at BUILD time (not on every boot).
# The .db and *.pkl files end up baked into the image under /app/backend/.
WORKDIR /app/backend
RUN python seed.py

# Runtime settings
ENV ENVIRONMENT=production \
    DEBUG=false \
    SERVE_FRONTEND=true \
    FRONTEND_DIST=/app/frontend/dist

EXPOSE 8000

# Render/Railway inject $PORT; default to 8000 locally
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
