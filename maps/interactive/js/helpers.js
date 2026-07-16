/* js/helpers.js
 * Pure utility functions — no DOM or data dependencies.
 * Loaded first; safe to call from any other module.
 */

/** Format a number with Indian locale separators, e.g. 1,69,694 */
function N(v, decimals = 0) {
  if (v == null || v === '' || isNaN(v)) return '—';
  return Number(v).toLocaleString('en-IN', { maximumFractionDigits: decimals });
}

/** Signed string, e.g. "+0.089" or "−0.004" */
function sgn(v, decimals = 3) {
  if (v == null) return '—';
  return (v >= 0 ? '+' : '−') + Math.abs(v).toFixed(decimals);
}

/** Up/down arrow character */
function arw(v) { return (v != null && v >= 0) ? '▲' : '▼'; }

/**
 * CSS colour for a change value.
 * posGood = true  → positive change is good (green), negative is bad (red)
 * posGood = false → positive change is bad  (red),  negative is good (green)
 */
function chgColor(v, posGood = true) {
  if (v == null) return 'var(--muted)';
  if (posGood) return v >= 0 ? 'var(--green)' : 'var(--red)';
  return v >= 0 ? 'var(--red)' : 'var(--green)';
}

/** Title-case a string, e.g. "PAURI GARHWAL" → "Pauri Garhwal" */
function titleCase(s) {
  return String(s).toLowerCase().replace(/\b\w/g, c => c.toUpperCase());
}

/**
 * Render an inline SVG sparkline from an array of values.
 * @param {number[]} vals   – data points (any range)
 * @param {string}   color  – stroke colour
 * @param {number}   w      – SVG width  (px)
 * @param {number}   h      – SVG height (px)
 * @returns {string} SVG markup string
 */
function spark(vals, color, w = 88, h = 34) {
  const clean = vals.filter(v => v != null && !isNaN(v));
  if (clean.length < 2) return '<span style="color:var(--muted);font-size:10px">—</span>';

  const mn  = Math.min(...clean);
  const mx  = Math.max(...clean);
  const rng = mx - mn || 0.001;
  const pad = 3;

  const pts = clean.map((v, i) => {
    const x = (i / (clean.length - 1)) * (w - 2 * pad) + pad;
    const y = h - pad - ((v - mn) / rng) * (h - 2 * pad);
    return `${x.toFixed(1)},${y.toFixed(1)}`;
  }).join(' ');

  const lx = w - pad;
  const ly = h - pad - ((clean[clean.length - 1] - mn) / rng) * (h - 2 * pad);
  const fx = pad;
  const fy = h - pad - ((clean[0] - mn) / rng) * (h - 2 * pad);

  return `<svg width="${w}" height="${h}" viewBox="0 0 ${w} ${h}"
              style="display:block;overflow:visible" aria-hidden="true">
    <circle cx="${fx.toFixed(1)}" cy="${fy.toFixed(1)}" r="2.2"
      fill="${color}" opacity=".4"/>
    <polyline points="${pts}" fill="none" stroke="${color}" stroke-width="2"
      stroke-linejoin="round" stroke-linecap="round"/>
    <circle cx="${lx.toFixed(1)}" cy="${ly.toFixed(1)}" r="3" fill="${color}"/>
  </svg>`;
}