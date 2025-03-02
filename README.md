# rnafold

## Install

1. Clone the repo and `cd`into it.

    ```console
    git clone https://github.com/LouisStefanuto/rnafold.git
    cd ./rnafold
    ```

2. Install [USalign](https://github.com/pylelab/USalign) (for evaluation).

    ```shell
    brew install brewsci/bio/usalign  # using brew (recommended and tested)
    conda install -c bioconda usalign  # using conda
    ```

3. Set up and activate your virtual environment using [Poetry](https://python-poetry.org).

    ```console
    poetry install --with dev,docs
    source $(poetry env info --path)/bin/activate
    ```

## Evaluation

Run the evaluation on a fake test set:

```shell
python rnafold/metrics.py
```
