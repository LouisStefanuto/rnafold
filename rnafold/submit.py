"""Zero submission for Kaggle."""

import pandas as pd

from rnafold.config import Settings


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


if __name__ == "__main__":
    COLUMS = ["target_id", "sequence"]

    sequences = pd.read_csv(Settings.sequences.val, usecols=COLUMS)
    submission = create_random_submission(sequences)
    submission.to_csv("submission.csv", index=False)

    print(submission)
