# Data plotting

import matplotlib.pyplot as plt

def save_figure(fig, path, dpi=300):

    path.parent.mkdir(parents=True, exist_ok=True)

    fig.savefig(
        path,
        dpi=dpi,
        bbox_inches="tight"
    )

def plot_boundaries(districts, taluks=None, title=None):
    fig, ax = plt.subplots(figsize=(8, 8))

    districts.plot(ax=ax, edgecolor="black", facecolor="none")

    if taluks is not None:
        taluks.plot(ax=ax, edgecolor="red", facecolor="none")

    if title is not None:
        ax.set_title(title)

    ax.set_axis_off()

    return fig, ax