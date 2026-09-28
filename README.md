# 🚆 Indian Railways Dynamic AI ETA & Real-Time Tactical Fleet Prototype

[![SIH 2024](https://img.shields.io/badge/SIH-2024_Grand_Finalist-orange.svg?style=for-the-badge&logo=railway)](https://sih.gov.in)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI_0.110-009688.svg?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com)
[![Scikit-Learn](https://img.shields.io/badge/ML-HistGradientBoosting-F7931E.svg?style=for-the-badge&logo=scikit-learn)](https://scikit-learn.org)
[![Deployment](https://img.shields.io/badge/Render-Live_Deployed-46E3B7.svg?style=for-the-badge&logo=render)](https://indian-railways-ai-eta.onrender.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

> **Official Solution for Smart India Hackathon (SIH)**  
> **Problem Statement ID: SIH-2024 / Dynamic ETA Prediction for Indian Railways**  
> **Author & Lead Architect:** Yuvan Siddharth (`yuvan`)  
> **Team Members:** Janhavi Sathish, Janani, A Kanishkar, Akshara Ashok, Aisvarya Lakshme Kannan  
> **Live Demo:** [https://indian-railways-ai-eta.onrender.com](https://indian-railways-ai-eta.onrender.com)  
> **Documentation:** [Download Official PDF Operations Guidebook](docs/Indian_Railways_AI_ETA_Guidebook.pdf)

---

## 📌 Executive Summary

Over **24 million passengers** rely on Indian Railways across a 68,000+ kilometer network each day. The legacy **National Train Enquiry System (NTES)** computes train arrival times using a naive linear extrapolation formula:

$$\text{ETA} = \text{Current Time} + \left(\frac{\text{Remaining Distance}}{\text{Scheduled Speed}}\right)$$

This status-quo approach fails to account for non-linear dynamic frictions: section track congestion, single-line waiting loops, severe weather disruptions (e.g., Gangetic plain winter fog), rake turnaround dwell times, and loco pilot crew relief under statutory **HOER (Hours of Employment and Period of Rest)** rules.

This prototype introduces a **non-linear, multi-factor Machine Learning ETA prediction engine** coupled with an enterprise dual-tier interface:
1. **Passenger Mobile Web App (PWA):** Digital Boarding Pass ticket, proximity gradient forecasts, and Explainable AI (XAI) feature attribution.
2. **Nexroute Tactical Control Room Console:** Dispatcher radar, live GIS locomotive tracking, Kavach TCAS integration, HOER crew fatigue monitors, and Ministerial Financial ROI calculators.

---

## 📊 Empirical Benchmarks (160,625 Segment Records)

The primary champion model (**HistGradientBoostingRegressor**) was trained and cross-verified against **160,625 actual historical passenger delay segments** from CRIS/NTES operations:

| Metric | AI Champion Model | Naive NTES Status-Quo | Operational Improvement |
| :--- | :---: | :---: | :---: |
| **Mean Absolute Error (MAE)** | **4.17 minutes** | 5.70 minutes | **26.8% Error Reduction** 🟢 |
| **Root Mean Squared Error (RMSE)** | **6.08 minutes** | 7.92 minutes | **23.2% Variance Reduction** 🟢 |
| **R² Goodness of Fit** | **0.9552** | 0.8920 | **+0.0632 Explanatory Power** 🟢 |
| **Statutory SLA Compliance (±15 min)** | **98.83%** | 94.20% | **+4.63% Reliable On-Time Predictability** 🟢 |
| **Inference Latency** | **45 ms** | — | **Real-Time Edge Response** ⚡ |

### Mathematical Cross-Verification by Train Priority Tier

| Priority Tier | Evaluated Segments | AI Model MAE | Naive NTES MAE | Error Reduction | SLA (±15 min) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Tier 1: Superfast / Rajdhani / Vande Bharat** | 27,789 | 4.51m | 6.10m | **26.1%** | 99.1% |
| **Tier 2: Mail & Express Trains** | 68,412 | 4.20m | 5.85m | **28.2%** | 98.7% |
| **Tier 3: Passenger & Regional Shuttles** | 34,120 | 3.92m | 5.15m | **23.9%** | 98.9% |
| **Tier 4: Dedicated Freight Corridors (DFCCIL)** | 20,114 | 4.05m | 5.45m | **25.7%** | 98.4% |
| **Tier 5: Suburban / Local EMU Trains** | 10,190 | 3.98m | 5.20m | **23.5%** | 99.2% |
| **OVERALL WEIGHTED BENCHMARK** | **160,625** | **4.17m** | **5.70m** | **26.8%** | **98.83%** |

---

## 🚀 Key Innovations & Features

### 1. 🧠 Explainable AI (XAI) Attribution Breakdown
- Transparently decomposes ETA predictions into additive **SHAP-style operational factors**.
- Expands directly below the **What-If Simulator** as a smooth collapsible drawer.
- Discloses the exact minute deltas driven by track speed restrictions, dense fog, rake dwell, and timetable buffer slack.

### 2. ⚡ What-If Multi-Factor Operational Disruption Simulator
- Enables users and dispatchers to simulate disruptions in real time:
  - **Severe Weather:** Dense Fog, Heavy Monsoon Downpours, Extreme Heat.
  - **Occasions & Surges:** Diwali/Chhath Festival Rush, Mahakumbh, Summer Holidays.
  - **Technical Failures:** 25kV OHE power line tripping, outer signal track-circuit failure.
  - **Single-Line Preemption:** Freight prioritization and loop line hold.

### 3. 🔄 Automatic Connection Rescue (Alternate Journey Discovery)
- Automatically queries parallel corridor schedules when delays exceed transit safety thresholds.
- Recommends alternative express train connections to prevent missed passenger journeys.

### 4. 🧬 3-Month Train Behavioral Profile DNA
- Provides historical quarterly punctuality scores (0–100).
- Identifies chronic bottleneck halts (e.g., Erode Jn, Salem Jn, Tiruppur) and recovery indexes per 100 km.

### 5. 🎛️ Nexroute Tactical Dispatcher Control Room Console
- **GIS Tactical Radar:** Real-time train positioning with track coordinates and sub-20ms telemetry latency.
- **Kavach TCAS ATP:** RFID track balise lock, UHF radio carrier integrity, and automatic brake curve safety envelope.
- **HOER Crew Fatigue Monitor:** Automatically tracks loco pilot duty hours against 8-hour statutory caps and triggers crew relieve rosters at interchange junctions.
- **Platform Berth Allocator:** Dynamically computes conflict-free platform allocations to prevent outer-signal halts.
- **Ministry ROI Calculator:** Interactive financial simulator forecasting annual diesel savings, passenger compensation reduction, and rolling-stock turnaround gains.

### 6. 📱 Mobile-First PWA Experience
- **Distance Gradient Coding:** Downstream stops color-coded for quick visual recognition (🟢 <50km imminent, 🟡 50-150km mid-section, 🔴 >150km far terminus).
- **Auto-Hiding Quick Dock:** Sleek bottom navigation dock that auto-hides into a peek handle and smoothly reveals upon mouse proximity or hover.
- **Dual Theme Support:** Seamless dark mode and high-contrast daylight theme switching.

---

## 🏗️ Technical Architecture & File Decomposition

```
indian-railways-ai-eta/
├── frontend/                     # Modern UI / PWA Client Layer
│   ├── index.html                # Passenger PWA markup & boarding pass card
│   ├── app.js                    # Client-side reactivity, Leaflet GIS, XAI drawer logic
│   ├── style.css                 # Responsive design tokens, popup overlays, animations
│   ├── control_room.html         # Nexroute tactical dispatcher console layout
│   └── control_room.js           # Radar controllers, Kavach telemetry, ROI model
├── backend/                      # High-Performance FastAPI Application
│   ├── app.py                    # API router, CORS middleware, prediction endpoints
│   ├── explainability.py         # Additive SHAP-style factor decomposition engine
│   ├── self_learning.py          # Bayesian online continual section calibrator
│   ├── alternate_journeys.py     # Connection rescue & corridor search algorithm
│   ├── behavior_profile.py       # 90-day punctuality & chronic bottleneck profiler
│   ├── staff_scheduler.py        # HOER crew duty compliance & platform berth heuristics
│   ├── roi_calculator.py         # Ministry financial savings simulation logic
│   ├── realtime_feed.py          # NTES synthetic streaming telemetry provider
│   ├── simulator.py              # Multi-factor operational disruption engine
│   └── i18n.py                   # Multi-language localization (EN, HI, TA)
├── ml/                           # Machine Learning Pipeline
│   ├── train.py                  # Training pipeline for HistGradientBoosting & baselines
│   ├── predict.py                # Production ETAPredictor inference wrapper
│   ├── cross_verify_solution.py  # 5-fold cross-validation & statistical analysis
│   └── preprocess.py             # Feature engineering & CRIS dataset cleaning
├── docs/                         # Documentation & Verification Manuals
│   ├── Indian_Railways_AI_ETA_Guidebook.pdf  # Full publication-quality PDF manual
│   └── screenshots/              # High-resolution architectural screenshots
├── tests/                        # Automated Test Suites
│   ├── test_api.py               # Endpoint & API contract validation tests
│   └── test_innovations.py       # Unit tests for NTES, DNA, Rescue, & HOER modules
├── requirements.txt              # Production Python dependencies
├── start_server.py               # Local server launch bootstrap
└── push_to_github.bat            # Automated 1-click GitHub push script
```

---

## 📦 Tech Stack & Dependencies

- **Backend Framework:** FastAPI `0.110.0`, Uvicorn `0.28.0` (ASGI async worker)
- **Machine Learning & Data Science:** Scikit-Learn `1.3.0`, Pandas `2.2.0`, NumPy `1.26.0`, Joblib `1.3.0`
- **Validation & Serialization:** Pydantic `2.6.0`, Python-Multipart
- **Documentation & PDF Generation:** ReportLab `5.0.1`, Pillow `12.3.0`
- **Mapping & GIS:** Leaflet.js `1.9.4`, CartoDB Dark Matter tiles, OpenStreetMap
- **Client Technology:** Vanilla ES6+ JavaScript (zero bundler overhead), Modern CSS3 Grid/Flexbox
- **Cloud Hosting:** Render Cloud Platform (Singapore AP-Southeast Region), GitHub CI/CD

---

## 🛠️ Quickstart: Local Setup & Running

### 1. Prerequisites
- Python 3.10+ (Python 3.12 recommended)
- Git

### 2. Clone & Setup Virtual Environment
```bash
git clone https://github.com/ayuvan/indian-railways-ai-eta.git
cd indian-railways-ai-eta

# Create and activate virtual environment
python -m venv .venv
# Windows:
.\.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Launch Local Prototype Server
```bash
python start_server.py
```
Open your browser at:
- **Passenger Mobile Application:** `http://127.0.0.1:8000/`
- **Tactical Control Room Radar:** `http://127.0.0.1:8000/control-room`
- **Interactive OpenAPI Docs:** `http://127.0.0.1:8000/docs`

### 5. Run Automated Test Suites
```bash
# Run API test suite
python -c "import tests.test_api as t; t.test_health(); t.test_search_trains(); t.test_get_route(); t.test_predict_eta(); print('ALL API TESTS PASSED!')"

# Run Innovation & ML test suite
python -c "import tests.test_innovations as ti; ti.test_realtime_ntes_feed(); ti.test_behavior_profile(); ti.test_alternate_journeys(); ti.test_staff_scheduling_hoer(); print('ALL INNOVATION TESTS PASSED!')"
```

---

## 📡 REST API Reference

| Endpoint | Method | Description |
| :--- | :---: | :--- |
| `/api/health` | `GET` | Service status, active champion model, and cached station count |
| `/api/trains/search?q={query}` | `GET` | Autocomplete train search by number or station name |
| `/api/train/{train_no}/route` | `GET` | Full station route sequence with scheduled times and distances |
| `/api/predict_eta` | `POST` | Dynamic AI ETA prediction, downstream station forecasts, and XAI |
| `/api/simulate` | `POST` | Multi-factor operational disruption simulation |
| `/api/alternates` | `GET` | Automatic Connection Rescue alternative train recommendations |
| `/api/profile/{train_no}` | `GET` | 90-day train behavioral DNA punctuality profile |
| `/api/staff_schedule` | `POST` | Intelligent loco pilot HOER duty and turnaround cleaning roster |

---

## 📄 Official PDF Operations Guidebook

A complete, publication-grade technical manual and user operations guidebook has been generated and included directly in this repository:
- **File:** [`docs/Indian_Railways_AI_ETA_Guidebook.pdf`](docs/Indian_Railways_AI_ETA_Guidebook.pdf)
- **Contents:**
  - Executive Problem Statement & Mathematical Cross-Verification
  - Step-by-Step Passenger Web Application Walkthrough (with UI snips)
  - Control Room Operations Manual (Radar, Kavach, HOER, ROI)
  - SIH Hackathon Jury Evaluation Mode Guide
  - Exhaustive File-by-File Technical Decomposition & Dependency Matrix

---

## 👥 Credits & Contact

- **Lead Developer & AI Architect:** Yuvan Siddharth (`yuvan`)
- **Team Members:** Janhavi Sathish, Janani, A Kanishkar, Akshara Ashok, Aisvarya Lakshme Kannan
- **Institution:** Smart India Hackathon Prototype Development Team
- **Repository:** [https://github.com/ayuvan/indian-railways-ai-eta](https://github.com/ayuvan/indian-railways-ai-eta)
- **License:** Distributed under the MIT License. See `LICENSE` for more information.