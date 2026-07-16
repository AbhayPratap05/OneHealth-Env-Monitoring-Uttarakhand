/* js/map.js
 * Leaflet map initialisation, GeoJSON overlay, choropleth layers,
 * hover/click interactions and the map legend.
 *
 * Depends on: helpers.js
 * Exposes:    initMap, buildGeoLayer, updateMapLayer, highlightDistrict,
 *             renderMapLegend
 */

/* ── module state ───────────────────────────────────── */
let _map          = null;
let _geoLayer     = null;
let _DATA         = {};
let _getFeature   = null;   // getFeatureName function from data.js
let _activeLayer  = 'NDVI';
let _selDistrict  = null;
let _onClickCb    = null;   // called with canonical district name on click

/* ── choropleth layer definitions ───────────────────── */
const LAYERS = {
  NDVI: {
    label: 'NDVI change 2016→2025 (Vegetation Loss)',
    getFill(name) {
      const pct = _DATA[name]?.env?.chg?.NDVI?.pct;
      if (pct == null) return '#666';
      if (pct < -17)   return '#c0392b';   // deep red — worst loss
      if (pct < -15)   return '#e67e22';   // orange
      return '#f4d03f';                    // yellow — moderate loss
    },
    legendItems() {
      return Object.entries(_DATA)
        .filter(([, d]) => d.env?.chg?.NDVI?.pct != null)
        .sort((a, b) => a[1].env.chg.NDVI.pct - b[1].env.chg.NDVI.pct)
        .map(([n, d]) => ({
          color: LAYERS.NDVI.getFill(n),
          text:  `<span style = "font-size: 12px; color: var(--text)";>${titleCase(n)}:   <span style = "color: var(--amber); font-weight: bold;">${d.env.chg.NDVI.pct.toFixed(1)}%</span> </span>`,
        }));
    },
  },

  NDWI: {
    label: 'NDWI change 2016→2025 (Water-Body Signal)',
    getFill(name) {
      const v = _DATA[name]?.env?.chg?.NDWI?.v;
      if (v == null) return '#666';
      if (v > 0.088) return '#1a6fa4';
      if (v > 0.083) return '#2980b9';
      return '#5dade2';
    },
    legendItems() {
      return Object.entries(_DATA)
        .filter(([, d]) => d.env?.chg?.NDWI?.v != null)
        .sort((a, b) => (b[1].env.chg.NDWI.v || 0) - (a[1].env.chg.NDWI.v || 0))
        .map(([n, d]) => ({
          color: LAYERS.NDWI.getFill(n),
          text:  `<span style = "font-size: 12px; color: var(--text)";>${titleCase(n)}:   <span style = "color: var(--blue); font-weight: bold;">${sgn(d.env.chg.NDWI.v)}%</span> </span>`,
        }));
    },
  },

  NDBI: {
    label: 'NDBI change 2016→2025 (Urban Expansion)',
    getFill(name) {
      const v = _DATA[name]?.env?.chg?.NDBI?.v;
      if (v == null) return '#666';
      if (v > 0.02)  return '#e74c3c';
      if (v > 0)     return '#f39c12';
      return '#27ae60';
    },
    legendItems() {
      return Object.entries(_DATA)
        .filter(([, d]) => d.env?.chg?.NDBI?.v != null)
        .sort((a, b) => (b[1].env.chg.NDBI.v || 0) - (a[1].env.chg.NDBI.v || 0))
        .map(([n, d]) => ({
          color: LAYERS.NDBI.getFill(n),
          text:  `<span style = "font-size: 12px; color: var(--text)";>${titleCase(n)}:   <span style = "color: var(--grey); font-weight: bold;">${sgn(d.env.chg.NDBI.v)}%</span> </span>`,
        }));
    },
  },
};

/* ── style helpers ──────────────────────────────────── */

function _featureStyle(feature) {
  const name      = _getFeature(feature);
  const isSelected = name === _selDistrict;
  const fillColor = name ? LAYERS[_activeLayer].getFill(name) : '#666';

  return {
    fillColor,
    fillOpacity: isSelected ? 0.60 : 0.42,
    color:       isSelected ? '#ffffff' : 'rgba(255,255,255,0.65)',
    weight:      isSelected ? 3 : 1.8,
    dashArray:   isSelected ? null : null,
  };
}

function _tooltipHTML(name) {
  const d = _DATA[name];
  if (!d) return `<b>${name}</b>`;
  const ndviPct = d.env?.chg?.NDVI?.pct;
  return (
    `<b style="font-size:13px">${titleCase(name)}</b>` +
    `<div style="color:#c7c7c7;font-size:11px;margin-top:3px">` +
      `OHRS: ${d.ohrs}/10</br>${d.riskLabel} RISK` +
    `</div>` +
    `<div style="color:#f0883e;font-size:10px;margin-top:3px">Click to explore →</div>`
  );
}

/* ── public API ─────────────────────────────────────── */

/**
 * Create the Leaflet map with an OpenStreetMap tile layer.
 * Call this once after DOM is ready.
 */
function initMap() {
  _map = L.map('map', { zoomControl: true });

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    maxZoom: 18,
  }).addTo(_map);

  return _map;
}

/**
 * Build (or rebuild) the GeoJSON district layer.
 *
 * @param {object}   DATA          – from loadAllData()
 * @param {object}   GEOJSON       – from loadAllData()
 * @param {Function} getFeatureName – from loadAllData()
 * @param {string}   activeLayer   – 'NDVI' | 'NDWI' | 'NDBI'
 * @param {string|null} selDistrict – currently selected district name
 * @param {Function} onDistrictClick – callback(canonicalName)
 */
function buildGeoLayer(DATA, GEOJSON, getFeatureName, activeLayer, selDistrict, onDistrictClick) {
  _DATA        = DATA;
  _getFeature  = getFeatureName;
  _activeLayer = activeLayer;
  _selDistrict = selDistrict;
  _onClickCb   = onDistrictClick;

  if (_geoLayer) _geoLayer.remove();

  _geoLayer = L.geoJSON(GEOJSON, {
    style:          _featureStyle,
    onEachFeature:  _attachEvents,
  }).addTo(_map);

  _map.fitBounds(_geoLayer.getBounds(), { padding: [28, 28] });
}

function _attachEvents(feature, layer) {
  const name = _getFeature(feature);
  if (!name) return;

  layer.on({
    mouseover(e) {
      if (name !== _selDistrict) {
        e.target.setStyle({ fillOpacity: 0.65, weight: 2.5, color: '#fff' });
        e.target.bringToFront();
      }
      layer
        .bindTooltip(_tooltipHTML(name), {
          className:  'district-tooltip',
          sticky:     true,
          direction:  'top',
          offset:     [0, -6],
        })
        .openTooltip();
    },
    mouseout(e) {
      if (name !== _selDistrict) _geoLayer.resetStyle(e.target);
      layer.closeTooltip();
      // Re-apply selected highlight if needed
      if (_selDistrict) _reapplySelected();
    },
    click() {
      if (_onClickCb) _onClickCb(name);
    },
  });
}

function _reapplySelected() {
  if (!_geoLayer || !_selDistrict) return;
  _geoLayer.eachLayer(l => {
    if (l.feature && _getFeature(l.feature) === _selDistrict) {
      l.setStyle(_featureStyle(l.feature));
      l.bringToFront();
    }
  });
}

/** Switch choropleth layer without rebuilding the GeoJSON layer. */
function updateMapLayer(layer) {
  _activeLayer = layer;
  if (_geoLayer) {
    _geoLayer.eachLayer(l => {
      if (l.feature) l.setStyle(_featureStyle(l.feature));
    });
    _reapplySelected();
  }
  renderMapLegend(layer);
}

/** Highlight a district (or clear highlight when name is null). */
function highlightDistrict(name) {
  _selDistrict = name;
  if (_geoLayer) {
    _geoLayer.eachLayer(l => {
      if (l.feature) l.setStyle(_featureStyle(l.feature));
    });
    _reapplySelected();
  }
}

/** Render the map legend for the given (or current) layer. */
function renderMapLegend(layer) {
  const el = document.getElementById('mapLegend');
  if (!el) return;

  const key   = layer || _activeLayer;
  const cfg   = LAYERS[key];
  const items = cfg.legendItems();

  el.innerHTML =
    `<div class="leg-title">${cfg.label}</div>` +
    items.map(i =>
      `<div class="leg-item">
         <div class="leg-swatch" style="background:${i.color}"></div>
         <span style="font-size:10px;color:#c9d1d9">${i.text}</span>
       </div>`
    ).join('');
}