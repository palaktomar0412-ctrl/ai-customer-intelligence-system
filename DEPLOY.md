# 🚀 Deployment Guide

Deploy the **whole project** (React UI + FastAPI API + SQLite DB + ML models) as a single web service.

---

## Architecture (single service)

```
┌─────────────────────────────────────────────┐
│              One Docker container           │
│                                             │
│  FastAPI (uvicorn, port 8000)               │
│  ├── /            → React SPA (built dist)  │
│  ├── /api/*       → REST API                │
│  ├── SQLite DB    → backend/customer_intelligence.db
│  └── ML models    → backend/ml/models/*.pkl │
└─────────────────────────────────────────────┘
```

The root `Dockerfile` (identical copy: `Dockerfile.web`) does three things:
1. `npm run build` → compiles the React frontend
2. `python seed.py` → creates the SQLite DB, seeds 1,000 customers, trains all ML models
3. Serves everything with one uvicorn process (`SERVE_FRONTEND=true`)

Login: `admin@customerintelligence.com` / `admin123`

---

## Option 1 — Render (recommended, easiest)

1. Push this repo to GitHub (already at `github.com/palaktomar0412-ctrl/ai-customer-intelligence-system`).
2. Go to [dashboard.render.com](https://dashboard.render.com) → **New +** → **Web Service** → select the repo.
3. Configure:
   - **Language:** `Docker` ← not Python 3
   - **Dockerfile path:** `./Dockerfile` (the default works — no override needed)
   - **Instance Type:** Free
4. Under **Advanced → Environment Variables**, add:
   ```
   JWT_SECRET_KEY = <any long random hex string>
   SERVE_FRONTEND = true
   FRONTEND_DIST  = /app/frontend/dist
   ENVIRONMENT    = production
   DEBUG          = false
   ```
5. Click **Deploy Web Service**. First build takes ~8–15 min (installs deps, trains models).
6. Your app goes live at the URL Render assigns (e.g. `https://customer-intelligence.onrender.com`).

> A `render.yaml` blueprint is also included for Blueprint-based deploys if you prefer that flow.

> **Important:** in the Render dashboard, update the `ALLOWED_ORIGINS` env var to match your actual onrender.com URL if it differs from the one in `render.yaml`. (Same-origin requests don't need CORS, so in most cases you can leave it as is.)

**Free-tier notes:**
- The service sleeps after 15 min idle; first request after that takes ~30–60 s to wake.
- SQLite lives on the instance disk — **data resets on each redeploy** (seed data returns). Attach a paid Render Disk mounted at `/app/backend` to persist, or switch `DB_TYPE` to an external MySQL.

---

## Option 2 — Railway

1. [railway.app](https://railway.app) → **New Project** → **Deploy from GitHub repo**.
2. In the service settings, set:
   - **Dockerfile path:** `Dockerfile` (repo root — default)
   - Env vars: `JWT_SECRET_KEY` (generate), `SERVE_FRONTEND=true`, `FRONTEND_DIST=/app/frontend/dist`, `ENVIRONMENT=production`, `DEBUG=false`
3. Under **Settings → Networking → Generate Domain**, expose port `8000`.

Railway also offers persistent **Volumes** — mount one at `/app/backend/data` and set `SQLITE_DB=/app/backend/data/customer_intelligence.db` to keep data across deploys.

---

## Option 3 — AWS (EC2 VM + Docker)

```bash
# On an Ubuntu 22.04 EC2 instance (t2.small or bigger; ML training needs ~2 GB RAM)
sudo apt update && sudo apt install -y docker.io
sudo usermod -aG docker $USER && newgrp docker

git clone https://github.com/palaktomar0412-ctrl/ai-customer-intelligence-system.git
cd ai-customer-intelligence-system

docker build -t ci-web .
docker run -d --name ci-web --restart always \
  -p 80:8000 \
  -e JWT_SECRET_KEY="$(openssl rand -hex 32)" \
  -e SERVE_FRONTEND=true -e FRONTEND_DIST=/app/frontend/dist \
  -e ENVIRONMENT=production -e DEBUG=false \
  ci-web
```

Open `http://<EC2-public-IP>` (allow port 80 in the Security Group). For HTTPS, put a load balancer or Caddy/nginx + certbot in front.

---

## Environment variables

| Variable | Default | Purpose |
|---|---|---|
| `JWT_SECRET_KEY` | dev fallback | **Set a strong random value in production** |
| `ENVIRONMENT` | `development` | `production` in deploys |
| `DEBUG` | `true` | `false` in deploys (also silences SQL echo) |
| `SERVE_FRONTEND` | `false` | `true` → FastAPI serves the built React app |
| `FRONTEND_DIST` | `""` | Path to `dist/` when `SERVE_FRONTEND=true` |
| `ALLOWED_ORIGINS` | localhost set | Comma-separated CORS origins for the API |
| `DB_TYPE` | `sqlite` | `mysql` + `DB_HOST/PORT/USER/PASSWORD/NAME` for MySQL |
| `SQLITE_DB` | backend dir | Absolute path override for the SQLite file |
| `PORT` | `8000` | Uvicorn port (Render/Railway inject this) |

---

## Verify the deployment

```bash
curl https://your-app-url/api/health          # → {"status":"healthy",...}
curl -I https://your-app-url/                 # → text/html (React app)
curl -X POST https://your-app-url/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@customerintelligence.com","password":"admin123"}'
```

Then open the URL in a browser and log in.

---

## Production checklist

- [x] Admin user auto-created at startup (no manual seed needed)
- [x] ML models trained at build time (baked into the image)
- [x] Health check endpoint for platform monitoring (`/api/health`)
- [ ] Rotate the admin password after first login (`admin123` is public in this repo)
- [ ] Set a unique `JWT_SECRET_KEY` (Render's blueprint does this automatically)
- [ ] Attach a disk or external DB if you need data to survive redeploys
- [ ] Enable HTTPS at the platform or via a reverse proxy
