/**
 * CRIS Nexroute • Indian Railways Section Control & Radar Console (JavaScript)
 * Author: SIH AI Prototype
 * Inspired by: UI Designs Ideas (PIC 1, PIC 2, PIC 3)
 */

const crState = {
  theme: localStorage.getItem('rail_theme') || 'dark',
  currentTrainNo: '12673',
  fleet: [],
  activeTrainData: null,
  route: [],
  currentStopIdx: 2,
  currentDelay: 25.0,
  speedKmh: 105.0,
  signalAspect: 'GREEN (Clear Track MPS)',
  zoom: 1.0,
  trainSimT: 0.35, // Position along radar track (0.0 to 1.0)
  kavach: {
    system_status: 'ARMED_RADIO_LOCK',
    movement_authority_km: 4.2,
    safe_braking_distance_m: 680,
    target_speed_kmh: 105,
    spad_risk_level: 'NOMINAL (Zero SPAD Violation Detected)',
    rfid_transponder: 'RFID-KM-214-UP-MAIN'
  },
  currentLang: 'en',
  translations: {}
};
let gisKavachArcLayer = null;

// DOM Cache
const crEl = {
  html: document.documentElement,
  themeToggleBtn: document.getElementById('theme-toggle-cr'),
  streamStatus: document.getElementById('cr-stream-status'),
  fleetList: document.getElementById('fleet-list'),
  fleetSearchInput: document.getElementById('fleet-search-input'),
  fleetCountBadge: document.getElementById('fleet-count-badge'),

  // Radar
  canvas: document.getElementById('nex-radar-canvas'),
  zoomIn: document.getElementById('radar-zoom-in'),
  zoomOut: document.getElementById('radar-zoom-out'),
  zoomVal: document.getElementById('radar-zoom-val'),
  btnInjectSignal: document.getElementById('cr-btn-inject-signal'),
  btnClearSignal: document.getElementById('cr-btn-clear-signal'),

  // Analytics
  chartVolume: document.getElementById('chart-volume'),
  chartLatency: document.getElementById('chart-latency'),
  chartVariance: document.getElementById('chart-variance'),

  // Inspector
  inspCategory: document.getElementById('insp-category'),
  inspHeadcode: document.getElementById('insp-headcode'),
  inspStatusBadge: document.getElementById('insp-status-badge'),
  inspOriginCode: document.getElementById('insp-origin-code'),
  inspOriginName: document.getElementById('insp-origin-name'),
  inspOriginTime: document.getElementById('insp-origin-time'),
  inspDestCode: document.getElementById('insp-dest-code'),
  inspDestName: document.getElementById('insp-dest-name'),
  inspDestEta: document.getElementById('insp-dest-eta'),
  inspJourneyHours: document.getElementById('insp-journey-hours'),

  inspLoco: document.getElementById('insp-loco'),
  inspSector: document.getElementById('insp-sector'),
  inspDriver: document.getElementById('insp-driver'),
  inspSpeed: document.getElementById('insp-speed'),
  inspPower: document.getElementById('insp-power'),
  inspBrakes: document.getElementById('insp-brakes'),
  inspPlatform: document.getElementById('insp-platform'),

  inspDutyStatus: document.getElementById('insp-duty-status'),
  inspDutyFill: document.getElementById('insp-duty-fill'),
  inspDutyAction: document.getElementById('insp-duty-action'),
  inspCleanBadge: document.getElementById('insp-clean-badge'),
  inspCleanAction: document.getElementById('insp-clean-action'),

  inspStepperList: document.getElementById('insp-stepper-list')
};

// Real-World GIS Map Engine State
let gisMap = null;
let gisTrainMarker = null;
let gisTrackPolyline = null;
let gisStationMarkers = [];
let gisSignalMarker = null;
let gisDarkTileLayer = null;
let gisLightTileLayer = null;
let gisRailOverlay = null;
let activeMapMode = 'gis'; // 'gis' (default) or 'cad'

// Comprehensive Real-World Coordinates for Indian Railway Corridors
const STATION_COORDS = {
  // Southern Trunk Line (MAS ➔ CBE)
  'MAS': [13.0827, 80.2707],
  'AJJ': [13.0818, 79.6687],
  'KPD': [12.9696, 79.1367],
  'JTJ': [12.5562, 78.5802],
  'SA':  [11.6643, 78.1460],
  'ED':  [11.3410, 77.7172],
  'TUP': [11.1085, 77.3411],
  'CBF': [11.0267, 76.9602],
  'CBE': [11.0016, 76.9628],

  // Konkan Railway Corridor (CSMT ➔ MAO)
  'CSMT': [18.9400, 72.8354],
  'DR':   [19.0178, 72.8478],
  'TNA':  [19.1860, 72.9759],
  'PNVL': [18.9886, 73.1105],
  'MNI':  [18.2530, 73.2840],
  'ROHA': [18.4357, 73.1177],
  'KHED': [17.7208, 73.3934],
  'CHI':  [17.5323, 73.5186],
  'SGR':  [17.1895, 73.5510],
  'RN':   [16.9902, 73.3120],
  'ADVI': [16.7450, 73.4900],
  'RAJP': [16.6500, 73.5200],
  'VBW':  [16.5100, 73.6900],
  'KKW':  [16.2700, 73.7100],
  'SNDD': [16.1400, 73.7000],
  'KUDL': [16.0100, 73.6900],
  'SWV':  [15.9100, 73.8200],
  'PERN': [15.7170, 73.7970],
  'THVM': [15.6300, 73.8400],
  'KRMI': [15.4900, 73.9200],
  'MAO':  [15.2736, 73.9580],

  // Freight & Western Sector
  'MJ':   [25.7333, 73.6000],
  'KBK':  [25.4333, 73.8333]
};

// Multilingual i18n for Control Room
async function loadCrLanguage(lang) {
  try {
    const res = await fetch(`/api/i18n/${lang}`);
    const data = await res.json();
    crState.currentLang = lang;
    crState.translations = data.strings || {};
    applyCrTranslations();
  } catch (err) {
    console.error('Failed to load control room translations:', err);
  }
}

function applyCrTranslations() {
  const t = crState.translations;
  if (!t || !t.title) return;

  const setTxt = (id, text) => {
    if (!text) return;
    const node = document.getElementById(id);
    if (node) node.textContent = text;
  };

  setTxt('cr-txt-portal-passenger', t.portal_passenger_app);
  setTxt('cr-txt-portal-public', t.cr_public_portal);
  setTxt('cr-txt-portal-control', t.portal_control_room);
  setTxt('cr-txt-portal-staff', t.cr_staff_active);
  setTxt('cr-stream-status', t.cr_stream_locked);
  setTxt('cr-txt-audio', t.audio_on);
  setTxt('cr-txt-roi-label', t.cr_ministry_roi);
  setTxt('cr-txt-fleet-title', t.cr_tracking_list);
  if (crEl.fleetSearchInput && t.cr_search_placeholder) {
    crEl.fleetSearchInput.placeholder = t.cr_search_placeholder;
  }
  setTxt('btn-mode-gis', t.cr_gis_map);
  setTxt('btn-mode-cad', t.cr_tactical_radar);
  setTxt('cr-btn-inject-signal', t.cr_inject_red_signal);
  setTxt('cr-btn-clear-signal', t.cr_clear_block);
  setTxt('cr-btn-recenter', t.cr_recenter);
}

// Initialize
document.addEventListener('DOMContentLoaded', async () => {
  applyTheme(crState.theme);
  await loadCrLanguage('en');
  setupListeners();
  initGisMap();
  await loadFleetTelemetry();
  await loadTrainRoute(crState.currentTrainNo);
  
  // Start radar animation loop & polling
  requestAnimationFrame(radarAnimationLoop);
  setInterval(pollTelemetryData, 4000);
});

function initGisMap() {
  const mapContainer = document.getElementById('nex-gis-map');
  if (!mapContainer || typeof L === 'undefined') return;

  // Center on Southern Mainline corridor (MAS to CBE)
  gisMap = L.map('nex-gis-map', {
    center: [12.2, 78.6],
    zoom: 8,
    zoomControl: false,
    attributionControl: true
  });

  // Base Map Tile Layers: Dark Matter vs Positron Light
  gisDarkTileLayer = L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
    subdomains: 'abcd',
    maxZoom: 19,
    attribution: '&copy; CartoDB &copy; OpenStreetMap'
  });

  gisLightTileLayer = L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
    subdomains: 'abcd',
    maxZoom: 19,
    attribution: '&copy; CartoDB &copy; OpenStreetMap'
  });

  if (crState.theme === 'light') {
    gisLightTileLayer.addTo(gisMap);
  } else {
    gisDarkTileLayer.addTo(gisMap);
  }

  // Railway Network Overlay: OpenRailwayMap Standard Tracks
  gisRailOverlay = L.tileLayer('https://{s}.tiles.openrailwaymap.org/standard/{z}/{x}/{y}.png', {
    maxZoom: 19,
    opacity: 0.85,
    attribution: 'Railway Data &copy; OpenRailwayMap'
  }).addTo(gisMap);

  // Invalidate map size once DOM layout completes
  setTimeout(() => {
    if (gisMap) gisMap.invalidateSize();
  }, 250);

  window.addEventListener('resize', () => {
    if (gisMap) gisMap.invalidateSize();
  });

  renderGisRoute();
}

function renderGisRoute() {
  if (!gisMap) return;

  // Clear existing markers & lines
  if (gisTrackPolyline) gisMap.removeLayer(gisTrackPolyline);
  gisStationMarkers.forEach(m => gisMap.removeLayer(m));
  gisStationMarkers = [];
  if (gisTrainMarker) {
    gisMap.removeLayer(gisTrainMarker);
    gisTrainMarker = null;
  }

  // Build corridor latlngs from current route or fallback
  const latlngs = [];
  const stationsToDraw = crState.route.length > 0 ? crState.route : [
    { station_code: 'MAS', station_name: 'Chennai Central' },
    { station_code: 'AJJ', station_name: 'Arakkonam Jn' },
    { station_code: 'KPD', station_name: 'Katpadi Jn' },
    { station_code: 'JTJ', station_name: 'Jolarpettai Jn' },
    { station_code: 'SA',  station_name: 'Salem Jn' },
    { station_code: 'ED',  station_name: 'Erode Jn' },
    { station_code: 'TUP', station_name: 'Tiruppur' },
    { station_code: 'CBE', station_name: 'Coimbatore Jn' }
  ];

  stationsToDraw.forEach((stn, idx) => {
    const code = stn.station_code;
    const coords = STATION_COORDS[code];
    if (coords) {
      latlngs.push(coords);
      const isCurrent = idx === crState.currentStopIdx;
      
      const customPin = L.divIcon({
        className: 'gis-station-pin',
        html: `
          <div class="gis-stn-dot ${isCurrent ? 'current' : ''}"></div>
          <div class="gis-stn-label font-mono">${code} • ${stn.station_name.split(' ')[0]}</div>
        `,
        iconSize: [80, 36],
        iconAnchor: [40, 7]
      });

      const marker = L.marker(coords, { icon: customPin }).addTo(gisMap);
      marker.bindPopup(`
        <div style="font-family: var(--font-sans); font-size: 12px; color: #0f172a; padding: 4px;">
          <strong style="color: #ea580c; font-size: 13px;">${stn.station_name} (${code})</strong><br>
          <span style="color:#64748b;">Scheduled Arrival:</span> <strong>${stn.scheduled_arr || '22:00'}</strong><br>
          <span style="color:#64748b;">Estimated Platform:</span> <strong>PF-2</strong><br>
          <span style="color:#64748b;">Section Speed:</span> <strong>MPS 110 km/h</strong>
        </div>
      `);
      marker.on('click', () => {
        if (window.railAudio) window.railAudio.playTap();
        crState.currentStopIdx = idx;
        triggerStaffRecalculate();
        if (gisTrainMarker) {
          gisTrainMarker.setLatLng(coords);
        }
      });
      gisStationMarkers.push(marker);
    }
  });

  // Glowing Orange Railway Track Polyline (PIC 3 style)
  if (latlngs.length > 1) {
    gisTrackPolyline = L.polyline(latlngs, {
      color: '#f97316',
      weight: 5,
      opacity: 0.95,
      lineCap: 'round',
      lineJoin: 'round',
      dashArray: null
    }).addTo(gisMap);

    gisMap.fitBounds(gisTrackPolyline.getBounds(), { padding: [50, 50] });
  }

  // Create High-Visibility Rotatable Train Locomotive Marker (PIC 3 style)
  if (latlngs.length > 0) {
    const trainIcon = L.divIcon({
      className: 'gis-train-marker',
      html: `
        <div id="gis-live-loco-rotator" class="gis-loco-rotator">
          <div class="gis-loco-beacon"></div>
          <div class="gis-headlight-beam"></div>
          <div class="gis-loco-body">
            <div class="gis-loco-cab"></div>
          </div>
        </div>
      `,
      iconSize: [50, 50],
      iconAnchor: [25, 25]
    });

    const startPos = latlngs[Math.min(crState.currentStopIdx, latlngs.length - 1)];
    gisTrainMarker = L.marker(startPos, { icon: trainIcon, zIndexOffset: 2000 }).addTo(gisMap);
    gisTrainMarker.bindTooltip(`🚆 ${crState.currentTrainNo} • ${crState.speedKmh} km/h • PF-2`, {
      permanent: true,
      direction: 'top',
      className: 'gis-train-tooltip font-mono',
      offset: [0, -18]
    });
  }
}

function updateGisTrainPosition() {
  if (!gisTrainMarker || !gisTrackPolyline) return;
  const latlngs = gisTrackPolyline.getLatLngs();
  if (latlngs.length < 2) return;

  const t = crState.trainSimT;
  const totalSegments = latlngs.length - 1;
  const segmentIdx = Math.min(totalSegments - 1, Math.floor(t * totalSegments));
  const segmentProgress = (t * totalSegments) - segmentIdx;

  const p1 = latlngs[segmentIdx];
  const p2 = latlngs[segmentIdx + 1];

  const lat = p1.lat + (p2.lat - p1.lat) * segmentProgress;
  const lng = p1.lng + (p2.lng - p1.lng) * segmentProgress;

  gisTrainMarker.setLatLng([lat, lng]);

  // Compute geographical azimuth and rotate locomotive
  const dLat = p2.lat - p1.lat;
  const dLng = p2.lng - p1.lng;
  const headingDeg = (Math.atan2(dLng, dLat) * 180 / Math.PI);

  const rotator = document.getElementById('gis-live-loco-rotator');
  if (rotator) {
    // 90deg offset aligns beam along CSS X-axis
    rotator.style.transform = `rotate(${headingDeg - 90}deg)`;
  }

  gisTrainMarker.setTooltipContent(`🚆 ${crState.currentTrainNo} • ${crState.speedKmh.toFixed(0)} km/h • Block 412 CLEAR`);

  // Update Kavach TCAS Safe Dynamic Braking Arc on GIS Map
  if (gisMap) {
    const isEmergency = crState.signalAspect && crState.signalAspect.includes('RED');
    const arcColor = isEmergency ? '#ef4444' : '#10b981';
    const brakeDistM = crState.kavach?.safe_braking_distance_m || 680;
    const brakeDistKm = brakeDistM / 1000.0;
    const headingRad = headingDeg * Math.PI / 180;
    const dLatBrake = (brakeDistKm / 111.0) * Math.cos(headingRad);
    const dLngBrake = (brakeDistKm / (111.0 * Math.cos(lat * Math.PI / 180))) * Math.sin(headingRad);
    const brakeTarget = [lat + dLatBrake, lng + dLngBrake];

    if (!gisKavachArcLayer) {
      gisKavachArcLayer = L.polyline([[lat, lng], brakeTarget], {
        color: arcColor,
        weight: 5,
        dashArray: '6, 5',
        opacity: 0.9
      }).addTo(gisMap);
      gisKavachArcLayer.bindTooltip(`🛡️ KAVACH ATP: Safe Braking Distance (${brakeDistM.toFixed(0)}m)`, {
        direction: 'right',
        className: 'font-mono'
      });
    } else {
      gisKavachArcLayer.setLatLngs([[lat, lng], brakeTarget]);
      gisKavachArcLayer.setStyle({ color: arcColor });
      gisKavachArcLayer.setTooltipContent(`🛡️ KAVACH ATP: Safe Braking Distance (${brakeDistM.toFixed(0)}m)`);
    }
  }
}

function setupListeners() {
  const themeToggle = document.getElementById('theme-toggle-cr') || crEl.themeToggleBtn;
  if (themeToggle) {
    themeToggle.addEventListener('click', () => {
      const nextTheme = crState.theme === 'dark' ? 'light' : 'dark';
      applyTheme(nextTheme);
    });
  }

  // Language selector
  const langSelect = document.getElementById('lang-selector-cr');
  if (langSelect) {
    langSelect.addEventListener('change', (e) => {
      loadCrLanguage(e.target.value);
    });
  }

  // Mode Switcher (GIS Map vs Tactical CAD Radar)
  const btnGis = document.getElementById('btn-mode-gis');
  const btnCad = document.getElementById('btn-mode-cad');
  const gisContainer = document.getElementById('nex-gis-map');
  const cadCanvas = document.getElementById('nex-radar-canvas');

  if (btnGis && btnCad) {
    btnGis.addEventListener('click', () => {
      activeMapMode = 'gis';
      btnGis.classList.add('active');
      btnCad.classList.remove('active');
      gisContainer.style.display = 'block';
      cadCanvas.style.display = 'none';
      if (gisMap) setTimeout(() => gisMap.invalidateSize(), 150);
    });

    btnCad.addEventListener('click', () => {
      activeMapMode = 'cad';
      btnCad.classList.add('active');
      btnGis.classList.remove('active');
      gisContainer.style.display = 'none';
      cadCanvas.style.display = 'block';
    });
  }

  // Zoom Controls
  if (crEl.zoomIn) {
    crEl.zoomIn.addEventListener('click', () => {
      if (activeMapMode === 'gis' && gisMap) {
        gisMap.zoomIn();
      } else {
        crState.zoom = Math.min(1.6, crState.zoom + 0.15);
        crEl.zoomVal.textContent = `${Math.round(crState.zoom * 100)}%`;
      }
    });
  }
  if (crEl.zoomOut) {
    crEl.zoomOut.addEventListener('click', () => {
      if (activeMapMode === 'gis' && gisMap) {
        gisMap.zoomOut();
      } else {
        crState.zoom = Math.max(0.6, crState.zoom - 0.15);
        crEl.zoomVal.textContent = `${Math.round(crState.zoom * 100)}%`;
      }
    });
  }

  // Signal Controls
  if (crEl.btnInjectSignal) {
    crEl.btnInjectSignal.addEventListener('click', () => {
      if (window.railAudio) window.railAudio.playRedSignalAlert();
      crState.currentDelay += 20;
      crState.speedKmh = 0;
      crState.signalAspect = 'RED (Signal Halt at Block 412)';
      crEl.inspSpeed.textContent = '0 km/h (Limit: 110)';
      crEl.inspBrakes.textContent = 'Full Service Emergency Brakes';
      crEl.inspBrakes.className = 'tg-val text-danger';

      // Drop Red Signal Marker on GIS Map
      if (gisMap && gisTrainMarker) {
        if (gisSignalMarker) gisMap.removeLayer(gisSignalMarker);
        const curPos = gisTrainMarker.getLatLng();
        const signalIcon = L.divIcon({
          html: '<div style="background:#ef4444; width:16px; height:16px; border-radius:50%; border:2px solid #fff; box-shadow:0 0 16px #ef4444; animation:pulse 1s infinite;"></div>',
          iconSize: [16, 16],
          iconAnchor: [8, 8]
        });
        gisSignalMarker = L.marker(curPos, { icon: signalIcon }).addTo(gisMap);
        gisSignalMarker.bindPopup('<strong>⚠️ RED SIGNAL HALT INJECTED</strong><br>Track Circuit Block 412 Occupied. Speed restricted to 0 km/h.').openPopup();
      }

      triggerStaffRecalculate();
    });
  }

  if (crEl.btnClearSignal) {
    crEl.btnClearSignal.addEventListener('click', () => {
      if (window.railAudio) window.railAudio.playClearSignalChime();
      crState.speedKmh = 105;
      crState.signalAspect = 'GREEN (Clear Track MPS)';
      crEl.inspSpeed.textContent = '105 km/h (Limit: 110)';
      crEl.inspBrakes.textContent = 'Released (5.0 bar)';
      crEl.inspBrakes.className = 'tg-val text-success';

      if (gisSignalMarker && gisMap) {
        gisMap.removeLayer(gisSignalMarker);
        gisSignalMarker = null;
      }

      triggerStaffRecalculate();
    });
  }

  // Recenter on Train
  const btnRecenter = document.getElementById('cr-btn-recenter');
  if (btnRecenter) {
    btnRecenter.addEventListener('click', () => {
      if (window.railAudio) window.railAudio.playTap();
      if (gisMap && gisTrainMarker) {
        gisMap.setView(gisTrainMarker.getLatLng(), 11, { animate: true });
      }
    });
  }

  // Search fleet
  if (crEl.fleetSearchInput) {
    crEl.fleetSearchInput.addEventListener('input', (e) => {
      const q = e.target.value.toLowerCase().trim();
      const filtered = crState.fleet.filter(f => 
        f.name.toLowerCase().includes(q) || 
        f.train_no.includes(q) || 
        f.headcode.toLowerCase().includes(q)
      );
      renderFleetList(filtered);
    });
  }

  // Ministry ROI Modal Controls
  const btnRoi = document.getElementById('btn-roi-calculator');
  const modalRoi = document.getElementById('modal-roi-calculator');
  const btnCloseRoi = document.getElementById('btn-close-roi');
  const sliderTrains = document.getElementById('roi-trains-slider');
  const sliderDelay = document.getElementById('roi-delay-slider');

  if (btnRoi && modalRoi) {
    btnRoi.addEventListener('click', () => {
      if (window.railAudio) window.railAudio.playChime();
      modalRoi.classList.remove('hidden');
      updateRoiMetrics(parseInt(sliderTrains?.value || 42, 10), parseFloat(sliderDelay?.value || 8.5));
    });
  }

  if (btnCloseRoi && modalRoi) {
    btnCloseRoi.addEventListener('click', () => {
      modalRoi.classList.add('hidden');
    });
  }

  if (modalRoi) {
    modalRoi.addEventListener('click', (e) => {
      if (e.target === modalRoi) modalRoi.classList.add('hidden');
    });
  }

  if (sliderTrains && sliderDelay) {
    const handleSliderChange = () => {
      const trains = parseInt(sliderTrains.value, 10);
      const delaySaved = parseFloat(sliderDelay.value);
      const valT = document.getElementById('val-trains-slider');
      const valD = document.getElementById('val-delay-slider');
      if (valT) valT.textContent = `${trains} Trains`;
      if (valD) valD.textContent = `${delaySaved.toFixed(1)} Minutes`;
      updateRoiMetrics(trains, delaySaved);
    };
    sliderTrains.addEventListener('input', handleSliderChange);
    sliderDelay.addEventListener('input', handleSliderChange);
  }
}

function applyTheme(theme) {
  crState.theme = theme;
  document.documentElement.setAttribute('data-theme', theme);
  if (document.body) {
    document.body.setAttribute('data-theme', theme);
  }
  localStorage.setItem('rail_theme', theme);

  // Switch Leaflet GIS base tile layer between Dark Matter and Positron Light
  if (gisMap) {
    if (theme === 'light') {
      if (gisDarkTileLayer && gisMap.hasLayer(gisDarkTileLayer)) gisMap.removeLayer(gisDarkTileLayer);
      if (!gisLightTileLayer) {
        gisLightTileLayer = L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
          subdomains: 'abcd',
          maxZoom: 19,
          attribution: '&copy; CartoDB &copy; OpenStreetMap'
        });
      }
      if (!gisMap.hasLayer(gisLightTileLayer)) gisLightTileLayer.addTo(gisMap);
    } else {
      if (gisLightTileLayer && gisMap.hasLayer(gisLightTileLayer)) gisMap.removeLayer(gisLightTileLayer);
      if (!gisDarkTileLayer) {
        gisDarkTileLayer = L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
          subdomains: 'abcd',
          maxZoom: 19,
          attribution: '&copy; CartoDB &copy; OpenStreetMap'
        });
      }
      if (!gisMap.hasLayer(gisDarkTileLayer)) gisDarkTileLayer.addTo(gisMap);
    }
  }

  // Redraw tactical CAD radar canvas if currently active
  if (activeMapMode === 'cad') {
    drawRadarCanvas();
  }
}

// Load Fleet Telemetry from API
async function loadFleetTelemetry() {
  try {
    const res = await fetch('/api/control_room/fleet_telemetry');
    const data = await res.json();
    crState.fleet = data.fleet || [];
    renderFleetList(crState.fleet);
    renderLatencyBars(data.latency_series || []);
    renderVarianceChart(data.velocity_variance || []);
  } catch (err) {
    console.error('Error loading fleet telemetry:', err);
  }
}

function renderFleetList(fleet) {
  crEl.fleetList.innerHTML = '';
  crEl.fleetCountBadge.textContent = `${fleet.length} Trains`;

  fleet.forEach(train => {
    const div = document.createElement('div');
    const isActive = train.train_no === crState.currentTrainNo;
    div.className = `fleet-card-item ${isActive ? 'active' : ''}`;

    let badgeClass = 'badge-transit';
    if (train.status === 'DELAYED') badgeClass = 'badge-danger';
    else if (train.status === 'BOARDING') badgeClass = 'badge-boarding';
    else if (train.status === 'ARRIVED') badgeClass = 'badge-arrived';
    else if (train.status === 'IN TRANSIT') badgeClass = 'badge-transit';

    const originCode = train.origin.match(/\(([A-Z]+)\)/)?.[1] || train.origin.substring(0, 3).toUpperCase();
    const destCode = train.dest.match(/\(([A-Z]+)\)/)?.[1] || train.dest.substring(0, 3).toUpperCase();
    const isFreight = train.category.toLowerCase().includes('freight') || train.category.toLowerCase().includes('hopper');
    const iconChar = isFreight ? '📦' : (train.category.includes('High Speed') || train.name.includes('Vande') ? '⚡' : '🚆');
    const iconClass = isFreight ? 'fci-icon-freight' : (train.category.includes('High Speed') || train.name.includes('Vande') ? 'fci-icon-vande' : 'fci-icon-pass');

    div.innerHTML = `
      <div class="fci-top-row">
        <div class="fci-icon-box ${iconClass}">${iconChar}</div>
        <div class="fci-title-group">
          <span class="fci-category font-bold">${train.category || 'Passenger Exp'}</span>
          <span class="fci-subname font-mono">${train.name}</span>
        </div>
        <span class="fci-headcode font-mono">${train.headcode}</span>
        <span class="fci-status-pill ${badgeClass}">${train.status}</span>
      </div>

      <div class="fci-schematic-row font-mono">
        <span class="fci-code">${originCode}</span>
        <div class="fci-track-line">
          <span class="fci-track-bar"></span>
          <span class="fci-track-marker">🚆</span>
          <span class="fci-track-duration">7H</span>
          <span class="fci-track-bar"></span>
        </div>
        <span class="fci-code text-accent">${destCode}</span>
      </div>

      <div class="fci-bottom-row">
        <span class="fci-orig-time">${train.origin.split(' ')[0]} ${train.depart_time}</span>
        <span class="fci-arrow">➔</span>
        <span class="fci-dest-eta ${train.delay_min > 20 ? 'text-danger' : 'text-accent'} font-bold">${train.dest.split(' ')[0]} ETA ${train.eta}</span>
      </div>
    `;

    div.addEventListener('click', () => {
      if (window.railAudio) window.railAudio.playChime();
      crState.currentTrainNo = train.train_no;
      renderFleetList(crState.fleet);
      loadTrainRoute(train.train_no);
    });

    crEl.fleetList.appendChild(div);
  });
}

function renderLatencyBars(series) {
  crEl.chartLatency.innerHTML = '';
  series.forEach(ms => {
    const bar = document.createElement('div');
    bar.className = 'lat-bar';
    const h = Math.min(100, (ms / 50) * 100);
    bar.style.height = `${h}%`;
    bar.title = `${ms} ms`;
    crEl.chartLatency.appendChild(bar);
  });
}

function renderVarianceChart(series) {
  crEl.chartVariance.innerHTML = '<div class="var-zero-line"></div>';
  series.forEach(item => {
    const col = document.createElement('div');
    col.className = 'var-col';

    const pos = document.createElement('div');
    pos.className = 'var-bar-pos';
    pos.style.height = `${item.positive * 3}px`;

    const neg = document.createElement('div');
    neg.className = 'var-bar-neg';
    neg.style.height = `${Math.abs(item.negative) * 3}px`;

    col.appendChild(pos);
    col.appendChild(neg);
    crEl.chartVariance.appendChild(col);
  });
}

// Load Route & Trigger AI Inference
async function loadTrainRoute(trainNo) {
  try {
    const res = await fetch(`/api/train/${trainNo}/route`);
    if (!res.ok) throw new Error('Route not found');
    const data = await res.json();
    crState.route = data.route || [];

    // Find fleet metadata
    const activeItem = crState.fleet.find(f => f.train_no === trainNo) || crState.fleet[0];
    if (activeItem) {
      crEl.inspCategory.textContent = activeItem.category;
      crEl.inspHeadcode.textContent = activeItem.headcode;
      crEl.inspStatusBadge.textContent = activeItem.status;
      crEl.inspStatusBadge.className = activeItem.status === 'DELAYED' ? 'badge badge-danger' : 'badge badge-success';
      crEl.inspOriginCode.textContent = activeItem.origin.split('(')[1]?.replace(')', '') || 'MAS';
      crEl.inspOriginName.textContent = activeItem.origin;
      crEl.inspOriginTime.textContent = `${activeItem.depart_time} IST`;
      crEl.inspDestCode.textContent = activeItem.dest.split('(')[1]?.replace(')', '') || 'CBE';
      crEl.inspDestName.textContent = activeItem.dest;
      crEl.inspDestEta.textContent = `ETA ${activeItem.eta}`;
      crEl.inspLoco.textContent = activeItem.loco;
      crEl.inspSector.textContent = activeItem.track_sector;
      crEl.inspDriver.textContent = activeItem.driver;
      crEl.inspSpeed.textContent = `${activeItem.speed_kmh} km/h (Limit: ${activeItem.speed_limit})`;
      crEl.inspPower.textContent = activeItem.power;
      crEl.inspBrakes.textContent = activeItem.brakes;

      // Update inspector locomotive preview artwork
      const locoImg = document.getElementById('cr-loco-img');
      if (locoImg) {
        if (activeItem.loco.includes('Vande') || activeItem.name.includes('Vande') || activeItem.train_no === '20643') {
          locoImg.src = '/static/assets/vande_bharat.svg';
        } else if (activeItem.loco.includes('WAG') || activeItem.category.toLowerCase().includes('freight')) {
          locoImg.src = '/static/assets/wag9_freight.svg';
        } else {
          locoImg.src = '/static/assets/wap7_locomotive.svg';
        }
      }
    }

    renderGisRoute();
    triggerStaffRecalculate();
  } catch (err) {
    console.error('Error loading route for control room:', err);
  }
}

async function triggerStaffRecalculate() {
  if (crState.route.length === 0) return;
  const currentStn = crState.route[crState.currentStopIdx] || crState.route[0];
  const nextStn = crState.route[Math.min(crState.currentStopIdx + 1, crState.route.length - 1)];

  // 1. Predict Dynamic ETA
  try {
    const predRes = await fetch('/api/predict_eta', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        train_no: crState.currentTrainNo,
        current_station_idx: crState.currentStopIdx,
        current_delay_min: crState.currentDelay,
        weather: 'Clear',
        congestion: 'Normal'
      })
    });
    const predData = await predRes.json();
    renderRouteStepper(predData.stations_forecast || []);
  } catch (e) {
    console.error(e);
  }

  // 2. Intelligent Staff Scheduling (HOER & Cleaning)
  try {
    const staffRes = await fetch(`/api/staff_schedule/${crState.currentTrainNo}?curr_stn=${currentStn.station_code}&next_stn=${nextStn.station_code}&delay=${crState.currentDelay}`);
    const staff = await staffRes.json();
    renderStaffInspector(staff);
  } catch (e) {
    console.error(e);
  }
}

function renderStaffInspector(staff) {
  const crew = staff.running_crew_hoer;
  const cleaning = staff.cleaning_services;

  const hrs = crew.projected_duty_hours;
  const pct = Math.min(100, Math.round((hrs / crew.regulatory_max_hours) * 100));
  crEl.inspDutyFill.style.width = `${pct}%`;

  if (hrs >= 7.5) {
    crEl.inspDutyFill.style.background = '#ef4444';
    crEl.inspDutyStatus.textContent = 'HOER Relief Dispatched';
    crEl.inspDutyStatus.className = 'badge badge-danger';
  } else {
    crEl.inspDutyFill.style.background = '#10b981';
    crEl.inspDutyStatus.textContent = 'Duty Normal';
    crEl.inspDutyStatus.className = 'badge badge-success';
  }

  crEl.inspDutyAction.textContent = `Duty ${hrs}h / 8.0h Max. ${crew.action}`;
  crEl.inspCleanAction.textContent = cleaning.shift_adjustment;
  crEl.inspPlatform.textContent = staff.estimated_platform;
}

function renderRouteStepper(forecast) {
  crEl.inspStepperList.innerHTML = '';
  forecast.forEach(stn => {
    const item = document.createElement('div');
    const isCurrent = stn.status === 'CURRENT_LOCATION';
    item.className = `stepper-item ${isCurrent ? 'current' : ''}`;

    const sched = stn.scheduled_arr || '--:--';
    const delay = stn.predicted_delay_min || 0;
    const pf = stn.estimated_platform || 'PF-2';

    item.innerHTML = `
      <div class="step-node font-mono">${isCurrent ? '●' : '✓'}</div>
      <div style="display:flex; justify-content:space-between; align-items:center;">
        <span class="step-stn font-bold">${stn.station_name} (${stn.station_code})</span>
        <span class="badge badge-platform font-mono">${pf}</span>
      </div>
      <div class="step-meta">
        <span>Sched: ${sched}</span> • 
        <span class="${delay > 20 ? 'text-danger' : 'text-warning'} font-bold">+${delay}m late</span> • 
        <span>${stn.distance_km} km</span>
      </div>
    `;

    crEl.inspStepperList.appendChild(item);
  });
}

// Radar Canvas Animation Loop (inspired by PIC 3 dark radar & real-world GIS)
function radarAnimationLoop() {
  if (activeMapMode === 'gis') {
    updateGisTrainPosition();
  } else {
    drawRadarCanvas();
  }
  // Advance simulation time if not stopped by red signal
  if (crState.speedKmh > 0) {
    crState.trainSimT = (crState.trainSimT + 0.0006) % 1.0;
  }
  requestAnimationFrame(radarAnimationLoop);
}

function drawRadarCanvas() {
  const canvas = crEl.canvas;
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  const w = canvas.width;
  const h = canvas.height;
  const isLight = crState.theme === 'light';

  ctx.clearRect(0, 0, w, h);
  if (isLight) {
    ctx.fillStyle = '#f8fafc';
    ctx.fillRect(0, 0, w, h);
  }

  // Background radar grid lines (dark tactical vs crisp light CAD)
  ctx.strokeStyle = isLight ? '#e2e8f0' : '#0a1224';
  ctx.lineWidth = 1;
  const step = 35;
  for (let x = 0; x < w; x += step) {
    ctx.beginPath();
    ctx.moveTo(x, 0);
    ctx.lineTo(x, h);
    ctx.stroke();
  }
  for (let y = 0; y < h; y += step) {
    ctx.beginPath();
    ctx.moveTo(0, y);
    ctx.lineTo(w, y);
    ctx.stroke();
  }

  // Draw Glowing Diagonal Corridor Track Circuits (as in PIC 3)
  ctx.save();
  ctx.translate(w / 2, h / 2);
  ctx.scale(crState.zoom, crState.zoom);
  ctx.translate(-w / 2, -h / 2);

  // 1. Draw City Sector Block Polygons (from PIC 3)
  ctx.fillStyle = isLight ? '#f1f5f9' : '#080f1e';
  ctx.strokeStyle = isLight ? '#cbd5e1' : '#121e35';
  ctx.lineWidth = 1;

  // Sector 1 (Port / Central Terminus Yard)
  ctx.beginPath();
  ctx.moveTo(30, 260); ctx.lineTo(120, 220); ctx.lineTo(180, 280); ctx.lineTo(90, 360); ctx.closePath();
  ctx.fill(); ctx.stroke();

  // Sector 2 (Industrial Junction Zone)
  ctx.beginPath();
  ctx.moveTo(210, 180); ctx.lineTo(340, 130); ctx.lineTo(410, 210); ctx.lineTo(280, 270); ctx.closePath();
  ctx.fill(); ctx.stroke();

  // Sector 3 (Main Suburban Transit Core)
  ctx.beginPath();
  ctx.moveTo(390, 80); ctx.lineTo(540, 50); ctx.lineTo(600, 140); ctx.lineTo(470, 180); ctx.closePath();
  ctx.fill(); ctx.stroke();

  // Sector 4 (Freight Marshalling Depot)
  ctx.beginPath();
  ctx.moveTo(580, 20); ctx.lineTo(760, 10); ctx.lineTo(820, 80); ctx.lineTo(680, 110); ctx.closePath();
  ctx.fill(); ctx.stroke();

  // 2. Secondary & Siding Tracks (slate blue)
  ctx.strokeStyle = isLight ? '#94a3b8' : '#1e293b';
  ctx.lineWidth = 3;
  ctx.beginPath();
  ctx.moveTo(40, 120); ctx.lineTo(260, 210); ctx.lineTo(550, 170); ctx.lineTo(780, 260);
  ctx.stroke();

  // 3. Main Double Track Corridors (Glowing Vibrant Orange #f97316 as in PIC 3)
  ctx.shadowColor = '#f97316';
  ctx.shadowBlur = isLight ? 6 : 14;
  ctx.strokeStyle = '#f97316';
  ctx.lineWidth = 4;

  // Track 1 (Up Mainline)
  ctx.beginPath();
  ctx.moveTo(60, 320);
  ctx.lineTo(240, 260);
  ctx.lineTo(440, 160);
  ctx.lineTo(650, 110);
  ctx.lineTo(820, 60);
  ctx.stroke();

  // Track 2 (Down Mainline)
  ctx.lineWidth = 3;
  ctx.beginPath();
  ctx.moveTo(66, 332);
  ctx.lineTo(246, 272);
  ctx.lineTo(446, 172);
  ctx.lineTo(656, 122);
  ctx.lineTo(826, 72);
  ctx.stroke();

  // Turnout Crossovers (connecting Track 1 and Track 2 at stations)
  ctx.lineWidth = 2.5;
  ctx.beginPath();
  ctx.moveTo(210, 268); ctx.lineTo(235, 260); // Arakkonam Crossover
  ctx.moveTo(410, 174); ctx.lineTo(435, 162); // Katpadi Crossover
  ctx.moveTo(620, 118); ctx.lineTo(645, 110); // Jolarpettai Crossover
  ctx.stroke();
  ctx.shadowBlur = 0;

  // 4. Station Nodes with Radar Pulsing Halos (from PIC 3)
  const stations = [
    { code: 'MAS', name: 'Chennai Central', x: 60, y: 320, pf: 'PF-1/2' },
    { code: 'AJJ', name: 'Arakkonam Jn', x: 240, y: 260, pf: 'PF-3' },
    { code: 'KPD', name: 'Katpadi Jn', x: 440, y: 160, pf: 'PF-2 (Current)' },
    { code: 'JTJ', name: 'Jolarpettai Jn', x: 650, y: 110, pf: 'PF-1' },
    { code: 'CBE', name: 'Coimbatore Jn', x: 820, y: 60, pf: 'PF-4' }
  ];

  const nowMs = Date.now();
  stations.forEach((stn, idx) => {
    const isCurrent = idx === 2; // Katpadi current section
    
    // Pulsing radar ring
    const pulseRad = 8 + ((nowMs / 40 + idx * 15) % 24);
    const pulseAlpha = Math.max(0, 1 - (pulseRad - 8) / 24);
    ctx.beginPath();
    ctx.arc(stn.x, stn.y, pulseRad, 0, Math.PI * 2);
    ctx.strokeStyle = isCurrent ? `rgba(16, 185, 129, ${pulseAlpha})` : `rgba(249, 115, 22, ${pulseAlpha * 0.6})`;
    ctx.lineWidth = 1.5;
    ctx.stroke();

    // Solid Station Node Core
    ctx.beginPath();
    ctx.arc(stn.x, stn.y, 6.5, 0, Math.PI * 2);
    ctx.fillStyle = isCurrent ? '#10b981' : '#f97316';
    ctx.fill();
    ctx.strokeStyle = '#ffffff';
    ctx.lineWidth = 2;
    ctx.stroke();

    // Station Name & Platform Label
    ctx.fillStyle = isCurrent ? (isLight ? '#0284c7' : '#38bdf8') : (isLight ? '#0f172a' : '#e2e8f0');
    ctx.font = 'bold 11px Plus Jakarta Sans, sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText(`${stn.code} • ${stn.name}`, stn.x, stn.y - 14);

    ctx.fillStyle = isLight ? '#64748b' : '#94a3b8';
    ctx.font = '9px JetBrains Mono, monospace';
    ctx.fillText(stn.pf, stn.x, stn.y + 20);
  });

  // 5. Calculate moving train position and tangent heading along track
  const t = crState.trainSimT;
  // Multi-segment track interpolation
  let tx, ty, angle;
  if (t < 0.25) {
    const u = t / 0.25;
    tx = 60 + (240 - 60) * u;
    ty = 320 + (260 - 320) * u;
    angle = Math.atan2(260 - 320, 240 - 60);
  } else if (t < 0.55) {
    const u = (t - 0.25) / 0.30;
    tx = 240 + (440 - 240) * u;
    ty = 260 + (160 - 260) * u;
    angle = Math.atan2(160 - 260, 440 - 240);
  } else if (t < 0.8) {
    const u = (t - 0.55) / 0.25;
    tx = 440 + (650 - 440) * u;
    ty = 160 + (110 - 160) * u;
    angle = Math.atan2(110 - 160, 650 - 440);
  } else {
    const u = (t - 0.8) / 0.20;
    tx = 650 + (820 - 650) * u;
    ty = 110 + (60 - 110) * u;
    angle = Math.atan2(60 - 110, 820 - 650);
  }

  // 6. Draw Forward-Reaching Headlight Beam Cone (from PIC 3)
  ctx.save();
  ctx.translate(tx, ty);
  ctx.rotate(angle);

  const beamGrad = ctx.createRadialGradient(20, 0, 2, 85, 0, 75);
  beamGrad.addColorStop(0, 'rgba(255, 255, 255, 0.7)');
  beamGrad.addColorStop(0.3, 'rgba(56, 189, 248, 0.3)');
  beamGrad.addColorStop(1, 'rgba(56, 189, 248, 0)');

  ctx.beginPath();
  ctx.moveTo(18, 0);
  ctx.lineTo(85, -24);
  ctx.lineTo(85, 24);
  ctx.closePath();
  ctx.fillStyle = beamGrad;
  ctx.fill();

  // 6b. Kavach TCAS ATP Dynamic Braking Arc (Tactical Radar)
  const isRedAspect = crState.signalAspect && crState.signalAspect.includes('RED');
  ctx.save();
  ctx.strokeStyle = isRedAspect ? 'rgba(239, 68, 68, 0.95)' : 'rgba(16, 185, 129, 0.9)';
  ctx.lineWidth = 2.2;
  ctx.setLineDash([4, 4]);
  ctx.beginPath();
  const arcDist = Math.max(35, (crState.speedKmh / 110) * 85);
  ctx.arc(0, 0, arcDist, -Math.PI / 3.8, Math.PI / 3.8);
  ctx.stroke();
  ctx.setLineDash([]);
  ctx.fillStyle = isRedAspect ? '#ef4444' : '#10b981';
  ctx.font = 'bold 8.5px JetBrains Mono, monospace';
  ctx.fillText('🛡️ KAVACH 680m', arcDist + 5, 3);
  ctx.restore();

  // 7. Draw Sleek White Train Locomotive Carriage (from PIC 3)
  ctx.shadowColor = '#38bdf8';
  ctx.shadowBlur = 12;
  ctx.fillStyle = '#ffffff';
  ctx.strokeStyle = '#0284c7';
  ctx.lineWidth = 1.5;

  // Rounded locomotive chassis
  ctx.beginPath();
  ctx.roundRect(-16, -6, 32, 12, 4);
  ctx.fill();
  ctx.stroke();

  // Front windshield & cabin stripe
  ctx.fillStyle = '#0f172a';
  ctx.beginPath();
  ctx.roundRect(4, -4, 9, 8, 2);
  ctx.fill();

  // Dual headlights
  ctx.fillStyle = '#38bdf8';
  ctx.beginPath();
  ctx.arc(14, -3.5, 1.8, 0, Math.PI * 2);
  ctx.arc(14, 3.5, 1.8, 0, Math.PI * 2);
  ctx.fill();
  ctx.restore();

  // 8. Floating Tactical HUD Label (from PIC 3)
  ctx.shadowBlur = 0;
  ctx.fillStyle = isLight ? 'rgba(255, 255, 255, 0.95)' : 'rgba(8, 14, 26, 0.9)';
  ctx.strokeStyle = isLight ? '#0284c7' : '#38bdf8';
  ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.roundRect(tx - 65, ty - 38, 130, 24, 6);
  ctx.fill();
  ctx.stroke();

  // Little HUD pointer
  ctx.beginPath();
  ctx.moveTo(tx - 4, ty - 14);
  ctx.lineTo(tx, ty - 8);
  ctx.lineTo(tx + 4, ty - 14);
  ctx.fillStyle = isLight ? '#0284c7' : '#38bdf8';
  ctx.fill();

  ctx.fillStyle = isLight ? '#0369a1' : '#38bdf8';
  ctx.font = 'bold 10px JetBrains Mono, monospace';
  ctx.textAlign = 'center';
  ctx.fillText(`🚆 ${crState.currentTrainNo} • ${crState.speedKmh.toFixed(0)} km/h`, tx, ty - 22);

  ctx.restore();
}

async function pollTelemetryData() {
  try {
    const res = await fetch(`/api/realtime/${crState.currentTrainNo}`);
    const data = await res.json();
    if (data.sync_status === 'REALTIME_ACTIVE') {
      crState.speedKmh = data.current_speed_kmh;
      crEl.inspSpeed.textContent = `${data.current_speed_kmh} km/h (Limit: 110)`;
      if (data.signal_aspect) {
        crState.signalAspect = data.signal_aspect;
      }
      if (data.kavach_tcas) {
        crState.kavach = data.kavach_tcas;
        renderKavachTelemetry(data.kavach_tcas);
      }
    }
  } catch (e) {}
}

function renderKavachTelemetry(k) {
  if (!k) return;
  const statusEl = document.getElementById('insp-kavach-status');
  const maEl = document.getElementById('insp-kavach-ma');
  const brakeEl = document.getElementById('insp-kavach-brake-dist');
  const targetSpdEl = document.getElementById('insp-kavach-target-spd');
  const spadEl = document.getElementById('insp-kavach-spad');
  const rfidEl = document.getElementById('insp-kavach-rfid');

  if (statusEl) statusEl.textContent = k.system_status ? k.system_status.replace('_', ' ') : 'ARMED • RADIO LOCK';
  if (maEl) maEl.textContent = `${k.movement_authority_km || 4.2} km (Clear)`;
  if (brakeEl) brakeEl.textContent = `${k.safe_braking_distance_m || 680} m`;
  if (targetSpdEl) targetSpdEl.textContent = `${k.target_speed_kmh || 105} / 110 km/h`;
  if (spadEl) spadEl.textContent = k.spad_risk_level || 'NOMINAL (0.00%)';
  if (rfidEl) rfidEl.textContent = `RFID: ${k.rfid_transponder || 'KM-214-UP'}`;
}

async function updateRoiMetrics(trains = 42, delaySaved = 8.5) {
  try {
    const res = await fetch(`/api/operations/roi_metrics?trains=${trains}&delay_saved=${delaySaved}`);
    if (!res.ok) return;
    const data = await res.json();

    const annEl = document.getElementById('disp-annual-savings');
    const hoerEl = document.getElementById('disp-hoer-saved');
    const cleanEl = document.getElementById('disp-cleaning-saved');
    const energyEl = document.getElementById('disp-energy-saved');
    const refundEl = document.getElementById('disp-refund-saved');
    const co2El = document.getElementById('disp-co2-saved');
    const kwhEl = document.getElementById('disp-kwh-saved');

    if (annEl) annEl.textContent = `₹${data.annual_projected_savings_crores} Crores`;
    if (hoerEl) hoerEl.textContent = `₹${(data.breakdown.crew_hoer_overtime_saved_inr || 0).toLocaleString('en-IN')} / day`;
    if (cleanEl) cleanEl.textContent = `₹${(data.breakdown.contractor_cleaning_slas_saved_inr || 0).toLocaleString('en-IN')} / day`;
    if (energyEl) energyEl.textContent = `₹${(data.breakdown.traction_energy_conserved_inr || 0).toLocaleString('en-IN')} / day`;
    if (refundEl) refundEl.textContent = `₹${(data.breakdown.passenger_tdr_refunds_protected_inr || 0).toLocaleString('en-IN')} / day`;
    if (co2El) co2El.textContent = `${data.environmental_impact.daily_co2_reduction_tonnes} Tonnes/day`;
    if (kwhEl) kwhEl.textContent = `${(data.environmental_impact.daily_kwh_conserved || 0).toLocaleString('en-IN')} kWh/day`;

    const topBtn = document.getElementById('btn-roi-calculator');
    if (topBtn) topBtn.innerHTML = `<span>💰</span><span>Ministry ROI: ₹${data.annual_projected_savings_crores} Cr/yr</span>`;
  } catch (e) {
    console.error('ROI calculation error:', e);
  }
}
