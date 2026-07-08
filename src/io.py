# Handle data loading

from pathlib import Path

import geopandas as gpd
import pandas as pd
import rasterio

from src.config import *

# ================ File Utilities ============================

def list_files(folder: Path):
    return sorted([f for f in folder.rglob("*") if f.is_file()])

def list_folders(folder: Path):
    return sorted([f for f in folder.rglob("*") if f.is_dir()])

# ================ Load Boundaries ============================

def load_district_boundary():
    path = BOUNDARIES / "District" / "DISTRICT_BOUNDARY.shp"
    return gpd.read_file(path)

def load_subdistrict_boundary():
    path = BOUNDARIES / "Taluk" / "SUBDISTRICT_BOUNDARY.shp"
    return gpd.read_file(path)

def load_state_boundary():
    path = BOUNDARIES / "District" / "STATE_BOUNDARY.shp"
    return gpd.read_file(path)

def load_major_towns():
    path = BOUNDARIES / "District" / "MAJOR_TOWNS.shp"
    return gpd.read_file(path)

# ================ Study Area ============================

STUDY_DISTRICTS = [
    "DEHRADUN",
    "HARIDWAR",
    "PAURI GARHWAL"
]

def load_study_districts():
    districts = load_district_boundary()
    return districts[
        districts["DISTRICT"].str.upper().isin(STUDY_DISTRICTS)
    ]

def load_study_taluks():
    taluks = load_subdistrict_boundary()
    return taluks[
        taluks["DISTRICT"].str.upper().isin(STUDY_DISTRICTS)
    ]

# ================ Satellite ============================

def list_satellite_years():

    return sorted([
        p.name
        for p in SATELLITE.iterdir()
        if p.is_dir()
    ])

def list_scenes(year):
    year_path = SATELLITE / str(year)

    return sorted([
        p
        for p in year_path.iterdir()
        if p.is_dir()
    ])

def list_band_files(scene_path):
    return sorted(scene_path.glob("BAND*.tif"))

def get_band_metadata(scene_path):
    return scene_path / "BAND_META.txt"

def get_accuracy_report(scene_path):
    return scene_path / "ACC_REP.txt"

def open_raster(path):
    return rasterio.open(path)

# ================ HMIS ============================

def get_hmis_files():
    return sorted(HEALTH.glob("*.xls"))

# ================ Census ============================

def get_census_files():
    return sorted(CENSUS.glob("*.xlsx"))

# ================ Livestock ============================

def get_livestock_file():
    pdf = list(LIVESTOCK.glob("*.pdf"))