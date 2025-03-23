from pathlib import Path

import pandas as pd
import typer
from pydantic import BaseModel, Field, FilePath

from rnafold.baseconfig import BaseConfig
from rnafold.pdb import parse_pdb_to_df
from rnafold.rhofold.main import predict_rna_structures, process_csv
from rnafold.submit import duplicate_xyz_columns

app = typer.Typer()


class RhoFoldRepoConfig(BaseModel):
    inference_script: FilePath = Field(..., description="Path to RhoFold inference script")  # fmt: skip
    model_ckpt: FilePath = Field(..., description="Path to model checkpoint")


class RhoFoldConfig(BaseConfig):
    csv_path: FilePath = Field(..., description="Path to the input CSV file")
    fasta_dir: Path = Field(..., description="Folder to store FASTA files")
    predictions_dir: Path = Field(..., description="Folder to store predictions")
    relax_steps: int = Field(..., description="Number of relaxation steps")
    submission_path: Path = Field(..., description="Path to save the submission CSV")
    rhofold_repo: RhoFoldRepoConfig
    device: str = Field(..., description="Device for inference (cpu/gpu)")


def run_rhofold(config: RhoFoldConfig):
    """Processes an RNA sequence CSV file, predicts structures, and exports results."""

    fasta = pd.read_csv(config.csv_path)
    process_csv(fasta, config.fasta_dir)

    execution_times = predict_rna_structures(
        fasta_dir=config.fasta_dir,
        predictions_dir=config.predictions_dir,
        relax_steps=config.relax_steps,
        inference_script=config.rhofold_repo.inference_script,
        model_ckpt=config.rhofold_repo.model_ckpt,
        device=config.device,
    )

    predictions = []
    for target_id in fasta["target_id"]:
        relax_name = f"relaxed_{config.relax_steps}_model.pdb"
        relax_pdb = config.predictions_dir / target_id / relax_name
        prediction = parse_pdb_to_df(str(relax_pdb), target_id)

        if len(prediction) != 1:
            raise ValueError("Multiple models for one sequence. Not handled yet.")

        prediction = prediction[0]
        predictions.append(prediction)

    print("Completed predictions.")

    predictions = pd.concat(predictions, axis=0)
    submission = duplicate_xyz_columns(predictions)
    submission.to_csv(config.submission_path, index=False)

    print(f"Submission exported as CSV to {config.submission_path}.")
    print(execution_times)


@app.command()
def cli_run_rhofold(
    config_path: FilePath = typer.Option(None, "--config", "-c", help="Path to config YAML. If provided, all the other fields are ignored."),
    inference_script: FilePath = typer.Option(None, help="Path to RhoFold inference script"),
    csv_path: FilePath = typer.Option(None, help="Path to the input CSV file"),
    fasta_dir: Path = typer.Option(None, help="Folder to store FASTA files"),
    predictions_dir: Path = typer.Option(None, help="Folder to store predictions"),
    relax_steps: int = typer.Option(None, help="Number of relaxation steps"),
    submission_path: Path = typer.Option(None, help="Path to save the final submission CSV"),
    model_ckpt: FilePath = typer.Option(None, help="Path to model checkpoint"),
    device: str = typer.Option("cpu", help="Accelerator for inference")
):  # fmt: skip
    """CLI command to process RNA sequences, predict structures, and export results."""
    if config_path:
        config = RhoFoldConfig.load_from_yaml(config_path)
    else:
        config = RhoFoldConfig(
            csv_path=csv_path,
            fasta_dir=fasta_dir,
            predictions_dir=predictions_dir,
            relax_steps=relax_steps,
            submission_path=submission_path,
            rhofold_repo=RhoFoldRepoConfig(
                inference_script=inference_script,
                model_ckpt=model_ckpt,
            ),
            device=device,
        )
    run_rhofold(config)


if __name__ == "__main__":
    app()
