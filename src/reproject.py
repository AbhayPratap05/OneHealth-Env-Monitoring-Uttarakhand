# Reproject raster to target CRS

from pathlib import Path

import rasterio
from rasterio.warp import calculate_default_transform
from rasterio.warp import reproject
from rasterio.warp import Resampling

TARGET_CRS = "EPSG:32644"


def reproject_raster(
    input_path,
    output_path,
    dst_crs=TARGET_CRS,
    resampling=Resampling.nearest,
):

    input_path = Path(input_path)
    output_path = Path(output_path)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with rasterio.open(input_path) as src:
        
        transform, width, height = calculate_default_transform(
            src.crs,
            dst_crs,
            src.width,
            src.height,
            *src.bounds,
        )

        kwargs = src.meta.copy()

        kwargs.update(
            {
                "crs": dst_crs,
                "transform": transform,
                "width": width,
                "height": height,
            }
        )

        with rasterio.open(output_path, "w", **kwargs) as dst:

            for band in range(1, src.count + 1):

                reproject(
                    source=rasterio.band(src, band),
                    destination=rasterio.band(dst, band),
                    src_transform=src.transform,
                    src_crs=src.crs,
                    dst_transform=transform,
                    dst_crs=dst_crs,
                    resampling=resampling,
                )

    return output_path

def batch_reproject(raw_root, output_root, years):

    """
    Reproject every raster under each year's Scene folders.
    """

    for year in years:
        raw_dir = Path(raw_root) / str(year)
        out_dir = Path(output_root) / str(year)

        for raster in raw_dir.rglob("*.tif"):

            relative = raster.relative_to(raw_dir)

            print(f"Reprojecting {relative}")
            reproject_raster(raster, out_dir / relative)