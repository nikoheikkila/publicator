import subprocess
from shlex import split

class ShellException(OSError):
    pass

def run(command: str) -> list[str]:
    result = subprocess.run(split(command), stdout=subprocess.PIPE)
    stdout = format(result.stdout)

    if not ok(result):
        raise ShellException(stdout)

    return stdout

def format(stream: bytes) -> list[str]:
    return stream.decode('utf-8').splitlines()

def ok(result: subprocess.CompletedProcess) -> bool:
    return result.returncode == 0