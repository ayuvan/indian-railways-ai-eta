"""
Indian Railways Dynamic ETA - Intelligent Staff Scheduling & Resource Auto-Rescheduler
Author: SIH AI Prototype
Description:
    Automatically adapts crew rosters, coach cleaning shifts, catering load windows,
    and station platform assignments dynamically to real-time AI predicted arrivals.
"""

from typing import Dict, Any, List
from datetime import datetime, timedelta

class IntelligentStaffScheduler:
    """Dynamically re-rosters railway staff and contractor services based on ML ETAs."""

    @staticmethod
    def compute_dynamic_staff_schedule(
        train_no: str,
        train_name: str,
        current_station: str,
        next_station: str,
        scheduled_arrival: str,
        predicted_delay_min: float,
        is_junction: bool
    ) -> Dict[str, Any]:
        """
        Generates automated shift adjustments and work schedules for railway operations.
        """
        delay = float(predicted_delay_min)
        
        # 1. Loco Pilot & Guard Running Staff (HOER Compliance)
        # Base shift duration + accumulated delay
        nominal_shift_hours = 4.2
        projected_total_duty = round(nominal_shift_hours + (delay / 60.0), 2)
        
        if projected_total_duty >= 7.5:
            crew_action = "CRITICAL HOER LIMIT BREACH IMMINENT: Dynamic Relief Crew Auto-Dispatched to Platform"
            crew_status = "RELIEF_DISPATCHED"
            crew_shift_adjustment = f"Duty extending to {projected_total_duty}h (Limit: 8.0h). Replacement crew summoned at {next_station}."
        elif projected_total_duty >= 6.0:
            crew_action = "DUTY MONITORING: Running Room rest slot deferred by +{} min".format(int(delay))
            crew_status = "SHIFT_EXTENDED"
            crew_shift_adjustment = f"Projected shift duration: {projected_total_duty}h. Outstation rest book updated."
        else:
            crew_action = "DUTY NORMAL: Crew running within standard shift hours"
            crew_status = "ON_SCHEDULE"
            crew_shift_adjustment = f"Projected shift: {projected_total_duty}h. No relief intervention required."

        # 2. Cleaning & Coach Watering Services
        cleaning_lead = 15  # min before train arrives
        if delay > 15:
            cleaning_status = "ROSTER_AUTO_DELAYED"
            cleaning_shift = f"Shift start pushed by +{int(delay)} min. Contractor team alerted to assemble 10 min prior to updated ETA."
            cleaning_personnel = "12 Sanitation Workers + 2 High-Pressure Jet Operators (Standby re-timed)"
        else:
            cleaning_status = "ROSTER_ON_TIME"
            cleaning_shift = "Cleaning crew staged on allocated platform as per schedule."
            cleaning_personnel = "12 Sanitation Workers (Staged)"

        # 3. Platform Master & Porter Allocation
        platform_id = f"PF-{(abs(hash(train_no)) % 4) + 1}"
        if delay > 30:
            platform_assignment = f"{platform_id} (Dynamic Turnaround Adjusted)"
            platform_notice = f"Train arriving {int(delay)}m behind schedule. Platform dwell compressed to 8 mins for timetable recovery."
        else:
            platform_assignment = f"{platform_id} (Standard Berth)"
            platform_notice = "Standard 15-minute berthing window secured."

        # 4. Station Catering & Parcel Handling
        pantry_shift = f"Pantry car meals load slot shifted by +{int(delay)} min to match dynamic arrival at {next_station}."
        parcel_notice = f"Mail/Parcel van loading team notified of dynamic ETA (+{int(delay)}m)."

        return {
            "train_no": train_no,
            "train_name": train_name,
            "station": next_station,
            "predicted_delay_min": delay,
            "estimated_platform": platform_assignment,
            "platform_notice": platform_notice,
            "running_crew_hoer": {
                "status": crew_status,
                "projected_duty_hours": projected_total_duty,
                "regulatory_max_hours": 8.0,
                "action": crew_action,
                "details": crew_shift_adjustment
            },
            "cleaning_services": {
                "status": cleaning_status,
                "shift_adjustment": cleaning_shift,
                "personnel_allocated": cleaning_personnel,
                "service_window": "Quick Turnaround (Coach Watering + Bio-Toilet Flushing)"
            },
            "station_logistics": {
                "catering_load_sync": pantry_shift,
                "parcel_handling": parcel_notice
            }
        }

scheduler_instance = IntelligentStaffScheduler()
