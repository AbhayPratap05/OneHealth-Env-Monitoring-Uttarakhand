from pathlib import Path

import geopandas as gpd


# ================ GeoDataFrame ============================

def export_geopackage(gdf, output_path):
    output_path = Path(output_path)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    gdf.to_file(
        output_path,
        driver="GPKG",
    )

    print(f"Saved {output_path}")


def export_geojson(gdf, output_path):

    output_path = Path(output_path)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    gdf.to_file(
        output_path,
        driver="GeoJSON",
    )

    print(f"Saved {output_path}")


def export_shapefile(gdf, output_folder):

    output_folder = Path(output_folder)

    output_folder.mkdir(
        parents=True,
        exist_ok=True,
    )

    gdf.to_file(output_folder)

    print(f"Saved {output_folder}")


# ================ Figures ============================

def save_figure(
    fig,
    output_path,
    dpi=300,
):

    output_path = Path(output_path)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    fig.savefig(
        output_path,
        dpi=dpi,
        bbox_inches="tight",
    )

    print(f"Saved {output_path}")