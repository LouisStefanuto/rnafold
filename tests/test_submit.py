import csv

import pandas as pd

from rnafold.submit import create_random_submission


def create_test_sequences_csv(file_path):
    data = [
        ["target_id", "sequence", "temporal_cutoff", "description", "all_sequences"],
        [
            "R1107",
            "GGGGGCCACAGCAGAAGCGUUCACGUCGCAGCCCCUGUCAGCCAUUGCACUCCGGCUGCGAAUUCUGCU",
            "2022-05-28",
            "CPEB3 ribozyme Human human CPEB3 HDV-like ribozyme",
            ">7QR4_1|Chain A|U1 small nuclear ribonucleoprotein A|Homo sapiens (9606)\nRPNHTIYINNLNEKIKKDELKKSLHAIFSRFGQILDILVSRSLKMRGQAFVIFKEVSSATNALRSMQGFPFYDKPMRIQYAKTDSDIIAKM\n>7QR4_2|Chain B|RNA CPEB3 ribozyme|Homo sapiens (9606)\nGGGGGCCACAGCAGAAGCGUUCACGUCGCAGCCCCUGUCAGCCAUUGCACUCCGGCUGCGAAUUCUGCU",
        ],
        [
            "R1108",
            "GGGGGCCACAGCAGAAGCGUUCACGUCGCGGCCCCUGUCAGCCAUUGCACUCCGGCUGCGAAUUCUGCU",
            "2022-05-27",
            "CPEB3 ribozyme Chimpanzee Chimpanzee CPEB3 HDV-like ribozyme",
            ">7QR3_1|Chains A, B|U1 small nuclear ribonucleoprotein A|Homo sapiens (9606)\nRPNHTIYINNLNEKIKKDELKKSLHAIFSRFGQILDILVSRSLKMRGQAFVIFKEVSSATNALRSMQGFPFYDKPMRIQYAKTDSDIIAKM\n>7QR3_2|Chains C, D|chimpanzee CPEB3 ribozyme|Pan troglodytes (9598)\nGGGGGCCACAGCAGAAGCGUUCACGUCGCGGCCCCUGUCAGCCAUUGCACUCCGGCUGCGAAUUCUGCU",
        ],
    ]

    with open(file_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerows(data)


def test_submit(tmpdir):
    file_path = tmpdir / "test_data.csv"
    create_test_sequences_csv(file_path)

    COLUMS = ["target_id", "sequence"]
    sequences = pd.read_csv(file_path, usecols=COLUMS)
    submission = create_random_submission(sequences)

    submission_csv = tmpdir / "submission.csv"
    submission.to_csv(submission_csv, index=False)

    COLUMNS = (
        ["ID", "resname", "resid"]
        + ["x_1", "y_1", "z_1", "x_2", "y_2", "z_2", "x_3", "y_3", "z_3"]
        + ["x_4", "y_4", "z_4", "x_5", "y_5", "z_5"]
    )

    df = pd.read_csv(submission_csv)

    assert df.shape == (138, 18)
    assert set(df.columns.tolist()) == set(COLUMNS)
