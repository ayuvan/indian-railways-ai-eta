# Cloud Server Deployment Guide • Indian Railways Dynamic AI ETA

This guide explains how to host the **Indian Railways Dynamic AI ETA Prototype** on a public 24/7 cloud server so that anyone on any device in the world can access it, completely independent of your local computer.

---

## ⚡ Quick Test Right Now (Instant Public Link)

If you want to test the website right now on your mobile phone or share it with others while your computer is on:

- **Public URL**: [**https://breezy-mugs-report.loca.lt**](https://breezy-mugs-report.loca.lt)
- **Control Room Console**: [**https://breezy-mugs-report.loca.lt/control-room**](https://breezy-mugs-report.loca.lt/control-room)
- **Tunnel Password (if asked on first open)**: `61.0.9.108` *(enter this number and click "Click to Submit")*

---

## 🌐 Option 1: 100% Free 24/7 Cloud Hosting on Render.com (Recommended)

Render provides free cloud hosting for web applications with automatic HTTPS, public `.onrender.com` domains, and automatic deployments.

### Step 1: Push your code to GitHub
1. Open [GitHub.com](https://github.com) and create a new repository called `indian-railways-ai-eta` (choose **Public**).
2. In your terminal / command prompt, run:
   ```bash
   git remote add origin https://github.com/<YOUR_GITHUB_USERNAME>/indian-railways-ai-eta.git
   git push -u origin main
   ```
   *(All code, ML model artifacts, schedule caches, and configuration files are already committed locally!)*

### Step 2: Deploy on Render.com
1. Go to [https://dashboard.render.com/](https://dashboard.render.com/) and sign up / log in with GitHub.
2. Click **New +** ➔ **Web Service**.
3. Select **Build and deploy from a Git repository** and pick your `indian-railways-ai-eta` repository.
4. Render will auto-detect the configuration, or you can configure:
   - **Name**: `indian-railways-ai-eta`
   - **Region**: Singapore or Frankfurt (closest to India)
   - **Runtime**: `Python`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn backend.app:app --host 0.0.0.0 --port $PORT`
   - **Instance Type**: `Free`
5. Click **Create Web Service**.
6. Within 2-3 minutes, your website is live 24/7 worldwide at:
   👉 `https://indian-railways-ai-eta.onrender.com`

---

## 🚀 Option 2: 100% Free 24/7 Hosting on Hugging Face Spaces (Never Sleeps)

Hugging Face Spaces is popular for hosting AI and machine learning prototypes with high uptime and free CPU resources.

1. Go to [https://huggingface.co/spaces](https://huggingface.co/spaces) and log in.
2. Click **Create new Space**.
3. Set:
   - **Space Name**: `ir-dynamic-ai-eta`
   - **License**: `MIT` or `Open Source`
   - **Space SDK**: Choose **Docker** ➔ **Blank**.
4. In your terminal, add the Hugging Face remote and push:
   ```bash
   git remote add hf https://huggingface.co/spaces/<YOUR_USERNAME>/ir-dynamic-ai-eta
   git push -u hf main
   ```
5. Hugging Face will automatically build the `Dockerfile` we created and launch your prototype with a permanent public link:
   👉 `https://<YOUR_USERNAME>-ir-dynamic-ai-eta.hf.space`

---

## 🚂 Option 3: Deploying with Docker on Any Cloud (AWS / GCP / DigitalOcean)

The project includes a production `Dockerfile`:
```bash
# Build container image
docker build -t ir-ai-eta:latest .

# Run container exposing port 8000
docker run -d -p 80:8000 --name ir-ai-eta-server ir-ai-eta:latest
```

---

## 📁 Pre-configured Deployment Files Included in the Repository

| File | Purpose |
| :--- | :--- |
| `Dockerfile` | Multi-platform container configuration for Docker, GCP Cloud Run, and Hugging Face. |
| `requirements.txt` | Clean, pinned Python dependencies (`fastapi`, `uvicorn`, `pandas`, `scikit-learn`). |
| `render.yaml` | Infrastructure-as-code blueprint for 1-click deploy on Render. |
| `Procfile` | Web process definition for Heroku, Railway, and Render. |
| `.gitignore` / `.dockerignore` | Keeps out the raw 970MB CSV files while keeping the lightweight 10MB fast binary cache (`sched_cache.pkl` and `model_cache.pkl`). |
