/* 
 * Application entry point.
 * Coordinates data loading → map init → panel init → event wiring.
 *
 * Depends on: helpers.js, data.js, map.js, panel.js  (all loaded before this)
 *
 * Exposes (global, called from onclick attrs in panel HTML):
 *   selectDistrict(name)
 *   deselectDistrict()
 */

/* ── application state ─────────────────────────────────────────── */
const APP_STATE = {
  data:         null,
  activeLayer: 'NDVI',
  selDistrict:  null,
};

/* ══════════════════════════════════════════════════════════════════
 * GLOBAL ACTIONS  (called from onclick attributes inside panel HTML)
 * ══════════════════════════════════════════════════════════════════ */

/**
 * Select a district — updates both map highlight and info panel.
 * @param {string} name – canonical district name, e.g. "HARIDWAR"
 */
function selectDistrict(name) {
  APP_STATE.selDistrict = name;
  highlightDistrict(name);       // map.js
  renderDetail(APP_STATE.data, name); // panel.js
}

/**
 * Deselect the current district and return to the overview panel.
 */
function deselectDistrict() {
  APP_STATE.selDistrict = null;
  highlightDistrict(null);       // map.js
  renderOverview(APP_STATE.data); // panel.js
}

/* ══════════════════════════════════════════════════════════════════
 * LAYER TOGGLE  (wired to .lbtn buttons in HTML)
 * ══════════════════════════════════════════════════════════════════ */

function _bindLayerButtons() {
  document.querySelectorAll('.lbtn').forEach(btn => {
    btn.addEventListener('click', () => {
      // Toggle active class
      document.querySelectorAll('.lbtn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      // Update state + map
      APP_STATE.activeLayer = btn.dataset.layer;
      updateMapLayer(APP_STATE.activeLayer); // map.js
    });
  });
}

/* ══════════════════════════════════════════════════════════════════
 * INITIALISATION
 * ══════════════════════════════════════════════════════════════════ */

async function init() {
  const panel = document.getElementById('panel');

  try {
    /* 1 ── Load all data files in parallel */
    const { DATA, GEOJSON, getFeatureName } = await loadAllData(); // data.js
    APP_STATE.data = DATA;

    /* 2 ── Initialise Leaflet map with OpenStreetMap tiles */
    initMap(); // map.js

    /* 3 ── Build GeoJSON district layer with choropleth */
    buildGeoLayer(
      DATA,
      GEOJSON,
      getFeatureName,
      APP_STATE.activeLayer,
      null,                        // nothing selected yet
      (name) => selectDistrict(name)
    ); // map.js

    /* 4 ── Render initial map legend */
    renderMapLegend(APP_STATE.activeLayer); // map.js

    /* 5 ── Render overview panel */
    renderOverview(DATA); // panel.js

    /* 6 ── Wire layer-toggle buttons */
    _bindLayerButtons();

  } catch (err) {
    console.error('[OneHealth Atlas] Initialisation failed:', err);

    panel.innerHTML = /* html */`
      <div class="error-state">
        <strong>Failed to load data</strong><br><br>
        ${err.message}<br><br>
        This app fetches CSV and GeoJSON files via <code>fetch()</code>, which
        requires an HTTP server — it won't work when opened directly from the
        file system (<code>file://</code> protocol).<br><br>
        Start a local server from the project root:<br>
        <code style="display:inline-block;margin-top:6px;font-size:11px;
                     background:var(--card2);padding:4px 8px;border-radius:4px">
          python -m http.server 8000
        </code>
        <br>
        then open
        <code style="font-size:11px">http://localhost:8000/OneHealth-Uttarakhand-Atlas.html</code>
      </div>`;
  }
}

/* Start once the DOM is ready */
document.addEventListener('DOMContentLoaded', init);