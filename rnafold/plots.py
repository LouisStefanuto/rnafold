from pathlib import Path
from typing import Optional

import matplotlib.pyplot as plt
import pandas as pd


def plot_sequence_length_distribution(
    datasets: list[pd.DataFrame],
    labels: list[str],
    bins: int = 20,
    log_scale: bool = True,
    save_path: Optional[str | Path] = None,
):
    """
    Plots the distribution of RNA sequence lengths for multiple datasets.

    Parameters:
        datasets (list of DataFrame): List of Pandas DataFrames containing a "sequence_length" column.
        labels (list of str): List of labels corresponding to each dataset.
        bins (int, optional): Number of bins for the histogram. Default is 20.
        log_scale (bool, optional): Whether to use a logarithmic scale for the y-axis. Default is True.
        save_path (str, optional): Path to save the figure. If None, the plot is not saved.
    """

    for data, label in zip(datasets, labels):
        plt.hist(data["sequence_length"], bins=bins, alpha=0.6, label=label)

    plt.xlabel("Sequence Length")
    plt.ylabel("Count")
    plt.title("Distribution of RNA Sequence Lengths")

    if log_scale:
        plt.yscale("log")

    plt.legend()

    # Save the figure if a path is provided
    if save_path:
        plt.savefig(save_path)
        print(f"Plot saved to: {save_path}")

    plt.show()


def plot_gc_content_distribution(
    dfs: list[pd.DataFrame],
    labels: list[str],
    save_path: Optional[Path | str] = None,
    bins: int = 20,
    log_scale: bool = False,
) -> None:
    """
    Plots the GC content distribution of RNA sequences for multiple datasets.

    Parameters:
        dfs (list[pd.DataFrame]): List of Pandas DataFrames containing a "GC_Content" column.
        labels (list[str]): List of labels corresponding to each dataset.
        save_path (Optional[str]): Path to save the figure. If None, the plot is not saved.
        bins (int): Number of bins for the histogram. Default is 20.
        log_scale (bool): Whether to use a log scale for the y-axis. Default is False.

    Returns:
        None
    """

    # Define a color palette for multiple datasets
    colors = ["royalblue", "darkorange", "green", "red", "purple"]

    # Iterate over datasets and plot histograms
    for i, (df, label) in enumerate(zip(dfs, labels)):
        plt.hist(
            df["GC_Content"],
            bins=bins,
            alpha=0.6,
            color=colors[i % len(colors)],
            edgecolor="black",
            label=label,
        )

    plt.xlabel("GC Content (%)")
    plt.ylabel("Count")
    plt.title("GC Content Distribution of RNA Sequences")

    if log_scale:
        plt.yscale("log")

    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.legend()

    # Save the figure if a path is provided
    if save_path:
        plt.savefig(save_path)
        print(f"Plot saved to: {save_path}")

    plt.show()


if __name__ == "__main__":
    from rnafold.config import Settings
    from rnafold.dataset import load_sequences

    sequences_train = load_sequences(Settings.sequences.train)
    sequences_test = load_sequences(Settings.sequences.test)

    plot_sequence_length_distribution(
        datasets=[sequences_train, sequences_test],
        labels=["train", "test"],
        save_path=Path().cwd() / "results/sequence_lengths.png",
    )

    plot_gc_content_distribution(
        dfs=[sequences_train, sequences_test],
        labels=["Train", "Test"],
        save_path=Path().cwd() / "results/gc_content_distribution.png",
    )
