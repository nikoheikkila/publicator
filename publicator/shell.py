import subprocess
from shlex import split

def run(command: str) -> list[str]:
    return subprocess.run(split(command), stdout=subprocess.PIPE).stdout.decode('utf-8').splitlines()