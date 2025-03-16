from pathlib import Path

import pandas as pd
from Bio.PDB import PDBParser, Structure


def read_pdb(pdbcode: str, pdbfilenm: str | Path) -> Structure:
    """
    Read a PDB structure from a file.

    Args:
        pdbcode (str): A PDB ID string
        pdbfilenm (str | Path): The PDB file

    Returns:
        Bio.PDB.Structure: a Bio.PDB.Structure object
    """
    pdbparser = PDBParser()
    structure = pdbparser.get_structure(pdbcode, pdbfilenm)
    return structure


def parse_pdb_to_df(pdb_file: str, target_id: str) -> list[pd.DataFrame]:
    structure = read_pdb("", pdb_file)

    df = []  # List to store dataframes of each chain
    for model in structure:
        for chain in model:
            chain_data = []  # List to store residue data for the current chain
            for residue in chain:
                # Only process nucleotide residues
                # And if the residue contains a C1' atom
                if residue.get_resname() in ["A", "U", "G", "C"] and "C1'" in residue:
                    atom = residue["C1'"]
                    xyz = atom.get_coord()
                    resname = residue.get_resname()
                    resid = residue.get_id()[1]

                    # Create a dictionary with residue information
                    chain_data.append(
                        {
                            "ID": f"{target_id}_{resid}",  # Combine target ID and residue ID
                            "resname": resname,
                            "resid": resid,
                            "x_1": xyz[0],
                            "y_1": xyz[1],
                            "z_1": xyz[2],
                        }
                    )

            # If the chain has any data, convert to DataFrame and add to list
            if chain_data:
                chain_df = pd.DataFrame(chain_data)
                df.append(chain_df)

    return df
