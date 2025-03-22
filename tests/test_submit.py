import pandas as pd

from rnafold.config import Settings
from rnafold.submit import create_random_submission


def test_submit(tmpdir):
    COLUMS = ["target_id", "sequence"]
    sequences = pd.read_csv(Settings.sequences.val, usecols=COLUMS)
    submission = create_random_submission(sequences)

    submission_csv = tmpdir / "submission.csv"
    submission.to_csv(submission_csv, index=False)

    COLUMNS = (
        ["ID", "resname", "resid"]
        + ["x_1", "y_1", "z_1", "x_2", "y_2", "z_2", "x_3", "y_3", "z_3"]
        + ["x_4", "y_4", "z_4", "x_5", "y_5", "z_5"]
    )

    df = pd.read_csv(submission_csv)
    assert df.shape == (2515, 18)
    assert set(df.columns.tolist()) == set(COLUMNS)
