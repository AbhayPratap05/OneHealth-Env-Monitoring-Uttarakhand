from pathlib import Path

import geopandas as gpd
import rasterio
from rasterio.mask import mask


def clip_raster(input_raster, boundary_file, output_raster):
    """
    Clip raster using a polygon boundary.
    """

    input_raster = Path(input_raster)
    boundary_file = Path(boundary_file)
    output_raster = Path(output_raster)

    output_raster.parent.mkdir(parents=True, exist_ok=True)

    boundary = gpd.read_file(boundary_file)

    with rasterio.open(input_raster) as src:

        if boundary.crs != src.crs:
            boundary = boundary.to_crs(src.crs)

        geometries = boundary.geometry.values

        clipped, transform = mask(
            src,
            geometries,
            crop=True,
            nodata=src.nodata,
        )

        metadata = src.meta.copy()

        metadata.update(
            {
                "height": clipped.shape[1],
                "width": clipped.shape[2],
                "transform": transform,
            }
        )

    with rasterio.open(output_raster, "w", **metadata) as dst:
        dst.write(clipped)

    return output_raster


def batch_clip(mosaic_root, boundary_file, output_root, years, bands):
    """
    Clip all mosaicked bands for every year
    """

    mosaic_root = Path(mosaic_root)
    output_root = Path(output_root)

    for year in years:

        print(f"\nProcessing {year}")

        year_in = mosaic_root / str(year)
        year_out = output_root / str(year)

        year_out.mkdir(parents=True, exist_ok=True)

        for band in bands:

            raster = year_in / f"{band}.tif"

            if not raster.exists():
                print(f"Skipping {band}")
                continue

            print(f"  Clipping {band}")

            clip_raster(
                raster,
                boundary_file,
                year_out / f"{band}.tif",
            )