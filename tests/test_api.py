"""
Indian Railways Dynamic ETA - Automated API and Integration Tests
Author: SIH AI Prototype
"""

import sys
import os

# Set working directory to project root
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from backend.app import app

client = TestClient(app)

def test_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ONLINE"
    print("[PASS] Health Check Passed:", data)

def test_search_trains():
    response = client.get("/api/trains/search?q=Cheran")
    assert response.status_code == 200
    data = response.json()
    assert len(data["results"]) > 0
    print(f"[PASS] Search Trains Passed ({len(data['results'])} matches):", data["results"][0])

def test_get_route():
    response = client.get("/api/train/12673/route")
    assert response.status_code == 200
    data = response.json()
    assert data["train_no"] == "12673"
    assert len(data["route"]) > 0
    print(f"[PASS] Route Retrieval Passed ({len(data['route'])} stations found)")

def test_predict_eta():
    payload = {
        "train_no": "12673",
        "current_station_idx": 2,
        "current_delay_min": 25.0,
        "weather": "Clear",
        "congestion": "Normal"
    }
    response = client.post("/api/predict_eta", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "stations_forecast" in data
    assert len(data["stations_forecast"]) > 0
    forecast = data["stations_forecast"]
    print(f"[PASS] Dynamic ETA Prediction Passed ({len(forecast)} station forecasts):")
    for f in forecast[:3]:
        print(f"   -> {f['station_code']} ({f['station_name']}): Delay={f.get('predicted_delay_min')}m, Trend={f.get('delay_trend')}")

def test_simulation():
    start_payload = {
        "train_no": "12673",
        "initial_delay": 15.0,
        "weather": "Clear",
        "congestion": "Normal"
    }
    res_start = client.post("/api/simulation/start", json=start_payload)
    assert res_start.status_code == 200
    sim_data = res_start.json()
    session_id = sim_data["session_id"]
    print("[PASS] Simulation Start Passed. Session ID:", session_id)

    step_payload = {
        "session_id": session_id,
        "inject_delay": 10.0,
        "weather": "Heavy Rain",
        "congestion": "High"
    }
    res_step = client.post("/api/simulation/step", json=step_payload)
    assert res_step.status_code == 200
    step_data = res_step.json()
    assert step_data["current_stop_idx"] == 1
    print("[PASS] Simulation Step Passed. Current Station:", step_data["current_station"]["station_name"])
    print("  Operational Platform:", step_data["operations"]["platform_management"]["assigned_platform"])

def test_i18n():
    for lang in ["en", "hi", "ta", "te"]:
        res = client.get(f"/api/i18n/{lang}")
        assert res.status_code == 200
        data = res.json()
        assert "title" in data["strings"]
        print(f"[PASS] i18n [{lang}] Passed.")

def test_frontend_serving():
    response = client.get("/")
    assert response.status_code == 200
    assert "Indian Railways" in response.text
    print("[PASS] Frontend HTML Serving Passed")

if __name__ == "__main__":
    print("=" * 60)
    print("RUNNING AUTOMATED TEST SUITE FOR INDIAN RAILWAYS AI ETA PROTOTYPE")
    print("=" * 60)
    test_health()
    test_search_trains()
    test_get_route()
    test_predict_eta()
    test_simulation()
    test_i18n()
    test_frontend_serving()
    print("=" * 60)
    print("ALL TESTS PASSED SUCCESSFULLY! 100% OPERATIONAL.")
    print("=" * 60)
