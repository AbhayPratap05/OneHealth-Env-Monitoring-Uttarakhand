from pathlib import Path

import geopandas as gpd
import pandas as pd
import numpy as np
import rasterio
from rasterstats import zonal_stats


STATS = [
    "mean",
    "median",
    "min",
    "max",
    "std",
    "count",
]

def zonal_statistics(
    raster_path,
    polygons,
    index_name,
    year,
    district_column="district",
):
    """
    Compute zonal statistics for one raster.
    """

    with rasterio.open(raster_path) as src:
        image = src.read(1)
        affine = src.transform

    stats = zonal_stats(
    polygons,
    image,
    affine=affine,
    stats=STATS,
    nodata=-9999.0,
    all_touched=True,
)
    
    rows = []

    for poly, values in zip(polygons.itertuples(), stats):

        row = {
            "district": getattr(poly, district_column),
            "year": year,
            "index": index_name,
        }

        row.update(values)
        rows.append(row)

    return pd.DataFrame(rows)


def batch_zonal_statistics(
    indices_root,
    district_file,
    output_csv,
    years,
    indices,
    district_column="DISTRICT",
):

    polygons = gpd.read_file(district_file)

    all_tables = []

    for year in years:
        print(f"\nProcessing {year}")

        year_dir = Path(indices_root) / str(year)

        for index_name in indices:
            raster = year_dir / f"{index_name}.tif"

            print(f"  {index_name}")

            with rasterio.open(raster) as src:
                polygons_proj = polygons.to_crs(src.crs)

            table = zonal_statistics(
                raster,
                polygons_proj,
                index_name,
                year,
                district_column,
            )

            all_tables.append(table)

    result = pd.concat(
        all_tables,
        ignore_index=True,
    )

    Path(output_csv).parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    result.to_csv(
        output_csv,
        index=False,
    )

    return result