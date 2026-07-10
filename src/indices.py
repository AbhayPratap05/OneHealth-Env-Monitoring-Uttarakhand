# Compute NDVI, NDWI and NDBI indices.

from pathlib import Path

import numpy as np
import rasterio


def _read_band(path):
    with rasterio.open(path) as src:
        band = src.read(1).astype(np.float32)
        meta = src.meta.copy()
    return band, meta


def _safe_divide(numerator, denominator):
    with np.errstate(divide="ignore", invalid="ignore"):
        result = numerator / denominator
        result[denominator == 0] = np.nan
    return result.astype(np.float32)


def calculate_index(numerator, denominator):
    return _safe_divide(
        numerator - denominator,
        numerator + denominator,
    )


def save_index(index_array, metadata, output_path):
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    metadata.update(
        dtype="float32",
        count=1,
        nodata=np.nan,
    )

    with rasterio.open(output_path, "w", **metadata) as dst:
        dst.write(index_array, 1)


def compute_ndvi(red_path, nir_path, output_path):
    red, meta = _read_band(red_path)
    nir, _ = _read_band(nir_path)

    ndvi = calculate_index(nir, red)

    save_index(ndvi, meta, output_path)


def compute_ndwi(green_path, nir_path, output_path):
    green, meta = _read_band(green_path)
    nir, _ = _read_band(nir_path)

    ndwi = calculate_index(green, nir)

    save_index(ndwi, meta, output_path)


def compute_ndbi(swir_path, nir_path, output_path):
    swir, meta = _read_band(swir_path)
    nir, _ = _read_band(nir_path)

    ndbi = calculate_index(swir, nir)

    save_index(ndbi, meta, output_path)


def batch_compute_indices(clipped_root, output_root, years):
    clipped_root = Path(clipped_root)
    output_root = Path(output_root)

    for year in years:

        print(f"\nProcessing {year}")

        in_dir = clipped_root / str(year)
        out_dir = output_root / str(year)

        out_dir.mkdir(parents=True, exist_ok=True)

        compute_ndvi(
            in_dir / "BAND3.tif",
            in_dir / "BAND4.tif",
            out_dir / "NDVI.tif",
        )

        print("  ✓ NDVI")

        compute_ndwi(
            in_dir / "BAND2.tif",
            in_dir / "BAND4.tif",
            out_dir / "NDWI.tif",
        )

        print("  ✓ NDWI")

        compute_ndbi(
            in_dir / "BAND5.tif",
            in_dir / "BAND4.tif",
            out_dir / "NDBI.tif",
        )

        print("  ✓ NDBI")