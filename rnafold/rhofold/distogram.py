from enum import StrEnum
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


class AtomType(StrEnum):
    N = "n"
    P = "p"
    C = "c"


class RhoFoldDistogram:
    _EXPECTED_FIELDS = {"dist_n", "dist_p", "dist_c", "ss_prob_map", "plddt"}

    def __init__(self, file_path: str | Path):
        """Load an npz file containing RNA distogram data."""
        _data = np.load(file_path)
        self.files = _data.files
        self.summary = self._summarize_data(_data)

        # Extract fields
        self.dist_n: np.ndarray = _data["dist_n"]
        self.dist_p: np.ndarray = _data["dist_p"]
        self.dist_c: np.ndarray = _data["dist_c"]
        self.ss_prob_map: np.ndarray = _data["ss_prob_map"]
        self.plddt: np.ndarray = _data["plddt"]

    def _summarize_data(self, data) -> pd.DataFrame:
        """
        Print basic statistics for the data.

        Args:
            X (np.lib.npyio.NpzFile): Opened distogram npz file

        Returns:
            pd.DataFrame: Description of the distrogram
        """
        summary = {}
        for key in data.files:
            summary[key] = {
                "shape": data[key].shape,
                "mean": np.mean(data[key]),
                "std": np.std(data[key]),
                "min": np.min(data[key]),
                "max": np.max(data[key]),
            }
        return pd.DataFrame(summary).T

    def plot_distance_distribution(self, atom_type: str):
        try:
            atom_enum = AtomType(atom_type.lower())
        except ValueError:
            raise ValueError(
                f"Invalid atom type: {atom_type}. Choose from 'n', 'p', or 'c'."
            )

        dist_matrix = getattr(self, f"dist_{atom_enum.value}")
        plot_distance_distribution(dist_matrix, atom_enum.value)

    def plot_secondary_structure(self):
        plot_secondary_structure(self.ss_prob_map)

    def plot_confidence(self):
        plot_confidence(self.plddt)


def plot_distance_distribution(dist_matrix: np.ndarray, atom_type: str = ""):
    """Plot the pairwise distance distribution for a given atom type."""
    mean_dist = np.max(dist_matrix, axis=0)

    plt.figure(figsize=(8, 6))
    sns.heatmap(mean_dist, cmap="coolwarm_r", cbar=True)

    if atom_type:
        plt.title(f"Pairwise Distance Distribution for {atom_type} atoms")
    plt.xlabel("Residue Index")
    plt.ylabel("Residue Index")
    plt.show()


def plot_secondary_structure(ss_prob_map: np.ndarray):
    """Visualize the secondary structure probability map."""
    plt.figure(figsize=(8, 6))
    sns.heatmap(ss_prob_map, cmap="viridis", square=True)
    plt.title("Secondary Structure Probability Map")
    plt.xlabel("Residue Index")
    plt.ylabel("Residue Index")
    plt.show()


def plot_confidence(plddt: np.ndarray):
    """Plot the per-residue confidence scores."""
    plt.figure(figsize=(8, 4))
    plt.plot(plddt.flatten(), marker="o", linestyle="")
    plt.title("Per-Residue Confidence Scores")
    plt.xlabel("Residue Index")
    plt.ylabel("Confidence Score")
    plt.ylim(0, 1)
    plt.grid()
    plt.show()
