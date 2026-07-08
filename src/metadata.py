# Metadata utilities for datasets

from pathlib import Path
import geopandas as gpd
import pandas as pd
import rasterio

def get_vector_metadata(gdf: gpd.GeoDataFrame) -> dict:

    bounds = gdf.total_bounds

    return {
        "Dataset Type": "Vector",
        "Features": len(gdf),
        "Columns": list(gdf.columns),
        "Geometry": gdf.geom_type.iloc[0] if not gdf.empty else None,
        "CRS": str(gdf.crs),
        "Bounds": {
            "xmin": bounds[0],
            "ymin": bounds[1],
            "xmax": bounds[2],
            "ymax": bounds[3],
        },
    }

def get_raster_metadata(src: rasterio.io.DatasetReader) -> dict:

    return {
        "Dataset Type": "Raster",
        "Width": src.width,
        "Height": src.height,
        "Bands": src.count,
        "CRS": str(src.crs),
        "Resolution": src.res,
        "Bounds": src.bounds,
        "Data Type": src.dtypes,
        "NoData": src.nodata,
        "Driver": src.driver,
        "Transform": src.transform,
        "Descriptions": src.descriptions,
    }

def get_dataframe_metadata(df: pd.DataFrame) -> dict:

    return {
        "Dataset Type": "Tabular",
        "Rows": df.shape[0],
        "Columns": df.shape[1],
        "Column Names": list(df.columns),
        "Missing Values": df.isnull().sum().to_dict(),
        "Data Types": df.dtypes.astype(str).to_dict(),
    }

def print_metadata(metadata: dict):
    
    print("=" * 70)

    for key, value in metadata.items():
        print(f"{key}: {value}")

    print("=" * 70)