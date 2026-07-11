"""
Functions:
- plot_change_bars
- plot_all_changes
- plot_correlation_heatmap
- plot_index_distribution
"""

from pathlib import Path

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# -------------------- Constants --------------------------

DISTRICT_COLORS = {
    "DEHRADUN":      "#227dbe",
    "HARIDWAR":      "#fe8317",
    "PAURI GARHWAL": "#31a431",
}

INDEX_META = {
    "NDVI": {
        "color":  "forestgreen",
        "ylabel": "NDVI",
        "title":  "NDVI: Vegetation Cover",
        "note":   "Higher = denser vegetation.  Positive change = gain.",
        "good":   "positive",
    },
    "NDWI": {
        "color":  "royalblue",
        "ylabel": "NDWI",
        "title":  "NDWI: Water Body Index",
        "note":   (
            "District mean NDWI values remain negative because land pixels dominate.\n"
            "Less negative values indicate a stronger water-related spectral signal."
        ),
        "good":   "positive",
    },
    "NDBI": {
        "color":  "darkorange",
        "ylabel": "NDBI",
        "title":  "NDBI: Built-up Index",
        "note":   "Higher = greater urban / impervious extent.  Positive change = expansion.",
        "good":   "negative",
    },
}

CHANGE_TITLES = {
    "NDVI_change_16_25": "Net NDVI change  2016 → 2025\n(vegetation cover)",
    "NDWI_change_16_25": "Net NDWI change  2016 → 2025\n(water-body signal)",
    "NDBI_change_16_25": "Net NDBI change  2016 → 2025\n(built-up / urban extent)",
    "NDVI_change_16_22": "Net NDVI change  2016 → 2022",
    "NDVI_change_22_25": "Net NDVI change  2022 → 2025",
}

STUDY_YEARS = [2016, 2022, 2025]


# -------------------------------- Helpers -------------------------------------

def _setup_style():

    plt.rcParams.update({
        "figure.dpi":         150,
        "savefig.dpi":        300,
        "figure.facecolor":   "white",
        "axes.facecolor":     "white",
        "axes.titlesize":     14,
        "axes.titleweight":   "bold",
        "axes.labelsize":     11,
        "xtick.labelsize":    10,
        "ytick.labelsize":    10,
        "legend.fontsize":    10,
        "axes.grid":          True,
        "grid.alpha":         0.25,
        "grid.linestyle":     "--",
        "grid.linewidth":     0.6,
        "axes.spines.top":    False,
        "axes.spines.right":  False,
        "savefig.bbox":       "tight",
    })


def _save(fig, path):
    """Save fig as PNG and PDF"""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout(rect=[0, 0.05, 1, 1])
    fig.savefig(path.with_suffix(".png"))
    fig.savefig(path.with_suffix(".pdf"))
    plt.close(fig)


def _zero_line(ax):
    """Draws a dashed line."""
    ax.axhline(0, color="black", linewidth=0.8, linestyle="--",
               alpha=0.35, zorder=1)

def _bar_colors(values, good_direction):
    """Returns color for each bar based on change."""
    if good_direction == "positive":
        return ["#2a9d8f" if v >= 0 else "#e76f51" for v in values]
    else:
        return ["#e76f51" if v >= 0 else "#2a9d8f" for v in values]


def _bar_annotations(ax, bars, values, fmt="{:+.4f}"):
    """Place value labels outside each bar end."""
    span = max(abs(v) for v in values) or 1
    pad  = span * 0.04

    for bar, v in zip(bars, values):
        x  = v + pad if v >= 0 else v - pad
        ha = "left" if v >= 0 else "right"
        ax.text(
            x,
            bar.get_y() + bar.get_height() / 2,
            fmt.format(v),
            ha=ha, va="center",
            fontsize=9.5, fontweight="bold",
        )


def _expand_bar_xlim(ax, values, margin=0.30):
    """Expand x-limits so bar annotations are not clipped."""
    span = max(abs(v) for v in values) or 0.01
    ax.set_xlim(-span * (1 + margin), span * (1 + margin))


# ------------------------------ Change bars ------------------------------

def plot_change_bars(ranking_df, metric, output_dir=None):
    """
    Horizontal bar chart of net change for one metric across districts.
    """
    _setup_style()

    if "NDVI" in metric:
        good  = INDEX_META["NDVI"]["good"]
    elif "NDWI" in metric:
        good  = INDEX_META["NDWI"]["good"]
    elif "NDBI" in metric:
        good  = INDEX_META["NDBI"]["good"]
    else:
        good = "positive"

    title = CHANGE_TITLES.get(
        metric,
        f"Net {metric.replace('_', ' ')} change",
    )

    df     = ranking_df.sort_values(metric).copy()
    values = df[metric].values
    labels = [d.title() for d in df["district"].values]
    colors = _bar_colors(values, good)

    fig, ax = plt.subplots(figsize=(8, max(3.5, len(labels) * 1.1)))

    bars = ax.barh(labels, values, color=colors, height=0.42, zorder=2)

    _bar_annotations(ax, bars, values)
    _expand_bar_xlim(ax, values)

    ax.axvline(0, color="black", linewidth=1, zorder=3)
    ax.set_xlabel("Change (index units)")
    ax.set_title(title)

    # Legend for color meaning
    if "NDVI" in metric:
        positive_label = "Vegetation gain"
        negative_label = "Vegetation loss"

    elif "NDWI" in metric:
        positive_label = "Stronger water signal"
        negative_label = "Weaker water signal"

    elif "NDBI" in metric:
        positive_label = "Built-up expansion"
        negative_label = "Built-up reduction"

    else:
        positive_label = "Positive change"
        negative_label = "Negative change"

    if good == "positive":
        legend_handles = [
            mpatches.Patch(color="#2a9d8f", label=positive_label),
            mpatches.Patch(color="#e76f51", label=negative_label),
        ]
    else:
        legend_handles = [
            mpatches.Patch(color="#e76f51", label=positive_label),
            mpatches.Patch(color="#2a9d8f", label=negative_label),
        ]

    ax.legend(handles=legend_handles, frameon=True, loc="best",
              fontsize=9)

    if output_dir:
        _save(fig, Path(output_dir) / metric)

    return fig

# ------------------------------ All index changes ------------------------------

def plot_all_changes(district_changes_df, output_dir=None):
    """
    Grouped horizontal bar chart: NDVI, NDWI, and NDBI net change
    (2016 → 2025) side by side for each district.
    """
    _setup_style()

    districts = list(district_changes_df["district"].values)
    n = len(districts)

    metrics = [
        ("NDVI_change_16_25", "NDVI", "forestgreen"),
        ("NDWI_change_16_25", "NDWI", "royalblue"),
        ("NDBI_change_16_25", "NDBI", "darkorange"),
    ]

    bar_h   = 0.22
    spacing = 0.85
    y_base  = np.arange(n) * spacing

    # Offsets so bars for each index are centred around y_base
    n_m     = len(metrics)
    offsets = np.linspace(-(n_m - 1) * bar_h / 2,
                          (n_m - 1) * bar_h / 2,
                          n_m)

    fig, ax = plt.subplots(figsize=(10, max(4, n * 2.2)))

    for (col, label, color), off in zip(metrics, offsets):
        vals = district_changes_df[col].values
        ys   = y_base + off

        ax.barh(ys, vals, height=bar_h, color=color,
                alpha=0.82, label=label, zorder=2)

        # Value labels
        for y, v in zip(ys, vals):
            ax.annotate(
                f"{v:+.3f}",
                xy=(v, y),
                xytext=(4 if v >= 0 else -4, 0),
                textcoords="offset points",
                ha="left" if v >= 0 else "right",
                va="center", fontsize=8.5,
            )

    ax.axvline(0, color="black", linewidth=1, zorder=3)
    ax.set_yticks(y_base)
    ax.set_yticklabels([d.title() for d in districts], fontsize=11)
    ax.set_xlabel("Net change (index units)")
    ax.set_title(
        "Environmental Index Changes, 2016 → 2025\n"
        "Dehradun · Haridwar · Pauri Garhwal",
    )
    ax.legend(loc="lower right", frameon=True)

    all_vals = np.concatenate([district_changes_df[c].values
                                for c, _, _ in metrics])
    span = max(abs(all_vals.max()), abs(all_vals.min()))
    ax.set_xlim(-span * 1.45, span * 1.45)

    if output_dir:
        _save(fig, Path(output_dir) / "All_Index_Changes")

    return fig


# ------------------------------ Correlation heatmap ------------------------------

def plot_correlation_heatmap(temporal_df, output_dir=None):
    """
    Pearson correlation matrix for NDVI, NDWI, NDBI.
    """
    _setup_style()

    corr  = temporal_df[["NDVI", "NDWI", "NDBI"]].corr()
    n_obs = len(temporal_df)

    fig, ax = plt.subplots(figsize=(6, 5))

    im = ax.imshow(corr, cmap="RdYlGn", vmin=-1, vmax=1, aspect="auto")

    ax.set_xticks(range(len(corr.columns)))
    ax.set_yticks(range(len(corr.columns)))
    ax.set_xticklabels(corr.columns, fontsize=11)
    ax.set_yticklabels(corr.columns, fontsize=11)

    for i in range(len(corr)):
        for j in range(len(corr)):
            val = corr.iloc[i, j]

            text_color = "white" if abs(val) > 0.75 else "black"
            ax.text(
                j, i, f"{val:.2f}",
                ha="center", va="center",
                fontsize=13, fontweight="bold",
                color=text_color,
            )

    plt.colorbar(im, ax=ax, fraction=0.045, pad=0.04)

    ax.set_title(
        f"Spectral Index Correlation Matrix\n"
        f"({len(temporal_df['district'].unique())} districts × "
        f"{len(temporal_df['year'].unique())} years)",
    )

    if output_dir:
        _save(fig, Path(output_dir) / "Correlation_Heatmap")

    return fig


# ------------------------------ Index distribution ------------------------------

def plot_index_distribution(temporal_df, index_name, output_dir=None):
    """
    Dot-plot of one spectral index with districts.
    """
    _setup_style()
    meta      = INDEX_META[index_name]
    districts = sorted(temporal_df["district"].unique())
    n_d       = len(districts)

    # Horizontal jitter: spread districts symmetrically around each year
    jitter_step = 0.25
    jitters = {
        d: (i - (n_d - 1) / 2) * jitter_step
        for i, d in enumerate(districts)
    }

    fig, ax = plt.subplots(figsize=(9, 5))

    for district in districts:
        sub   = temporal_df[temporal_df["district"] == district].sort_values("year")
        color = DISTRICT_COLORS.get(district, "#888888")
        jit   = jitters[district]
        xs    = sub["year"] + jit

        # Dashed guide line for district
        ax.plot(xs, sub[index_name],
                color=color, linewidth=1.4, alpha=0.4,
                linestyle="--", zorder=2)

        # Dots for district
        ax.scatter(xs, sub[index_name],
                   s=90, color=color, edgecolor="white",
                   linewidth=1.5, zorder=4, label=district.title())

        # Value label above each dot
        for x, val in zip(xs, sub[index_name]):
            ax.annotate(
                f"{val:.3f}",
                xy=(x, val),
                xytext=(0, 8),
                textcoords="offset points",
                ha="center", va="bottom",
                fontsize=8.5, color=color,
            )

    if index_name in ("NDWI", "NDBI"):
        _zero_line(ax)

    ax.set_xlabel("Year")
    ax.set_ylabel(meta["ylabel"])
    ax.set_title(
        f"{meta['title']}",
    )

    # Tick labels at actual study years
    ax.set_xticks(STUDY_YEARS)
    ax.set_xticklabels(STUDY_YEARS)

    ax.legend(frameon=True, loc="best")

    fig.text(
        0.02,
        0.01,
        meta["note"],
        ha="left",
        va="bottom",
        fontsize=8,
        color="dimgray",
        style="italic",
    )

    if output_dir:
        _save(fig, Path(output_dir) / f"{index_name}_Distribution")

    return fig
