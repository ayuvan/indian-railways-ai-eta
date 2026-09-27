"""
Indian Railways Dynamic ETA - Model Inference Service
Author: SIH AI Prototype
Description:
    Loads trained ML artifacts and provides fast, vector-accelerated ETA predictions
    for upcoming stations along any Indian Railways train route.
"""

import os
import json
import joblib
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARTIFACTS_DIR = os.path.join(BASE_DIR, "ml", "model_artifacts")
DATA_DIR = os.path.join(BASE_DIR, "IR Delay Dataset Dummy")

PRIORITY_MAP = {
    "T18-TRAINS": 5, "RAJ-TRAINS": 5, "SHT-TRAINS": 5, "SF-TRAINS": 4,
    "GRB-TRAINS": 3, "EXP-TRAINS": 3, "PRM-TRAINS": 2, "PASS-TRAINS": 1
}

ZONES = ["NR", "CR", "WR", "SR", "ER", "ECR", "SCR", "SER", "NWR", "NCR", "SWR", "WCR", "ECoR", "SECR", "NFR", "NER"]
ZONE_MAP = {z: idx for idx, z in enumerate(ZONES)}

class ETAPredictor:
    _instance = None

    def __init__(self):
        model_pkl = os.path.join(ARTIFACTS_DIR, "model_cache.pkl")
        if os.path.exists(model_pkl):
            import pickle
            with open(model_pkl, "rb") as f:
                self.model = pickle.load(f)
        else:
            self.model = joblib.load(os.path.join(ARTIFACTS_DIR, "champion_eta_model.joblib"))
        with open(os.path.join(ARTIFACTS_DIR, "feature_columns.json"), "r") as f:
            self.feature_cols = json.load(f)
        with open(os.path.join(ARTIFACTS_DIR, "station_delay_profiles.json"), "r") as f:
            self.station_profiles = json.load(f)

        # Load metadata caches
        trains_df = pd.read_csv(os.path.join(DATA_DIR, "train_details.csv"))
        stations_df = pd.read_csv(os.path.join(DATA_DIR, "station_full_names.csv"))

        self.train_types = dict(zip(trains_df["train_no"].astype(str), trains_df["type_code"]))
        self.train_names = dict(zip(trains_df["train_no"].astype(str), trains_df["train_name"]))
        
        self.station_zones = dict(zip(stations_df["station_name"], stations_df["station_zone"]))
        self.station_full_names = dict(zip(stations_df["station_name"], stations_df["station_full_name"]))
        self.station_junctions = {
            stn: 1 if ("JN" in str(name).upper() or "JUNCTION" in str(name).upper()) else 0
            for stn, name in self.station_full_names.items()
        }

        cache_pkl = os.path.join(DATA_DIR, "sched_cache.pkl")
        if os.path.exists(cache_pkl):
            self.sched_df = pd.read_pickle(cache_pkl)
        else:
            self.sched_df = pd.read_csv(os.path.join(DATA_DIR, "combined_schedule.csv"))
            self.sched_df["train_no_clean"] = self.sched_df["train_no"].astype(str).str.lstrip("0")
            self.sched_df["station_no"] = pd.to_numeric(self.sched_df["station_no"], errors="coerce")
            self.sched_df["distance_from_origin"] = pd.to_numeric(self.sched_df["distance_from_origin"], errors="coerce")
            self.sched_df.to_pickle(cache_pkl)

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def search_trains(self, query: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Search trains by number or name."""
        q = query.strip().upper()
        results = []
        for t_no, name in self.train_names.items():
            t_str = str(t_no).lstrip("0")
            name_str = str(name).upper()
            if q in t_str or q in name_str:
                raw_type = self.train_types.get(str(t_no), "EXP-TRAINS")
                results.append({
                    "train_no": t_str,
                    "train_name": str(name),
                    "type_code": raw_type,
                    "priority": PRIORITY_MAP.get(raw_type, 3)
                })
                if len(results) >= limit:
                    break
        return results

    def get_train_route(self, train_no: str) -> List[Dict[str, Any]]:
        """Retrieves ordered stations for the train."""
        clean_no = str(train_no).lstrip("0")
        sub = self.sched_df[self.sched_df["train_no_clean"] == clean_no].sort_values(by="station_no")
        if sub.empty:
            return []

        route = []
        for _, row in sub.iterrows():
            stn_code = str(row["station_name"]).strip()
            route.append({
                "station_no": int(row["station_no"]),
                "station_code": stn_code,
                "station_name": self.station_full_names.get(stn_code, stn_code),
                "distance_km": float(row["distance_from_origin"]) if pd.notna(row["distance_from_origin"]) else 0.0,
                "scheduled_arr": str(row["arrival_time"]) if pd.notna(row["arrival_time"]) else "Source",
                "scheduled_dep": str(row["departure_time"]) if pd.notna(row["departure_time"]) else "Dest",
                "is_junction": bool(self.station_junctions.get(stn_code, 0)),
                "zone": self.station_zones.get(stn_code, "NR")
            })
        return route

    def predict_downstream_eta(
        self,
        train_no: str,
        current_station_idx: int,
        current_delay_min: float,
        weather: str = "Clear",  # Clear, Heavy Rain, Dense Fog
        congestion_level: str = "Normal",  # Low, Normal, High
        day_of_week: str = "Mid-Week",
        occasion: str = "None",
        civil_disruption: str = "None",
        technical_malfunction: str = "None",
        timetable_precedence: str = "None",
        departure_timestamp: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """
        Dynamically predicts arrival times for all remaining stations along the route,
        incorporating real-world operational disruptions, events, and track conditions.
        """
        route = self.get_train_route(train_no)
        if not route:
            return {"error": f"Train {train_no} route not found"}

        if current_station_idx < 0 or current_station_idx >= len(route):
            current_station_idx = 0

        now = departure_timestamp or datetime.now()
        clean_no = str(train_no).lstrip("0")
        raw_type = self.train_types.get(clean_no, "EXP-TRAINS")
        priority = PRIORITY_MAP.get(raw_type, 3)
        train_name = self.train_names.get(clean_no, f"Train {clean_no}")

        current_stop = route[current_station_idx]
        curr_dist = current_stop["distance_km"]
        total_dist = route[-1]["distance_km"] if route[-1]["distance_km"] > 0 else 500.0

        # Operational Weather & Congestion Multipliers
        weather_penalty = {"Clear": 0.0, "Heavy Rain": 6.0, "Dense Fog": 18.0}.get(weather, 0.0)
        congestion_penalty = {"Low": -2.0, "Normal": 0.0, "High": 8.0}.get(congestion_level, 0.0)

        # Indian Railways Real-World Scenario Disruption Penalties
        day_penalties = {
            "Mid-Week": 0.0,
            "Monday Rush": 4.0,       # Heavy morning urban commuter cross-traffic
            "Friday Evening": 6.0,    # Weekend outbound exodus & dwell elongation
            "Sunday Holiday": 2.0     # Weekend return surge
        }
        occasion_penalties = {
            "None": 0.0,
            "Festival Rush (Diwali/Chhath/Pongal)": 14.0,   # Massive baggage & prolonged boarding dwell (+3m/stop)
            "Pilgrimage (Kumbh/Sabarimala/Puri)": 18.0,    # Regulated headway & station crowd dispersal holds
            "Mega Concert / Stadium Match / Expo": 10.0,   # Heavy station precinct congestion
            "State / District Election Results": 12.0      # Special trains & VIP security escort precedence
        }
        civil_penalties = {
            "None": 0.0,
            "Rail Roko / Track Blockade Protest": 45.0,    # Trains held at outer signals; caution order clearance
            "Trade Union / Loco Pilot Strike": 25.0,       # Work-to-rule caution orders & crew relief bottlenecks
            "Severe Overcrowding / Boarding Hold": 15.0    # Unreserved coaches overflowing, safety whistle holds
        }
        tech_penalties = {
            "None": 0.0,
            "OHE Power Tripping / Wire Break": 35.0,       # 25kV traction cutoff; neutral section dead zone
            "Loco Traction / Pantograph / Brake Defect": 20.0, # Speed capped at 50 km/h caution order
            "Track Circuit / Point Interlock Failure": 30.0    # Manual clamping & padlocking (15 km/h walking pace)
        }
        timetable_penalties = {
            "None": 0.0,
            "VIP / Vande Bharat Rajdhani Overtake": 18.0,  # Loop line precedence hold for premier train
            "New Train Release / Timetable Conflict": 12.0,# Section slot clashing & unscheduled crossings
            "Scheduled Track Mega Block (Single Line)": 26.0# Single line pilot working during engineering block
        }

        p_day = day_penalties.get(day_of_week, 0.0)
        p_occ = occasion_penalties.get(occasion, 0.0)
        p_civ = civil_penalties.get(civil_disruption, 0.0)
        p_tech = tech_penalties.get(technical_malfunction, 0.0)
        p_tt = timetable_penalties.get(timetable_precedence, 0.0)

        total_scenario_penalty = weather_penalty + congestion_penalty + p_day + p_occ + p_civ + p_tech + p_tt

        feature_rows = []
        downstream_indices = []

        for j in range(current_station_idx + 1, len(route)):
            target_stop = route[j]
            target_code = target_stop["station_code"]
            dist_to_target = max(1.0, target_stop["distance_km"] - curr_dist)
            
            # Scheduled transit calculation
            sched_transit = (dist_to_target / 65.0) * 60.0  # fallback ~65 km/h
            target_zone = target_stop["zone"]
            zone_code = ZONE_MAP.get(target_zone, 0)
            is_junc = 1 if target_stop["is_junction"] else 0
            hist_d = self.station_profiles.get(target_code, {}).get("mean_delay", 15.0)

            feature_rows.append({
                "train_priority": priority,
                "current_delay": float(current_delay_min),
                "distance_to_target": float(dist_to_target),
                "stops_remaining": j - current_station_idx,
                "total_route_distance": float(total_dist),
                "pct_journey_completed": float(curr_dist / max(1.0, total_dist)),
                "scheduled_transit_min": float(sched_transit),
                "dep_hour": float(now.hour + now.minute / 60.0),
                "is_target_junction": is_junc,
                "target_zone_code": zone_code,
                "target_hist_delay": float(hist_d)
            })
            downstream_indices.append(j)

        predictions = []

        # Current station status
        predictions.append({
            "station_no": current_stop["station_no"],
            "station_code": current_stop["station_code"],
            "station_name": current_stop["station_name"],
            "distance_km": current_stop["distance_km"],
            "status": "CURRENT_LOCATION",
            "scheduled_arr": current_stop["scheduled_arr"],
            "static_eta": current_stop["scheduled_arr"],
            "linear_eta": current_stop["scheduled_arr"],
            "ai_eta": current_stop["scheduled_arr"],
            "predicted_delay_min": round(current_delay_min, 1),
            "delay_trend": "REPORTED",
            "is_junction": current_stop["is_junction"],
            "zone": current_stop["zone"]
        })

        if feature_rows:
            X_infer = pd.DataFrame(feature_rows)[self.feature_cols]
            pred_delays = self.model.predict(X_infer)

            for idx, j in enumerate(downstream_indices):
                target_stop = route[j]
                raw_pred_d = float(pred_delays[idx]) + total_scenario_penalty
                predicted_delay = max(-15.0, round(raw_pred_d, 1))
                
                # Format estimated times
                sched_arr_str = target_stop["scheduled_arr"]
                
                # Dynamic ETA calculation
                delay_delta = predicted_delay - current_delay_min
                if delay_delta < -2.0:
                    trend = "RECOVERING"  # Making up time
                elif delay_delta > 3.0:
                    trend = "COMPOUNDING"  # Gaining delay
                else:
                    trend = "STEADY"

                platform_no = f"PF-{(abs(hash(target_code + clean_no)) % 4) + 1}"

                predictions.append({
                    "station_no": target_stop["station_no"],
                    "station_code": target_stop["station_code"],
                    "station_name": target_stop["station_name"],
                    "distance_km": target_stop["distance_km"],
                    "distance_from_current_km": round(dist_to_target, 1),
                    "estimated_platform": platform_no,
                    "status": "UPCOMING",
                    "scheduled_arr": sched_arr_str,
                    "static_delay_min": round(current_delay_min, 1),  # Naive projection
                    "predicted_delay_min": predicted_delay,           # ML Dynamic prediction
                    "recovery_min": round(current_delay_min - predicted_delay, 1),
                    "delay_trend": trend,
                    "is_junction": target_stop["is_junction"],
                    "zone": target_stop["zone"],
                    "confidence_window": f"\u00b1{max(3.0, round(3.5 + 0.015 * feature_rows[idx]['distance_to_target'], 1))} min"
                })

        # Generate Human-Readable AI Operational Advisory
        advisory_flags = []
        if weather != "Clear": advisory_flags.append(f"Weather: {weather} (+{weather_penalty:.0f}m)")
        if congestion_level == "High": advisory_flags.append("Track Congestion: High (+8m)")
        if p_day > 0: advisory_flags.append(f"Traffic Pattern: {day_of_week} (+{p_day:.0f}m)")
        if p_occ > 0: advisory_flags.append(f"Event: {occasion} (+{p_occ:.0f}m)")
        if p_civ > 0: advisory_flags.append(f"Civil Condition: {civil_disruption} (+{p_civ:.0f}m)")
        if p_tech > 0: advisory_flags.append(f"Technical Defect: {technical_malfunction} (+{p_tech:.0f}m)")
        if p_tt > 0: advisory_flags.append(f"Timetable Clashing: {timetable_precedence} (+{p_tt:.0f}m)")

        advisory_text = " | ".join(advisory_flags) if advisory_flags else "Nominal operating track conditions across all divisions."

        return {
            "train_no": clean_no,
            "train_name": train_name,
            "train_type": raw_type,
            "priority_tier": priority,
            "weather": weather,
            "congestion": congestion_level,
            "day_of_week": day_of_week,
            "occasion": occasion,
            "civil_disruption": civil_disruption,
            "technical_malfunction": technical_malfunction,
            "timetable_precedence": timetable_precedence,
            "total_scenario_penalty_min": round(total_scenario_penalty, 1),
            "ai_operational_advisory": advisory_text,
            "current_station": current_stop["station_name"],
            "current_delay_min": current_delay_min,
            "stations_forecast": predictions
        }

if __name__ == "__main__":
    predictor = ETAPredictor.get_instance()
    sample = predictor.predict_downstream_eta(
        train_no="12673",
        current_station_idx=2,
        current_delay_min=30.0,
        weather="Clear",
        congestion_level="Normal"
    )
    print("Inference Test Result:")
    print(f"Train: {sample['train_name']} ({sample['train_no']})")
    print(f"Current Delay at {sample['current_station']}: {sample['current_delay_min']} mins")
    print("-" * 65)
    for stn in sample["stations_forecast"]:
        status = stn.get("status")
        trend = stn.get("delay_trend", "")
        delay = stn.get("predicted_delay_min", 0)
        rec = stn.get("recovery_min", 0)
        print(f"  {stn['station_code']:<5} {stn['station_name']:<25} | Sched: {stn['scheduled_arr']:<6} | Pred Delay: {delay:>5.1f}m | Trend: {trend:<11} | Recovery: {rec:>4.1f}m")
