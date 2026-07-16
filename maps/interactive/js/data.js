/* js/data.js
 * Fetches all CSV files and districts.geojson, then assembles the
 * canonical DATA object keyed by normalised district name.
 *
 * Depends on: helpers.js (loaded before this file)
 */

/* ── name normalisation ────────────────────────────── */

const _NAME_MAP = {
  'dehradun':      'DEHRADUN',
  'haridwar':      'HARIDWAR',
  'hardwar':       'HARIDWAR',
  'pauri garhwal': 'PAURI GARHWAL',
  'pauri':         'PAURI GARHWAL',
  'pouri garhwal': 'PAURI GARHWAL',
};

function _normName(raw) {
  if (raw == null) return null;
  const s = String(raw)
    .toLowerCase()
    .replace(/\s*(district|zila|jila)\s*/gi, '')
    .trim();
  return _NAME_MAP[s] || null;
}

/* Property keys to try when extracting a district name from GeoJSON */
const _GJ_NAME_KEYS = [
  'dtname', 'DTNAME', 'name', 'NAME', 'DISTRICT', 'District',
  'district', 'NAME_2', 'dist_name', 'DIST_NAME', 'Dist_Name', 'ST_NM',
];

/**
 * Returns the canonical district name (e.g. "HARIDWAR") for a GeoJSON
 * feature, or null if unrecognised.
 */
function getFeatureName(feature) {
  const props = feature.properties || {};

  for (const key of _GJ_NAME_KEYS) {
    if (props[key] != null) {
      const n = _normName(props[key]);
      if (n) return n;
    }
  }

  // Fallback: iterate all string values
  for (const val of Object.values(props)) {
    if (typeof val === 'string') {
      const n = _normName(val);
      if (n) return n;
    }
  }
  return null;
}

/* ── static lookup tables ──────────────────────────── */

const DISTRICT_COLORS = {
  'DEHRADUN':      '#4a9eff',
  'HARIDWAR':      '#ff8c42',
  'PAURI GARHWAL': '#56c96a',
};

/** Approximate district areas in km² (Census 2011) */
const DISTRICT_AREAS = {
  'DEHRADUN':      3088,
  'HARIDWAR':      2360,
  'PAURI GARHWAL': 5438,
};

/** Sex ratio (females per 1000 males) — Census 2011; not in the CSV */
const SEX_RATIOS = {
  'DEHRADUN':      902,
  'HARIDWAR':      881,
  'PAURI GARHWAL': 1103,
};

/* ── CSV / GeoJSON loaders ─────────────────────────── */

function _parseCSV(path) {
  return new Promise((resolve, reject) => {
    Papa.parse(path, {
      download:      true,
      header:        true,
      dynamicTyping: true,
      skipEmptyLines: true,
      complete: r  => resolve(r.data),
      error:    err => reject(new Error(`CSV parse error (${path}): ${err}`)),
    });
  });
}

async function _fetchGeoJSON(path) {
  const res = await fetch(path);
  if (!res.ok) throw new Error(`GeoJSON fetch failed (${path}): HTTP ${res.status}`);
  return res.json();
}

/* ── OHRS computation ──────────────────────────────── */

/**
 * One Health Risk Score (0–10).
 * Components:
 *   vegetation loss (70%) – based on NDVI % change magnitude
 *   urban expansion (30%) – NDBI positive change, clamped
 */
function _computeOHRS(ndviPct, ndbiChg) {
  const vegScore   = Math.min(10, Math.abs(ndviPct || 0) / 2);
  const urbanScore = (ndbiChg > 0) ? Math.min(10, ndbiChg / 0.005) : 0;
  return parseFloat((0.7 * vegScore + 0.3 * urbanScore).toFixed(1));
}

/* ── main entry point ──────────────────────────────── */

/**
 * Loads all data files in parallel and returns:
 *   { DATA, GEOJSON, getFeatureName }
 *
 * DATA is an object keyed by canonical district name, e.g.
 *   DATA['HARIDWAR'] = { color, area, ohrs, env, census, hmis, lstk, … }
 */
async function loadAllData() {
  const [censusRows, hmisRows, lstkRows, tempRows, geojson] = await Promise.all([
    _parseCSV('data/census_district_summary.csv'),
    _parseCSV('data/hmis_district_summary.csv'),
    _parseCSV('data/livestock.csv'),
    _parseCSV('data/temporal_summary.csv'),
    _fetchGeoJSON('data/districts.geojson'),
  ]);

  /* Index each CSV by normalised district name */
  const _idx = (rows, keyCol) => {
    const map = {};
    rows.forEach(r => {
      const name = _normName(r[keyCol]);
      if (name) map[name] = r;
    });
    return map;
  };

  const cMap = _idx(censusRows, 'District');
  const hMap = _idx(hmisRows,   'District');
  const lMap = _idx(lstkRows,   'District');

  /* Build temporal index: name → year → { NDVI, NDWI, NDBI } */
  const tMap = {};
  tempRows.forEach(r => {
    const name = _normName(r.district);
    if (!name) return;
    if (!tMap[name]) tMap[name] = {};
    tMap[name][r.year] = { NDVI: r.NDVI, NDWI: r.NDWI, NDBI: r.NDBI };
  });

  /* Collect all known district names */
  const allNames = new Set([
    ...Object.keys(cMap),
    ...Object.keys(tMap),
    ...Object.keys(hMap),
    ...Object.keys(lMap),
  ]);

  const DATA = {};

  allNames.forEach(name => {
    const t   = tMap[name] || {};
    const y16 = t[2016] || {};
    const y22 = t[2022] || {};
    const y25 = t[2025] || {};
    const c   = cMap[name] || {};
    const h   = hMap[name] || {};
    const l   = lMap[name] || {};

    /* Derived change values */
    const ndviChg = (y25.NDVI != null && y16.NDVI != null) ? y25.NDVI - y16.NDVI : null;
    const ndwiChg = (y25.NDWI != null && y16.NDWI != null) ? y25.NDWI - y16.NDWI : null;
    const ndbiChg = (y25.NDBI != null && y16.NDBI != null) ? y25.NDBI - y16.NDBI : null;
    const ndviPct = (ndviChg != null && y16.NDVI) ? (ndviChg / Math.abs(y16.NDVI)) * 100 : null;

    const ohrs      = _computeOHRS(ndviPct, ndbiChg);
    const riskLabel = ohrs >= 7.5 ? 'HIGH' : ohrs >= 5.5 ? 'MODERATE' : 'LOW';
    const riskClass = ohrs >= 7.5 ? 'high'  : ohrs >= 5.5 ? 'medium'  : 'low';
    const ohrsColor = ohrs >= 7.5 ? 'var(--red)'
                    : ohrs >= 5.5 ? 'var(--amber)'
                    :               'var(--green)';

    const area = DISTRICT_AREAS[name] || null;

    DATA[name] = {
      color:     DISTRICT_COLORS[name] || '#888888',
      area,
      ohrs, riskLabel, riskClass, ohrsColor,

      env: {
        cur: { NDVI: y25.NDVI, NDWI: y25.NDWI, NDBI: y25.NDBI },
        all: {
          NDVI: [y16.NDVI, y22.NDVI, y25.NDVI],
          NDWI: [y16.NDWI, y22.NDWI, y25.NDWI],
          NDBI: [y16.NDBI, y22.NDBI, y25.NDBI],
        },
        chg: {
          NDVI: { v: ndviChg, pct: ndviPct },
          NDWI: { v: ndwiChg },
          NDBI: { v: ndbiChg },
        },
      },

      census: {
        Pop:      c.Population  || null,
        HH:       c.Households  || null,
        Literacy: c.LiteracyRate || null,
        SexRatio: SEX_RATIOS[name] || null,
        Density:  (area && c.Population) ? Math.round(c.Population / area) : null,
        SC:       c.SC_Rate    || null,
        ST:       c.ST_Rate    || null,
        Workers:  c.WorkerRate || null,
      },

      hmis: {
        ANC:       h.ANC_Registered          || null,
        Delivery:  h.Institutional_Deliveries || null,
        CSection:  h.CSection_Deliveries      || null,
        ImmM:      h.Fully_Immunized_Male     || null,
        ImmF:      h.Fully_Immunized_Female   || null,
        LBW:       h.Low_Birth_Weight         || null,
        SAM:       h.SAM                      ?? null,
        Malaria:   h.Malaria                  ?? null,
        Dengue:    h.Dengue                   ?? null,
        TB:        h.Tuberculosis             ?? null,
        Diarrhoea: h.Diarrhoea               || null,
        OPD:       h.OPD                      || null,
        IPD:       h.Inpatients               || null,
        Lab:       h.Lab_Tests                || null,
      },

      lstk: {
        Treatment:   l.Treatment                || null,
        AI:          l.AI_Total                 || null,
        Poultry:     l.Poultry_Units            || null,
        Benefited:   l.Animals_Benefited        || null,
        DrenchLarge: l.Mass_Drenching_Large     || null,
        DrenchSmall: l.Mass_Drenching_SheepGoat || null,
        Chicks:      l.Chicks_Distributed       || null,
      },
    };
  });

  return { DATA, GEOJSON: geojson, getFeatureName };
}