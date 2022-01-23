from subprocess import CalledProcessError
from pytest import raises
from publicator import shell

def test_run_with_empty_command():
    result = shell.run("")
    assert not result

def test_run_with_single_command():
    result = shell.run('echo "Hello World!"')
    assert result.pop() == "Hello World!"

def test_run_command_with_multiline_output():
    result = shell.run('echo "Hello\nWorld"')
    assert result == ["Hello", "World"]

def test_run_with_nonexistent_command():
    with raises(FileNotFoundError, match="No such file or directory"):
        shell.run("123")

def test_run_with_failing_command():
    with raises(CalledProcessError, match="returned non-zero exit status 1"):
        shell.run("false")