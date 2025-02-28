import typer

app = typer.Typer()


@app.command()
def hello(name: str) -> None:
    """
    Prints Hello.

    Args:
        name (str): name to say hello to
    """
    print(f"Hello {name}")


@app.command()
def goodbye(name: str, formal: bool = False) -> None:
    """
    Prints goodbye.

    Args:
        name (str): name to say goob bye to.
        formal (bool, optional): if True, will be more formal. Defaults to False.
    """
    if formal:
        print(f"Goodbye Ms. {name}. Have a good day.")
    else:
        print(f"Bye {name}!")


if __name__ == "__main__":
    app()
