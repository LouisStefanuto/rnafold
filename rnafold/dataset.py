from io import StringIO
from pathlib import Path

import pandas as pd
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio.SeqUtils import gc_fraction


def load_sequences(file: str | Path) -> pd.DataFrame:
    sequences = pd.read_csv(file)

    if "sequence" not in sequences.columns:
        raise ValueError("Missing 'sequence' column.")

    sequences["sequence_length"] = sequences["sequence"].apply(len)
    sequences["GC_Content"] = sequences["sequence"].apply(get_gc_fraction)

    return sequences


def load_labels(file: str | Path) -> pd.DataFrame:
    return pd.read_csv(file)


def get_gc_fraction(seq: str) -> float:
    return gc_fraction(Seq(seq))


def load_extra_sequences(fasta_string: str) -> list[SeqRecord]:
    # Use StringIO to simulate a file
    fasta_handle = StringIO(fasta_string)

    # Parse the multi-record string
    records = list(SeqIO.parse(fasta_handle, "fasta"))
    return records
