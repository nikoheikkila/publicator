from subprocess import CalledProcessError
import sys
from pytest import raises
from publicator import shell


def is_windows() -> bool:
    return sys.platform.startswith("win")


def test_run_with_empty_command() -> None:
    result = shell.run("")
    assert not result


def test_run_with_single_command() -> None:
    result = shell.run('echo "Hello World!"')
    assert result.pop() == "Hello World!"


def test_run_command_with_multiline_output() -> None:
    result = shell.run('echo "Hello\nWorld"')
    assert result == ["Hello", "World"]


def test_run_with_nonexistent_command() -> None:
    pattern = "The system cannot find the file specified" if is_windows() else "No such file or directory"

    with raises(FileNotFoundError, match=pattern):
        shell.run("123")


def test_run_with_failing_command() -> None:
    with raises(CalledProcessError, match="returned non-zero exit status 1"):
        shell.run("false")
