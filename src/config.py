# For project configuration and path definition

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

DATA = ROOT / "data"
RAW = DATA / "raw"
PROCESSED = DATA / "processed"
SAMPLE = DATA / "sample"

# Raw Data:
BOUNDARIES = RAW / "boundaries"
SATELLITE = RAW / "satellite"
HEALTH = RAW / "health"
LIVESTOCK = RAW / "livestock"
CENSUS = RAW / "census"

# Outputs
MAPS = ROOT / "maps"
STATIC_MAPS = MAPS / "static"
INTERACTIVE_MAPS = MAPS / "interactive"

REPORT = ROOT / "report"
NOTEBOOKS = ROOT / "notebooks"

# CRS
DEFAULT_CRS = "EPSG:4326"
TARGET_CRS = "EPSG:32644"