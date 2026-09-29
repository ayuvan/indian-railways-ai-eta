"""
Indian Railways Dynamic ETA - Comprehensive Multilingual Localization (i18n)
Author: SIH AI Prototype
Description:
    Provides complete 4-language support across all prototype features:
    English (EN), Hindi (हिंदी - HI), Tamil (தமிழ் - TA), and Telugu (తెలుగు - TE).
    Covers Passenger Mobile App, What-If Disruption Simulator, Explainable AI (XAI)
    Attribution Drawer, Connection Rescue, Behavioral DNA, Distance Gradient Forecasts,
    Floating Quick Dock, and SIH Jury Evaluation Modal.
"""

from typing import Dict

TRANSLATIONS: Dict[str, Dict[str, str]] = {
    "en": {
        # Navigation & Portals
        "portal_passenger_app": "Passenger Mobile App",
        "portal_control_room": "Control Room Dashboard",
        "btn_sih_jury": "🏆 SIH Jury Mode",
        "ntes_live_active": "NTES Live Active",
        "audio_on": "🔊 Audio ON",
        "audio_muted": "🔇 Muted",
        
        # Header
        "title": "Indian Railways Dynamic AI ETA Forecasting",
        "subtitle": "Accurate Real-Time Train Forecast • Platform Allocations • Smart Connection Rescue",
        "ml_precision_badge": "ML Precision (±15m)",
        
        # Search & Carousel
        "search_train_placeholder": "Search by Train No, Name or Station (e.g. 12673, Cheran, Kovai, Mandovi)...",
        "search_button": "Track Train",
        "popular_trains": "Popular Trains:",
        "flagship_corridors_title": "⚡ Flagship Express Corridors",
        "flagship_corridors_sub": "Live Telemetry Feeds Available",
        "track_live_btn": "Track Live ➔",
        
        # Date Strip
        "journey_date_label": "Journey Date:",
        "today": "Today",
        
        # Boarding Pass Ticket
        "departure": "DEPARTURE",
        "arrival": "ARRIVAL",
        "dynamic_eta_prefix": "Dynamic ETA",
        "btn_track_map": "🗺️ Virtual Track Map",
        "btn_what_if": "⚡ What-If Simulator",
        "btn_explain_eta": "🧠 Explain My ETA",
        "est_platform": "Estimated Platform",
        "current_delay": "Current Delay",
        "live_gps_speed": "Live GPS Speed",
        "signal_ahead": "Signal Ahead",
        "signal_green": "GREEN (MPS)",
        "signal_yellow": "YELLOW (Caution 30 km/h)",
        "signal_double_yellow": "DOUBLE YELLOW (Prepare Halt)",
        "signal_red": "RED (Danger / Stop)",
        "rolling_stock_title": "⚡ TRACTION & ROLLING STOCK",
        "pnr_no": "PNR",
        "seat_no": "SEAT",
        "class_label": "CLASS",
        "status_confirmed": "CONFIRMED",
        
        # What-If Disruption Simulator
        "sim_title": "⚡ Interactive 'What-If' Scenario Simulator",
        "sim_note": "Recalculate dynamic arrival times based on real-time track conditions",
        "sim_loc_label": "📍 Simulate Current Location:",
        "sim_delay_label": "⏱️ Live Delay (min):",
        "weather_condition": "🌦️ Weather Factor:",
        "weather_clear": "☀️ Clear (Normal MPS 110 km/h)",
        "weather_rain": "🌧️ Heavy Monsoon Rain (-10 km/h)",
        "weather_fog": "🌫️ Dense Fog / FogPass (-30 km/h)",
        "track_congestion": "🚦 Track Headway:",
        "congestion_normal": "🟢 Normal Headway",
        "congestion_high": "🔴 High Bottleneck (Suburban Junction Hold)",
        "congestion_low": "⚡ Clear High-Speed Corridor",
        "sim_day_label": "📅 Day of the Week:",
        "sim_occasion_label": "🎪 Occasion / Public Event:",
        "sim_civil_label": "📢 Civil & Public Disruption:",
        "sim_tech_label": "🔧 Technical & Track Defect:",
        "sim_priority_label": "⏱️ Timetable & Priority Clash:",
        "btn_recalculate": "⚡ Recalculate Dynamic ETA",
        "btn_step_sim": "▶️ Advance Next Section",
        "btn_inject_delay": "⚠️ Inject 20m Signal Halt",
        "btn_reset_sim": "🔄 Reset Journey",
        
        # Explainable AI (XAI) Dropdown Drawer
        "xai_title": "Explainable AI (XAI) Attribution Breakdown",
        "xai_sub": "SHAP-Style Dynamic Decomposition • Transparent Operational Drivers",
        "xai_collapse": "▲ Collapse",
        "xai_confidence": "Confidence (160k Ground Truth)",
        "xai_net_delay": "Net Forecast Delay",
        "xai_factor_drivers": "Factor Drivers",
        "xai_model_version": "Model: Continual v1.2",
        "xai_factors_heading": "Decomposed Operational Factors (Additive SHAP Delta):",
        "xai_self_learning_active": "Bayesian Continual Self-Learning Engine: ACTIVE",
        "xai_calibration_locked": "Online Section Calibration: Locked",
        
        # Connection Rescue (Alternate Journeys)
        "rescue_title": "Automatic Alternate Journey Discovery (Connection Rescue)",
        "rescue_sub": "Train delay detected. Smart alternative train connections found on this corridor.",
        "rescue_badge": "Connection Rescue Active",
        
        # Train Behavioral Profile DNA
        "dna_title": "Train Behavioral Profile DNA (Quarterly Analysis)",
        "dna_sub": "Based on 2025 actual scraped running data across 90 days",
        "punctuality_score_label": "Punctuality Score:",
        "right_time_arrivals": "Right-Time Arrivals",
        "slight_delay": "Slight Delay (<30m)",
        "significant_delay": "Significant Delay (>60m)",
        "chronic_bottlenecks": "⚠️ Chronic Operating Bottlenecks (2025 Historical Scraping):",
        "recovery_pattern_label": "Speed Recovery Index:",
        
        # Downstream Station Forecast Table
        "table_title": "Dynamic Downstream Station Forecasts",
        "table_badge": "Adaptive ML Inference",
        "dist_gradient_label": "Distance Gradient:",
        "dist_grad_green": "🟢 <50km (Imminent)",
        "dist_grad_yellow": "🟡 50-150km (Mid Section)",
        "dist_grad_red": "🔴 >150km (Far Terminus)",
        "station": "Station",
        "th_platform": "Est. Platform",
        "th_dist_grad": "Proximity Gradient",
        "sched_arr": "Scheduled",
        "static_eta": "Static / Linear",
        "ai_eta": "Dynamic AI ETA",
        "delay": "Predicted Delay",
        "trend": "Trend",
        "recovery": "Buffer Recovery",
        "trend_recovering": "Recovering Time",
        "trend_compounding": "Compounding Delay",
        "trend_steady": "Maintaining Speed",
        "select_train_prompt": "Please search and select a train above to view dynamic ETA forecasts.",
        
        # Floating Quick Mobile Dock
        "dock_quick_menu": "QUICK MENU",
        "dock_ticket": "Ticket",
        "dock_map": "Track Map",
        "dock_sim": "Simulator",
        "dock_dna": "DNA Profile",
        "dock_staff": "Staff Radar",
        
        # SIH Jury Pitch & Benchmark Modal
        "jury_modal_title": "SIH Jury Pitch & Empirical Benchmark Verification",
        "jury_modal_sub": "Smart India Hackathon (SIH 2026) • Problem Statement ID: 26028 • Team ID: 151003",
        "tab_benchmarks": "📊 Empirical Verification (160k Segments)",
        "tab_scenarios": "⚡ 1-Click Live Disruption Demos",
        "tab_architecture": "🏗️ Architecture & Continual Learning",
        "tab_roi": "💰 Ministry Operational ROI",
        "jbs_ai_mae": "AI Champion MAE",
        "jbs_error_reduction": "Error Reduction",
        "jbs_sla_accuracy": "SLA Accuracy (±15m)",
        "jbs_r2": "R² Goodness of Fit",
        "demo_fog_btn": "🌫️ Dense Fog Caution (30 km/h)",
        "demo_festival_btn": "🪔 Diwali / Chhath Festival Surge (+3m/stop)",
        "demo_ohe_btn": "⚡ 25kV OHE Power Line Tripping (+35m)",
        "demo_kavach_btn": "🛡️ Inspect Live Kavach TCAS Radar",
        
        # Control Room Dashboard
        "cr_tracking_list": "Tracking List",
        "cr_search_placeholder": "Search Headcode or UID...",
        "cr_inject_red_signal": "⚠️ Inject Red Signal Halt",
        "cr_clear_block": "🟢 Clear Block Section",
        "cr_recenter": "🎯 Re-center",
        "cr_gis_map": "🗺️ GIS Rail Map",
        "cr_tactical_radar": "🎛️ Tactical Radar",
        "cr_stream_locked": "NTES 100Hz STREAM: LOCKED",
        "cr_ministry_roi": "Ministry ROI: ₹19.4 Cr/yr",
        "cr_public_portal": "Public Portal",
        "cr_staff_active": "Staff Active",
        
        # Common / Status
        "status_online": "ONLINE",
        "status_running": "Running",
        "minutes_late": "min Late",
        "minutes_early": "min Early",
        "right_time": "Right Time"
    },

    "hi": {
        # Navigation & Portals
        "portal_passenger_app": "यात्री मोबाइल ऐप",
        "portal_control_room": "कंट्रोल रूम डैशबोर्ड",
        "btn_sih_jury": "🏆 SIH जूरी मोड",
        "ntes_live_active": "NTES लाइव सक्रिय",
        "audio_on": "🔊 ऑडियो चालू",
        "audio_muted": "🔇 म्यूट",
        
        # Header
        "title": "भारतीय रेल गतिशील AI आगमन समय (ETA) पूर्वानुमान",
        "subtitle": "सटीक रियल-टाइम ट्रेन पूर्वानुमान • प्लेटफ़ॉर्म आवंटन • स्मार्ट वैकल्पिक यात्रा बचाव",
        "ml_precision_badge": "ML सटीकता (±15 मिनट)",
        
        # Search & Carousel
        "search_train_placeholder": "ट्रेन नंबर, नाम या स्टेशन से खोजें (उदा. 12673, Cheran, Kovai, Mandovi)...",
        "search_button": "ट्रेन खोजें",
        "popular_trains": "लोकप्रिय ट्रेनें:",
        "flagship_corridors_title": "⚡ प्रमुख एक्सप्रेस रेल गलियारे",
        "flagship_corridors_sub": "लाइव टेलीमेट्री फीड उपलब्ध",
        "track_live_btn": "लाइव ट्रैक करें ➔",
        
        # Date Strip
        "journey_date_label": "यात्रा की तिथि:",
        "today": "आज",
        
        # Boarding Pass Ticket
        "departure": "प्रस्थान",
        "arrival": "आगमन",
        "dynamic_eta_prefix": "गतिशील ETA",
        "btn_track_map": "🗺️ वर्चुअल ट्रैक मैप",
        "btn_what_if": "⚡ सिमुलेटर",
        "btn_explain_eta": "🧠 ETA का कारण जानें",
        "est_platform": "अनुमानित प्लेटफ़ॉर्म",
        "current_delay": "वर्तमान विलंब (देरी)",
        "live_gps_speed": "लाइव GPS गति",
        "signal_ahead": "आगे का सिग्नल",
        "signal_green": "हरा सिग्नल (अधिकतम गति)",
        "signal_yellow": "पीला सिग्नल (सावधानी 30 किमी/घंटा)",
        "signal_double_yellow": "दोहरा पीला (रुकने की तैयारी)",
        "signal_red": "लाल सिग्नल (खतरा / रुकें)",
        "rolling_stock_title": "⚡ इंजन एवं कोच रोलिंग स्टॉक",
        "pnr_no": "पीएनआर",
        "seat_no": "सीट",
        "class_label": "श्रेणी",
        "status_confirmed": "पुष्ट (CONFIRMED)",
        
        # What-If Disruption Simulator
        "sim_title": "⚡ इंटरएक्टिव 'व्हाट-इफ' परिचालन परिदृश्य सिम्युलेटर",
        "sim_note": "वास्तविक ट्रैक स्थितियों के आधार पर गतिशील आगमन समय की पुनर्गणना करें",
        "sim_loc_label": "📍 वर्तमान स्टेशन स्थिति चुनें:",
        "sim_delay_label": "⏱️ लाइव विलंब / देरी (मिनट):",
        "weather_condition": "🌦️ मौसम की स्थिति:",
        "weather_clear": "☀️ साफ मौसम (सामान्य गति 110 किमी/घंटा)",
        "weather_rain": "🌧️ भारी मानसूनी बारिश (-10 किमी/घंटा)",
        "weather_fog": "🌫️ घना कोहरा / फॉगपास डिवाइस (-30 किमी/घंटा)",
        "track_congestion": "🚦 ट्रैक संकुलन (ट्रैफिक):",
        "congestion_normal": "🟢 सामान्य ट्रैक दबाव",
        "congestion_high": "🔴 अत्यधिक भीड़ / उपनगरीय जंक्शन दबाव",
        "congestion_low": "⚡ खाली हाई-स्पीड रेल गलियारा",
        "sim_day_label": "📅 सप्ताह का दिन:",
        "sim_occasion_label": "🎪 विशेष अवसर / सार्वजनिक भीड़:",
        "sim_civil_label": "📢 नागरिक एवं सामाजिक व्यवधान:",
        "sim_tech_label": "🔧 तकनीकी एवं ट्रैक खराबी:",
        "sim_priority_label": "⏱️ समय सारिणी एवं वरीयता टकराव:",
        "btn_recalculate": "⚡ गतिशील ETA की पुनर्गणना करें",
        "btn_step_sim": "▶️ अगला खंड सिमुलेट करें",
        "btn_inject_delay": "⚠️ 20 मिनट सिग्नल हॉल्ट जोड़ें",
        "btn_reset_sim": "🔄 यात्रा रीसेट करें",
        
        # Explainable AI (XAI) Dropdown Drawer
        "xai_title": "व्याख्यात्मक AI (XAI) विलंब कारक विश्लेषण",
        "xai_sub": "SHAP-शैली गतिशील अपघटन • पारदर्शी परिचालन कारक",
        "xai_collapse": "▲ बंद करें",
        "xai_confidence": "सटीकता विश्वास (1.6 लाख वास्तविक डेटा)",
        "xai_net_delay": "कुल अनुमानित विलंब",
        "xai_factor_drivers": "प्रमुख परिचालन कारक",
        "xai_model_version": "मॉडल: निरंतर ऑनलाइन v1.2",
        "xai_factors_heading": "विभाजित परिचालन कारक (Additive SHAP Delta):",
        "xai_self_learning_active": "बायेसियन सतत सेल्फ-लर्निंग इंजन: सक्रिय",
        "xai_calibration_locked": "ऑनलाइन ट्रैक खंड कैलिब्रेशन: सक्रिय",
        
        # Connection Rescue (Alternate Journeys)
        "rescue_title": "स्वचालित वैकल्पिक यात्रा खोज (कनेक्शन रेस्क्यू)",
        "rescue_sub": "ट्रेन में देरी पाई गई। इस मार्ग पर स्मार्ट वैकल्पिक ट्रेन कनेक्शन उपलब्ध हैं।",
        "rescue_badge": "कनेक्शन रेस्क्यू सक्रिय",
        
        # Train Behavioral Profile DNA
        "dna_title": "ट्रेन व्यवहार प्रोफाइल डीएनए (त्रैमासिक विश्लेषण)",
        "dna_sub": "90 दिनों के वास्तविक स्क्रैप किए गए NTES डेटा पर आधारित",
        "punctuality_score_label": "समयपालन स्कोर:",
        "right_time_arrivals": "समय पर आगमन",
        "slight_delay": "मामूली देरी (<30 मिनट)",
        "significant_delay": "अधिक देरी (>60 मिनट)",
        "chronic_bottlenecks": "⚠️ प्रमुख ऐतिहासिक बाधा स्टेशन (Bottlenecks):",
        "recovery_pattern_label": "गति रिकवरी इंडेक्स:",
        
        # Downstream Station Forecast Table
        "table_title": "गतिशील आगामी स्टेशन आगमन पूर्वानुमान",
        "table_badge": "अनुकूली मशीन लर्निंग",
        "dist_gradient_label": "दूरी प्रवणता (Distance Gradient):",
        "dist_grad_green": "🟢 <50 किमी (निकट)",
        "dist_grad_yellow": "🟡 50-150 किमी (मध्य खंड)",
        "dist_grad_red": "🔴 >150 किमी (दूरस्थ स्टेशन)",
        "station": "स्टेशन",
        "th_platform": "अनुमानित प्लेटफ़ॉर्म",
        "th_dist_grad": "दूरी प्रवणता",
        "sched_arr": "निर्धारित समय",
        "static_eta": "पारंपरिक / रैखिक ETA",
        "ai_eta": "गतिशील AI ETA",
        "delay": "अनुमानित देरी",
        "trend": "रुझान",
        "recovery": "समय रिकवरी",
        "trend_recovering": "समय सुधर रहा है",
        "trend_compounding": "देरी बढ़ रही है",
        "trend_steady": "स्थिर गति",
        "select_train_prompt": "लाइव आगमन पूर्वानुमान देखने के लिए कृपया ऊपर ट्रेन चुनें।",
        
        # Floating Quick Mobile Dock
        "dock_quick_menu": "त्वरित मेनू",
        "dock_ticket": "टिकट",
        "dock_map": "ट्रैक मैप",
        "dock_sim": "सिम्युलेटर",
        "dock_dna": "डीएनए प्रोफाइल",
        "dock_staff": "कंट्रोल रडार",
        
        # SIH Jury Pitch & Benchmark Modal
        "jury_modal_title": "SIH जूरी प्रस्तुति एवं अनुभवजन्य मानक सत्यापन",
        "jury_modal_sub": "स्मार्ट इंडिया हैकाथॉन (SIH 2026) • समस्या विवरण ID: 26028 • टीम ID: 151003",
        "tab_benchmarks": "📊 अनुभवजन्य सत्यापन (1.6 लाख खंड)",
        "tab_scenarios": "⚡ 1-क्लिक लाइव व्यवधान डेमो",
        "tab_architecture": "🏗️ आर्किटेक्चर एवं सतत अधिगम",
        "tab_roi": "💰 रेलवे मंत्रालय वित्तीय बचत (ROI)",
        "jbs_ai_mae": "AI मॉडल औसत त्रुटि (MAE)",
        "jbs_error_reduction": "त्रुटि में शुद्ध कमी",
        "jbs_sla_accuracy": "मानक SLA सटीकता (±15 मिनट)",
        "jbs_r2": "R² फिट गुणवत्ता स्कोर",
        "demo_fog_btn": "🌫️ घना कोहरा सिमुलेट करें (30 किमी/घंटा)",
        "demo_festival_btn": "🪔 दिवाली / छठ भीड़ सिमुलेट करें (+3 मिनट/स्टॉप)",
        "demo_ohe_btn": "⚡ 25kV OHE बिजली तार टूटना (+35 मिनट देरी)",
        "demo_kavach_btn": "🛡️ लाइव कवच TCAS रडार देखें",
        
        # Control Room Dashboard
        "cr_tracking_list": "ट्रैकिंग सूची",
        "cr_search_placeholder": "ट्रेन या हेडकोड खोजें...",
        "cr_inject_red_signal": "⚠️ लाल सिग्नल रोक लगाएं",
        "cr_clear_block": "🟢 ब्लॉक सेक्शन क्लियर करें",
        "cr_recenter": "🎯 री-सेंटर करें",
        "cr_gis_map": "🗺️ GIS रेल मानचित्र",
        "cr_tactical_radar": "🎛️ सामरिक रडार",
        "cr_stream_locked": "NTES 100Hz स्ट्रीम: सक्रिय",
        "cr_ministry_roi": "मंत्रालय बचत: ₹19.4 करोड़/वर्ष",
        "cr_public_portal": "सार्वजनिक पोर्टल",
        "cr_staff_active": "स्टाफ सक्रिय",
        
        # Common / Status
        "status_online": "ऑनलाइन",
        "status_running": "चल रही है",
        "minutes_late": "मिनट देरी",
        "minutes_early": "मिनट पहले",
        "right_time": "सही समय पर"
    },

    "ta": {
        # Navigation & Portals
        "portal_passenger_app": "பயணிகள் மொபைல் ஆப்",
        "portal_control_room": "கட்டுப்பாட்டு அறை (Control Room)",
        "btn_sih_jury": "🏆 SIH நடுவர் பயன்முறை",
        "ntes_live_active": "NTES நேரலை இயங்குகிறது",
        "audio_on": "🔊 ஆடியோ ஆன்",
        "audio_muted": "🔇 ஒலியடக்கு",
        
        # Header
        "title": "இந்திய ரயில்வே டைனமிக் AI வருகை நேர முன்னறிவிப்பு (ETA)",
        "subtitle": "துல்லியமான நேரலை ரயில் கணிப்பு • நடைமேடை ஒதுக்கீடு • ஸ்மார்ட் மாற்று இணைப்பு ரயில்",
        "ml_precision_badge": "ML துல்லியம் (±15 நிமி)",
        
        # Search & Carousel
        "search_train_placeholder": "ரயில் எண், பெயர் அல்லது நிலையத்தை உள்ளிடவும் (எ.கா. 12673, Cheran, Kovai)...",
        "search_button": "ரயிலைக் கண்டுபிடி",
        "popular_trains": "பிரபலமான ரயில்கள்:",
        "flagship_corridors_title": "⚡ முதன்மை விரைவு ரயில் பாதைகள்",
        "flagship_corridors_sub": "நேரடி தொலை அளவீட்டு ஊட்டங்கள் கிடைக்கின்றன",
        "track_live_btn": "நேரலையைக் காண்க ➔",
        
        # Date Strip
        "journey_date_label": "பயணத் தேதி:",
        "today": "இன்று",
        
        # Boarding Pass Ticket
        "departure": "புறப்பாடு",
        "arrival": "வருகை",
        "dynamic_eta_prefix": "டைனமிக் ETA",
        "btn_track_map": "🗺️ வரைபடம்",
        "btn_what_if": "⚡ சிமுலேட்டர்",
        "btn_explain_eta": "🧠 ETA விளக்கம்",
        "est_platform": "மதிப்பிடப்பட்ட நடைமேடை",
        "current_delay": "தற்போதைய தாமதம்",
        "live_gps_speed": "நேரலை GPS வேகம்",
        "signal_ahead": "முன்னுள்ள சிக்னல்",
        "signal_green": "பச்சை (அதிகபட்ச வேகம்)",
        "signal_yellow": "மஞ்சள் (எச்சரிக்கை 30 கி.மீ/மணி)",
        "signal_double_yellow": "இரட்டை மஞ்சள் (நிறுத்தத் தயார்)",
        "signal_red": "சிவப்பு (ஆபத்து / நிறுத்து)",
        "rolling_stock_title": "⚡ இழுவை மற்றும் ரயில் பெட்டிகள்",
        "pnr_no": "பி.என்.ஆர்",
        "seat_no": "இருக்கை",
        "class_label": "வகுப்பு",
        "status_confirmed": "உறுதியானது (CONFIRMED)",
        
        # What-If Disruption Simulator
        "sim_title": "⚡ ஊடாடும் 'வாட்-இஃப்' பயண மாதிரி சிமுலேட்டர்",
        "sim_note": "நேரடி பாதை நிலைமைகளின் அடிப்படையில் வருகை நேரத்தை உடனடியாக மறு கணக்கீடு செய்யுங்கள்",
        "sim_loc_label": "📍 தற்போதைய நிலையத்தைத் தேர்வு செய்க:",
        "sim_delay_label": "⏱️ நேரலைத் தாமதம் (நிமிடம்):",
        "weather_condition": "🌦️ வானிலை காரணி:",
        "weather_clear": "☀️ தெளிவான வானிலை (இயல்பு வேகம் 110 கி.மீ/மணி)",
        "weather_rain": "🌧️ கனமழை (-10 கி.மீ/மணி)",
        "weather_fog": "🌫️ அடர்ந்த பனிமூட்டம் (-30 கி.மீ/மணி)",
        "track_congestion": "🚦 ரயில் பாதை நெரிசல்:",
        "congestion_normal": "🟢 இயல்பான பாதை",
        "congestion_high": "🔴 அதிக நெரிசல் (சந்திப்பு நிறுத்தம்)",
        "congestion_low": "⚡ தடையில்லா அதிவேகப் பாதை",
        "sim_day_label": "📅 வாரத்தின் நாள்:",
        "sim_occasion_label": "🎪 திருவிழா / கூட்ட நெரிசல்:",
        "sim_civil_label": "📢 பொதுப் போராட்டம் / மறியல்:",
        "sim_tech_label": "🔧 தொழில்நுட்ப மற்றும் பாதை பழுது:",
        "sim_priority_label": "⏱️ கால அட்டவணை முன்னுரிமை மோதல்:",
        "btn_recalculate": "⚡ AI வருகை நேரத்தை மறு கணக்கீடு செய்க",
        "btn_step_sim": "▶️ அடுத்த நிலைக்கு நகர்த்தவும்",
        "btn_inject_delay": "⚠️ 20 நிமிடம் சிக்னல் நிறுத்தம் சேர்க்கவும்",
        "btn_reset_sim": "🔄 பயணத்தை மீட்டமைக்க",
        
        # Explainable AI (XAI) Dropdown Drawer
        "xai_title": "விளக்கக்கூடிய AI (XAI) காரணிகள் பகுப்பாய்வு",
        "xai_sub": "SHAP முறைப்படியான முறிவு • வெளிப்படையான இயக்கக் காரணிகள்",
        "xai_collapse": "▲ மூடு",
        "xai_confidence": "நம்பகத்தன்மை (1.6 லட்சம் தரவுகள்)",
        "xai_net_delay": "மொத்த கணிக்கப்பட்ட தாமதம்",
        "xai_factor_drivers": "முக்கிய இயக்கக் காரணிகள்",
        "xai_model_version": "மாதிரி: தொடர் ஆன்லைன் v1.2",
        "xai_factors_heading": "பிரிக்கப்பட்ட செயல்பாட்டுக் காரணிகள் (Additive SHAP Delta):",
        "xai_self_learning_active": "பேய்சியன் தொடர் கற்றல் எஞ்சின்: செயலில் உள்ளது",
        "xai_calibration_locked": "ஆன்லைன் பாதை அளவுத்திருத்தம்: பூட்டப்பட்டது",
        
        # Connection Rescue (Alternate Journeys)
        "rescue_title": "தானியங்கி மாற்றுப் பயணக் கண்டுபிடிப்பு (ரெஸ்க்யூ)",
        "rescue_sub": "ரயில் தாமதம் கண்டறியப்பட்டது. இந்த வழித்தடத்தில் சிறந்த மாற்று ரயில்கள் உள்ளன.",
        "rescue_badge": "இணைப்பு ரெஸ்க்யூ செயலில் உள்ளது",
        
        # Train Behavioral Profile DNA
        "dna_title": "ரயில் செயல்பாட்டு நடத்தை DNA (காலாண்டு ஆய்வு)",
        "dna_sub": "90 நாள் உண்மையான NTES ரயில் தரவுகளின் அடிப்படையில்",
        "punctuality_score_label": "நேரந்தவறாமை மதிப்பீடு:",
        "right_time_arrivals": "சரியான நேர வருகை",
        "slight_delay": "சிறிய தாமதம் (<30 நிமிடம்)",
        "significant_delay": "அதிக தாமதம் (>60 நிமிடம்)",
        "chronic_bottlenecks": "⚠️ தொடர் தாமத நிலையங்கள் (Bottlenecks):",
        "recovery_pattern_label": "வேக மீட்புக் குறியீடு:",
        
        # Downstream Station Forecast Table
        "table_title": "அடுத்தடுத்த நிலையங்களுக்கான வருகை முன்னறிவிப்பு",
        "table_badge": "தழுவல் இயந்திர கற்றல்",
        "dist_gradient_label": "தொலைவு சாய்வு (Distance Gradient):",
        "dist_grad_green": "🟢 <50 கி.மீ (மிக அருகில்)",
        "dist_grad_yellow": "🟡 50-150 கி.மீ (நடுத்தர தூரம்)",
        "dist_grad_red": "🔴 >150 கி.மீ (தொலைதூர நிலையம்)",
        "station": "நிலையம்",
        "th_platform": "மதிப்பிடப்பட்ட நடைமேடை",
        "th_dist_grad": "அருகாமை சாய்வு",
        "sched_arr": "அட்டவணை நேரம்",
        "static_eta": "பழைய முறை ETA",
        "ai_eta": "டைனமிக் AI ETA",
        "delay": "கணிக்கப்பட்ட தாமதம்",
        "trend": "போக்கு",
        "recovery": "நேர மீட்பு",
        "trend_recovering": "நேரம் மீட்கப்படுகிறது",
        "trend_compounding": "தாமதம் அதிகரிக்கிறது",
        "trend_steady": "சீரான வேகம்",
        "select_train_prompt": "முன்னறிவிப்பைக் காண மேலே ரயிலைத் தேர்ந்தெடுக்கவும்.",
        
        # Floating Quick Mobile Dock
        "dock_quick_menu": "விரைவு மெனு",
        "dock_ticket": "டிக்கெட்",
        "dock_map": "வரைபடம்",
        "dock_sim": "சிமுலேட்டர்",
        "dock_dna": "DNA விவரம்",
        "dock_staff": "ரேடார்",
        
        # SIH Jury Pitch & Benchmark Modal
        "jury_modal_title": "SIH நடுவர் விளக்கக்காட்சி மற்றும் நேரடி தரவு சரிபார்ப்பு",
        "jury_modal_sub": "ஸ்மார்ட் இந்தியா ஹேக்கத்தான் (SIH 2026) • சிக்கல் அறிக்கை ID: 26028 • குழு ID: 151003",
        "tab_benchmarks": "📊 தரவு சரிபார்ப்பு (1.6 லட்சம் பகுதிகள்)",
        "tab_scenarios": "⚡ 1-கிளிக் நேரலை செயல்விளக்கம்",
        "tab_architecture": "🏗️ கட்டமைப்பு மற்றும் தொடர் கற்றல்",
        "tab_roi": "💰 அமைச்சக செயல்பாட்டுச் சேமிப்பு (ROI)",
        "jbs_ai_mae": "AI மாதிரி பிழை சராசரி (MAE)",
        "jbs_error_reduction": "பிழை குறைப்பு விகிதம்",
        "jbs_sla_accuracy": "SLA துல்லியம் (±15 நிமிடம்)",
        "jbs_r2": "R² பொருத்தம் அளவீடு",
        "demo_fog_btn": "🌫️ அடர்ந்த பனிமூட்டம் (30 கி.மீ/மணி)",
        "demo_festival_btn": "🪔 தீபாவளி / பொங்கல் கூட்ட நெரிசல் (+3 நிமி/நிறுத்தம்)",
        "demo_ohe_btn": "⚡ 25kV OHE மின் கம்பி துண்டிப்பு (+35 நிமிடம்)",
        "demo_kavach_btn": "🛡️ கவாச் TCAS ரேடாரைப் பார்க்கவும்",
        
        # Control Room Dashboard
        "cr_tracking_list": "கண்காணிப்பு பட்டியல்",
        "cr_search_placeholder": "ரயில் அல்லது ஹேட்கோட் தேடுக...",
        "cr_inject_red_signal": "⚠️ சிவப்பு சிக்னல் நிறுத்தம் புகுத்து",
        "cr_clear_block": "🟢 பிளாக் பகுதியை விடுவி",
        "cr_recenter": "🎯 மையப்படுத்து",
        "cr_gis_map": "🗺️ GIS ரயில் வரைபடம்",
        "cr_tactical_radar": "🎛️ கட்டுப்பாட்டு ரேடார்",
        "cr_stream_locked": "NTES 100Hz ஸ்ட்ரீம்: இணைக்கப்பட்டது",
        "cr_ministry_roi": "அமைச்சக சேமிப்பு: ₹19.4 கோடி/ஆண்டு",
        "cr_public_portal": "பொது தளம்",
        "cr_staff_active": "பணியாளர் தளம்",
        
        # Common / Status
        "status_online": "ஆன்லைன்",
        "status_running": "இயங்குகிறது",
        "minutes_late": "நிமிடம் தாமதம்",
        "minutes_early": "நிமிடம் முன்னதாக",
        "right_time": "சரியான நேரம்"
    },

    "te": {
        # Navigation & Portals
        "portal_passenger_app": "ప్రయాణీకుల మొబైల్ యాప్",
        "portal_control_room": "కంట్రోల్ రూమ్ డ్యాష్‌బోర్డ్",
        "btn_sih_jury": "🏆 SIH జ్యూరీ మోడ్",
        "ntes_live_active": "NTES లైవ్ క్రియాశీలం",
        "audio_on": "🔊 ఆడియో ఆన్",
        "audio_muted": "🔇 మ్యూట్",
        
        # Header
        "title": "భారతీయ రైల్వే డైనమిక్ AI రాక సమయ అంచనా (ETA)",
        "subtitle": "ఖచ్చితమైన రైలు రాక సమయ అంచనాలు • ప్లాట్‌ఫారమ్ కేటాయింపు • ప్రత్యామ్నాయ కనెక్షన్",
        "ml_precision_badge": "ML ఖచ్చితత్వం (±15 నిమి)",
        
        # Search & Carousel
        "search_train_placeholder": "రైలు సంఖ్య, పేరు లేదా స్టేషన్‌ను నమోదు చేయండి (ఉదా. 12673, Cheran, Kovai)...",
        "search_button": "రైలును శోధించండి",
        "popular_trains": "ప్రసిద్ధ రైళ్లు:",
        "flagship_corridors_title": "⚡ ప్రధాన ఎక్స్‌ప్రెస్ కారిడార్లు",
        "flagship_corridors_sub": "ప్రత్యక్ష టెలిమెట్రీ అందుబాటులో ఉంది",
        "track_live_btn": "లైవ్ ట్రాక్ చేయండి ➔",
        
        # Date Strip
        "journey_date_label": "ప్రయాణ తేదీ:",
        "today": "ఈరోజు",
        
        # Boarding Pass Ticket
        "departure": "బయలుదేరు సమయం",
        "arrival": "చేరుకునే సమయం",
        "dynamic_eta_prefix": "డైనమిక్ ETA",
        "btn_track_map": "🗺️ ట్రాక్ మ్యాప్",
        "btn_what_if": "⚡ సిమ్యులేటర్",
        "btn_explain_eta": "🧠 ETA కారణం",
        "est_platform": "అంచనా ప్లాట్‌ఫారమ్",
        "current_delay": "ప్రస్తుత ఆలస్యం",
        "live_gps_speed": "లైవ్ GPS వేగం",
        "signal_ahead": "ముందున్న సిగ్నల్",
        "signal_green": "గ్రీన్ (పూర్తి వేగం)",
        "signal_yellow": "ఎల్లో (జాగ్రత్త 30 కిమీ/గం)",
        "signal_double_yellow": "డబుల్ ఎల్లో (ఆగడానికి సిద్ధం)",
        "signal_red": "రెడ్ (ఆపండి / ప్రమాదం)",
        "rolling_stock_title": "⚡ ట్రాక్షన్ & ఇంజిన్ వివరాలు",
        "pnr_no": "పీఎన్ఆర్",
        "seat_no": "సీటు",
        "class_label": "తరగతి",
        "status_confirmed": "ధృవీకరించబడింది (CONFIRMED)",
        
        # What-If Disruption Simulator
        "sim_title": "⚡ ఇంటరాక్టివ్ 'వాట్-ఇఫ్' దృశ్య సిమ్యులేటర్",
        "sim_note": "ట్రాక్ పరిస్థితుల ఆధారంగా రాక సమయాన్ని తిరిగి లెక్కించండి",
        "sim_loc_label": "📍 ప్రస్తుత స్టేషన్ ఎంచుకోండి:",
        "sim_delay_label": "⏱️ లైవ్ ఆలస్యం (నిమిషాలు):",
        "weather_condition": "🌦️ వాతావరణం:",
        "weather_clear": "☀️ సాధారణ వాతావరణం (110 కిమీ/గం)",
        "weather_rain": "🌧️ భారీ వర్షం (-10 కిమీ/గం)",
        "weather_fog": "🌫️ దట్టమైన పొగమంచు (-30 కిమీ/గం)",
        "track_congestion": "🚦 ట్రాక్ రద్దీ:",
        "congestion_normal": "🟢 సాధారణ రద్దీ",
        "congestion_high": "🔴 అధిక రద్దీ / జంక్షన్ హోల్డ్",
        "congestion_low": "⚡ క్లియర్ హై-స్పీడ్ ట్రాక్",
        "sim_day_label": "📅 వారపు రోజు:",
        "sim_occasion_label": "🎪 పండుగ రద్దీ / ప్రత్యేక సందర్భం:",
        "sim_civil_label": "📢 ప్రజా ఆందోళన / రైల్ రోకో:",
        "sim_tech_label": "🔧 సాంకేతిక & ట్రాక్ లోపాలు:",
        "sim_priority_label": "⏱️ ప్రాధాన్యత రైలు క్రాసింగ్:",
        "btn_recalculate": "⚡ AI రాక సమయాన్ని తిరిగి లెక్కించండి",
        "btn_step_sim": "▶️ తదుపరి స్టేషన్ సిమ్యులేట్ చేయండి",
        "btn_inject_delay": "⚠️ 20 నిమిషాల సిగ్నల్ ఆలస్యం జోడించండి",
        "btn_reset_sim": "🔄 ప్రయాణాన్ని రీసెట్ చేయండి",
        
        # Explainable AI (XAI) Dropdown Drawer
        "xai_title": "వివరణాత్మక AI (XAI) ఆలస్య విశ్లేషణ",
        "xai_sub": "SHAP-శైలి విశ్లేషణ • పారదర్శక కార్యాచరణ అంశాలు",
        "xai_collapse": "▲ మూసివేయి",
        "xai_confidence": "ఖచ్చితత్వ విశ్వాసం (1.6 లక్షల రికార్డులు)",
        "xai_net_delay": "మొత్తం అంచనా ఆలస్యం",
        "xai_factor_drivers": "ప్రధాన కార్యాచరణ కారకాలు",
        "xai_model_version": "మోడల్: కంటిన్యూవల్ v1.2",
        "xai_factors_heading": "విభజించబడిన కార్యాచరణ కారకాలు (Additive SHAP Delta):",
        "xai_self_learning_active": "బయేసియన్ నిరంతర లెర్నింగ్ ఇంజిన్: క్రియాశీలం",
        "xai_calibration_locked": "ఆన్‌లైన్ ట్రాక్ క్రమాంకనం: పూర్తయింది",
        
        # Connection Rescue (Alternate Journeys)
        "rescue_title": "ఆటోమేటిక్ ప్రత్యామ్నాయ ప్రయాణ గుర్తింపు (కనెక్షన్ రెస్క్యూ)",
        "rescue_sub": "రైలు ఆలస్యం గుర్తించబడింది. ఈ మార్గంలో ప్రత్యామ్నాయ రైలు కనెక్షన్లు ఉన్నాయి.",
        "rescue_badge": "కనెక్షన్ రెస్క్యూ ఆన్ చేయబడింది",
        
        # Train Behavioral Profile DNA
        "dna_title": "రైలు ప్రవర్తన ప్రొఫైల్ DNA (త్రైమాసిక విశ్లేషణ)",
        "dna_sub": "90 రోజుల వాస్తవ NTES డేటా ఆధారంగా",
        "punctuality_score_label": "సమయపాలన స్కోర్:",
        "right_time_arrivals": "సరైన సమయానికి రాక",
        "slight_delay": "స్వల్ప ఆలస్యం (<30 నిమిషాలు)",
        "significant_delay": "అధిక ఆలస్యం (>60 నిమిషాలు)",
        "chronic_bottlenecks": "⚠️ దీర్ఘకాలిక ఆలస్య స్టేషన్లు (Bottlenecks):",
        "recovery_pattern_label": "వేగ రికవరీ సూచిక:",
        
        # Downstream Station Forecast Table
        "table_title": "రాబోయే స్టేషన్ల రాక సమయ అంచనాలు",
        "table_badge": "అడాప్టివ్ మెషిన్ లెర్నింగ్",
        "dist_gradient_label": "దూర సూచిక (Distance Gradient):",
        "dist_grad_green": "🟢 <50 కిమీ (చాలా దగ్గర)",
        "dist_grad_yellow": "🟡 50-150 కిమీ (మధ్యస్థ దూరం)",
        "dist_grad_red": "🔴 >150 కిమీ (సుదూర స్టేషన్)",
        "station": "స్టేషన్",
        "th_platform": "అంచనా ప్లాట్‌ఫారమ్",
        "th_dist_grad": "దూర సూచిక",
        "sched_arr": "షెడ్యూల్ సమయం",
        "static_eta": "పాత విధానపు ETA",
        "ai_eta": "డైనమిక్ AI ETA",
        "delay": "అంచనా వేసిన ఆలస్యం",
        "trend": "ఆలస్య ధోరణి",
        "recovery": "సమయ రికవరీ",
        "trend_recovering": "సమయం రికవర్ అవుతోంది",
        "trend_compounding": "ఆలస్యం పెరుగుతోంది",
        "trend_steady": "స్థిరమైన వేగం",
        "select_train_prompt": "లైవ్ అంచనాలను చూడటానికి దయచేసి పైన రైలును ఎంచుకోండి.",
        
        # Floating Quick Mobile Dock
        "dock_quick_menu": "త్వరిత మెనూ",
        "dock_ticket": "టికెట్",
        "dock_map": "ట్రాక్ మ్యాప్",
        "dock_sim": "సిమ్యులేటర్",
        "dock_dna": "DNA ప్రొఫైల్",
        "dock_staff": "కంట్రోల్ రడార్",
        
        # SIH Jury Pitch & Benchmark Modal
        "jury_modal_title": "SIH జ్యూరీ ప్రదర్శన & గణాంక ధృవీకరణ",
        "jury_modal_sub": "స్మార్ట్ ఇండియా హ్యాకథాన్ (SIH 2026) • సమస్య ప్రకటన ID: 26028 • జట్టు ID: 151003",
        "tab_benchmarks": "📊 గణాంక ధృవీకరణ (1.6 లక్షల విభాగాలు)",
        "tab_scenarios": "⚡ 1-క్లిక్ లైవ్ డెమోలు",
        "tab_architecture": "🏗️ ఆర్కిటెక్చర్ & నిరంతర అభ్యాసం",
        "tab_roi": "💰 మంత్రిత్వ శాఖ నిర్వహణ ఆదా (ROI)",
        "jbs_ai_mae": "AI మోడల్ సగటు లోపం (MAE)",
        "jbs_error_reduction": "లోపం తగ్గింపు శాతం",
        "jbs_sla_accuracy": "SLA ఖచ్చితత్వం (±15 నిమిషాలు)",
        "jbs_r2": "R² అనుకూలత స్కోర్",
        "demo_fog_btn": "🌫️ దట్టమైన పొగమంచు (30 కిమీ/గం)",
        "demo_festival_btn": "🪔 దీపావళి / సంక్రాంతి రద్దీ (+3 నిమి/స్టాప్)",
        "demo_ohe_btn": "⚡ 25kV OHE విద్యుత్ వైరు తెగిపోవడం (+35 నిమి)",
        "demo_kavach_btn": "🛡️ లైవ్ కవచ్ TCAS రడార్ చూడండి",
        
        # Control Room Dashboard
        "cr_tracking_list": "ట్రాకింగ్ జాబితా",
        "cr_search_placeholder": "రైలు లేదా హెడ్‌కోడ్ శోధించండి...",
        "cr_inject_red_signal": "⚠️ ఎరుపు సిగ్నల్ నిలుపుదల",
        "cr_clear_block": "🟢 బ్లాక్ సెక్షన్ క్లియర్ చేయండి",
        "cr_recenter": "🎯 రీ-సెంటర్ చేయండి",
        "cr_gis_map": "🗺️ GIS రైలు మ్యాప్",
        "cr_tactical_radar": "🎛️ టాక్టికల్ రాడార్",
        "cr_stream_locked": "NTES 100Hz స్ట్రీమ్: లాక్ చేయబడింది",
        "cr_ministry_roi": "మంత్రిత్వ శాఖ ఆదా: ₹19.4 కోట్లు/సంవత్సరం",
        "cr_public_portal": "ప్రజా పోర్టల్",
        "cr_staff_active": "సిబ్బంది పోర్టల్",
        
        # Common / Status
        "status_online": "ఆన్‌లైన్",
        "status_running": "నడుస్తోంది",
        "minutes_late": "నిమిషాలు ఆలస్యం",
        "minutes_early": "నిమిషాలు ముందుగా",
        "right_time": "సరైన సమయానికి"
    }
}

def get_i18n(lang: str = "en") -> Dict[str, str]:
    """Returns the translation dictionary for the selected language."""
    return TRANSLATIONS.get(lang.lower(), TRANSLATIONS["en"])
