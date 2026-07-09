from pathlib import Path

import rasterio
from rasterio.merge import merge


def mosaic_band(input_files, output_file):
    """
    Mosaic multiple rasters of the same band but diff scenes
    """

    output_file = Path(output_file)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    src_files = [rasterio.open(fp) for fp in input_files]

    mosaic, transform = merge(src_files)

    metadata = src_files[0].meta.copy()

    metadata.update(
        {
            "driver": "GTiff",
            "height": mosaic.shape[1],
            "width": mosaic.shape[2],
            "transform": transform,
        }
    )

    with rasterio.open(output_file, "w", **metadata) as dst:
        dst.write(mosaic)

    for src in src_files:
        src.close()

    return output_file


def batch_mosaic(reprojected_root, output_root, years, bands):
    """
    Mosaic each spectral band for every year
    """

    reprojected_root = Path(reprojected_root)
    output_root = Path(output_root)

    for year in years:

        year_dir = reprojected_root / str(year)
        out_dir = output_root / str(year)

        out_dir.mkdir(parents=True, exist_ok=True)

        print(f"\nProcessing {year}")

        for band in bands:

            rasters = sorted(year_dir.rglob(f"{band}.tif"))

            if len(rasters) == 0:
                print(f"Skipping {band}")
                continue

            print(f"  {band}: {len(rasters)} scenes")

            mosaic_band(
                rasters,
                out_dir / f"{band}.tif",
            )