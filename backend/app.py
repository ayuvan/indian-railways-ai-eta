"""
Indian Railways Dynamic ETA - FastAPI Server & Microservice (Dual-Portal Enabled)
Author: SIH AI Prototype
Description:
    Async FastAPI backend serving:
      1. Dynamic multi-hop ML ETA inference
      2. Real-time NTES & CRIS open telemetry streaming
      3. 3-Month Train Behavioral Profiles
      4. Automatic Alternate Journey Discovery
      5. Intelligent Staff Scheduling (HOER Crew & Cleaning Roster)
      6. Dual Web Portals: Passenger Mobile App & Railway Control Room Console
"""

import os
import json
from typing import Optional
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

from ml.predict import ETAPredictor
from backend.simulator import simulator_instance
from backend.i18n import get_i18n, TRANSLATIONS
from backend.operations import StationOperationsHub
from backend.realtime_feed import ntes_client
from backend.behavior_profile import profiler_instance
from backend.alternate_journeys import journey_finder
from backend.staff_scheduler import scheduler_instance
from backend.self_learning import self_learning_engine
from backend.explainability import generate_eta_explanation
from backend.roi_calculator import calculate_divisional_roi

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")
ARTIFACTS_DIR = os.path.join(BASE_DIR, "ml", "model_artifacts")

app = FastAPI(
    title="Indian Railways Dynamic ETA & Operations Platform",
    description="SIH AI Prototype: Real-Time Telemetry, Passenger Mobile App, and Staff Control Room",
    version="2.0.0"
)

# Enable CORS for cross-origin web/mobile integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

predictor = ETAPredictor.get_instance()

# Request schemas
class PredictionRequest(BaseModel):
    train_no: str
    current_station_idx: int = 0
    current_delay_min: float = 0.0
    weather: str = "Clear"
    congestion: str = "Normal"
    day_of_week: str = "Mid-Week"
    occasion: str = "None"
    civil_disruption: str = "None"
    technical_malfunction: str = "None"
    timetable_precedence: str = "None"

class SimStartRequest(BaseModel):
    train_no: str
    initial_delay: float = 0.0
    weather: str = "Clear"
    congestion: str = "Normal"

class SimStepRequest(BaseModel):
    session_id: str
    inject_delay: float = 0.0
    weather: Optional[str] = None
    congestion: Optional[str] = None

@app.get("/api/health")
async def health_check():
    return {
        "status": "ONLINE",
        "service": "Indian Railways Dynamic ETA Prediction Engine",
        "model": "HistGradientBoostingRegressor (Champion)",
        "features": [
            "Realtime NTES Stream",
            "Train Behavioral Profiles",
            "Automatic Alternate Journeys",
            "Intelligent Staff Scheduling (HOER)",
            "Distance Gradient Colour Coding",
            "Estimated Platform of Arrival"
        ],
        "cached_stations": len(predictor.station_profiles)
    }

@app.get("/api/trains/search")
async def search_trains(q: str = Query(..., min_length=1), limit: int = 15):
    """Searches trains by number or partial name."""
    results = predictor.search_trains(q, limit=limit)
    return {"results": results}

@app.get("/api/train/{train_no}/route")
async def get_route(train_no: str):
    """Returns the ordered station schedule for a given train."""
    route = predictor.get_train_route(train_no)
    if not route:
        raise HTTPException(status_code=404, detail=f"Train {train_no} route not found")
    clean_no = str(train_no).lstrip("0")
    return {
        "train_no": clean_no,
        "train_name": predictor.train_names.get(clean_no, f"Train {clean_no}"),
        "type_code": predictor.train_types.get(clean_no, "EXP-TRAINS"),
        "stops_count": len(route),
        "route": route
    }

class LearningFeedbackRequest(BaseModel):
    train_no: str
    station_code: str
    predicted_delay_min: float
    actual_delay_min: float

@app.post("/api/predict_eta")
async def predict_eta(req: PredictionRequest):
    """Generates dynamic AI ETA predictions for upcoming stops with online self-learning calibration & XAI."""
    result = predictor.predict_downstream_eta(
        train_no=req.train_no,
        current_station_idx=req.current_station_idx,
        current_delay_min=req.current_delay_min,
        weather=req.weather,
        congestion_level=req.congestion,
        day_of_week=req.day_of_week,
        occasion=req.occasion,
        civil_disruption=req.civil_disruption,
        technical_malfunction=req.technical_malfunction,
        timetable_precedence=req.timetable_precedence
    )
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    # 1. Apply Online Continual Self-Learning Bias Corrections to Station Forecasts
    forecasts = result.get("stations_forecast", [])
    for stn in forecasts:
        stn_code = stn.get("station_code")
        bias = self_learning_engine.get_bias_correction(stn_code)
        if bias != 0.0:
            stn["predicted_delay_min"] = max(0.0, round(stn["predicted_delay_min"] + bias, 1))
            stn["self_learning_bias_applied_min"] = bias

    # 2. Attach Explainable AI (XAI) Attribution Factor Decomposition
    dest_stop = forecasts[-1] if forecasts else None
    final_delay = dest_stop["predicted_delay_min"] if dest_stop else req.current_delay_min
    remaining_dist = dest_stop["distance_from_current_km"] if dest_stop else 100.0
    remaining_stops = len(forecasts)

    xai_breakdown = generate_eta_explanation(
        train_no=result.get("train_no", req.train_no),
        train_name=result.get("train_name", "Express"),
        train_type=result.get("train_type", "EXP-TRAINS"),
        current_delay=req.current_delay_min,
        predicted_delay=final_delay,
        distance_km=remaining_dist,
        stops_remaining=remaining_stops,
        weather=req.weather,
        congestion=req.congestion,
        day_of_week=req.day_of_week,
        occasion=req.occasion,
        civil_disruption=req.civil_disruption,
        technical_malfunction=req.technical_malfunction,
        timetable_precedence=req.timetable_precedence
    )
    result["ai_explainability"] = xai_breakdown
    result["model_version"] = self_learning_engine.model_version
    return result

# --- CONTINUAL SELF-LEARNING & XAI ENDPOINTS ---

@app.get("/api/self_learning/status")
async def get_self_learning_status():
    """Returns real-time telemetry metrics from the Bayesian continual learning engine."""
    return self_learning_engine.get_status()

@app.post("/api/self_learning/feedback")
async def submit_learning_feedback(req: LearningFeedbackRequest):
    """Ingests ground truth arrival report, adjusts Kalman section weights, and detects drift."""
    return self_learning_engine.record_actual_arrival(
        train_no=req.train_no,
        station_code=req.station_code,
        predicted_delay=req.predicted_delay_min,
        actual_delay=req.actual_delay_min
    )

@app.get("/api/operations/roi_metrics")
async def get_operations_roi(trains: int = 42, delay_saved: float = 8.5):
    """Computes quantified financial, human-capital (HOER), energy, and TDR savings."""
    return calculate_divisional_roi(active_trains_count=trains, avg_delay_mitigation_mins=delay_saved)

@app.get("/api/cross_verification_report")
async def get_cross_verification_report():
    """Returns official mathematical cross-verification report against empirical 2025 logs."""
    report_path = os.path.join(ARTIFACTS_DIR, "cross_verification_report.json")
    if os.path.exists(report_path):
        with open(report_path, "r") as f:
            return json.load(f)
    return {"status": "Pending execution"}

# --- REAL-TIME & INNOVATION ENDPOINTS ---

@app.get("/api/realtime/{train_no}")
async def get_realtime_ntes_feed(train_no: str, stn: Optional[str] = None):
    """Connects to NTES/CRIS open telemetry stream for live train telemetry."""
    feed = ntes_client.fetch_live_status(train_no, current_station_code=stn)
    return feed

@app.get("/api/train/{train_no}/behavior_profile")
async def get_train_behavior_profile(train_no: str):
    """Generates 3-month quarterly behavioral running profile."""
    profile = profiler_instance.get_behavior_profile(train_no)
    return profile

@app.get("/api/train/{train_no}/alternate_journeys")
async def get_alternate_journeys(train_no: str, curr_stn: str = "MAS", dest_stn: str = "CBE", delay: float = 25.0):
    """Automatic Alternate Journey Discovery when delays threaten arrival."""
    alternates = journey_finder.find_alternates(train_no, curr_stn, dest_stn, delay)
    return alternates

@app.get("/api/staff_schedule/{train_no}")
async def get_staff_schedule(
    train_no: str,
    curr_stn: str = "KPD",
    next_stn: str = "JTJ",
    delay: float = 30.0
):
    """Intelligent staff & facility auto-rescheduler (HOER crew duty, cleaning, platforms)."""
    clean_no = str(train_no).lstrip("0")
    t_name = predictor.train_names.get(clean_no, f"Train {clean_no}")
    schedule = scheduler_instance.compute_dynamic_staff_schedule(
        train_no=clean_no,
        train_name=t_name,
        current_station=curr_stn,
        next_station=next_stn,
        scheduled_arrival="Dynamic",
        predicted_delay_min=delay,
        is_junction=True
    )
    return schedule

@app.get("/api/control_room/fleet_telemetry")
async def get_fleet_telemetry():
    """Returns active corridor fleet overview and radar metrics inspired by Nexroute console."""
    return {
        "fleet": [
            {
                "train_no": "12673",
                "headcode": "1A23",
                "name": "Cheran Superfast",
                "category": "Passenger Exp",
                "status": "IN TRANSIT",
                "status_type": "transit",
                "origin": "Chennai Central (MAS)",
                "dest": "Coimbatore Jn (CBE)",
                "depart_time": "22:00",
                "eta": "06:00",
                "speed_kmh": 105,
                "speed_limit": 110,
                "delay_min": 25,
                "loco": "WAP-7 #30452 (RPM)",
                "driver": "R. Sharma (ID: 842)",
                "power": "25kV AC (Pantograph Up)",
                "brakes": "Released (5.0 bar)",
                "occupancy_pct": 84,
                "track_sector": "Sector 4, Southern Trunk Mainline"
            },
            {
                "train_no": "12681",
                "headcode": "2V55",
                "name": "Kovai Superfast",
                "category": "Superfast Exp",
                "status": "IN TRANSIT",
                "status_type": "transit",
                "origin": "Chennai Central (MAS)",
                "dest": "Coimbatore Jn (CBE)",
                "depart_time": "14:30",
                "eta": "22:15",
                "speed_kmh": 110,
                "speed_limit": 110,
                "delay_min": 8,
                "loco": "WAP-7 #30311 (ED)",
                "driver": "K. Venkatesh (ID: 914)",
                "power": "25kV AC (Pantograph Up)",
                "brakes": "Released (5.0 bar)",
                "occupancy_pct": 92,
                "track_sector": "Sector 3, Arakkonam Quad Line"
            },
            {
                "train_no": "00961",
                "headcode": "9M11",
                "name": "Heavy Freight Rake",
                "category": "Heavy Freight",
                "status": "DELAYED",
                "status_type": "delayed",
                "origin": "Southampton / Marwar (MJ)",
                "dest": "Trafford Park / Khambli (KBK)",
                "depart_time": "09:45",
                "eta": "14:20",
                "speed_kmh": 42,
                "speed_limit": 75,
                "delay_min": 55,
                "loco": "WAG-9 #31200 (TKD)",
                "driver": "A. Joseph (ID: 618)",
                "power": "25kV AC (Pantograph Up)",
                "brakes": "Dynamic Re-gen Active",
                "occupancy_pct": 100,
                "track_sector": "Loop Siding 2, Jolarpettai Yard"
            },
            {
                "train_no": "20643",
                "headcode": "1E14",
                "name": "Coimbatore Vande Bharat",
                "category": "High Speed Vande Bharat",
                "status": "BOARDING",
                "status_type": "boarding",
                "origin": "Chennai Central (MAS)",
                "dest": "Coimbatore Jn (CBE)",
                "depart_time": "06:10",
                "eta": "11:50",
                "speed_kmh": 0,
                "speed_limit": 130,
                "delay_min": 0,
                "loco": "T18 Vande Bharat Trainset",
                "driver": "M. Sundaram (ID: 104)",
                "power": "25kV AC (Aux Active)",
                "brakes": "Parking Brakes Applied",
                "occupancy_pct": 96,
                "track_sector": "Platform 11, Chennai Central"
            },
            {
                "train_no": "10103",
                "headcode": "3C90",
                "name": "Mandovi Express",
                "category": "Passenger Exp",
                "status": "IN TRANSIT",
                "status_type": "transit",
                "origin": "CSMT Mumbai",
                "dest": "Madgaon (MAO)",
                "depart_time": "07:10",
                "eta": "19:10",
                "speed_kmh": 85,
                "speed_limit": 100,
                "delay_min": 32,
                "loco": "WDG-4D #12890 (KJM)",
                "driver": "P. Naik (ID: 550)",
                "power": "Diesel Electric Traction",
                "brakes": "Released (5.0 bar)",
                "occupancy_pct": 89,
                "track_sector": "Sector 7, Konkan Mountain Viaduct"
            }
        ],
        "volume_series": [
            {"time": "06:00", "count": 142},
            {"time": "08:00", "count": 288},
            {"time": "10:00", "count": 210},
            {"time": "12:00", "count": 325}
        ],
        "latency_series": [18, 22, 16, 42, 28, 19, 24, 31, 20, 15, 27, 33, 19, 21, 25],
        "velocity_variance": [
            {"time": "06:00", "positive": 8, "negative": -3},
            {"time": "07:00", "positive": 5, "negative": -6},
            {"time": "08:00", "positive": 2, "negative": -12},
            {"time": "09:00", "positive": 7, "negative": -4},
            {"time": "10:00", "positive": 9, "negative": -2},
            {"time": "11:00", "positive": 4, "negative": -9},
            {"time": "12:00", "positive": 11, "negative": -3}
        ]
    }

# --- SIMULATION & DISPATCH ENDPOINTS ---

@app.post("/api/simulation/start")
async def start_sim(req: SimStartRequest):
    state = simulator_instance.start_simulation(
        train_no=req.train_no,
        initial_delay=req.initial_delay,
        weather=req.weather,
        congestion=req.congestion
    )
    if "error" in state:
        raise HTTPException(status_code=400, detail=state["error"])
    return state

@app.post("/api/simulation/step")
async def step_sim(req: SimStepRequest):
    state = simulator_instance.step_simulation(
        session_id=req.session_id,
        inject_delay=req.inject_delay,
        weather_override=req.weather,
        congestion_override=req.congestion
    )
    if "error" in state:
        raise HTTPException(status_code=400, detail=state["error"])
    return state

@app.get("/api/simulation/state/{session_id}")
async def get_sim_state(session_id: str):
    state = simulator_instance.get_current_state(session_id)
    if "error" in state:
        raise HTTPException(status_code=404, detail=state["error"])
    return state

@app.get("/api/metrics")
async def get_metrics():
    metrics_path = os.path.join(ARTIFACTS_DIR, "model_comparison_metrics.json")
    if os.path.exists(metrics_path):
        with open(metrics_path, "r") as f:
            return {"metrics": json.load(f)}
    return {"metrics": []}

@app.get("/api/i18n/{lang}")
async def get_translations(lang: str = "en"):
    return {"lang": lang, "strings": get_i18n(lang)}

# Mount static files
if os.path.exists(FRONTEND_DIR):
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

# --- DUAL PORTAL SERVING ---

@app.get("/")
@app.get("/passenger")
async def serve_passenger_app():
    """Serves the Aesthetic Passenger Mobile Web App."""
    index_path = os.path.join(FRONTEND_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "Passenger Web App not found."}

@app.get("/control-room")
@app.get("/staff")
async def serve_control_room():
    """Serves the Technical Railways Control Room Dashboard."""
    cr_path = os.path.join(FRONTEND_DIR, "control_room.html")
    if os.path.exists(cr_path):
        return FileResponse(cr_path)
    return {"message": "Control Room Dashboard not found."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
