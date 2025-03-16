import os
import subprocess  # nosec


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


def run_rhofold(
    input_fas: str,
    output_dir: str,
    relax_steps: int = 1,
    single_seq_pred: bool = True,
    device: str = "cpu",
    ckpt: str = "../models/RhoFold_pretrained.pt",
):
    """
    Runs the RhoFold inference script with the given parameters.

    Parameters:
        input_fas (str): Path to the input FASTA file.
        output_dir (str): Directory to store the output.
        relax_steps (int): Number of relaxation steps (default: 1).
        single_seq_pred (bool): Whether to use single sequence prediction (default: True).
        device (str): Device to run the inference on (default: 'cpu').
        ckpt (str): Path to the checkpoint file (default: '../models/RhoFold_pretrained.pt').
    """
    cmd = [
        "python",
        "../../RhoFold/inference.py",
        "--relax_steps",
        str(relax_steps),
        "--input_fas",
        input_fas,
        "--single_seq_pred",
        str(single_seq_pred),
        "--output_dir",
        output_dir,
        "--device",
        device,
        "--ckpt",
        ckpt,
    ]

    subprocess.run(cmd, check=True)  # nosec
