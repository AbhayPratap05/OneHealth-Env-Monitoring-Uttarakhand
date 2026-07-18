# 🌏 One Health Environmental Risk Monitoring — Uttarakhand

<div align="center">

**A Remote Sensing and GIS based Decision Support System for Environmental Health Risk Assessment**

[![Live Map](https://img.shields.io/badge/🗺️%20Interactive%20Map-Live-brightgreen?style=for-the-badge)](https://abhaypratap05.github.io/OneHealth-Env-Monitoring-Uttarakhand/)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

[![SDG 3](https://img.shields.io/badge/SDG-3%20Good%20Health-red?style=for-the-badge)](https://sdgs.un.org/goals/goal3)
[![SDG 6](https://img.shields.io/badge/SDG-6%20Clean%20Water-blue?style=for-the-badge)](https://sdgs.un.org/goals/goal6)
[![SDG 15](https://img.shields.io/badge/SDG-15%20Life%20on%20Land-green?style=for-the-badge)](https://sdgs.un.org/goals/goal15)

*A geospatial pipeline connecting Resourcesat-2 satellite imagery with health and livestock data to produce district-level One Health Risk Scores for Uttarakhand, India.*

</div>

---

## 📍 Study Area

**Districts:** Dehradun · Haridwar · Pauri Garhwal — Uttarakhand, India  
**Time span:** 2016 → 2022 → 2025 (9-year change detection)  
**Data source (satellite):** Resourcesat-2 LISS-III via ISRO Bhoonidhi

<div align="center">

| | |
|:---:|:---:|
| ![India Context](https://raw.githubusercontent.com/AbhayPratap05/OneHealth-Env-Monitoring-Uttarakhand/main/maps/static/01_india_context.png) | ![Study Area](https://raw.githubusercontent.com/AbhayPratap05/OneHealth-Env-Monitoring-Uttarakhand/main/maps/static/02_study_area.png) |
| *Geographic context — India* | *Study area — 3 districts of Uttarakhand* |

</div>

---

## 🗺️ Interactive Atlas

**[→ Open OneHealth Environmental Atlas](https://abhaypratap05.github.io/OneHealth-Env-Monitoring-Uttarakhand/)**

The interactive dashboard allows you to:
- Click any district to explore its full environmental, demographic, health, and livestock profile
- Toggle choropleth layers between **Vegetation (NDVI)**, **Water signal (NDWI)**, and **Built-up (NDBI)** change
- View temporal sparklines showing index trends across 2016, 2022, and 2025
- See the computed **One Health Risk Score (OHRS)** per district

---

## 📊 Key Findings

### One Health Risk Score

| District | OHRS | Risk Level | NDVI Change | NDBI Change |
|---|:---:|:---:|:---:|:---:|
| **Haridwar** | **8.1 / 10** | 🔴 HIGH | −17.9% | +0.030 (urban expansion) |
| **Dehradun** | **6.2 / 10** | 🟡 MODERATE | −17.7% | −0.004 |
| **Pauri Garhwal** | **5.1 / 10** | 🟢 LOW | −14.7% | −0.020 |

> **OHRS** = 0.7 × Vegetation loss score + 0.3 × Urban expansion score (scaled 0–10)

### Summary of Environmental Changes (2016 → 2025)
- All three districts show significant **vegetation decline** (NDVI), with Haridwar recording the sharpest drop.
- **NDWI** increased (became less negative) across all districts, a signal linked to reduced NIR reflectance from vegetation loss rather than water gain.
- **Haridwar** is the only district with a positive NDBI change, confirming measurable **urban expansion**.

---

## 🛰️ Index Maps

### NDVI — Vegetation Cover

<div align="center">

| 2016 | 2022 | 2025 |
|:---:|:---:|:---:|
| ![NDVI 2016](https://raw.githubusercontent.com/AbhayPratap05/OneHealth-Env-Monitoring-Uttarakhand/main/maps/static/index_maps/NDVI_2016.png) | ![NDVI 2022](https://raw.githubusercontent.com/AbhayPratap05/OneHealth-Env-Monitoring-Uttarakhand/main/maps/static/index_maps/NDVI_2022.png) | ![NDVI 2025](https://raw.githubusercontent.com/AbhayPratap05/OneHealth-Env-Monitoring-Uttarakhand/main/maps/static/index_maps/NDVI_2025.png) |

</div>

### NDWI — Water Body Index

<div align="center">

| 2016 | 2022 | 2025 |
|:---:|:---:|:---:|
| ![NDWI 2016](https://raw.githubusercontent.com/AbhayPratap05/OneHealth-Env-Monitoring-Uttarakhand/main/maps/static/index_maps/NDWI_2016.png) | ![NDWI 2022](https://raw.githubusercontent.com/AbhayPratap05/OneHealth-Env-Monitoring-Uttarakhand/main/maps/static/index_maps/NDWI_2022.png) | ![NDWI 2025](https://raw.githubusercontent.com/AbhayPratap05/OneHealth-Env-Monitoring-Uttarakhand/main/maps/static/index_maps/NDWI_2025.png) |

</div>

### NDBI — Built-up Index

<div align="center">

| 2016 | 2022 | 2025 |
|:---:|:---:|:---:|
| ![NDBI 2016](https://raw.githubusercontent.com/AbhayPratap05/OneHealth-Env-Monitoring-Uttarakhand/main/maps/static/index_maps/NDBI_2016.png) | ![NDBI 2022](https://raw.githubusercontent.com/AbhayPratap05/OneHealth-Env-Monitoring-Uttarakhand/main/maps/static/index_maps/NDBI_2022.png) | ![NDBI 2025](https://raw.githubusercontent.com/AbhayPratap05/OneHealth-Env-Monitoring-Uttarakhand/main/maps/static/index_maps/NDBI_2025.png) |

</div>

---

## 🗺️ Change Detection Maps (2016 → 2025)

<div align="center">

| NDVI Change | NDWI Change | NDBI Change |
|:---:|:---:|:---:|
| ![NDVI Change](https://raw.githubusercontent.com/AbhayPratap05/OneHealth-Env-Monitoring-Uttarakhand/main/maps/static/change_maps/NDVI_change_16_25.png) | ![NDWI Change](https://raw.githubusercontent.com/AbhayPratap05/OneHealth-Env-Monitoring-Uttarakhand/main/maps/static/change_maps/NDWI_change_16_25.png) | ![NDBI Change](https://raw.githubusercontent.com/AbhayPratap05/OneHealth-Env-Monitoring-Uttarakhand/main/maps/static/change_maps/NDBI_change_16_25.png) |
| *Vegetation loss* | *Water signal shift* | *Urban expansion* |

</div>

---

## 📈 Statistical Analysis

<div align="center">

| All Index Changes | Correlation Heatmap |
|:---:|:---:|
| ![All Index Changes](https://raw.githubusercontent.com/AbhayPratap05/OneHealth-Env-Monitoring-Uttarakhand/main/data/results/figures/All_Index_Changes.png) | ![Correlation Heatmap](https://raw.githubusercontent.com/AbhayPratap05/OneHealth-Env-Monitoring-Uttarakhand/main/data/results/figures/Correlation_Heatmap.png) |

</div>

<div align="center">

| NDVI Change | NDWI Change | NDBI Change |
|:---:|:---:|:---:|
| ![NDVI change](https://raw.githubusercontent.com/AbhayPratap05/OneHealth-Env-Monitoring-Uttarakhand/main/data/results/figures/NDVI_change_16_25.png) | ![NDWI change](https://raw.githubusercontent.com/AbhayPratap05/OneHealth-Env-Monitoring-Uttarakhand/main/data/results/figures/NDWI_change_16_25.png) | ![NDBI change](https://raw.githubusercontent.com/AbhayPratap05/OneHealth-Env-Monitoring-Uttarakhand/main/data/results/figures/NDBI_change_16_25.png) |

</div>

<div align="center">

| NDVI Distribution | NDWI Distribution | NDBI Distribution |
|:---:|:---:|:---:|
| ![NDVI Distribution](https://raw.githubusercontent.com/AbhayPratap05/OneHealth-Env-Monitoring-Uttarakhand/main/data/results/figures/NDVI_Distribution.png) | ![NDWI Distribution](https://raw.githubusercontent.com/AbhayPratap05/OneHealth-Env-Monitoring-Uttarakhand/main/data/results/figures/NDWI_Distribution.png) | ![NDBI Distribution](https://raw.githubusercontent.com/AbhayPratap05/OneHealth-Env-Monitoring-Uttarakhand/main/data/results/figures/NDBI_Distribution.png) |

</div>

---

## 🗂️ Data Sources

| Layer | Source | Period | Format |
|---|---|:---:|:---:|
| Satellite imagery (LISS-III) | ISRO Bhoonidhi | 2016, 2022, 2025 | GeoTIFF (4 bands) |
| Administrative boundaries | Survey of India | 2025 | Shapefile |
| Census socioeconomic data | Census of India 2011 | 2011 | XLSX → CSV |
| HMIS health facility data | Ministry of Health (HMIS) | 2015–22 | XLSX → CSV |
| Animal husbandry statistics | Dept. of Animal Husbandry, Uttarakhand | 2024 | PDF → CSV |

---

## 🔧 Tools & Technologies

| Category | Tools |
|---|---|
| **Remote sensing** | Rasterio, NumPy — band computation, reprojection, mosaicking, clipping |
| **Spatial analysis** | GeoPandas, Rasterstats — zonal statistics, spatial joins |
| **Visualisation** | Matplotlib, Folium — static maps, charts, interactive atlas |
| **GIS** | QGIS 3.x — visual inspection, styling, Print Layout exports |
| **Web** | Leaflet.js, PapaParse, Vanilla JS, CSS — interactive dashboard |
| **Data** | Pandas — CSV processing, HMIS/census wrangling |
| **Build** | Python 3.10+, pyproject.toml, FOSS toolchain |

---

## 📁 Project Structure

```
.
├── data/
│   ├── raw/                    # Original satellite tiles, shapefiles, HMIS, census
│   ├── processed/              # Reprojected → mosaicked → clipped bands, indices
│   └── results/
│       ├── csv/                # Zonal statistics, temporal summaries, change tables
│       └── figures/            # Analysis charts (PNG + PDF)
├── maps/
│   ├── static/                 # QGIS-exported index maps and change maps (PNG)
│   └── interactive/            # OneHealth Atlas (HTML + CSS + JS)
│       ├── index.html
│       ├── css/style.css
│       ├── data/               # GeoJSON, CSVs served to the browser
│       └── js/
│           ├── app.js          # Initialisation and state management
│           ├── data.js         # CSV + GeoJSON loader, OHRS computation
│           ├── helpers.js      # Utility functions (formatting, sparklines)
│           ├── map.js          # Leaflet map, choropleth layers
│           └── panel.js        # Info panel rendering
├── notebooks/
│   ├── 01_data_audit.ipynb
│   ├── 02_reproject_mosaic_clip.ipynb
│   ├── 03_compute_indices.ipynb
│   ├── 04_zonal_statistics.ipynb
│   ├── 05_temporal_analysis.ipynb
│   ├── 06_visualization.ipynb
│   ├── 07_static_maps.ipynb
│   └── 08_prepare_auxiliary_data.ipynb
├── src/                        # Reusable Python modules (indices, zonal, mapping …)
├── report/
│   ├── PROJECT_REPORT.md
│   └── TECHNICAL_DETAILS.md
├── requirements.txt
└── pyproject.toml
```

---

## ⚙️ Setup & Installation

```bash
# 1. Clone the repository
git clone https://github.com/AbhayPratap05/OneHealth-Env-Monitoring-Uttarakhand.git
cd OneHealth-Env-Monitoring-Uttarakhand

# 2. Create a virtual environment
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
# or, using pyproject.toml:
pip install -e .

# 4. Run notebooks in order
jupyter notebook notebooks/
```

### Viewing the interactive map locally

```bash
# Serve from the interactive map folder (fetch() requires HTTP, not file://)
cd maps/interactive
python -m http.server 8000
# then open http://localhost:8000
```

---

## 📄 Documentation

| Document | Description |
|---|---|
| [`report/PROJECT_REPORT.md`](report/PROJECT_REPORT.md) | Introduction, objectives, methodology, results and conclusions |
| [`report/TECHNICAL_DETAILS.md`](report/TECHNICAL_DETAILS.md) | Full pipeline walkthrough — raw imagery to interactive dashboard |
| [`report/DATA_INVENTORY.md`](report/DATA_INVENTORY.md) | Dataset catalogue and file inventory |

---

## 🇺🇳 SDG Alignment

| SDG | Goal | Relevance |
|:---:|---|---|
| **SDG 3** | Good Health and Well-Being | Mapping health facility access and disease burden |
| **SDG 6** | Clean Water and Sanitation | Waterbody change detection via NDWI |
| **SDG 15** | Life on Land | Vegetation cover change and land degradation monitoring |

---

## 👤 Author

**Abhay Pratap**  
B.Tech CSE (Health Informatics) · Vellore Institute of Technology  
[GitHub](https://github.com/AbhayPratap05) · [LinkedIn](https://linkedin.com/in/abhaypratap05)

---

## 🙏 Acknowledgements

- **ISRO NRSC / Bhoonidhi -** Resourcesat-2 LISS-III satellite imagery
- **Survey of India -** Administrative boundary shapefiles
- **Ministry of Health & Family Welfare -** HMIS data portal
- **Department of Animal Husbandry, Uttarakhand -** Livestock statistics
- **Census of India 2011 -** Demographic and socioeconomic data

---

<div align="center">
<sub>Built with Python · QGIS · Leaflet.js · All FOSS toolchain</sub>
</div>