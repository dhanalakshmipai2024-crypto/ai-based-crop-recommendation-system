/**
 * AgriVision AI - Precision Crop Recommendation Frontend Application
 * Handles state, bidirectional slider sync, REST API calls,
 * live satellite weather lookup, interactive diagnostics, and QA test execution.
 */

// Application State
const STATE = {
  currentTab: 'tab-recommender',
  crops: [],
  presets: [],
  metrics: null,
  activePresetId: null,
};

// DOM Elements
const elements = {
  // Tabs
  navTabs: document.querySelectorAll('.nav-tab'),
  tabPanels: document.querySelectorAll('.tab-panel'),

  // Form & Sliders
  form: document.getElementById('crop-form'),
  btnPredict: document.getElementById('btn-predict'),
  btnReset: document.getElementById('btn-reset'),
  presetsContainer: document.getElementById('presets-container'),

  // Weather Box
  cityInput: document.getElementById('city-input'),
  btnFetchWeather: document.getElementById('btn-fetch-weather'),
  weatherAlert: document.getElementById('weather-alert'),

  // Inputs & Sliders
  inputN: document.getElementById('input-n'),
  sliderN: document.getElementById('slider-n'),
  statusN: document.getElementById('status-n'),

  inputP: document.getElementById('input-p'),
  sliderP: document.getElementById('slider-p'),
  statusP: document.getElementById('status-p'),

  inputK: document.getElementById('input-k'),
  sliderK: document.getElementById('slider-k'),
  statusK: document.getElementById('status-k'),

  inputTemp: document.getElementById('input-temperature'),
  sliderTemp: document.getElementById('slider-temperature'),
  statusTemp: document.getElementById('status-temperature'),

  inputHumidity: document.getElementById('input-humidity'),
  sliderHumidity: document.getElementById('slider-humidity'),
  statusHumidity: document.getElementById('status-humidity'),

  inputPh: document.getElementById('input-ph'),
  sliderPh: document.getElementById('slider-ph'),
  statusPh: document.getElementById('status-ph'),

  inputRainfall: document.getElementById('input-rainfall'),
  sliderRainfall: document.getElementById('slider-rainfall'),
  statusRainfall: document.getElementById('status-rainfall'),

  // Dashboard Results
  emptyState: document.getElementById('empty-state-card'),
  loadingState: document.getElementById('loading-card'),
  dashboard: document.getElementById('dashboard-card'),

  resIcon: document.getElementById('res-icon'),
  resCropName: document.getElementById('res-crop-name'),
  resBotanical: document.getElementById('res-botanical'),
  resConfidence: document.getElementById('res-confidence'),
  resCategory: document.getElementById('res-category'),
  resGrowth: document.getElementById('res-growth'),
  resWater: document.getElementById('res-water'),
  resSoil: document.getElementById('res-soil'),
  resMarket: document.getElementById('res-market'),

  resContendersList: document.getElementById('res-contenders-list'),
  resPhBadge: document.getElementById('res-ph-badge'),
  resPhAdvice: document.getElementById('res-ph-advice'),
  resPhMarker: document.getElementById('res-ph-marker'),
  resNpkRatio: document.getElementById('res-npk-ratio'),
  resMsgN: document.getElementById('res-msg-n'),
  resMsgP: document.getElementById('res-msg-p'),
  resMsgK: document.getElementById('res-msg-k'),

  resAdvSoil: document.getElementById('res-adv-soil'),
  resAdvFert: document.getElementById('res-adv-fert'),
  resAdvWater: document.getElementById('res-adv-water'),
  resAdvTips: document.getElementById('res-adv-tips'),

  // Tab 2: Crop Directory
  cropGrid: document.getElementById('crop-grid'),
  cropSearch: document.getElementById('crop-search'),
  cropFilters: document.getElementById('crop-category-filters'),

  // Tab 3: Model Analytics
  featureBarsList: document.getElementById('feature-bars-list'),

  // Tab 4: QA Suite
  btnRunTests: document.getElementById('btn-run-tests'),
  qaTableBody: document.getElementById('qa-table-body'),
  qaOverallStatus: document.getElementById('qa-overall-status'),
  qaTotalCount: document.getElementById('qa-total-count'),
  qaTotalTime: document.getElementById('qa-total-time'),

  // Tab 5: Batch Analysis
  btnRunBatch: document.getElementById('btn-run-batch'),
  batchTableBody: document.getElementById('batch-table-body'),
};

// ==========================================================================
// 1. INITIALIZATION & DATA FETCHING
// ==========================================================================
async function initApp() {
  setupTabs();
  setupSliders();
  setupForm();
  setupWeather();
  setupQASuite();
  setupBatchSuite();

  // Load backend assets
  await Promise.all([
    fetchPresets(),
    fetchCrops(),
    fetchMetrics(),
  ]);

  updateAllInputBadges();
}

// Tab Switching
function setupTabs() {
  elements.navTabs.forEach(tab => {
    tab.addEventListener('click', () => {
      const targetTab = tab.getAttribute('data-tab');
      switchTab(targetTab);
    });
  });
}

function switchTab(tabId) {
  STATE.currentTab = tabId;

  elements.navTabs.forEach(t => {
    t.classList.toggle('active', t.getAttribute('data-tab') === tabId);
  });

  elements.tabPanels.forEach(p => {
    p.classList.toggle('active', p.id === tabId);
  });

  window.scrollTo({ top: 0, behavior: 'smooth' });
}

// ==========================================================================
// 2. SLIDER & INPUT BIDIRECTIONAL SYNC
// ==========================================================================
function bindSync(slider, input, callback) {
  slider.addEventListener('input', () => {
    input.value = slider.value;
    if (callback) callback(parseFloat(slider.value));
  });

  input.addEventListener('input', () => {
    let val = parseFloat(input.value);
    const min = parseFloat(slider.min);
    const max = parseFloat(slider.max);
    if (!isNaN(val)) {
      if (val < min) val = min;
      if (val > max) val = max;
      slider.value = val;
      if (callback) callback(val);
    }
  });
}

function setupSliders() {
  bindSync(elements.sliderN, elements.inputN, val => updateBadgeN(val));
  bindSync(elements.sliderP, elements.inputP, val => updateBadgeP(val));
  bindSync(elements.sliderK, elements.inputK, val => updateBadgeK(val));
  bindSync(elements.sliderTemp, elements.inputTemp, val => updateBadgeTemp(val));
  bindSync(elements.sliderHumidity, elements.inputHumidity, val => updateBadgeHumidity(val));
  bindSync(elements.sliderPh, elements.inputPh, val => updateBadgePh(val));
  bindSync(elements.sliderRainfall, elements.inputRainfall, val => updateBadgeRainfall(val));

  elements.btnReset.addEventListener('click', (e) => {
    e.preventDefault();
    resetFormValues({
      N: 90, P: 42, K: 43,
      temperature: 23.5, humidity: 82.0, ph: 6.5, rainfall: 200.0
    });
    // Remove active preset highlight
    document.querySelectorAll('.preset-chip').forEach(c => c.classList.remove('active'));
    STATE.activePresetId = null;
  });
}

function resetFormValues(vals) {
  elements.inputN.value = vals.N;
  elements.sliderN.value = vals.N;
  updateBadgeN(vals.N);

  elements.inputP.value = vals.P;
  elements.sliderP.value = vals.P;
  updateBadgeP(vals.P);

  elements.inputK.value = vals.K;
  elements.sliderK.value = vals.K;
  updateBadgeK(vals.K);

  elements.inputTemp.value = vals.temperature;
  elements.sliderTemp.value = vals.temperature;
  updateBadgeTemp(vals.temperature);

  elements.inputHumidity.value = vals.humidity;
  elements.sliderHumidity.value = vals.humidity;
  updateBadgeHumidity(vals.humidity);

  elements.inputPh.value = vals.ph;
  elements.sliderPh.value = vals.ph;
  updateBadgePh(vals.ph);

  elements.inputRainfall.value = vals.rainfall;
  elements.sliderRainfall.value = vals.rainfall;
  updateBadgeRainfall(vals.rainfall);
}

function updateBadgeN(val) {
  if (val < 40) setBadge(elements.statusN, 'Low / Deficient', 'tag-warning');
  else if (val <= 110) setBadge(elements.statusN, 'Balanced', 'tag-normal');
  else setBadge(elements.statusN, 'High / Surplus', 'tag-neutral');
}

function updateBadgeP(val) {
  if (val < 30) setBadge(elements.statusP, 'Low', 'tag-warning');
  else if (val <= 80) setBadge(elements.statusP, 'Balanced', 'tag-normal');
  else setBadge(elements.statusP, 'High / Surplus', 'tag-neutral');
}

function updateBadgeK(val) {
  if (val < 30) setBadge(elements.statusK, 'Low', 'tag-warning');
  else if (val <= 85) setBadge(elements.statusK, 'Balanced', 'tag-normal');
  else setBadge(elements.statusK, 'High / Surplus', 'tag-neutral');
}

function updateBadgeTemp(val) {
  if (val < 18) setBadge(elements.statusTemp, 'Cool Temperate', 'tag-neutral');
  else if (val <= 32) setBadge(elements.statusTemp, 'Tropical Warm', 'tag-normal');
  else setBadge(elements.statusTemp, 'Thermal Stress', 'tag-warning');
}

function updateBadgeHumidity(val) {
  if (val < 40) setBadge(elements.statusHumidity, 'Dry / Arid', 'tag-warning');
  else if (val <= 75) setBadge(elements.statusHumidity, 'Moderate', 'tag-neutral');
  else setBadge(elements.statusHumidity, 'Humid / Wet', 'tag-normal');
}

function updateBadgePh(val) {
  if (val < 5.5) setBadge(elements.statusPh, 'Acidic', 'tag-danger');
  else if (val < 6.5) setBadge(elements.statusPh, 'Slightly Acidic', 'tag-warning');
  else if (val <= 7.5) setBadge(elements.statusPh, 'Optimal Neutral', 'tag-normal');
  else if (val <= 8.5) setBadge(elements.statusPh, 'Moderately Alkaline', 'tag-warning');
  else setBadge(elements.statusPh, 'Alkaline / Sodic', 'tag-danger');
}

function updateBadgeRainfall(val) {
  if (val < 70) setBadge(elements.statusRainfall, 'Arid / Low', 'tag-warning');
  else if (val <= 150) setBadge(elements.statusRainfall, 'Moderate Rain', 'tag-neutral');
  else if (val <= 250) setBadge(elements.statusRainfall, 'Monsoon Abundant', 'tag-normal');
  else setBadge(elements.statusRainfall, 'Heavy Monsoon', 'tag-normal');
}

function updateAllInputBadges() {
  updateBadgeN(parseFloat(elements.inputN.value));
  updateBadgeP(parseFloat(elements.inputP.value));
  updateBadgeK(parseFloat(elements.inputK.value));
  updateBadgeTemp(parseFloat(elements.inputTemp.value));
  updateBadgeHumidity(parseFloat(elements.inputHumidity.value));
  updateBadgePh(parseFloat(elements.inputPh.value));
  updateBadgeRainfall(parseFloat(elements.inputRainfall.value));
}

function setBadge(el, text, className) {
  el.textContent = text;
  el.className = 'status-tag ' + className;
}

// ==========================================================================
// 3. PRESETS LOADER
// ==========================================================================
async function fetchPresets() {
  try {
    const res = await fetch('/api/presets');
    const data = await res.json();
    STATE.presets = data.presets || [];
    renderPresets();
  } catch (err) {
    console.error('Failed to load presets:', err);
  }
}

function renderPresets() {
  elements.presetsContainer.innerHTML = '';
  STATE.presets.forEach(p => {
    const chip = document.createElement('button');
    chip.type = 'button';
    chip.className = 'preset-chip';
    chip.id = `preset-${p.id}`;
    chip.innerHTML = `<span>${p.icon}</span><span>${p.name.split(' (')[0]}</span>`;
    chip.title = `${p.name}: ${p.description}`;

    chip.addEventListener('click', () => {
      document.querySelectorAll('.preset-chip').forEach(c => c.classList.remove('active'));
      chip.classList.add('active');
      STATE.activePresetId = p.id;
      resetFormValues(p.values);
      // Auto trigger prediction for seamless UX
      triggerPrediction();
    });

    elements.presetsContainer.appendChild(chip);
  });
}

// ==========================================================================
// 4. LIVE WEATHER SATELLITE INTEGRATION
// ==========================================================================
function setupWeather() {
  elements.btnFetchWeather.addEventListener('click', async (e) => {
    e.preventDefault();
    const city = elements.cityInput.value.trim();
    if (!city) {
      showWeatherAlert('Please enter a city or region name.', true);
      return;
    }

    elements.btnFetchWeather.disabled = true;
    elements.btnFetchWeather.textContent = 'Fetching...';

    try {
      const res = await fetch(`/api/weather?city=${encodeURIComponent(city)}`);
      const data = await res.json();

      if (res.ok && data.status === 'success') {
        // Auto-fill temperature & humidity
        elements.inputTemp.value = data.temperature;
        elements.sliderTemp.value = data.temperature;
        updateBadgeTemp(data.temperature);

        elements.inputHumidity.value = data.humidity;
        elements.sliderHumidity.value = data.humidity;
        updateBadgeHumidity(data.humidity);

        showWeatherAlert(
          `🛰️ ${data.city}: ${data.weather_condition}, Temp: ${data.temperature}°C, Humidity: ${data.humidity}% (Updated in form)`,
          false
        );
      } else {
        showWeatherAlert(data.message || 'Location not found. Enter values manually.', true);
      }
    } catch (err) {
      showWeatherAlert('Weather lookup service temporarily unavailable. Enter values manually.', true);
    } finally {
      elements.btnFetchWeather.disabled = false;
      elements.btnFetchWeather.textContent = 'Fetch Weather';
    }
  });
}

function showWeatherAlert(msg, isError = false) {
  elements.weatherAlert.textContent = msg;
  elements.weatherAlert.className = isError ? 'weather-alert error' : 'weather-alert';
  elements.weatherAlert.classList.remove('hidden');
}

// ==========================================================================
// 5. CROP PREDICTION INFERENCE
// ==========================================================================
function setupForm() {
  elements.form.addEventListener('submit', (e) => {
    e.preventDefault();
    triggerPrediction();
  });
}

async function triggerPrediction() {
  const payload = {
    N: parseFloat(elements.inputN.value),
    P: parseFloat(elements.inputP.value),
    K: parseFloat(elements.inputK.value),
    temperature: parseFloat(elements.inputTemp.value),
    humidity: parseFloat(elements.inputHumidity.value),
    ph: parseFloat(elements.inputPh.value),
    rainfall: parseFloat(elements.inputRainfall.value),
  };

  // Switch UI to loading state
  elements.emptyState.classList.add('hidden');
  elements.dashboard.classList.add('hidden');
  elements.loadingState.classList.remove('hidden');

  try {
    const res = await fetch('/api/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    const data = await res.json();

    if (!res.ok || data.status !== 'success') {
      alert(`Prediction Error: ${data.message || 'Invalid input'}`);
      elements.loadingState.classList.add('hidden');
      elements.emptyState.classList.remove('hidden');
      return;
    }

    renderPredictionResults(data);
  } catch (err) {
    console.error('Prediction request failed:', err);
    alert('Failed to connect to recommendation server.');
    elements.loadingState.classList.add('hidden');
    elements.emptyState.classList.remove('hidden');
  }
}

function renderPredictionResults(data) {
  elements.loadingState.classList.add('hidden');
  elements.dashboard.classList.remove('hidden');

  const rec = data.primary_recommendation;
  const diag = data.soil_diagnostics;

  // Winner Card
  elements.resIcon.textContent = rec.icon || '🌱';
  elements.resCropName.textContent = rec.crop_name;
  elements.resBotanical.textContent = rec.botanical_name || 'Standard Agricultural Variety';
  elements.resConfidence.textContent = `${rec.confidence_percentage}%`;
  elements.resCategory.textContent = rec.category || 'Agricultural Crop';
  elements.resGrowth.textContent = rec.growth_period_days || '90-120 Days';
  elements.resWater.textContent = rec.water_requirement || 'Moderate';
  elements.resSoil.textContent = rec.soil_preference || 'Arable Loam';
  elements.resMarket.textContent = rec.market_profile || 'High retail liquidity and domestic trade.';

  // Contenders List (Top 5)
  elements.resContendersList.innerHTML = '';
  data.top_contenders.forEach(c => {
    const item = document.createElement('div');
    item.className = 'contender-item';
    item.innerHTML = `
      <div class="contender-icon">${c.icon}</div>
      <div class="contender-name">${c.crop_name}</div>
      <div class="contender-bar-track">
        <div class="contender-bar-fill" style="width: ${c.probability}%;"></div>
      </div>
      <div class="contender-prob">${c.probability}%</div>
    `;
    elements.resContendersList.appendChild(item);
  });

  // pH Diagnostics
  const phInfo = diag.ph_analysis;
  elements.resPhBadge.textContent = phInfo.category;
  elements.resPhBadge.className = `status-tag tag-${phInfo.status === 'optimal' ? 'normal' : phInfo.status}`;
  elements.resPhAdvice.textContent = phInfo.advice;

  // Compute marker position on pH scale (0 to 14 mapped to 0% to 100%)
  const phVal = diag.input_summary.ph;
  const phMarkerPct = Math.min(100, Math.max(0, (phVal / 14) * 100));
  elements.resPhMarker.style.left = `${phMarkerPct}%`;

  // NPK Balance
  const npk = diag.npk_analysis;
  elements.resNpkRatio.textContent = `Current: ${npk.npk_ratio}`;
  elements.resMsgN.textContent = npk.N.message;
  elements.resMsgP.textContent = npk.P.message;
  elements.resMsgK.textContent = npk.K.message;

  // Agronomic Advisory
  const adv = rec.advisory || {};
  elements.resAdvSoil.textContent = adv.soil_prep || 'Prepare standard fine seedbed with good aeration.';
  elements.resAdvFert.textContent = adv.fertilizer || 'Apply balanced NPK according to soil test recommendations.';
  elements.resAdvWater.textContent = adv.water || 'Ensure adequate soil moisture through regular irrigation cycles.';
  elements.resAdvTips.textContent = adv.tips || 'Monitor crop regularly for common local pests and diseases.';
}

// ==========================================================================
// 6. CROP ENCYCLOPEDIA (TAB 2)
// ==========================================================================
async function fetchCrops() {
  try {
    const res = await fetch('/api/crops');
    const data = await res.json();
    STATE.crops = data.crops || [];
    renderCropDirectory();
    setupCropFilters();
  } catch (err) {
    console.error('Failed to load crops directory:', err);
  }
}

function renderCropDirectory(filter = 'all', searchQuery = '') {
  elements.cropGrid.innerHTML = '';

  const filtered = STATE.crops.filter(c => {
    const matchesCategory =
      filter === 'all' ||
      (filter === 'cereal' && c.category.toLowerCase().includes('cereal')) ||
      (filter === 'pulse' && c.category.toLowerCase().includes('pulse')) ||
      (filter === 'fruit' && c.category.toLowerCase().includes('fruit')) ||
      (filter === 'cash' && (c.category.toLowerCase().includes('cash') || c.category.toLowerCase().includes('fiber') || c.category.toLowerCase().includes('plantation')));

    const q = searchQuery.toLowerCase();
    const matchesSearch =
      c.name.toLowerCase().includes(q) ||
      c.botanical_name.toLowerCase().includes(q) ||
      c.category.toLowerCase().includes(q);

    return matchesCategory && matchesSearch;
  });

  if (filtered.length === 0) {
    elements.cropGrid.innerHTML = `
      <div style="grid-column: 1/-1; text-align: center; padding: 3rem; color: var(--text-muted);">
        No matching crops found in the encyclopedia.
      </div>
    `;
    return;
  }

  filtered.forEach(c => {
    const card = document.createElement('div');
    card.className = 'crop-card';

    const b = c.benchmarks || {};
    const nMean = b.N ? b.N.mean : '--';
    const tempMean = b.temperature ? b.temperature.mean : '--';
    const rainMean = b.rainfall ? b.rainfall.mean : '--';

    card.innerHTML = `
      <div class="crop-card-top">
        <div class="crop-card-icon">${c.icon}</div>
        <span class="crop-card-tag">${c.category.split('/')[0]}</span>
      </div>
      <div class="crop-card-title">${c.name}</div>
      <div class="crop-card-scientific">${c.botanical_name}</div>

      <div class="crop-card-benchmarks">
        <div class="benchmark-col">
          <div class="benchmark-lbl">N Target</div>
          <div class="benchmark-val">${nMean}</div>
        </div>
        <div class="benchmark-col">
          <div class="benchmark-lbl">Temp</div>
          <div class="benchmark-val">${tempMean}°C</div>
        </div>
        <div class="benchmark-col">
          <div class="benchmark-lbl">Rain</div>
          <div class="benchmark-val">${rainMean} mm</div>
        </div>
      </div>

      <button class="crop-card-btn" data-crop-id="${c.id}">
        🌾 Load Ideal Parameters
      </button>
    `;

    // Click handler to load crop profile into recommender
    card.querySelector('.crop-card-btn').addEventListener('click', () => {
      loadCropIntoRecommender(c);
    });

    elements.cropGrid.appendChild(card);
  });
}

function loadCropIntoRecommender(crop) {
  const b = crop.benchmarks || {};
  if (b.N) {
    resetFormValues({
      N: b.N.mean,
      P: b.P.mean,
      K: b.K.mean,
      temperature: b.temperature.mean,
      humidity: b.humidity.mean,
      ph: b.ph.mean,
      rainfall: b.rainfall.mean,
    });
  }
  switchTab('tab-recommender');
  triggerPrediction();
}

function setupCropFilters() {
  const pills = elements.cropFilters.querySelectorAll('.filter-pill');
  pills.forEach(pill => {
    pill.addEventListener('click', () => {
      pills.forEach(p => p.classList.remove('active'));
      pill.classList.add('active');
      renderCropDirectory(pill.getAttribute('data-filter'), elements.cropSearch.value.trim());
    });
  });

  elements.cropSearch.addEventListener('input', () => {
    const activePill = elements.cropFilters.querySelector('.filter-pill.active');
    const filter = activePill ? activePill.getAttribute('data-filter') : 'all';
    renderCropDirectory(filter, elements.cropSearch.value.trim());
  });
}

// ==========================================================================
// 7. MODEL & ANALYTICS (TAB 3)
// ==========================================================================
async function fetchMetrics() {
  try {
    const res = await fetch('/api/metrics');
    const data = await res.json();
    STATE.metrics = data;
    renderAnalytics(data);
  } catch (err) {
    console.error('Failed to load metrics:', err);
  }
}

function renderAnalytics(data) {
  const feats = data.feature_importances || {};
  elements.featureBarsList.innerHTML = '';

  const featLabels = {
    rainfall: 'Rainfall (Precipitation)',
    humidity: 'Relative Humidity',
    K: 'Potassium (K) Ratio',
    P: 'Phosphorus (P) Ratio',
    N: 'Nitrogen (N) Ratio',
    temperature: 'Ambient Temperature',
    ph: 'Soil pH Reaction'
  };

  const gradients = [
    'linear-gradient(90deg, #059669, #34d399)',
    'linear-gradient(90deg, #0284c7, #38bdf8)',
    'linear-gradient(90deg, #7c3aed, #a855f7)',
    'linear-gradient(90deg, #d97706, #fbbf24)',
    'linear-gradient(90deg, #2563eb, #60a5fa)',
    'linear-gradient(90deg, #e11d48, #fb7185)',
    'linear-gradient(90deg, #0d9488, #2dd4bf)',
  ];

  let idx = 0;
  for (const [key, val] of Object.entries(feats)) {
    const row = document.createElement('div');
    row.className = 'feat-bar-row';
    const pct = (val * 100).toFixed(2);
    const grad = gradients[idx % gradients.length];
    idx++;

    row.innerHTML = `
      <div class="feat-bar-name">${featLabels[key] || key}</div>
      <div class="feat-bar-track">
        <div class="feat-bar-fill" style="width: ${Math.min(100, pct * 3.5)}%; background: ${grad};"></div>
      </div>
      <div class="feat-bar-pct">${pct}%</div>
    `;
    elements.featureBarsList.appendChild(row);
  }
}

// ==========================================================================
// 8. AUTOMATED QA TEST SUITE (TAB 4)
// ==========================================================================
function setupQASuite() {
  elements.btnRunTests.addEventListener('click', async () => {
    elements.btnRunTests.disabled = true;
    elements.btnRunTests.innerHTML = '<span>⏳ Executing QA Benchmarks...</span>';
    elements.qaTableBody.innerHTML = `
      <tr>
        <td colspan="6" class="text-center py-4">Running 10 test scenarios against the ML inference engine...</td>
      </tr>
    `;

    try {
      const startTime = performance.now();
      const res = await fetch('/api/tests');
      const data = await res.json();
      const elapsed = Math.round(performance.now() - startTime);

      renderQAResults(data, elapsed);
    } catch (err) {
      elements.qaTableBody.innerHTML = `
        <tr>
          <td colspan="6" class="text-center py-4 text-danger">Failed to execute test suite: ${err.message}</td>
        </tr>
      `;
    } finally {
      elements.btnRunTests.disabled = false;
      elements.btnRunTests.innerHTML = '<span>▶ Run All Test Cases</span>';
    }
  });
}

function renderQAResults(data, totalElapsedMs) {
  elements.qaOverallStatus.textContent = data.overall_status;
  elements.qaOverallStatus.className = data.overall_status === 'ALL PASSED' ? 'status-tag tag-normal' : 'status-tag tag-warning';
  elements.qaTotalCount.textContent = `${data.total_tests} Verified Cases`;
  elements.qaTotalTime.textContent = `${totalElapsedMs} ms total`;

  elements.qaTableBody.innerHTML = '';
  data.results.forEach(t => {
    const tr = document.createElement('tr');
    const badgeClass = t.status === 'PASS' ? 'tag-normal' : (t.status === 'WARN' ? 'tag-warning' : 'tag-danger');

    tr.innerHTML = `
      <td><strong>${t.id}</strong></td>
      <td>
        <div style="font-weight: 600; color: var(--text-primary);">${t.name}</div>
        <div style="font-size: 0.75rem; color: var(--text-muted);">${t.description}</div>
      </td>
      <td>${t.expected}</td>
      <td style="color: var(--text-primary); font-weight: 600;">${t.actual}</td>
      <td style="font-family: var(--font-mono);">${t.latency_ms} ms</td>
      <td><span class="status-tag ${badgeClass}">${t.status}</span></td>
    `;
    elements.qaTableBody.appendChild(tr);
  });
}

// ==========================================================================
// 9. BATCH PLOT TESTER (TAB 5)
// ==========================================================================
const BATCH_SAMPLE_PLOTS = [
  { plotId: "P-101", region: "Indo-Gangetic Basin", N: 90, P: 42, K: 43, temperature: 20.8, humidity: 82.0, ph: 6.5, rainfall: 202.9 },
  { plotId: "P-102", region: "Himalayan Foothills", N: 20, P: 134, K: 200, temperature: 22.0, humidity: 92.0, ph: 6.0, rainfall: 112.0 },
  { plotId: "P-103", region: "Deccan Plateau Vertisol", N: 115, P: 45, K: 20, temperature: 24.0, humidity: 80.0, ph: 6.9, rainfall: 80.0 },
  { plotId: "P-104", region: "Western Ghats Highlands", N: 100, P: 30, K: 30, temperature: 25.0, humidity: 65.0, ph: 6.5, rainfall: 160.0 },
  { plotId: "P-105", region: "Thar Semi-Arid Dryland", N: 40, P: 65, K: 80, temperature: 19.0, humidity: 16.5, ph: 7.3, rainfall: 75.0 },
  { plotId: "P-106", region: "Coromandel Coastal Sand", N: 20, P: 15, K: 30, temperature: 27.0, humidity: 95.0, ph: 6.0, rainfall: 175.0 },
  { plotId: "P-107", region: "Yamuna Riverine Belt", N: 100, P: 18, K: 50, temperature: 26.0, humidity: 85.0, ph: 6.5, rainfall: 50.0 },
];

function setupBatchSuite() {
  renderBatchTable(BATCH_SAMPLE_PLOTS, null);

  elements.btnRunBatch.addEventListener('click', async () => {
    elements.btnRunBatch.disabled = true;
    elements.btnRunBatch.innerHTML = '<span>⏳ Evaluating Plots...</span>';

    try {
      const payload = {
        samples: BATCH_SAMPLE_PLOTS.map(p => ({
          N: p.N, P: p.P, K: p.K,
          temperature: p.temperature,
          humidity: p.humidity,
          ph: p.ph,
          rainfall: p.rainfall
        }))
      };

      const res = await fetch('/api/batch', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      const data = await res.json();
      if (res.ok && data.status === 'success') {
        renderBatchTable(BATCH_SAMPLE_PLOTS, data.results);
      }
    } catch (err) {
      alert('Batch evaluation error: ' + err.message);
    } finally {
      elements.btnRunBatch.disabled = false;
      elements.btnRunBatch.innerHTML = '<span>⚡ Evaluate All Plots</span>';
    }
  });
}

function renderBatchTable(plots, results) {
  elements.batchTableBody.innerHTML = '';
  plots.forEach((p, idx) => {
    const tr = document.createElement('tr');
    const res = results ? results[idx] : null;

    tr.innerHTML = `
      <td><strong>${p.plotId}</strong></td>
      <td>${p.region}</td>
      <td style="font-family: var(--font-mono);">${p.N}</td>
      <td style="font-family: var(--font-mono);">${p.P}</td>
      <td style="font-family: var(--font-mono);">${p.K}</td>
      <td style="font-family: var(--font-mono);">${p.temperature}°C</td>
      <td style="font-family: var(--font-mono);">${p.humidity}%</td>
      <td style="font-family: var(--font-mono);">${p.ph}</td>
      <td style="font-family: var(--font-mono);">${p.rainfall} mm</td>
      <td>
        ${res ? `<span style="font-size: 1.1rem; margin-right: 0.3rem;">${res.icon}</span><strong>${res.crop_name}</strong>` : '<span style="color: var(--text-dim);">Pending</span>'}
      </td>
      <td>
        ${res ? `<span class="status-tag tag-normal">${res.confidence}%</span>` : '--'}
      </td>
    `;
    elements.batchTableBody.appendChild(tr);
  });
}

// Start application
document.addEventListener('DOMContentLoaded', initApp);
