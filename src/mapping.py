"""
Generate:
- Year-wise index maps
- Change maps
"""

from pathlib import Path

import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.patheffects as pe
import pandas as pd

# ------------------------------------------------- Styling -------------------------------------------------

INDEX_META = {
    "NDVI": {
        "legend": "Mean NDVI",
        "title": "Normalized Difference Vegetation Index",
        "footer": "Higher values (green) indicate denser vegetation.\nNegative changes (yellow) represent vegetation loss.",
    },
    "NDWI": {
        "legend": "Mean NDWI",
        "title": "Normalized Difference Water Index",
        "footer": "Higher values (blue) indicate a stronger water signal.\nPositive changes represent increased water presence.",
    },
    "NDBI": {
        "legend": "Mean NDBI",
        "title": "Normalized Difference Built-up Index",
        "footer": "Higher values (red) indicate greater built-up area.\nPositive changes represent urban expansion.",
    },
}

CHANGE_MAP_META = {
    "NDVI_change_16_25": {
        "title": "Vegetation Change\n2016 - 2025",
        "label": "NDVI Change",
        "footer": "Green = vegetation gain\nRed = vegetation loss",
    },
    "NDWI_change_16_25": {
        "title": "Water Body Signal Change\n2016 - 2025",
        "label": "NDWI Change",
        "footer": "Blue = stronger water signal\nRed = weaker water signal",
    },
    "NDBI_change_16_25": {
        "title": "Built-up Area Change\n2016 - 2025",
        "label": "NDBI Change",
        "footer": "Red = urban expansion\nGreen = reduction in built-up area",
    },
}

COLORMAPS = {
    "NDVI": "YlGn",
    "NDWI": "YlGnBu",
    "NDBI": "YlOrRd",

    "NDVI_change_16_25": "RdYlGn",
    "NDWI_change_16_25": "RdBu",
    "NDBI_change_16_25": "RdYlGn_r",
}

COLOR_LIMITS = {
    "NDVI_change_16_25": (-0.10, 0.10),
    "NDWI_change_16_25": (-0.10, 0.10),
    "NDBI_change_16_25": (-0.04, 0.04),
}

def _setup_style():

    plt.rcParams.update({
        "figure.dpi": 150,
        "savefig.dpi": 300,
        "font.size": 11,
        "axes.titlesize": 15,
        "axes.titleweight": "bold",
        "savefig.bbox": "tight",
    })


def _save(fig, output_path):

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fig.savefig(output_path.with_suffix(".png"))

    plt.close(fig)


# ------------------------------------------------- Data preparation -------------------------------------------------

def prepare_map_data(districts_file, temporal_summary_csv):
    """
    Join district geometries with temporal statistics.
    """
    districts = gpd.read_file(districts_file)
    summary = pd.read_csv(temporal_summary_csv)

    merged = districts.merge(
        summary,
        left_on="DISTRICT",
        right_on="district",
    )

    return merged

# ------------------------------------------------- Index Maps -------------------------------------------------

def plot_index_map(
    gdf,
    index_name,
    year,
    output_dir=None,
):

    _setup_style()

    meta = INDEX_META[index_name]
    data = gdf[gdf["year"] == year]

    fig, ax = plt.subplots(figsize=(8, 8))

    data.plot(
        column=index_name,
        cmap=COLORMAPS[index_name],
        linewidth=0.8,
        edgecolor="black",
        legend=True,
        legend_kwds={
            "label": meta["legend"],
            "shrink": 0.75,
        },
        ax=ax,
    )

    # District labels
    for _, row in data.iterrows():

        point = row.geometry.representative_point()

        ax.text(
            point.x,
            point.y,
            row["district"].title(),
            fontsize=8,
            ha="center",
            fontweight="bold",
            path_effects=[
                pe.withStroke(
                    linewidth=3,
                    foreground="white"
                )
            ]
        )

    ax.set_title(
        f"{meta['title']}\n{year}",
        pad=15,
    )

    ax.set_axis_off()

    fig.text(
        0.02,
        0.02,
        meta['footer'],
        fontsize=8,
        color="dimgray",
    )

    if output_dir:

        filename = f"{index_name}_{year}"

        _save(
            fig,
            Path(output_dir) / filename,
        )

    return fig


def batch_generate_index_maps(
    districts_file,
    temporal_summary_csv,
    output_dir,
):

    gdf = prepare_map_data(
        districts_file,
        temporal_summary_csv,
    )

    for index in ["NDVI", "NDWI", "NDBI"]:

        for year in [2016, 2022, 2025]:

            print(f"{index} {year}")

            plot_index_map(
                gdf,
                index,
                year,
                output_dir,
            )

    return gdf

# ------------------------------------------------- Change Maps -------------------------------------------------

def plot_change_map(
    district_gdf,
    change_df,
    metric,
    output_dir=None,
):

    meta = CHANGE_MAP_META[metric]

    gdf = district_gdf.merge(
    change_df,
    left_on="DISTRICT",
    right_on="district",
    how="left",
    )

    values = gdf[metric]

    vmax = max(abs(values.min()), abs(values.max()))

    norm = colors.TwoSlopeNorm(
        vmin=-vmax,
        vcenter=0,
        vmax=vmax,
    )

    fig, ax = plt.subplots(figsize=(8, 8))

    gdf.plot(
        column=metric,
        cmap=COLORMAPS[metric],
        linewidth=0.8,
        edgecolor="black",
        legend=True,
        norm=norm,
        legend_kwds={
            "label": meta["label"],
            "shrink": 0.72,
        },
        ax=ax,
        vmin=COLOR_LIMITS[metric][0],
        vmax=COLOR_LIMITS[metric][1],
    )

    for _, row in gdf.iterrows():

        pt = row.geometry.representative_point()
        x = pt.x
        y = pt.y

        ax.text(
            x,
            y,
            row["district"].title(),
            fontsize=10,
            weight="bold",
            ha="center",
            va="center",
            path_effects=[
                pe.withStroke(
                    linewidth=3,
                    foreground="white"
                )
            ]
        )

    ax.set_title(
        meta["title"],
        fontsize=18,
        weight="bold",
        pad=18,
    )

    ax.set_axis_off()

    fig.text(
        0.01,
        0.02,
        meta['footer'],
        fontsize=9,
        color="dimgray",
    )

    if output_dir:

        output_dir = Path(output_dir)

        output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        plt.savefig(
            output_dir / f"{metric}.png",
            dpi=300,
            bbox_inches="tight",
        )

    plt.close()

    return fig


def batch_generate_change_maps(
    district_gdf,
    change_df,
    output_dir,
):

    metrics = [
        "NDVI_change_16_25",
        "NDWI_change_16_25",
        "NDBI_change_16_25",
    ]

    for metric in metrics:
        plot_change_map(
            district_gdf,
            change_df,
            metric,
            output_dir,
        )
