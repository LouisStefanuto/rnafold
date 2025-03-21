import pandas as pd

from rnafold.config import Settings


def _load_all_sequences() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    sequences_train = pd.read_csv(Settings.sequences.train)
    sequences_val = pd.read_csv(Settings.sequences.val)
    sequences_test = pd.read_csv(Settings.sequences.test)
    return (sequences_train, sequences_val, sequences_test)


def _print_sequences(
    sequences_train: pd.DataFrame,
    sequences_val: pd.DataFrame,
    sequences_test: pd.DataFrame,
):
    set1 = set(sequences_train.target_id)
    set2 = set(sequences_val.target_id)
    set3 = set(sequences_test.target_id)

    print("# SEQUENCES")
    print("- Train:", len(set1), "sequences")
    print("- Val:\t", len(set2), "sequences")
    print("- Test:\t", len(set3), "sequences")

    print("No intersection between train and val:", len(set1.intersection(set2)) == 0)
    print("Val == test:", set2 == set3)


def report() -> None:
    sequences_train, sequences_val, sequences_test = _load_all_sequences()
    _print_sequences(sequences_train, sequences_val, sequences_test)


if __name__ == "__main__":
    report()
