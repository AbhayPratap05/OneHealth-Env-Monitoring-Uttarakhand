/* js/panel.js
 * Renders the right-hand info panel in both states:
 *   1. Overview  — all districts side-by-side
 *   2. Detail    — single selected district
 *
 * Depends on: helpers.js  (N, sgn, arw, chgColor, spark, titleCase)
 * Exposes (global):  renderOverview, renderDetail, toggleSec
 *
 * Private helpers (let/const) are not attached to window and are
 * only reachable from within this file.
 */

/* ── value-bar ranges (global min/max across all districts/years) ── */
const _ENV_RANGES = {
  NDVI: { min: 0.37, max: 0.56 },
  NDWI: { min: -0.43, max: -0.25 },
  NDBI: { min: -0.25, max: -0.11 },
};

const _barPct = (v, min, max) =>
  v == null ? 0 : Math.max(0, Math.min(100, ((v - min) / (max - min)) * 100)).toFixed(1);

/* ── section accordion (global — called from onclick attr) ─────── */
function toggleSec(hdr) {
  const body = hdr.nextElementSibling;
  const chev = hdr.querySelector('.sec-chev');
  if (!body || !chev) return;
  body.classList.toggle('open');
  chev.classList.toggle('open');
}

/* ── environmental section ─────────────────────────────────────── */
const _envSection = (d) => {
  const e   = d.env;
  const cur = e.cur;
  const chg = e.chg;

  const nvPct = _barPct(cur.NDVI, _ENV_RANGES.NDVI.min, _ENV_RANGES.NDVI.max);
  const nwPct = _barPct(cur.NDWI, _ENV_RANGES.NDWI.min, _ENV_RANGES.NDWI.max);
  const nbPct = _barPct(cur.NDBI, _ENV_RANGES.NDBI.min, _ENV_RANGES.NDBI.max);

  return /* html */`
  <div class="sec">
    <div class="sec-hdr" onclick="toggleSec(this)">
      <span class="sec-title">Environmental Indicators</span>
      <span class="sec-chev open">▼</span>
    </div>
    <div class="sec-body open">
      <div class="sub-label">
       <span class="year-accent">(2025)</span>
      </div>

      <div class="env-row">
        <span class="env-key">NDVI</span>
        <div class="vbar-bg">
          <div class="vbar-fill" style="width:${nvPct}%;background:var(--green)"></div>
        </div>
        <span class="env-val">${cur.NDVI != null ? cur.NDVI.toFixed(3) : '—'}</span>
      </div>
      <div class="env-row">
        <span class="env-key">NDWI</span>
        <div class="vbar-bg">
          <div class="vbar-fill" style="width:${nwPct}%;background:var(--blue)"></div>
        </div>
        <span class="env-val">${cur.NDWI != null ? cur.NDWI.toFixed(3) : '—'}</span>
      </div>
      <div class="env-row">
        <span class="env-key">NDBI</span>
        <div class="vbar-bg">
          <div class="vbar-fill" style="width:${nbPct}%;background:var(--amber)"></div>
        </div>
        <span class="env-val">${cur.NDBI != null ? cur.NDBI.toFixed(3) : '—'}</span>
      </div>

      <div class="div"></div>
      <div class="sub-label">
        Net change <span class="year-accent">2016 → 2025</span>
      </div>

      <div class="chg-row">
        <div class="chg-chip">
          <div class="cc-lbl">Vegetation</div>
          <div class="cc-val" style="color:${chgColor(chg.NDVI.v, true)}">
            ${arw(chg.NDVI.v)} ${chg.NDVI.v != null ? Math.abs(chg.NDVI.v).toFixed(3) : '—'}
          </div>
          <div class="cc-sub">NDVI Shift</div>
        </div>
        <div class="chg-chip">
          <div class="cc-lbl">Water Signal</div>
          <div class="cc-val" style="color:${chgColor(chg.NDWI.v, true)}">
            ${arw(chg.NDWI.v)} ${chg.NDWI.v != null ? Math.abs(chg.NDWI.v).toFixed(3) : '—'}
          </div>
          <div class="cc-sub">NDWI Shift</div>
        </div>
        <div class="chg-chip">
          <div class="cc-lbl">Built Up</div>
          <div class="cc-val" style="color:${chgColor(chg.NDBI.v, false)}">
            ${arw(chg.NDBI.v)} ${chg.NDBI.v != null ? Math.abs(chg.NDBI.v).toFixed(3) : '—'}
          </div>
          <div class="cc-sub">NDBI shift</div>
        </div>
      </div>

      <div class="sub-label">
        Temporal trend
        <span class="year-accent">2016 · 2022 · 2025</span>
      </div>

      <div class="spark-row">
        <div class="spark-chip">
          <div class="sk-lbl">NDVI</div>
          <div class="sk-graph">
            ${spark(e.all.NDVI, '#3fb950')}
          </div>
          <div class="sk-vals">
            ${e.all.NDVI.map(v => v != null ? v.toFixed(3) : '—').join(' · ')}
          </div>
        </div>
        <div class="spark-chip">
          <div class="sk-lbl">NDWI</div>
          ${spark(e.all.NDWI, '#58a6ff')}
          <div class="sk-vals">
            ${e.all.NDWI.map(v => v != null ? v.toFixed(3) : '—').join(' · ')}
          </div>
        </div>
        <div class="spark-chip">
          <div class="sk-lbl">NDBI</div>
          ${spark(e.all.NDBI, '#f0883e')}
          <div class="sk-vals">
            ${e.all.NDBI.map(v => v != null ? v.toFixed(3) : '—').join(' · ')}
          </div>
        </div>
      </div>

    </div>
  </div>`;
};

/* ── census section ────────────────────────────────────────────── */
const _censusSection = (d) => {
  const c = d.census;
  const litClass = c.Literacy >= 70 ? 'c-green' : c.Literacy >= 60 ? 'c-amber' : 'c-red';
  const srClass  = c.SexRatio >= 950 ? 'c-green' : c.SexRatio >= 900 ? 'c-amber' : 'c-red';

  return /* html */`
  <div class="sec">
    <div class="sec-hdr" onclick="toggleSec(this)">
      <span class="sec-title">Census (2011)</span>
      <span class="sec-chev open">▼</span>
    </div>
    <div class="sec-body open">
      <div class="stat-grid">
        <div class="stat">
          <div class="stat-lbl">Population</div>
          <div class="stat-val c-blue">${N(c.Pop)}</div>
        </div>
        <div class="stat">
          <div class="stat-lbl">Households</div>
          <div class="stat-val">${N(c.HH)}</div>
        </div>
        <div class="stat">
          <div class="stat-lbl">Literacy Rate</div>
          <div class="stat-val ${litClass}">
            ${N(c.Literacy, 2)}<span class="stat-unit">%</span>
          </div>
        </div>
        <div class="stat">
          <div class="stat-lbl">Sex Ratio</div>
          <div class="stat-val ${srClass}">
            ${N(c.SexRatio)}<span class="stat-unit">/1000♂</span>
          </div>
        </div>
        <div class="stat">
          <div class="stat-lbl">Population Density</div>
          <div class="stat-val">
            ${N(c.Density)}<span class="stat-unit">/km²</span>
          </div>
        </div>
        <div class="stat">
          <div class="stat-lbl">District Area</div>
          <div class="stat-val">
            ${N(d.area)}<span class="stat-unit">km²</span>
          </div>
        </div>
        <div class="stat">
          <div class="stat-lbl">SC Population</div>
          <div class="stat-val">${N(c.SC, 2)}<span class="stat-unit">%</span></div>
        </div>
        <div class="stat">
          <div class="stat-lbl">ST Population</div>
          <div class="stat-val">${N(c.ST, 2)}<span class="stat-unit">%</span></div>
        </div>
        <div class="stat">
          <div class="stat-lbl">Worker Rate</div>
          <div class="stat-val">${N(c.Workers, 2)}<span class="stat-unit">%</span></div>
        </div>
      </div>
    </div>
  </div>`;
};

/* ── health section ────────────────────────────────────────────── */
const _healthSection = (d) => {
  const h = d.hmis;
  const malC = (h.Malaria  > 0) ? 'c-red'   : 'c-green';
  const tbC  = (h.TB       > 0) ? 'c-red'   : 'c-green';
  const denC = (h.Dengue   > 0) ? 'c-red'   : 'c-green';
  const samC = (h.SAM      > 0) ? 'c-amber' : 'c-green';
  const lbwC = (h.LBW    > 400) ? 'c-red'   : (h.LBW > 200) ? 'c-amber' : 'c-teal';
  const diaC = (h.Diarrhoea > 300) ? 'c-red' : (h.Diarrhoea > 100) ? 'c-amber' : 'c-teal';

  return /* html */`
  <div class="sec">
    <div class="sec-hdr" onclick="toggleSec(this)">
      <span class="sec-title">Health Indicators (HMIS 2024)</span>
      <span class="sec-chev open">▼</span>
    </div>
    <div class="sec-body open">

      <div class="sub-label">Maternal &amp; Child Health</div>
      <div class="stat-grid">
        <div class="stat">
          <div class="stat-lbl">ANC Registered</div>
          <div class="stat-val c-teal">${N(h.ANC)}</div>
        </div>
        <div class="stat">
          <div class="stat-lbl">Inst. Deliveries</div>
          <div class="stat-val c-green">${N(h.Delivery)}</div>
        </div>
        <div class="stat">
          <div class="stat-lbl">C-Section Deliveries</div>
          <div class="stat-val">${N(h.CSection)}</div>
        </div>
        <div class="stat">
          <div class="stat-lbl">Low Birth Weight</div>
          <div class="stat-val ${lbwC}">${N(h.LBW)}</div>
        </div>
        <div class="stat">
          <div class="stat-lbl">Immunised (Male)</div>
          <div class="stat-val c-green">${N(h.ImmM)}</div>
        </div>
        <div class="stat">
          <div class="stat-lbl">Immunised (Female)</div>
          <div class="stat-val c-green">${N(h.ImmF)}</div>
        </div>
      </div>

      <div class="div"></div>
      <div class="sub-label">Disease Burden</div>
      <div class="stat-grid">
        <div class="stat">
          <div class="stat-lbl">Malaria Cases</div>
          <div class="stat-val ${malC}">${N(h.Malaria)}</div>
        </div>
        <div class="stat">
          <div class="stat-lbl">Tuberculosis</div>
          <div class="stat-val ${tbC}">${N(h.TB)}</div>
        </div>
        <div class="stat">
          <div class="stat-lbl">Dengue Cases</div>
          <div class="stat-val ${denC}">${N(h.Dengue)}</div>
        </div>
        <div class="stat">
          <div class="stat-lbl">Diarrhoea Cases</div>
          <div class="stat-val ${diaC}">${N(h.Diarrhoea)}</div>
        </div>
        <div class="stat">
          <div class="stat-lbl">SAM Cases</div>
          <div class="stat-val ${samC}">${N(h.SAM)}</div>
        </div>
      </div>

      <div class="div"></div>
      <div class="sub-label">Facility Utilisation</div>
      <div class="stat-grid">
        <div class="stat">
          <div class="stat-lbl">OPD Visits</div>
          <div class="stat-val c-blue">${N(h.OPD)}</div>
        </div>
        <div class="stat">
          <div class="stat-lbl">Inpatients</div>
          <div class="stat-val c-purple">${N(h.IPD)}</div>
        </div>
        <div class="stat">
          <div class="stat-lbl">Lab Tests</div>
          <div class="stat-val">${N(h.Lab)}</div>
        </div>
      </div>

    </div>
  </div>`;
};

/* ── livestock section ─────────────────────────────────────────── */
const _livestockSection = (d) => {
  const l = d.lstk;

  return `
  <div class="sec">
    <div class="sec-hdr" onclick="toggleSec(this)">
      <span class="sec-title">Livestock &amp; Animal Health (2024)</span>
      <span class="sec-chev open">▼</span>
    </div>
    <div class="sec-body open">
      <div class="stat-grid">
        <div class="stat">
          <div class="stat-lbl">Animals Treated</div>
          <div class="stat-val c-green">${N(l.Treatment)}</div>
        </div>
        <div class="stat">
          <div class="stat-lbl">Animals Benefited</div>
          <div class="stat-val c-teal">${N(l.Benefited)}</div>
        </div>
        <div class="stat">
          <div class="stat-lbl">Artificial Insemination</div>
          <div class="stat-val c-blue">${N(l.AI)}</div>
        </div>
        <div class="stat">
          <div class="stat-lbl">Poultry Units</div>
          <div class="stat-val">${N(l.Poultry)}</div>
        </div>
        <div class="stat">
          <div class="stat-lbl">Large Animal Drenching</div>
          <div class="stat-val">${N(l.DrenchLarge)}</div>
        </div>
        <div class="stat">
          <div class="stat-lbl">Sheep / Goat Drenching</div>
          <div class="stat-val">${N(l.DrenchSmall)}</div>
        </div>
        <div class="stat">
          <div class="stat-lbl">Chicks Distributed</div>
          <div class="stat-val">${N(l.Chicks)}</div>
        </div>
      </div>
    </div>
  </div>
  <div style="height:12px"></div>`;
};

/* ══════════════════════════════════════════════════════════════════
 * PUBLIC FUNCTIONS
 * ══════════════════════════════════════════════════════════════════ */

/**
 * Render the overview panel (no district selected).
 * @param {object} DATA – full data object from loadAllData()
 */
function renderOverview(DATA) {
  const panel = document.getElementById('panel');

  const cards = Object.entries(DATA)
    .map(([name, d]) => /* html */`
      <div class="dc-card" onclick="selectDistrict('${name}')">
        <div class="dc-dot" style="background:${d.color}"></div>
        <span class="dc-name">${titleCase(name)}</span>
        <span class="dc-score" style="color:${d.ohrsColor}">${d.ohrs}</span>
        <span class="badge badge-${d.riskClass}">( ${d.riskLabel} )</span>
      </div>`)
    .join('');

  panel.innerHTML = /* html */`
    <div class="ov-title">OneHealth Atlas</div>
    <p class="ov-sub">
      Click any district on the map to explore environmental, demographic,
      health, and livestock data integrated across 2016–2025.
    </p>

    <div class="dc-cards">${cards}</div>

    <div class="about-box">
      <div style="font-size:14px;font-weight:600;color:var(--text);margin-bottom:6px">
        One Health Risk Score (OHRS)
      </div>
      <strong>OHRS</strong> (0–10) combines:<br/>
      <strong>- Vegetation Loss</strong> (NDVI % change) → weight = 0.7<br/>
      <strong>- Urban Expansion</strong> (NDBI positive change) → weight = 0.3<br/><br/>
      Higher scores indicate greater environmental stress and potential risk
      to human and animal health.
      <div class="footer-note">
        Data: Resourcesat-2 LISS-III (ISRO-NRSC) · Census 2011 ·
        HMIS · Animal Husbandry Dept. 2024 ·
        Boundaries: Survey of India
      </div>
    </div>`;
}

/**
 * Render the district detail panel.
 * @param {object} DATA – full data object
 * @param {string} name – canonical district name (e.g. "HARIDWAR")
 */
function renderDetail(DATA, name) {
  const d     = DATA[name];
  const panel = document.getElementById('panel');

  if (!d) {
    panel.innerHTML = `<div class="error-state">No data found for "${name}".</div>`;
    return;
  }

  const ohrsPct = ((d.ohrs / 10) * 100).toFixed(1);

  panel.innerHTML = /* html */`
    <button class="back-btn" onclick="deselectDistrict()">← All districts</button>

    <div class="dh-row">
      <div class="dh-dot" style="background:${d.color}"></div>
      <div>
        <div class="dh-name">${titleCase(name)}</div>
        <div class="dh-meta">
          <span class="badge badge-${d.riskClass}">${d.riskLabel} RISK</span>
        </div>
      </div>
    </div>

    <div class="ohrs-wrap">
      <div class="ohrs-top">
        <span class="ohrs-label">One Health Risk Score</span>
        <span class="ohrs-num" style="color:${d.ohrsColor}">
          ${d.ohrs}<span class="ohrs-denom"> / 10</span>
        </span>
      </div>
      <div class="ohrs-bg">
        <div class="ohrs-fill"
             style="width:${ohrsPct}%;background:${d.ohrsColor}">
        </div>
      </div>
      <div class="ohrs-ticks">
        <span>0 (Low)</span><span>5 (Moderate)</span><span>10 (High)</span>
      </div>
    </div>

    ${_envSection(d)}
    ${_censusSection(d)}
    ${_healthSection(d)}
    ${_livestockSection(d)}`;

  panel.scrollTop = 0;
}