# Data plotting

import matplotlib.pyplot as plt

def plot_boundaries(
    districts,
    taluks=None,
    title=None,
    district_facecolor="#FDB863",
    district_edgecolor="black",
    taluk_edgecolor="white",
    figsize=(8, 8),
):

    fig, ax = plt.subplots(figsize=figsize)

    districts.plot(
        ax=ax,
        facecolor=district_facecolor,
        edgecolor=district_edgecolor,
        linewidth=1.2,
    )

    if taluks is not None:
        taluks.plot(
            ax=ax,
            facecolor="none",
            edgecolor=taluk_edgecolor,
            linewidth=0.4,
        )

    if title:
        ax.set_title(title, fontsize=16)

    ax.set_axis_off()
    plt.tight_layout()

    return fig, ax

def plot_india_context(
    india,
    study_area,
    title="Study Area within India",
):

    fig, ax = plt.subplots(figsize=(8, 8))

    india.plot(
        ax=ax,
        facecolor="#DDDDDD",
        edgecolor="black",
        linewidth=0.4,
    )

    study_area.plot(
        ax=ax,
        facecolor="#FDB863",
        edgecolor="red",
        linewidth=1.2,
    )

    ax.set_title(title)

    ax.set_axis_off()
    plt.tight_layout()

    return fig, ax