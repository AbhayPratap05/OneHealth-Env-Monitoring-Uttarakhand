# Handle data loading

from pathlib import Path

import geopandas as gpd
import pandas as pd
import rasterio

from src.config import (
    BOUNDARIES,
    SATELLITE,
    HEALTH,
    CENSUS,
)

def list_files(folder: Path, extension=None):
    if extension:

        return sorted(folder.rglob(f"*{extension}"))
    return sorted(folder.rglob("*"))

def load_shapefile(path):
    return gpd.read_file(path)

def load_excel(path):
    return pd.read_excel(path)

def load_csv(path):
    return pd.read_csv(path)

def open_raster(path):
    return rasterio.open(path)

def list_satellite_years():

    years = [
        p.name
        for p in SATELLITE.iterdir()
        if p.is_dir()
    ]
    return sorted(years)

def list_scenes(year):
    year_path = SATELLITE / str(year)

    return sorted(
        [
            p
            for p in year_path.iterdir()
            if p.is_dir()
        ]
    )

def list_band_files(scene_path):
    return sorted(scene_path.glob("BAND*.tif"))

def get_accuracy_report(scene_path):
    return scene_path / "ACC_REP.txt"