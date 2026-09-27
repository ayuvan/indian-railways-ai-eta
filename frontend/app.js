/**
 * RailYatri AI • Indian Railways Dynamic ETA Passenger Application (JavaScript)
 * Author: SIH AI Prototype
 */

const state = {
  theme: localStorage.getItem('rail_theme') || 'dark',
  currentLang: 'en',
  translations: {},
  currentTrain: null,
  route: [],
  selectedStationIdx: 0,
  currentDelay: 25,
  weather: 'Clear',
  congestion: 'Normal',
  isMapVisible: false,
  mapMode: 'gis',
  simT: 0.35
};

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

// Leaflet GIS Map Engine State for Passenger App
let passengerGisMap = null;
let passengerTrainMarker = null;
let passengerTrackPolyline = null;
let passengerStationMarkers = [];
let passengerDarkTileLayer = null;
let passengerLightTileLayer = null;
let passengerRailOverlay = null;

// DOM Cache
const el = {
  html: document.documentElement,
  themeToggleBtn: document.getElementById('theme-toggle-btn'),
  langSelector: document.getElementById('lang-selector'),
  searchInput: document.getElementById('train-search-input'),
  searchBtn: document.getElementById('search-btn'),
  suggestionsBox: document.getElementById('search-suggestions'),
  trainSummaryCard: document.getElementById('train-summary-card'),
  
  // Boarding Pass Elements
  bpOriginCode: document.getElementById('bp-origin-code'),
  bpOriginCity: document.getElementById('bp-origin-city'),
  bpOriginTime: document.getElementById('bp-origin-time'),
  bpDestCode: document.getElementById('bp-dest-code'),
  bpDestCity: document.getElementById('bp-dest-city'),
  bpDestTime: document.getElementById('bp-dest-time'),
  bpTotalDist: document.getElementById('bp-total-dist'),
  bpTotalDuration: document.getElementById('bp-total-duration'),
  bpTrainLocoMarker: document.getElementById('bp-train-loco-marker'),

  badgeTrainNo: document.getElementById('badge-train-no'),
  badgeTrainType: document.getElementById('badge-train-type'),
  dispTrainName: document.getElementById('disp-train-name'),
  dispLivePlatformTop: document.getElementById('disp-live-platform-top'),
  dispCurrentDelay: document.getElementById('disp-current-delay'),
  dispLiveSpeed: document.getElementById('disp-live-speed'),
  dispLiveSignal: document.getElementById('disp-live-signal'),

  dispCurrStnName: document.getElementById('disp-curr-stn-name'),
  dispDistanceCovered: document.getElementById('disp-distance-covered'),
  dispDistanceRemaining: document.getElementById('disp-distance-remaining'),

  // Map & Controls
  btnToggleMap: document.getElementById('btn-toggle-map'),
  virtualMapDrawer: document.getElementById('virtual-map-drawer'),
  passengerTrackCanvas: document.getElementById('passenger-track-canvas'),

  simStationSelect: document.getElementById('sim-station-select'),
  simDelayInput: document.getElementById('sim-delay-input'),
  simWeatherSelect: document.getElementById('sim-weather-select'),
  simCongestionSelect: document.getElementById('sim-congestion-select'),
  simDaySelect: document.getElementById('sim-day-select'),
  simOccasionSelect: document.getElementById('sim-occasion-select'),
  simCivilSelect: document.getElementById('sim-civil-select'),
  simTechSelect: document.getElementById('sim-tech-select'),
  simTimetableSelect: document.getElementById('sim-timetable-select'),
  simAdvisoryBanner: document.getElementById('sim-advisory-banner'),
  dispSimAdvisory: document.getElementById('disp-sim-advisory'),
  btnRecalculate: document.getElementById('btn-recalculate'),
  btnStepSim: document.getElementById('btn-step-sim'),
  btnInjectDelay: document.getElementById('btn-inject-delay'),
  btnResetSim: document.getElementById('btn-reset-sim'),

  // Alternate Journeys
  alternateJourneysCard: document.getElementById('alternate-journeys-card'),
  dispAlternateReason: document.getElementById('disp-alternate-reason'),
  alternatesList: document.getElementById('alternates-list'),

  // Behavioral Profile
  behaviorProfileCard: document.getElementById('behavior-profile-card'),
  dispProfileQuarter: document.getElementById('disp-profile-quarter'),
  dispPunctualityScore: document.getElementById('disp-punctuality-score'),
  dispPctRightTime: document.getElementById('disp-pct-right-time'),
  dispPctSlightDelay: document.getElementById('disp-pct-slight-delay'),
  dispPctSigDelay: document.getElementById('disp-pct-sig-delay'),
  dispRecoveryPattern: document.getElementById('disp-recovery-pattern'),
  dispProfileVerdict: document.getElementById('disp-profile-verdict'),
  dispBottlenecksList: document.getElementById('disp-bottlenecks-list'),

  // Forecast Table
  etaTableBody: document.getElementById('eta-table-body'),
  quickChips: document.querySelectorAll('.chip'),
  datePills: document.querySelectorAll('.date-pill')
};

// Initialize
document.addEventListener('DOMContentLoaded', async () => {
  applyTheme(state.theme);
  await loadLanguage('en');
  setupEventListeners();
  // Select initial train for instant visualization
  selectTrain('12673');
  // Periodic NTES live stream polling
  setInterval(pollPassengerTelemetry, 4500);
  // Start GIS locomotive position animation loop
  requestAnimationFrame(passengerMapAnimationLoop);
});

function setupEventListeners() {
  // Theme Switcher (3D Toggle)
  if (el.themeToggleBtn) {
    el.themeToggleBtn.addEventListener('click', () => {
      const nextTheme = state.theme === 'dark' ? 'light' : 'dark';
      applyTheme(nextTheme);
    });
  }

  // Language selector
  el.langSelector.addEventListener('change', (e) => {
    loadLanguage(e.target.value);
  });

  // Date strip pills
  el.datePills.forEach(pill => {
    pill.addEventListener('click', () => {
      el.datePills.forEach(p => p.classList.remove('active'));
      pill.classList.add('active');
    });
  });

  // Search input with debounce
  let debounceTimeout = null;
  el.searchInput.addEventListener('input', (e) => {
    clearTimeout(debounceTimeout);
    const query = e.target.value.trim();
    if (query.length < 2) {
      el.suggestionsBox.classList.add('hidden');
      return;
    }
    debounceTimeout = setTimeout(() => searchTrains(query), 200);
  });

  el.searchBtn.addEventListener('click', () => {
    const q = el.searchInput.value.trim();
    if (q) searchTrains(q);
  });

  // Quick Preset Chips
  el.quickChips.forEach(chip => {
    chip.addEventListener('click', () => {
      el.quickChips.forEach(c => c.classList.remove('chip-active'));
      chip.classList.add('chip-active');
      const trainNo = chip.getAttribute('data-train');
      selectTrain(trainNo, true);
    });
  });

  // Virtual Map Toggle
  if (el.btnToggleMap) {
    el.btnToggleMap.addEventListener('click', () => {
      state.isMapVisible = !state.isMapVisible;
      if (state.isMapVisible) {
        el.virtualMapDrawer.classList.remove('hidden');
        el.btnToggleMap.innerHTML = '<span>🔼 Hide Virtual Track Map</span>';
        initOrUpdatePassengerMap();
      } else {
        el.virtualMapDrawer.classList.add('hidden');
        el.btnToggleMap.innerHTML = '<span>🗺️ View Virtual Train Track Map</span>';
      }
    });
  }

  // Rolling Stock 3D Angle View Toggle
  const btnToggleLoco = document.getElementById('btn-toggle-loco-view');
  if (btnToggleLoco) {
    btnToggleLoco.addEventListener('click', () => {
      if (window.railAudio) window.railAudio.playTap();
      const container = document.getElementById('rss-train-container');
      if (container) {
        container.classList.toggle('perspective-3d');
        btnToggleLoco.classList.toggle('active');
      }
    });
  }

  // Passenger Map Mode Switcher (GIS vs Schematic)
  const btnModeGis = document.getElementById('p-btn-mode-gis');
  const btnModeSchematic = document.getElementById('p-btn-mode-schematic');
  const gisMapElem = document.getElementById('passenger-gis-map');
  const canvasElem = document.getElementById('passenger-track-canvas');

  if (btnModeGis && btnModeSchematic) {
    btnModeGis.addEventListener('click', () => {
      state.mapMode = 'gis';
      btnModeGis.classList.add('active');
      btnModeSchematic.classList.remove('active');
      if (gisMapElem) gisMapElem.style.display = 'block';
      if (canvasElem) canvasElem.style.display = 'none';
      if (passengerGisMap) {
        setTimeout(() => passengerGisMap.invalidateSize(), 150);
      } else {
        initOrUpdatePassengerMap();
      }
    });

    btnModeSchematic.addEventListener('click', () => {
      state.mapMode = 'schematic';
      btnModeSchematic.classList.add('active');
      btnModeGis.classList.remove('active');
      if (gisMapElem) gisMapElem.style.display = 'none';
      if (canvasElem) canvasElem.style.display = 'block';
      drawPassengerTrackMap();
    });
  }

  // Recenter Map on Live Train
  const btnRecenter = document.getElementById('p-btn-recenter');
  if (btnRecenter) {
    btnRecenter.addEventListener('click', () => {
      if (window.railAudio) window.railAudio.playTap();
      if (passengerGisMap && passengerTrainMarker) {
        passengerGisMap.setView(passengerTrainMarker.getLatLng(), 11, { animate: true });
      }
    });
  }

  // Flagship Corridor Cards Click
  document.querySelectorAll('.fc-card').forEach(card => {
    card.addEventListener('click', () => {
      const trainNo = card.getAttribute('data-train');
      if (trainNo) {
        document.querySelectorAll('.fc-card').forEach(c => c.classList.remove('active-fc-card'));
        card.classList.add('active-fc-card');
        selectTrain(trainNo, true);
      }
    });
  });

  // Floating Mobile Dock Navigation
  const dockMap = [
    { btnId: 'dock-btn-track', targetSel: '#train-summary-card' },
    { btnId: 'dock-btn-map', targetSel: '#virtual-map-drawer', openMap: true },
    { btnId: 'dock-btn-sim', targetSel: '.simulation-drawer' },
    { btnId: 'dock-btn-dna', targetSel: '#behavior-profile-card' }
  ];

  dockMap.forEach(({ btnId, targetSel, openMap }) => {
    const btn = document.getElementById(btnId);
    if (btn) {
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        document.querySelectorAll('.dock-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        if (openMap && el.virtualMapDrawer) {
          el.virtualMapDrawer.classList.remove('hidden');
          state.isMapVisible = true;
          if (el.btnToggleMap) el.btnToggleMap.innerHTML = '<span>🔼 Hide Virtual Track Map</span>';
          initOrUpdatePassengerMap();
        }
        const target = document.querySelector(targetSel);
        if (target) {
          target.classList.remove('hidden');
          target.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
      });
    }
  });

  // Simulator Controls
  el.simStationSelect.addEventListener('change', (e) => {
    state.selectedStationIdx = parseInt(e.target.value, 10);
    triggerRecalculate();
  });

  el.simDelayInput.addEventListener('input', (e) => {
    state.currentDelay = parseFloat(e.target.value) || 0;
    triggerRecalculate();
  });

  el.simWeatherSelect.addEventListener('change', (e) => {
    state.weather = e.target.value;
    triggerRecalculate();
  });

  el.simCongestionSelect.addEventListener('change', (e) => {
    state.congestion = e.target.value;
    triggerRecalculate();
  });

  [el.simDaySelect, el.simOccasionSelect, el.simCivilSelect, el.simTechSelect, el.simTimetableSelect].forEach(sel => {
    if (sel) {
      sel.addEventListener('change', () => {
        triggerRecalculate();
      });
    }
  });

  el.btnRecalculate.addEventListener('click', () => {
    if (window.railAudio) window.railAudio.playTap();
    triggerRecalculate();
  });

  el.btnStepSim.addEventListener('click', () => {
    advanceSimulationStep();
  });

  el.btnInjectDelay.addEventListener('click', () => {
    if (window.railAudio) window.railAudio.playRedSignalAlert();
    state.currentDelay += 20;
    el.simDelayInput.value = state.currentDelay;
    triggerRecalculate();
  });

  el.btnResetSim.addEventListener('click', () => {
    state.selectedStationIdx = 0;
    state.currentDelay = 0;
    state.weather = 'Clear';
    state.congestion = 'Normal';
    el.simDelayInput.value = 0;
    el.simStationSelect.value = 0;
    el.simWeatherSelect.value = 'Clear';
    el.simCongestionSelect.value = 'Normal';
    if (el.simDaySelect) el.simDaySelect.value = 'Mid-Week';
    if (el.simOccasionSelect) el.simOccasionSelect.value = 'None';
    if (el.simCivilSelect) el.simCivilSelect.value = 'None';
    if (el.simTechSelect) el.simTechSelect.value = 'None';
    if (el.simTimetableSelect) el.simTimetableSelect.value = 'None';
    if (el.simAdvisoryBanner) el.simAdvisoryBanner.classList.add('hidden');
    triggerRecalculate();
  });

  document.addEventListener('click', (e) => {
    if (!el.searchInput.contains(e.target) && !el.suggestionsBox.contains(e.target)) {
      el.suggestionsBox.classList.add('hidden');
    }
  });
}

function applyTheme(theme) {
  state.theme = theme;
  document.documentElement.setAttribute('data-theme', theme);
  if (document.body) {
    document.body.setAttribute('data-theme', theme);
  }
  localStorage.setItem('rail_theme', theme);

  if (passengerGisMap) {
    if (theme === 'light') {
      if (passengerDarkTileLayer && passengerGisMap.hasLayer(passengerDarkTileLayer)) passengerGisMap.removeLayer(passengerDarkTileLayer);
      if (!passengerLightTileLayer) {
        passengerLightTileLayer = L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
          subdomains: 'abcd',
          maxZoom: 19,
          attribution: '&copy; CartoDB &copy; OpenStreetMap'
        });
      }
      if (!passengerGisMap.hasLayer(passengerLightTileLayer)) passengerLightTileLayer.addTo(passengerGisMap);
    } else {
      if (passengerLightTileLayer && passengerGisMap.hasLayer(passengerLightTileLayer)) passengerGisMap.removeLayer(passengerLightTileLayer);
      if (!passengerDarkTileLayer) {
        passengerDarkTileLayer = L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
          subdomains: 'abcd',
          maxZoom: 19,
          attribution: '&copy; CartoDB &copy; OpenStreetMap'
        });
      }
      if (!passengerGisMap.hasLayer(passengerDarkTileLayer)) passengerDarkTileLayer.addTo(passengerGisMap);
    }
  }

  if (state.isMapVisible && state.mapMode === 'schematic') drawPassengerTrackMap();
}

// Multilingual i18n
async function loadLanguage(lang) {
  try {
    const res = await fetch(`/api/i18n/${lang}`);
    const data = await res.json();
    state.currentLang = lang;
    state.translations = data.strings || {};
    applyTranslations();
  } catch (err) {
    console.error('Failed to load translations:', err);
  }
}

function applyTranslations() {
  const t = state.translations;
  if (!t.title) return;

  document.getElementById('txt-title').textContent = t.title;
  document.getElementById('txt-subtitle').textContent = t.subtitle;
  el.searchInput.placeholder = t.search_train_placeholder;
  document.getElementById('txt-search-btn').textContent = t.search_button;
  document.getElementById('txt-current-delay-label').textContent = t.current_delay;
  document.getElementById('txt-weather-label').textContent = t.weather_condition;
  document.getElementById('txt-congestion-label').textContent = t.track_congestion;
  document.getElementById('txt-table-title').textContent = t.predict_eta_btn;

  document.getElementById('th-stn').textContent = t.station;
  document.getElementById('th-sched').textContent = t.sched_arr;
  document.getElementById('th-static').textContent = t.static_eta;
  document.getElementById('th-ai').textContent = t.ai_eta;
  document.getElementById('th-delay').textContent = t.delay;
  document.getElementById('th-trend').textContent = t.trend;
  document.getElementById('th-rec').textContent = t.recovery;
}

// Search
async function searchTrains(query) {
  try {
    const res = await fetch(`/api/trains/search?q=${encodeURIComponent(query)}&limit=8`);
    const data = await res.json();
    renderSuggestions(data.results || []);
  } catch (err) {
    console.error('Search error:', err);
  }
}

function renderSuggestions(results) {
  el.suggestionsBox.innerHTML = '';
  if (results.length === 0) {
    el.suggestionsBox.classList.add('hidden');
    return;
  }

  results.forEach(train => {
    const item = document.createElement('div');
    item.className = 'suggestion-item';
    item.innerHTML = `
      <div>
        <span class="suggestion-name font-bold">${train.train_no} • ${train.train_name}</span>
      </div>
      <span class="badge badge-type">${train.type_code}</span>
    `;
    item.addEventListener('click', () => {
      el.suggestionsBox.classList.add('hidden');
      el.searchInput.value = `${train.train_no} - ${train.train_name}`;
      selectTrain(train.train_no, true);
    });
    el.suggestionsBox.appendChild(item);
  });

  el.suggestionsBox.classList.remove('hidden');
}

// Select Train
async function selectTrain(trainNo, playSound = false) {
  try {
    if (playSound && window.railAudio) window.railAudio.playChime();
    const res = await fetch(`/api/train/${trainNo}/route`);
    if (!res.ok) throw new Error('Route not found');
    const data = await res.json();
    
    state.currentTrain = data;
    state.route = data.route;
    state.selectedStationIdx = 0;
    state.currentDelay = 25;
    state.simT = 0.15;

    renderTrainHeader();
    renderRollingStockShowcase(data);
    populateStationDropdown();
    triggerRecalculate();
    loadBehaviorProfile(trainNo);
    if (state.isMapVisible) initOrUpdatePassengerMap();
  } catch (err) {
    console.error('Failed to select train:', err);
  }
}

function renderTrainHeader() {
  const train = state.currentTrain;
  el.trainSummaryCard.classList.remove('hidden');
  el.badgeTrainNo.textContent = train.train_no;
  el.badgeTrainType.textContent = train.type_code.replace('-TRAINS', ' Express');
  el.dispTrainName.textContent = train.train_name;

  const src = state.route[0];
  const dest = state.route[state.route.length - 1];

  if (src) {
    el.bpOriginCode.textContent = src.station_code;
    el.bpOriginCity.textContent = src.station_name;
    el.bpOriginTime.textContent = `Dep ${src.scheduled_dep || '22:00'}`;
  }
  if (dest) {
    el.bpDestCode.textContent = dest.station_code;
    el.bpDestCity.textContent = dest.station_name;
    el.bpTotalDist.textContent = `${dest.distance_km || 500} KM`;
  }
}

// Render Locomotive & Rolling Stock Showcase (Vector / 3D Render)
function renderRollingStockShowcase(train) {
  if (!train) return;
  const titleEl = document.getElementById('disp-loco-title');
  const badgeEl = document.getElementById('disp-loco-badge');
  const imgEl = document.getElementById('rss-train-img');
  const hpEl = document.getElementById('disp-spec-hp');
  const mpsEl = document.getElementById('disp-spec-mps');
  const brakesEl = document.getElementById('disp-spec-brakes');

  if (!imgEl) return;

  const tName = (train.train_name || '').toLowerCase();
  const tType = (train.type_code || '').toUpperCase();
  const tNo = String(train.train_no || '');

  let defaultSvg = '/static/assets/wap7_locomotive.svg';
  let title = 'WAP-7 High Speed Electric Locomotive';
  let badge = '6350 HP • CLW Livery';
  let hp = '6,350 HP';
  let mps = '140 km/h';
  let brakes = 'Microprocessor Dual-Pipe Air';

  if (tName.includes('vande') || tType.includes('VANDE') || ['20643', '20644', '22436'].includes(tNo)) {
    defaultSvg = '/static/assets/vande_bharat.svg';
    title = 'Vande Bharat Express (Train 18) Trainset';
    badge = 'Semi-High Speed EMU • Distributed Power';
    hp = '12,000 HP (8 Motor Coaches)';
    mps = '160 km/h (180 km/h Tested)';
    brakes = 'Electro-Pneumatic Regenerative';
  } else if (tType.includes('FRT') || tName.includes('freight') || tName.includes('mandovi') || ['10103'].includes(tNo)) {
    defaultSvg = '/static/assets/wag9_freight.svg';
    title = 'WAG-9 Heavy Haul Electric Locomotive';
    badge = '6120 HP • High Adhesion Co-Co';
    hp = '6,120 HP';
    mps = '120 km/h';
    brakes = 'Twin Pipe Air Brake + Dynamic Regen';
  }

  if (titleEl) titleEl.textContent = title;
  if (badgeEl) badgeEl.textContent = badge;
  if (hpEl) hpEl.textContent = hp;
  if (mpsEl) mpsEl.textContent = mps;
  if (brakesEl) brakesEl.textContent = brakes;

  // Set standard vector graphic
  imgEl.src = defaultSvg;

  // Proactively check if user dropped custom 3D image in /static/assets/custom/loco_3d.png
  const customImg = new Image();
  customImg.onload = () => {
    imgEl.src = '/static/assets/custom/loco_3d.png';
    if (badgeEl) badgeEl.textContent = 'Custom 3D Render Active';
  };
  customImg.src = '/static/assets/custom/loco_3d.png';
}

function populateStationDropdown() {
  el.simStationSelect.innerHTML = '';
  state.route.forEach((stn, idx) => {
    const opt = document.createElement('option');
    opt.value = idx;
    opt.textContent = `${idx + 1}. ${stn.station_code} - ${stn.station_name} (${stn.distance_km} km)`;
    el.simStationSelect.appendChild(opt);
  });
  el.simStationSelect.value = state.selectedStationIdx;
  el.simDelayInput.value = state.currentDelay;
}

// Behavioral Profile Load
async function loadBehaviorProfile(trainNo) {
  try {
    const res = await fetch(`/api/train/${trainNo}/behavior_profile`);
    if (!res.ok) return;
    const p = await res.json();
    
    el.behaviorProfileCard.classList.remove('hidden');
    el.dispProfileQuarter.textContent = p.quarter;
    el.dispPunctualityScore.textContent = `${p.punctuality_score} / 100`;
    el.dispPctRightTime.textContent = `${p.pct_right_time}%`;
    el.dispPctSlightDelay.textContent = `${p.pct_slight_delay}%`;
    el.dispPctSigDelay.textContent = `${p.pct_significant_delay}%`;
    el.dispRecoveryPattern.textContent = p.recovery_pattern;
    el.dispProfileVerdict.textContent = p.verdict;

    el.dispBottlenecksList.innerHTML = '';
    (p.chronic_bottlenecks || []).forEach(b => {
      const li = document.createElement('li');
      li.textContent = b;
      el.dispBottlenecksList.appendChild(li);
    });
  } catch (e) {
    console.error('Error loading behavior profile:', e);
  }
}

// Dynamic ETA Recalculation
async function triggerRecalculate() {
  if (!state.currentTrain) return;

  const currIdx = state.selectedStationIdx;
  const currentStn = state.route[currIdx];
  const destStn = state.route[state.route.length - 1];

  el.dispCurrStnName.textContent = currentStn.station_name;
  el.dispCurrentDelay.textContent = state.currentDelay > 0 
    ? `${state.currentDelay} min Late` 
    : (state.currentDelay < 0 ? `${Math.abs(state.currentDelay)} min Early` : 'Right Time');

  // Journey Progress
  const currDist = currentStn.distance_km;
  const totalDist = destStn.distance_km > 0 ? destStn.distance_km : 500;
  const pct = Math.min(95, Math.max(5, Math.round((currDist / totalDist) * 100)));

  // Animate train marker along boarding pass route line
  el.bpTrainLocoMarker.style.left = `${pct}%`;
  el.dispDistanceCovered.textContent = `${currDist.toFixed(0)} km`;
  const distRem = Math.max(0, totalDist - currDist);
  el.dispDistanceRemaining.textContent = `${distRem.toFixed(0)} km`;

  // Update Dynamic Proximity Gradient Needle (Green -> Yellow -> Red)
  const pgNeedle = document.getElementById('pg-needle');
  const pgStatus = document.getElementById('disp-proximity-desc');
  if (pgNeedle) {
    let needlePct = 15;
    if (distRem < 50) {
      needlePct = Math.min(30, Math.max(8, (distRem / 50) * 30));
      if (pgStatus) {
        pgStatus.textContent = '🟢 Imminent Arrival (<50km Zone)';
        pgStatus.style.color = '#10b981';
      }
    } else if (distRem <= 150) {
      needlePct = 35 + ((distRem - 50) / 100) * 30;
      if (pgStatus) {
        pgStatus.textContent = '🟡 Midway Corridor (50-150km Zone)';
        pgStatus.style.color = '#f59e0b';
      }
    } else {
      needlePct = Math.min(95, 70 + ((distRem - 150) / 300) * 25);
      if (pgStatus) {
        pgStatus.textContent = '🔴 Far Terminus (>150km Zone)';
        pgStatus.style.color = '#ef4444';
      }
    }
    pgNeedle.style.left = `${needlePct}%`;
  }

  // Inference API
  try {
    const dayOfWeek = el.simDaySelect ? el.simDaySelect.value : 'Mid-Week';
    const occasion = el.simOccasionSelect ? el.simOccasionSelect.value : 'None';
    const civilDisruption = el.simCivilSelect ? el.simCivilSelect.value : 'None';
    const techMalfunction = el.simTechSelect ? el.simTechSelect.value : 'None';
    const timetableClash = el.simTimetableSelect ? el.simTimetableSelect.value : 'None';

    const payload = {
      train_no: state.currentTrain.train_no,
      current_station_idx: currIdx,
      current_delay_min: state.currentDelay,
      weather: state.weather,
      congestion: state.congestion,
      day_of_week: dayOfWeek,
      occasion: occasion,
      civil_disruption: civilDisruption,
      technical_malfunction: techMalfunction,
      timetable_precedence: timetableClash
    };

    const res = await fetch('/api/predict_eta', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    const data = await res.json();
    const forecast = data.stations_forecast || [];
    renderETATable(forecast, currDist);

    // Render dynamic operational advisory banner
    if (el.simAdvisoryBanner && el.dispSimAdvisory) {
      if (data.ai_operational_advisory && data.ai_operational_advisory !== 'Nominal operating track conditions across all divisions.') {
        el.simAdvisoryBanner.classList.remove('hidden');
        el.dispSimAdvisory.textContent = `⚡ Operational Context: ${data.ai_operational_advisory} (Compounded Disruption Penalty: +${data.total_scenario_penalty_min || 0}m)`;
      } else {
        el.simAdvisoryBanner.classList.add('hidden');
      }
    }

    // Update destination ETA on Boarding Pass
    if (forecast.length > 0) {
      const lastForecast = forecast[forecast.length - 1];
      const finalEta = addMinutesToTimeStr(lastForecast.scheduled_arr, lastForecast.predicted_delay_min || 0);
      el.bpDestTime.textContent = `Dynamic ETA ${finalEta}`;
      
      const currentForecast = forecast[0];
      el.dispLivePlatformTop.textContent = currentForecast.estimated_platform || 'PF-2';
    }

    // Refresh virtual GIS map or schematic canvas if open
    if (state.isMapVisible) initOrUpdatePassengerMap();

    // Check alternate journeys if delayed
    loadAlternateJourneys(currentStn.station_code, destStn.station_code);
  } catch (err) {
    console.error('Inference error:', err);
  }
}

// Render ETA Table with Distance Gradient & Platform of Arrival
function renderETATable(forecast, currentDistanceKm) {
  el.etaTableBody.innerHTML = '';

  if (forecast.length === 0) {
    el.etaTableBody.innerHTML = `<tr><td colspan="9" class="empty-state-cell"><p>No upcoming stations</p></td></tr>`;
    return;
  }

  forecast.forEach(stn => {
    const tr = document.createElement('tr');
    const isCurrent = stn.status === 'CURRENT_LOCATION';
    if (isCurrent) tr.className = 'row-current';

    const distFromCurr = isCurrent ? 0 : Math.max(0, stn.distance_km - currentDistanceKm);

    // GRADIENT COLOR CODING (Green -> Yellow -> Red based on distance)
    let gradClass = 'pill-grad-green';
    let gradLabel = `${distFromCurr.toFixed(0)} km (Near)`;
    if (isCurrent) {
      gradClass = 'pill-grad-current';
      gradLabel = 'Present Stop';
    } else if (distFromCurr > 180) {
      gradClass = 'pill-grad-red';
      gradLabel = `${distFromCurr.toFixed(0)} km (Far)`;
    } else if (distFromCurr > 50) {
      gradClass = 'pill-grad-yellow';
      gradLabel = `${distFromCurr.toFixed(0)} km (Mid)`;
    }

    const sched = stn.scheduled_arr || '--:--';
    const staticEta = addMinutesToTimeStr(sched, state.currentDelay);
    const aiEta = addMinutesToTimeStr(sched, stn.predicted_delay_min || 0);

    let trendHtml = `<span class="trend-badge trend-steady">■ Steady</span>`;
    if (stn.delay_trend === 'RECOVERING') {
      trendHtml = `<span class="trend-badge trend-recovering">▲ Recovering</span>`;
    } else if (stn.delay_trend === 'COMPOUNDING') {
      trendHtml = `<span class="trend-badge trend-compounding">▼ Compounding</span>`;
    } else if (isCurrent) {
      trendHtml = `<span class="badge badge-train">● Current</span>`;
    }

    const rec = stn.recovery_min !== undefined ? `${stn.recovery_min > 0 ? '+' : ''}${stn.recovery_min}m` : '--';
    const recClass = stn.recovery_min > 0 ? 'text-success font-bold' : '';
    const pf = stn.estimated_platform || 'PF-2';

    tr.innerHTML = `
      <td>
        <div class="stn-cell">
          <span class="stn-name font-bold">${stn.station_name} ${stn.is_junction ? '⚡' : ''}</span>
          <span class="stn-code">${stn.station_code} • ${stn.zone || 'IR'}</span>
        </div>
      </td>
      <td class="col-platform">
        <span class="platform-badge-cell font-mono">${pf}</span>
      </td>
      <td>
        <span class="dist-gradient-pill ${gradClass} font-mono">${gradLabel}</span>
      </td>
      <td class="cell-time">${sched}</td>
      <td class="cell-time text-muted">${staticEta}</td>
      <td class="cell-time ai-time font-bold">${aiEta}</td>
      <td class="cell-time ${stn.predicted_delay_min > 25 ? 'text-danger' : 'text-warning'} font-bold">
        +${stn.predicted_delay_min}m
      </td>
      <td>${trendHtml}</td>
      <td class="cell-time ${recClass}">${rec}</td>
    `;

    el.etaTableBody.appendChild(tr);
  });
}

// Virtual Train Track Map Canvas
function drawPassengerTrackMap() {
  const canvas = el.passengerTrackCanvas;
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  const w = canvas.width;
  const h = canvas.height;

  ctx.clearRect(0, 0, w, h);

  // Background grid
  ctx.strokeStyle = state.theme === 'dark' ? 'rgba(30, 41, 59, 0.4)' : 'rgba(203, 213, 225, 0.4)';
  ctx.lineWidth = 1;
  for (let x = 0; x < w; x += 40) {
    ctx.beginPath();
    ctx.moveTo(x, 0);
    ctx.lineTo(x, h);
    ctx.stroke();
  }

  const route = state.route;
  if (!route || route.length === 0) return;

  const totalDist = route[route.length - 1].distance_km || 500;
  const currIdx = state.selectedStationIdx;

  // Track path
  ctx.beginPath();
  ctx.lineWidth = 6;
  ctx.strokeStyle = state.theme === 'dark' ? '#1e293b' : '#cbd5e1';
  ctx.moveTo(50, h / 2);
  ctx.lineTo(w - 50, h / 2);
  ctx.stroke();

  // Highlight covered track
  const currentRatio = Math.min(1, route[currIdx].distance_km / totalDist);
  const trainX = 50 + (w - 100) * currentRatio;

  ctx.beginPath();
  ctx.lineWidth = 6;
  ctx.strokeStyle = '#f97316';
  ctx.moveTo(50, h / 2);
  ctx.lineTo(trainX, h / 2);
  ctx.stroke();

  // Draw Stations
  route.forEach((stn, idx) => {
    const ratio = Math.min(1, stn.distance_km / totalDist);
    const x = 50 + (w - 100) * ratio;
    const y = h / 2;

    const isPassed = idx <= currIdx;
    const isCurrent = idx === currIdx;

    ctx.beginPath();
    ctx.arc(x, y, isCurrent ? 9 : 6, 0, Math.PI * 2);
    ctx.fillStyle = isCurrent ? '#10b981' : (isPassed ? '#f97316' : '#64748b');
    ctx.fill();
    ctx.lineWidth = 2;
    ctx.strokeStyle = '#fff';
    ctx.stroke();

    // Station Code Label
    ctx.fillStyle = state.theme === 'dark' ? '#f8fafc' : '#0f172a';
    ctx.font = 'bold 11px Plus Jakarta Sans, sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText(stn.station_code, x, y - 14);

    // Distance Label
    ctx.fillStyle = '#94a3b8';
    ctx.font = '9px JetBrains Mono, monospace';
    ctx.fillText(`${stn.distance_km.toFixed(0)}k`, x, y + 20);
  });

  // Train Loco Marker
  ctx.beginPath();
  ctx.arc(trainX, h / 2, 12, 0, Math.PI * 2);
  ctx.fillStyle = '#2563eb';
  ctx.fill();
  ctx.lineWidth = 3;
  ctx.strokeStyle = '#38bdf8';
  ctx.stroke();

  ctx.font = '14px sans-serif';
  ctx.textAlign = 'center';
  ctx.fillText('🚆', trainX, (h / 2) + 5);
}

// ==========================================================================
// REAL-WORLD PASSENGER GIS MAP IMPLEMENTATION (Leaflet + OpenRailwayMap)
// ==========================================================================

function initPassengerGisMap() {
  const container = document.getElementById('passenger-gis-map');
  if (!container || typeof L === 'undefined' || passengerGisMap) return;

  passengerGisMap = L.map('passenger-gis-map', {
    center: [12.2, 78.6],
    zoom: 8,
    zoomControl: true,
    attributionControl: false
  });

  passengerDarkTileLayer = L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
    subdomains: 'abcd',
    maxZoom: 19
  });

  passengerLightTileLayer = L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
    subdomains: 'abcd',
    maxZoom: 19
  });

  if (state.theme === 'light') {
    passengerLightTileLayer.addTo(passengerGisMap);
  } else {
    passengerDarkTileLayer.addTo(passengerGisMap);
  }

  // OpenRailwayMap track infrastructure overlay
  passengerRailOverlay = L.tileLayer('https://{s}.tiles.openrailwaymap.org/standard/{z}/{x}/{y}.png', {
    maxZoom: 19,
    opacity: 0.85
  }).addTo(passengerGisMap);

  setTimeout(() => {
    if (passengerGisMap) passengerGisMap.invalidateSize();
  }, 200);
}

function renderPassengerGisRoute() {
  if (!passengerGisMap) return;

  // Clear existing layers
  if (passengerTrackPolyline) {
    passengerGisMap.removeLayer(passengerTrackPolyline);
    passengerTrackPolyline = null;
  }
  passengerStationMarkers.forEach(m => passengerGisMap.removeLayer(m));
  passengerStationMarkers = [];
  if (passengerTrainMarker) {
    passengerGisMap.removeLayer(passengerTrainMarker);
    passengerTrainMarker = null;
  }

  const route = state.route;
  if (!route || route.length === 0) return;

  const latlngs = [];
  route.forEach((stn, idx) => {
    const coords = STATION_COORDS[stn.station_code];
    if (coords) {
      latlngs.push(coords);
      const isCurrent = idx === state.selectedStationIdx;

      const customPin = L.divIcon({
        className: 'gis-station-pin',
        html: `
          <div class="gis-stn-dot ${isCurrent ? 'current' : ''}"></div>
          <div class="gis-stn-label font-mono">${stn.station_code} • ${stn.station_name.split(' ')[0]}</div>
        `,
        iconSize: [75, 34],
        iconAnchor: [37, 7]
      });

      const marker = L.marker(coords, { icon: customPin }).addTo(passengerGisMap);
      marker.bindPopup(`
        <div style="font-family: var(--font-sans); font-size: 12px; color: #0f172a; padding: 4px;">
          <strong style="color: #ea580c; font-size: 13px;">${stn.station_name} (${stn.station_code})</strong><br>
          <span style="color:#64748b;">Distance:</span> <strong>${stn.distance_km} km</strong><br>
          <span style="color:#64748b;">Scheduled Arrival:</span> <strong>${stn.scheduled_arr || '22:00'}</strong><br>
          <span style="color:#64748b;">Estimated Platform:</span> <strong>${stn.estimated_platform || 'PF-2'}</strong>
        </div>
      `);
      marker.on('click', () => {
        state.selectedStationIdx = idx;
        if (el.simStationSelect) el.simStationSelect.value = idx;
        triggerRecalculate();
      });
      passengerStationMarkers.push(marker);
    }
  });

  if (latlngs.length > 1) {
    passengerTrackPolyline = L.polyline(latlngs, {
      color: '#f97316',
      weight: 5,
      opacity: 0.95,
      lineCap: 'round',
      lineJoin: 'round'
    }).addTo(passengerGisMap);

    passengerGisMap.fitBounds(passengerTrackPolyline.getBounds(), { padding: [35, 35] });
  }

  // Create High-Visibility Rotatable Train Locomotive Marker
  if (latlngs.length > 0) {
    const trainIcon = L.divIcon({
      className: 'gis-train-marker',
      html: `
        <div id="passenger-live-loco-rotator" class="gis-loco-rotator">
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

    const startPos = latlngs[Math.min(state.selectedStationIdx, latlngs.length - 1)];
    passengerTrainMarker = L.marker(startPos, { icon: trainIcon, zIndexOffset: 2000 }).addTo(passengerGisMap);
    passengerTrainMarker.bindTooltip(`🚆 ${state.currentTrain?.train_no || '12673'} • Live GPS Tracking`, {
      permanent: true,
      direction: 'top',
      className: 'gis-train-tooltip font-mono',
      offset: [0, -18]
    });
  }
}

function updatePassengerTrainPosition() {
  if (!passengerTrainMarker || !passengerTrackPolyline) return;
  const latlngs = passengerTrackPolyline.getLatLngs();
  if (latlngs.length < 2) return;

  const t = state.simT;
  const totalSegments = latlngs.length - 1;
  const segmentIdx = Math.min(totalSegments - 1, Math.floor(t * totalSegments));
  const segmentProgress = (t * totalSegments) - segmentIdx;

  const p1 = latlngs[segmentIdx];
  const p2 = latlngs[segmentIdx + 1];

  const lat = p1.lat + (p2.lat - p1.lat) * segmentProgress;
  const lng = p1.lng + (p2.lng - p1.lng) * segmentProgress;

  passengerTrainMarker.setLatLng([lat, lng]);

  // Compute tangent azimuth
  const dLat = p2.lat - p1.lat;
  const dLng = p2.lng - p1.lng;
  const headingDeg = (Math.atan2(dLng, dLat) * 180 / Math.PI);

  const rotator = document.getElementById('passenger-live-loco-rotator');
  if (rotator) {
    rotator.style.transform = `rotate(${headingDeg - 90}deg)`;
  }

  const subCoords = document.getElementById('vmap-sub-coords');
  if (subCoords) {
    subCoords.textContent = `GPS Lat: ${lat.toFixed(4)}° N, Lng: ${lng.toFixed(4)}° E • Live Speed: ${el.dispLiveSpeed?.textContent || '105 km/h'}`;
  }
}

function initOrUpdatePassengerMap() {
  if (!state.isMapVisible) return;
  if (state.mapMode === 'gis') {
    if (!passengerGisMap) {
      initPassengerGisMap();
    }
    renderPassengerGisRoute();
    setTimeout(() => {
      if (passengerGisMap) passengerGisMap.invalidateSize();
    }, 150);
  } else {
    drawPassengerTrackMap();
  }
}

function passengerMapAnimationLoop() {
  if (state.isMapVisible && state.mapMode === 'gis') {
    updatePassengerTrainPosition();
  }
  if (state.currentTrain) {
    state.simT = (state.simT + 0.0006) % 1.0;
  }
  requestAnimationFrame(passengerMapAnimationLoop);
}

// Alternate Journey Discovery Load
async function loadAlternateJourneys(currStnCode, destStnCode) {
  try {
    const res = await fetch(`/api/train/${state.currentTrain.train_no}/alternate_journeys?curr_stn=${currStnCode}&dest_stn=${destStnCode}&delay=${state.currentDelay}`);
    if (!res.ok) return;
    const data = await res.json();

    if (data.rescue_active && data.alternatives && data.alternatives.length > 0) {
      el.alternateJourneysCard.classList.remove('hidden');
      el.dispAlternateReason.textContent = data.reason;
      el.alternatesList.innerHTML = '';

      data.alternatives.forEach(alt => {
        const item = document.createElement('div');
        item.className = 'alternate-train-card';
        item.innerHTML = `
          <div class="alt-top-row">
            <div>
              <span class="font-bold text-accent">${alt.train_no} • ${alt.train_name}</span>
              <span class="badge badge-type" style="margin-left: 0.5rem;">${alt.train_type}</span>
            </div>
            <span class="badge badge-success">${alt.recommended_action}</span>
          </div>
          <p class="alt-details">
            Departs: <strong>${alt.departs_from_station}</strong> | Arrives: <strong>${alt.arrives_at_destination}</strong> (${alt.advantage})
          </p>
          <div class="alt-footer">
            <span class="text-secondary font-mono">${alt.seat_availability}</span>
            <span class="text-success font-bold">Priority: ${alt.priority_status}</span>
          </div>
        `;
        el.alternatesList.appendChild(item);
      });
    } else {
      el.alternateJourneysCard.classList.add('hidden');
    }
  } catch (e) {
    console.error('Alternate journey error:', e);
  }
}

// Telemetry Polling
async function pollPassengerTelemetry() {
  if (!state.currentTrain) return;
  try {
    const res = await fetch(`/api/realtime/${state.currentTrain.train_no}`);
    const data = await res.json();
    if (data.sync_status === 'REALTIME_ACTIVE') {
      el.dispLiveSpeed.textContent = `${data.current_speed_kmh} km/h`;
      el.dispLiveSignal.textContent = data.signal_aspect;
    }
  } catch (e) {}
}

// Advance simulation by 1 section
function advanceSimulationStep() {
  if (state.selectedStationIdx < state.route.length - 1) {
    if (window.railAudio) window.railAudio.playClearSignalChime();
    state.selectedStationIdx++;
    el.simStationSelect.value = state.selectedStationIdx;
    const recovery = state.currentTrain.type_code.includes('SF') ? -2 : 1;
    state.currentDelay = Math.max(0, state.currentDelay + recovery);
    el.simDelayInput.value = state.currentDelay;
    triggerRecalculate();
  }
}

function addMinutesToTimeStr(timeStr, minsToAdd) {
  if (!timeStr || !timeStr.includes(':')) return timeStr || '--:--';
  const parts = timeStr.split(':');
  let h = parseInt(parts[0], 10);
  let m = parseInt(parts[1], 10);
  const totalMins = ((h * 60 + m + Math.round(minsToAdd)) % 1440 + 1440) % 1440;
  return `${String(Math.floor(totalMins / 60)).padStart(2, '0')}:${String(totalMins % 60).padStart(2, '0')}`;
}
