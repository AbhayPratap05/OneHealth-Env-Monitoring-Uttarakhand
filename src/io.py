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