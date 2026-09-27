"""
Indian Railways Dynamic ETA - Real-Time Journey & GPS Simulator
Author: SIH AI Prototype
Description:
    Simulates real-time train movement, block section signaling, GPS progress,
    and allows dynamic injection of track disruptions (signal stops, fog, bottlenecks).
"""

import random
from typing import Dict, Any, Optional
from ml.predict import ETAPredictor
from backend.operations import StationOperationsHub

class TrainJourneySimulator:
    """Maintains simulation state for active train journeys."""

    def __init__(self):
        self.active_sessions: Dict[str, Dict[str, Any]] = {}
        self.predictor = ETAPredictor.get_instance()

    def start_simulation(
        self,
        train_no: str,
        initial_delay: float = 0.0,
        weather: str = "Clear",
        congestion: str = "Normal"
    ) -> Dict[str, Any]:
        """Initializes a new live journey simulation session."""
        route = self.predictor.get_train_route(train_no)
        if not route:
            return {"error": f"Route for train {train_no} not found"}

        session_id = f"sim_{train_no}"
        self.active_sessions[session_id] = {
            "session_id": session_id,
            "train_no": str(train_no).lstrip("0"),
            "current_stop_idx": 0,
            "current_delay_min": float(initial_delay),
            "weather": weather,
            "congestion": congestion,
            "speed_kmh": 95.0,
            "total_stops": len(route),
            "history": []
        }

        return self.get_current_state(session_id)

    def step_simulation(
        self,
        session_id: str,
        inject_delay: float = 0.0,
        weather_override: Optional[str] = None,
        congestion_override: Optional[str] = None
    ) -> Dict[str, Any]:
        """Advances the train to the next station or block section."""
        session = self.active_sessions.get(session_id)
        if not session:
            return {"error": "Session not found. Please start simulation first."}

        if weather_override:
            session["weather"] = weather_override
        if congestion_override:
            session["congestion"] = congestion_override

        # Advance stop index if not at destination
        if session["current_stop_idx"] < session["total_stops"] - 1:
            session["current_stop_idx"] += 1

        # Apply stochastic event or manual injection
        stochastic_drift = random.uniform(-1.5, 3.5)
        new_delay = session["current_delay_min"] + inject_delay + stochastic_drift
        session["current_delay_min"] = max(-15.0, round(new_delay, 1))

        # Adjust simulated speed
        base_speed = 100.0 if session["weather"] == "Clear" else (75.0 if session["weather"] == "Heavy Rain" else 50.0)
        if session["congestion"] == "High":
            base_speed -= 25.0
        session["speed_kmh"] = max(20.0, round(base_speed + random.uniform(-5.0, 5.0), 1))

        return self.get_current_state(session_id)

    def get_current_state(self, session_id: str) -> Dict[str, Any]:
        """Calculates dynamic forecast and operations for current state."""
        session = self.active_sessions.get(session_id)
        if not session:
            return {"error": "Session not found"}

        t_no = session["train_no"]
        stop_idx = session["current_stop_idx"]
        delay = session["current_delay_min"]
        weather = session["weather"]
        congestion = session["congestion"]

        forecast = self.predictor.predict_downstream_eta(
            train_no=t_no,
            current_station_idx=stop_idx,
            current_delay_min=delay,
            weather=weather,
            congestion_level=congestion
        )

        route = self.predictor.get_train_route(t_no)
        current_station = route[stop_idx]
        dest_station = route[-1]

        # Station operations for next junction or upcoming station
        target_station = route[min(stop_idx + 1, len(route) - 1)]
        pred_delay_at_target = delay
        for stn in forecast.get("stations_forecast", []):
            if stn.get("station_code") == target_station["station_code"]:
                pred_delay_at_target = stn.get("predicted_delay_min", delay)
                break

        operations = StationOperationsHub.get_station_operations(
            station_code=target_station["station_code"],
            station_name=target_station["station_name"],
            train_no=t_no,
            train_name=forecast.get("train_name", f"Train {t_no}"),
            scheduled_arrival=target_station["scheduled_arr"],
            predicted_delay_min=pred_delay_at_target,
            is_junction=target_station["is_junction"]
        )

        return {
            "session_id": session_id,
            "train_no": t_no,
            "train_name": forecast.get("train_name"),
            "train_type": forecast.get("train_type"),
            "current_stop_idx": stop_idx,
            "current_station": current_station,
            "destination_station": dest_station,
            "current_delay_min": delay,
            "speed_kmh": session["speed_kmh"],
            "weather": weather,
            "congestion": congestion,
            "is_completed": (stop_idx >= len(route) - 1),
            "forecast": forecast.get("stations_forecast", []),
            "operations": operations
        }

simulator_instance = TrainJourneySimulator()
