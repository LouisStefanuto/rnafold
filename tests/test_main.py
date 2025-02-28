from typer.testing import CliRunner

from rnafold.main import app

runner = CliRunner()


def test_hello_command():
    result = runner.invoke(app, ["hello", "Alice"])
    assert result.exit_code == 0
    assert "Hello Alice" in result.output


def test_goodbye_command():
    result = runner.invoke(app, ["goodbye", "Bob"])
    assert result.exit_code == 0
    assert "Bye Bob!" in result.output


def test_goodbye_command_formal():
    result = runner.invoke(app, ["goodbye", "--formal", "Emily"])
    assert result.exit_code == 0
    assert "Goodbye Ms. Emily. Have a good day." in result.output


def test_hello_command_missing_argument():
    result = runner.invoke(app, ["hello"])
    assert result.exit_code != 0


def test_goodbye_command_missing_argument():
    result = runner.invoke(app, ["goodbye"])
    assert result.exit_code != 0
