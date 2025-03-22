import os
import subprocess  # nosec
import time
from pathlib import Path

import pandas as pd


def generate_fasta(file_path, sequence_id, sequence):
    with open(file_path, "w") as fasta_file:
        fasta_file.write(f">{sequence_id}\n")
        for i in range(0, len(sequence), 80):  # Wrap lines at 80 chars
            fasta_file.write(sequence[i : i + 80] + "\n")
    print(f"FASTA file saved at {file_path}")


def process_csv(fastas, output_folder):
    os.makedirs(output_folder, exist_ok=True)

    for index, row in fastas.iterrows():
        sequence_id = row["target_id"]
        sequence = row["sequence"]
        fasta_file_path = os.path.join(output_folder, f"{sequence_id}.fasta")
        generate_fasta(fasta_file_path, sequence_id, sequence)


def predict_rna_structure(
    input_fas: str | Path,
    predictions_dir: str | Path,
    model_ckpt: str | Path,
    inference_script: str | Path,
    relax_steps: int = 1,
    single_seq_pred: bool = True,
    device: str = "cpu",
):
    """
    Runs the RhoFold inference script with the given parameters.

    Parameters:
        input_fas (str): Path to the input FASTA file.
        predictions_dir (str): Directory to store the output.
        relax_steps (int): Number of relaxation steps (default: 1).
        single_seq_pred (bool): Whether to use single sequence prediction (default: True).
        device (str): Device to run the inference on (default: 'cpu').
        model_ckpt (str): Path to the checkpoint file (default: '../models/RhoFold_pretrained.pt').
    """
    cmd = [
        "python",
        str(inference_script),
        "--relax_steps",
        str(relax_steps),
        "--input_fas",
        input_fas,
        "--single_seq_pred",
        str(single_seq_pred),
        "--output_dir",
        predictions_dir,
        "--device",
        device,
        "--ckpt",
        model_ckpt,
    ]

    subprocess.run(cmd, check=True)  # nosec


def get_sequence_length(fasta_file: Path) -> int:
    with open(fasta_file, "r") as f:
        lines = f.readlines()
        sequence = "".join(line.strip() for line in lines if not line.startswith(">"))
    return len(sequence)


def predict_rna_structures(
    fasta_dir: Path,
    predictions_dir: Path,
    relax_steps: int,
    inference_script: str | Path,
    model_ckpt: Path,
) -> pd.DataFrame:
    results = []

    for fasta_file in Path(fasta_dir).glob("*.fasta"):
        start_time = time.time()

        seq_predictions_dir = predictions_dir / fasta_file.stem
        predict_rna_structure(
            input_fas=fasta_file,
            predictions_dir=seq_predictions_dir,
            relax_steps=relax_steps,
            model_ckpt=model_ckpt,
            inference_script=inference_script,
        )
        end_time = time.time()

        sequence_length = get_sequence_length(fasta_file)

        results.append(
            {
                "target_id": fasta_file.stem,
                "sequence_length": sequence_length,
                "execution_time": round(end_time - start_time, 3),
            }
        )

    return pd.DataFrame(results)
