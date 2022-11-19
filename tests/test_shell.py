from subprocess import CalledProcessError
import sys
from pytest import raises
from publicator import shell
from assertpy import assert_that as verify


class TestShell:
    @staticmethod
    def is_windows() -> bool:
        return sys.platform.startswith("win")

    def test_run_with_empty_command(self) -> None:
        verify(shell.run("")).is_empty()

    def test_run_with_single_command(self) -> None:
        result = shell.run('echo "Hello World!"')

        verify(result.pop()).is_equal_to("Hello World!")

    def test_run_command_with_multiline_output(self) -> None:
        result = shell.run('echo "Hello\nWorld"')

        verify(result).is_length(2).contains("Hello", "World")

    def test_run_with_nonexistent_command(self) -> None:
        pattern = "The system cannot find the file specified" if self.is_windows() else "No such file or directory"

        with raises(FileNotFoundError, match=pattern):
            shell.run("123")

    def test_run_with_failing_command(self) -> None:
        with raises(CalledProcessError, match="returned non-zero exit status 1"):
            shell.run("false")
