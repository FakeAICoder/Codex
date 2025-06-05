"""Visualization utilities to create market map images."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Dict, Set

import matplotlib.pyplot as plt


def create_market_map(
    categories: Dict[str, Set[str]], output: str | Path = "market_map.png"
) -> None:
    """Render the market map and save to ``output``."""
    fig, ax = plt.subplots(figsize=(8, 6))
    y = 0
    for cat, names in categories.items():
        ax.text(0.05, 0.9 - y * 0.15, cat, fontsize=12, fontweight="bold")
        for i, name in enumerate(sorted(names)):
            ax.text(0.1, 0.88 - (y * 0.15 + i * 0.04), name, fontsize=10)
        y += 1

    ax.set_axis_off()
    fig.tight_layout()
    fig.savefig(str(output))
    plt.close(fig)
    logging.info("Market map saved to %s", output)
