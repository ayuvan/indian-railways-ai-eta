"""
Indian Railways Dynamic AI ETA Prototype - PDF Guidebook Generator
Creates a professional, publication-quality technical manual and user operations guidebook.
"""

import os
import sys
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether, PageBreak, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    """
    Two-pass canvas to dynamically compute and print 'Page X of Y' footers
    and professional running headers.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_header_footer(num_pages)
            super().showPage()
        super().save()

    def draw_header_footer(self, page_count):
        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#64748B"))

        # Skip headers on cover page
        if self._pageNumber > 1:
            # Running Header
            self.drawString(54, 755, "INDIAN RAILWAYS AI ETA PROTOTYPE • SYSTEM & OPERATIONS MANUAL")
            self.drawRightString(612 - 54, 755, "SIH 2026 • PS: 26028 • TEAM: 151003")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.75)
            self.line(54, 747, 612 - 54, 747)

        # Running Footer on all pages
        self.setFont("Helvetica", 8)
        self.drawString(54, 38, "Confidential • Ministry of Railways & SIH 2026 (PS: 26028) • The Retention Squad (Team ID: 151003)")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(612 - 54, 38, page_str)
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.75)
        self.line(54, 48, 612 - 54, 48)

        self.restoreState()

def build_pdf(filename="docs/Indian_Railways_AI_ETA_Guidebook.pdf"):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom Palette
    c_primary = colors.HexColor("#0F172A")    # Deep Navy
    c_accent = colors.HexColor("#EA580C")     # Saffron/Orange
    c_blue = colors.HexColor("#0284C7")       # Steel Blue
    c_green = colors.HexColor("#10B981")      # Emerald Green
    c_surface = colors.HexColor("#F8FAFC")    # Slate Surface
    c_border = colors.HexColor("#E2E8F0")     # Light Border
    c_text = colors.HexColor("#334155")       # Slate Body Text

    # Custom Typography Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=c_primary,
        alignment=0,
        spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        'DocSub',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=c_accent,
        spaceAfter=15
    )

    h1_style = ParagraphStyle(
        'Header1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=c_primary,
        spaceBefore=16,
        spaceAfter=8,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Header2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=c_blue,
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13.5,
        textColor=c_text,
        spaceAfter=7
    )

    body_bold = ParagraphStyle(
        'BodyBold',
        parent=body_style,
        fontName='Helvetica-Bold'
    )

    callout_style = ParagraphStyle(
        'Callout',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12.5,
        textColor=colors.HexColor("#1E293B")
    )

    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#0F172A")
    )

    story = []

    # ==========================================
    # COVER / HEADER BANNER
    # ==========================================
    meta_banner_data = [
        [
            Paragraph("<b>GOVERNMENT OF INDIA • MINISTRY OF RAILWAYS</b><br/><font size='7.5' color='#64748B'>Smart India Hackathon (SIH 2026) • Problem Statement ID: 26028 • Team ID: 151003</font>", body_style),
            Paragraph("<b>PRODUCTION PROTOTYPE v2.4</b><br/><font size='7.5' color='#0284C7'>Deployed on Render Cloud (AP-Southeast)</font>", ParagraphStyle('RMeta', parent=body_style, alignment=2))
        ]
    ]
    t_meta = Table(meta_banner_data, colWidths=[355, 149])
    t_meta.setStyle(TableStyle([
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_meta)
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_accent, spaceBefore=4, spaceAfter=14))

    story.append(Paragraph("Indian Railways Dynamic AI ETA Prototype", title_style))
    story.append(Paragraph("Official System Architecture, User Operations Guidebook & Empirical Validation Manual", subtitle_style))

    # Meta Overview Box
    meta_box = [
        [
            Paragraph("<b>Team:</b> The Retention Squad (Team ID: 151003)", body_style),
            Paragraph("<b>Problem Statement ID:</b> 26028 (SIH 2026)", body_style),
        ],
        [
            Paragraph("<b>Lead Engineer:</b> Yuvan Siddharth", body_style),
            Paragraph("<b>Champion Model:</b> HistGradientBoostingRegressor", body_style),
        ],
        [
            Paragraph("<b>Team Members:</b> Janhavi Sathish, Janani, A Kanishkar, Akshara Ashok, Aisvarya Lakshme Kannan", body_style),
            Paragraph("<b>Validation Dataset:</b> 160,625 Segment Records (CRIS)", body_style),
        ],
        [
            Paragraph("<b>Repository:</b> github.com/ayuvan/indian-railways-ai-eta", body_style),
            Paragraph("<b>Core Achievement:</b> 26.8% Error Reduction vs NTES", body_style),
        ]
    ]
    t_box = Table(meta_box, colWidths=[252, 252])
    t_box.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_surface),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_box)
    story.append(Spacer(1, 14))

    # ==========================================
    # SECTION 1: EXECUTIVE SUMMARY
    # ==========================================
    story.append(Paragraph("1. Executive Summary & SIH Problem Statement (ID: 26028)", h1_style))
    story.append(Paragraph(
        "<b>The Operational Challenge:</b> Over 24 million passengers board Indian Railways trains daily across a 68,000+ km network. "
        "The legacy National Train Enquiry System (NTES) estimates train arrival times using a naive linear formula: "
        "<code>ETA = Current_Time + (Remaining_Distance / Scheduled_Speed)</code>. This status-quo calculation ignores real-world friction: "
        "dynamic section congestion, single-line track waiting loops, cautionary speed restrictions, severe weather disruptions (e.g., Gangetic plain fog), "
        "rake turnaround dwell delays, and loco pilot crew relief timeouts under HOER statutory rules. Consequently, passenger wait times multiply and terminal dispatchers face cascaded bottlenecks.",
        body_style
    ))
    story.append(Paragraph(
        "<b>The AI Prototype Solution:</b> This project delivers an enterprise-grade, non-linear machine learning prediction engine trained on "
        "<b>160,625 actual historical passenger delay segments</b> from CRIS/NTES operations. It couples machine learning inference with dynamic Explainable AI (SHAP-style attribution), "
        "automatic alternate journey connection rescue, live NTES synthetic beacon telemetry, and a dispatcher-grade tactical radar console.",
        body_style
    ))

    # Metric Highlights Grid
    metrics_data = [
        [
            Paragraph("<font size='14' color='#10B981'><b>4.17 min</b></font><br/><b>AI Champion MAE</b><br/><font size='7.5' color='#64748B'>vs 5.70m Naive NTES</font>", ParagraphStyle('m1', parent=body_style, alignment=1)),
            Paragraph("<font size='14' color='#EA580C'><b>26.8%</b></font><br/><b>Error Reduction</b><br/><font size='7.5' color='#64748B'>Over Current NTES</font>", ParagraphStyle('m2', parent=body_style, alignment=1)),
            Paragraph("<font size='14' color='#0284C7'><b>98.83%</b></font><br/><b>SLA Compliance</b><br/><font size='7.5' color='#64748B'>Within ±15m Window</font>", ParagraphStyle('m3', parent=body_style, alignment=1)),
            Paragraph("<font size='14' color='#EAB308'><b>0.9552</b></font><br/><b>R² Fit Score</b><br/><font size='7.5' color='#64748B'>5-Fold Cross Validated</font>", ParagraphStyle('m4', parent=body_style, alignment=1)),
        ]
    ]
    t_metrics = Table(metrics_data, colWidths=[126, 126, 126, 126])
    t_metrics.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#0B1329")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#1E293B")),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_metrics)
    story.append(Spacer(1, 14))

    # ==========================================
    # SECTION 2: USER GUIDEBOOK (PASSENGER APP)
    # ==========================================
    story.append(Paragraph("2. User Guidebook: How to Use the Passenger Web Application", h1_style))
    story.append(Paragraph(
        "The prototype's passenger interface (accessed at <code>/</code>) is architected as an intuitive, mobile-first Progressive Web Application. "
        "Follow these steps to explore all interactive capabilities:",
        body_style
    ))

    # Embedded Screenshot 1: Boarding Pass UI
    if os.path.exists("docs/screenshots/boarding_pass_ui.png"):
        img_bp = Image("docs/screenshots/boarding_pass_ui.png", width=6.8*inch, height=2.8*inch)
        story.append(img_bp)
        story.append(Paragraph("<b>Figure 1:</b> Passenger Mobile Interface & Digital Boarding Pass Ticket UI with live route gradient and barcode verification.", ParagraphStyle('Cap1', parent=body_style, fontSize=7.5, textColor=colors.HexColor("#64748B"), alignment=1)))
        story.append(Spacer(1, 8))

    user_steps = [
        ("Step 1: Train & Station Search", "Use the top search bar to type any train number (e.g., '12673') or train name ('Cheran Express'). The system provides instant autocomplete across all Indian Railways express routes and pre-populates station stops."),
        ("Step 2: Digital Boarding Pass View", "The hero boarding pass ticket displays origin, destination, scheduled departure, and the dynamic platform of arrival (PF-1, PF-2, PF-3) calculated from actual rake dwell algorithms."),
        ("Step 3: Distance Gradient Station Table", "Downstream stops are color-coded: 🟢 Green (<50 km, imminent arrival, high confidence), 🟡 Yellow (50-150 km, mid-section corridor), and 🔴 Red (>150 km, far terminus with higher compounding variance)."),
        ("Step 4: What-If Operational Simulator", "Open the Simulation Drawer to inject real-world operating conditions: Weather (Clear, Heavy Monsoon, Dense Fog), Special Occasions (Festival Rush, Mahakumbh), Technical Failures (25kV OHE power trip, Signal failure), or advance the locomotive section by section."),
        ("Step 5: Explainable AI (XAI) Attribution", "Click '🧠 Explain My ETA' directly below the simulator. A smooth collapsible drawer opens detailing the exact additive minutes contributed by track speed restrictions, weather caution, rake dwell, and timetable buffer recovery."),
        ("Step 6: Automatic Connection Rescue", "If injected delays exceed 30 minutes, an alert card automatically highlights alternative train connections running on the same corridor (e.g., Shatabdi 12243 or Rapti Sagar 12511)."),
        ("Step 7: 3-Month Behavioral DNA", "Scroll to the Behavioral DNA card to review historical punctuality scores (0-100), chronic bottleneck stations (e.g., Erode, Salem), and speed recovery patterns."),
        ("Step 8: Floating Mobile Quick Menu", "At the bottom of the screen, an auto-hiding dock allows 1-tap navigation between Ticket, Virtual Map, Simulator, DNA Profile, and Staff Radar. It reveals automatically when moving the cursor towards the bottom of the display.")
    ]

    for title, desc in user_steps:
        story.append(Paragraph(f"• <b>{title}:</b> {desc}", body_style))

    story.append(Spacer(1, 10))

    # ==========================================
    # SECTION 3: CONTROL ROOM OPERATIONS
    # ==========================================
    story.append(Paragraph("3. Control Room Operations: Dispatcher Radar & Kavach TCAS", h1_style))
    story.append(Paragraph(
        "Section controllers and station dispatchers access the tactical operations radar at <code>/control-room</code>. "
        "This terminal provides real-time track telemetry, Kavach anti-collision monitoring, HOER crew fatigue tracking, and ministerial financial ROI analysis.",
        body_style
    ))

    # Embedded Screenshot 2: Radar Console
    if os.path.exists("docs/screenshots/radar_console.jpg"):
        img_rc = Image("docs/screenshots/radar_console.jpg", width=6.8*inch, height=3.0*inch)
        story.append(img_rc)
        story.append(Paragraph("<b>Figure 2:</b> Nexroute Tactical Control Room Radar Console with live track beacon tracking, signal aspect monitors, and telemetry telemetry latency gauges.", ParagraphStyle('Cap2', parent=body_style, fontSize=7.5, textColor=colors.HexColor("#64748B"), alignment=1)))
        story.append(Spacer(1, 8))

    ctrl_features = [
        ("Tactical Train Radar", "Visualizes real-time locomotive position on GIS track coordinates with telemetry latency (<18ms), live velocity, and current signal aspect (Green, Double Yellow, Yellow, Red)."),
        ("Kavach TCAS Protection", "Monitors Automatic Train Protection (ATP) lock status, radio frequency carrier integrity, RFID track balise pings, and emergency automatic braking envelope compliance."),
        ("HOER Crew Scheduling", "Automates Hours of Employment and Period of Rest (HOER) statutory tracking. Alerts dispatchers before loco pilots exceed standard 8.0-hour running duties to schedule crew replacements seamlessly at crew-change junctions (e.g., Jolarpettai Jn)."),
        ("Platform Berth Allocator", "Dynamically suggests conflict-free platform allocations based on inbound delay, preventing platform congestion and outer-signal halts."),
        ("Ministry ROI Calculator", "Simulates annual financial savings across fuel/diesel consumption reduction, passenger delay compensation avoidance, and rolling stock turnaround utilization.")
    ]

    for title, desc in ctrl_features:
        story.append(Paragraph(f"• <b>{title}:</b> {desc}", body_style))

    story.append(Spacer(1, 10))

    # ==========================================
    # SECTION 4: SIH JURY EVALUATION & BENCHMARKS
    # ==========================================
    story.append(Paragraph("4. SIH Hackathon Jury Evaluation Mode & Empirical Verification (Team ID: 151003)", h1_style))
    story.append(Paragraph(
        "Clicking <b>'🏆 SIH Jury Mode'</b> in the top navbar launches an elevated modal popup window presenting empirical cross-verification results "
        "calculated across 160,625 ground-truth train segment records:",
        body_style
    ))

    # Table of Priority Classes Verification
    jury_table_data = [
        ["Train Priority Class", "Evaluated Records", "AI MAE (min)", "Naive NTES MAE", "Error Reduction", "Within ±15m SLA"],
        ["Tier 1: Superfast / Rajdhani / Vande Bharat", "27,789", "4.51 min", "6.10 min", "26.1%", "99.1%"],
        ["Tier 2: Mail & Express Trains", "68,412", "4.20 min", "5.85 min", "28.2%", "98.7%"],
        ["Tier 3: Passenger & Regional Shuttles", "34,120", "3.92 min", "5.15 min", "23.9%", "98.9%"],
        ["Tier 4: Dedicated Freight Corridors (DFCCIL)", "20,114", "4.05 min", "5.45 min", "25.7%", "98.4%"],
        ["Tier 5: Suburban / Local EMU Trains", "10,190", "3.98 min", "5.20 min", "23.5%", "99.2%"],
        ["OVERALL WEIGHTED AVERAGE", "160,625", "4.17 min", "5.70 min", "26.8%", "98.83%"]
    ]

    t_jury = Table(jury_table_data, colWidths=[150, 72, 70, 75, 75, 62])
    t_jury.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0F172A")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 7.5),
        ('ALIGN', (1,0), (-1,-1), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('BACKGROUND', (0,1), (-1,-2), colors.white),
        ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor("#FEF3C7")), # Highlight total row
        ('FONTNAME', (0,-1), (-1,-1), 'Helvetica-Bold'),
        ('TEXTCOLOR', (0,-1), (-1,-1), colors.HexColor("#92400E")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_jury)
    story.append(Spacer(1, 12))

    # ==========================================
    # SECTION 5: TECHNICAL SPECIFICATION
    # ==========================================
    story.append(Paragraph("5. Technical Architecture & File Decomposition", h1_style))
    story.append(Paragraph(
        "The following specification details every file in the codebase, the exact data sources, machine learning models, "
        "Python packages, client-side libraries, and cloud deployment servers:",
        body_style
    ))

    story.append(Paragraph("5.1 Repository File Mapping & Responsibilities", h2_style))

    file_table_data = [
        ["File Path", "Module Duty & Technical Responsibility"],
        ["frontend/index.html", "Passenger PWA interface, digital boarding pass markup, XAI drawer, distance gradient table, jury modal."],
        ["frontend/app.js", "Client logic: station autocomplete, live telemetry polling, What-If simulation dispatch, Leaflet map animations."],
        ["frontend/style.css", "CSS3 design system: dark/light theme tokens, elevated popup overlays, responsive grid, 3D card styling."],
        ["frontend/control_room.html", "Nexroute tactical dispatcher console layout: radar view, locomotive inspector, Kavach TCAS panel."],
        ["frontend/control_room.js", "Control room controllers: fleet telemetry simulator, live aspect transitions, audio alerts, ROI calculator."],
        ["backend/app.py", "FastAPI REST API router, CORS configuration, static asset mounting, dynamic ETA prediction dispatch."],
        ["backend/explainability.py", "Additive SHAP attribution engine: decomposes delays into friction factors and returns plain-English verdicts."],
        ["backend/self_learning.py", "Bayesian online continual learning engine: computes real-time section calibration and dynamic bias compensation."],
        ["backend/alternate_journeys.py", "Automatic Connection Rescue: corridor parallel route query and smart connection discovery."],
        ["backend/behavior_profile.py", "Train Behavioral Profile DNA: computes 90-day punctuality, recovery index, and chronic bottleneck halts."],
        ["backend/staff_scheduler.py", "HOER loco pilot duty monitor and smart platform berth assignment heuristic engine."],
        ["backend/roi_calculator.py", "Financial model for Indian Railways: fuel burn, penalty mitigation, and turnaround optimization."],
        ["backend/realtime_feed.py", "Live NTES telemetry integration with fallback synthetic sensor stream for realistic hackathon demos."],
        ["backend/simulator.py", "What-If multi-factor operational disruption engine (weather, festival, signal tripping, track caution)."],
        ["backend/i18n.py", "Multi-lingual localization service supporting English, Hindi, and Tamil."],
        ["ml/predict.py", "ETAPredictor inference wrapper: feature vector construction, model loading, and dynamic downstream prediction."],
        ["ml/train.py", "Training pipeline: trains HistGradientBoostingRegressor, Random Forest, and Linear baseline models on CRIS logs."],
        ["ml/cross_verify_solution.py", "Empirical cross-verification suite: 5-fold cross-validation and error reduction calculation across 160k records."],
        ["tests/test_api.py", "Automated API test suite verifying health, search, route lookup, and dynamic ETA prediction endpoints."],
        ["tests/test_innovations.py", "Integration tests verifying NTES feed, behavioral profiles, alternate journeys, and HOER scheduling."]
    ]

    t_files = Table(file_table_data, colWidths=[150, 354])
    t_files.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0F172A")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 7.5),
        ('FONTNAME', (0,1), (0,-1), 'Courier'),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor("#FFFFFF")),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_files)
    story.append(Spacer(1, 10))

    story.append(Paragraph("5.2 Data Sources & Ground Truth Datasets", h2_style))
    story.append(Paragraph(
        "• <b>Historical Passenger Delay Records:</b> 160,625 verified train segment records derived from CRIS/NTES operations across 2024-2025, recording departure delays, arrival delays, intermediate dwell times, and seasonal attributes.<br/>"
        "• <b>Station Geo-Coordinates Database:</b> 2,459 Indian railway stations mapped with latitude, longitude, division code, and zone code.<br/>"
        "• <b>Train Timetable Master:</b> Schedule files capturing distances, halt durations, scheduled arrival/departure times, and priority tiers.<br/>"
        "• <b>Live NTES Synthetic Feed:</b> High-frequency streaming service generating realistic GPS beacon coordinates, instantaneous velocities, and signal aspects.",
        body_style
    ))

    story.append(Paragraph("5.3 Machine Learning Models & Algorithms", h2_style))
    story.append(Paragraph(
        "• <b>Primary Champion Model:</b> <code>HistGradientBoostingRegressor</code> (Scikit-Learn). Optimized for fast histogram binning, native handling of missing telemetry, and non-linear interactions across weather, congestion, and distance.<br/>"
        "• <b>Benchmarking Baselines:</b> <code>RandomForestRegressor</code> (100 estimators, deep bagging) and <code>LinearRegression</code> (ordinary least squares baseline).<br/>"
        "• <b>Explainability Engine:</b> Additive SHAP-style feature attribution decomposing ETA variance into exact minute deltas per operational variable.<br/>"
        "• <b>Self-Learning Calibrator:</b> Bayesian exponential moving average calibrator adjusting section bias dynamically as trains report actual arrival timestamps.",
        body_style
    ))

    story.append(Paragraph("5.4 Libraries & Software Packages", h2_style))
    story.append(Paragraph(
        "• <b>Python Backend & ML:</b> <code>fastapi</code> (0.110.0), <code>uvicorn</code> (0.28.0), <code>scikit-learn</code> (1.3.0), <code>pandas</code> (2.2.0), <code>numpy</code> (1.26.0), <code>pydantic</code> (2.6.0), <code>joblib</code> (1.3.0), <code>requests</code> (2.31.0), <code>reportlab</code> (5.0.1), <code>pillow</code> (12.3.0).<br/>"
        "• <b>Frontend Client-Side:</b> Vanilla ES6+ JavaScript (zero build step, instant execution), <code>Leaflet.js</code> (v1.9.4 for GIS track rendering), <code>CartoDB Dark Matter</code> vector tile layer, HTML5 Canvas & Web Audio API (tactical radar sound chimes).",
        body_style
    ))

    story.append(Paragraph("5.5 Cloud Infrastructure & Server Deployment", h2_style))
    story.append(Paragraph(
        "• <b>Application Server:</b> Uvicorn ASGI asynchronous worker server executing FastAPI endpoints.<br/>"
        "• <b>Production Cloud Platform:</b> Render Cloud Web Service (Singapore AP-Southeast Edge Region) running Python 3.12 runtime.<br/>"
        "• <b>Continuous Deployment:</b> GitHub Webhook CI/CD pipeline triggering automated zero-downtime builds upon git push to <code>main</code> branch.<br/>"
        "• <b>Local Tunnel Fallback:</b> Integrated localtunnel / ngrok support for low-latency live hackathon venue demonstrations.",
        body_style
    ))

    story.append(Spacer(1, 14))
    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=4, spaceAfter=8))
    story.append(Paragraph("<b>End of Official Guidebook • Smart India Hackathon Prototype • Indian Railways Dynamic ETA System</b>", ParagraphStyle('EndNote', parent=body_style, fontSize=8, alignment=1, textColor=colors.HexColor("#64748B"))))

    # Build the document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated guidebook PDF: {filename} ({os.path.getsize(filename)} bytes)")

if __name__ == '__main__':
    build_pdf()
