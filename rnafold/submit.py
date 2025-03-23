"""Zero submission for Kaggle."""

import pandas as pd
import typer

app = typer.Typer()


def compute_sequence_length(sequences: pd.Series) -> pd.Series:
    return sequences.apply(len)


def create_random_submission(sequences: pd.DataFrame) -> pd.DataFrame:
    sequences["len"] = compute_sequence_length(sequences["sequence"])

    data_submission = []
    for _, row in sequences.iterrows():
        sequence = row["sequence"]
        target_id = row["target_id"]

        for i, resname in enumerate(sequence):
            # NB: 1-indexing
            data_submission.append(
                {
                    "ID": f"{target_id}_{i+1}",
                    "resname": resname,
                    "resid": i + 1,
                }
            )

    submission = pd.DataFrame.from_records(data_submission)

    # Add empty columns for xyz predictions
    NUM_PREDICTIONS = 5
    for i in range(1, NUM_PREDICTIONS + 1):
        submission[f"x_{i}"] = 0.0
        submission[f"y_{i}"] = 0.0
        submission[f"z_{i}"] = 0.0

    return submission


def duplicate_xyz_columns(df: pd.DataFrame, n: int = 5) -> pd.DataFrame:
    """
    Duplicates the 'x_1', 'y_1', and 'z_1' columns in a DataFrame up to 'n' times.

    Parameters:
        df (pd.DataFrame): The input DataFrame containing at least 'x_1', 'y_1', and 'z_1' columns.
        n (int, optional): The number of duplicate columns to create. Defaults to 5.

    Returns:
        pd.DataFrame: The modified DataFrame with additional duplicated columns.
    """
    for i in range(2, n + 1):
        df[f"x_{i}"] = df["x_1"]
        df[f"y_{i}"] = df["y_1"]
        df[f"z_{i}"] = df["z_1"]

    return df


@app.command()
def main(csv_path: str):
    """Reads a CSV file, processes sequences, and saves a full-zero submission."""
    COLUMNS = ["target_id", "sequence"]

    sequences = pd.read_csv(csv_path, usecols=COLUMNS)
    submission = create_random_submission(sequences)
    submission.to_csv("submission.csv", index=False)

    print(submission)


if __name__ == "__main__":
    app()
