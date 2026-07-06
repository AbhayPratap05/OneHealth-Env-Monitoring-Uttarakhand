# One Health Environmental Risk Monitoring - Uttarakhand

- (Darft)

A Remote Sensing and GIS based Decision Support System for Environmental Health Risk Assessment in Uttarakhand.

A geospatial data workflow that connects satellite-derived environmental data with health infrastructure accessibility to produce district-level One Health risk scores for Uttarakhand, India.

Built to demonstrate how remote sensing and GIS can support environmental risk
detection and inform field diagnostic workflows, aligned with the One Health
framework linking human, animal, and environmental health.

## Study Area
Dehradun · Haridwar · Pauri Garhwal · Tehri Garhwal - Uttarakhand, India

## Data Sources
| Layer | Source | Years |
|---|---|---|
| Admin boundaries (district) | Survey of India | 2025 |
| Admin boundaries (taluk) | Survey of India | 2025 |
| LISS-III tiles  | Bhoonidhi | 2016, 2022, 2025 |
| District shapefiles | data.gov.in | - |
| Health facilities | data.gov.in | 2015-22 |
| Animal husbandry | data.gov.in | 2024 |

## Workflow
1. Data inventory & spatial baseline (`notebooks/01_data_inventory.ipynb`)
2. LULC change detection (`notebooks/02_lulc_change_detection.ipynb`)
3. Waterbody degradation via NDWI (`notebooks/03_ndwi_analysis.ipynb`)
4. Health data integration (`notebooks/04_health_integration.ipynb`)
5. One Health risk score (`notebooks/05_risk_score.ipynb`)

## Tools
QGIS 3.x · Python (GeoPandas · Rasterio · Folium · Rasterstats) · All FOSS

## SDG Alignment
SDG 3 (Good health) · SDG 6 (Clean water) · SDG 15 (Life on land)